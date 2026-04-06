# ///////////////////////////////////////////////////////////////
# SERVICES.CONFIG.CONFIG_SERVICE - Config service implementation
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Configuration service — full implementation (absorbs ConfigManager logic)."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import shutil
import sys
from collections.abc import Mapping, MutableMapping
from importlib.resources import files as _pkg_files
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, ValidationError

# Third-party imports
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

# Local imports
from ...domain.ports.config_service import ConfigServiceProtocol
from ...utils.diagnostics import warn_user
from ...utils.printer import get_printer
from ...utils.runtime_paths import APP_PATH, get_bin_path


# ///////////////////////////////////////////////////////////////
# PYDANTIC VALIDATION MODELS
# ///////////////////////////////////////////////////////////////
class _AppSectionSchema(BaseModel):
    """Validation schema for the ``app`` section in app config."""

    model_config = ConfigDict(extra="forbid")

    name: str | None = None
    description: str | None = None
    app_width: int | None = None
    app_min_width: int | None = None
    app_height: int | None = None
    app_min_height: int | None = None
    debug_printer: bool | None = None
    menu_panel_shrinked_width: int | None = None
    menu_panel_extended_width: int | None = None
    settings_panel_width: int | None = None
    time_animation: int | None = None
    settings_storage_root: str | None = None
    config_version: int | None = None


class _SettingsPanelOptionSchema(BaseModel):
    """Validation schema for one settings panel entry."""

    model_config = ConfigDict(extra="forbid")

    type: str | None = None
    label: str | None = None
    default: Any = None
    description: str | None = None
    enabled: bool | None = None
    options: list[str] | None = None
    min: int | None = None
    max: int | None = None
    unit: str | None = None


class _AppConfigSchema(BaseModel):
    """Validation schema for ``app.config.yaml`` payload."""

    model_config = ConfigDict(extra="forbid")

    app: _AppSectionSchema | None = None
    settings_panel: dict[str, _SettingsPanelOptionSchema] | None = None


class _TranslationSectionSchema(BaseModel):
    """Validation schema for the ``translation`` section."""

    model_config = ConfigDict(extra="forbid")

    collect_strings: bool | None = None
    auto_translation_enabled: bool | None = None
    auto_translate_new_strings: bool | None = None
    save_to_ts_files: bool | None = None
    cache_translations: bool | None = None
    max_cache_age_days: int | None = None


class _LanguageDetectionSectionSchema(BaseModel):
    """Validation schema for the ``language_detection`` section."""

    model_config = ConfigDict(extra="forbid")

    auto_detect_language: bool | None = None
    confidence_threshold: float | None = None


class _SupportedLanguageSchema(BaseModel):
    """Validation schema for one supported language entry."""

    model_config = ConfigDict(extra="forbid")

    code: str
    name: str
    native_name: str
    description: str


class _TranslationConfigSchema(BaseModel):
    """Validation schema for ``translation.config.yaml`` payload."""

    model_config = ConfigDict(extra="forbid")

    translation: _TranslationSectionSchema | None = None
    language_detection: _LanguageDetectionSectionSchema | None = None
    supported_languages: list[_SupportedLanguageSchema] | None = None


class _ThemeConfigSchema(BaseModel):
    """Validation schema for ``theme.config.yaml`` payload."""

    model_config = ConfigDict(extra="forbid")

    palette: dict[str, Any]


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class ConfigService(ConfigServiceProtocol):
    """Modular configuration service for EzQt_App."""

    def __init__(self):
        self._config_cache: dict[str, Any] = {}
        self._config_files: dict[str, Path] = {}
        self._project_root: Path | None = None
        self._yaml_writer = YAML(typ="rt")
        self._yaml_writer.preserve_quotes = True
        self._yaml_writer.default_flow_style = False
        self._yaml_writer.indent(mapping=2, sequence=4, offset=2)

    # -----------------------------------------------------------
    # Port methods (ConfigServiceProtocol)
    # -----------------------------------------------------------

    def set_project_root(self, project_root: Path | str) -> None:
        """Set the active project root directory."""
        self._project_root = (
            project_root if isinstance(project_root, Path) else Path(project_root)
        )
        from ...utils.runtime_paths import _sync_bin_path_from_root

        _sync_bin_path_from_root(self._project_root / "bin")

    def load_config(
        self, config_name: str, force_reload: bool = False
    ) -> dict[str, Any]:
        """Load a named configuration from the first matching path.

        Parameters
        ----------
        config_name:
            Configuration file name (without extension, e.g. ``"app"``).
        force_reload:
            Bypass cache and reload from disk.

        Returns
        -------
        dict[str, Any]
            Loaded configuration data, or empty dict on failure.
        """
        if not force_reload and config_name in self._config_cache:
            return self._config_cache[config_name]

        config_file = self._resolve_config_file(config_name)

        if not config_file:
            warn_user(
                code="config.service.missing_file",
                user_message=f"No configuration file found for '{config_name}'",
                log_message=f"No configuration file found for '{config_name}'",
            )
            get_printer().verbose_msg(
                f"Searched paths: {self.get_config_paths(config_name)}"
            )
            return {}

        try:
            with open(config_file, encoding="utf-8") as f:
                config_data = yaml.safe_load(f)

            self._config_cache[config_name] = config_data
            self._config_files[config_name] = config_file

            get_printer().verbose_msg(
                f"Configuration '{config_name}' loaded from: {config_file}"
            )
            return config_data

        except Exception as e:
            get_printer().error(f"Error loading '{config_name}': {e}")
            return {}

    def get_config_value(
        self, config_name: str, key_path: str, default: Any = None
    ) -> Any:
        """Read a specific value from a configuration using dot-notation key path.

        Parameters
        ----------
        config_name:
            Configuration file name.
        key_path:
            Dot-separated path (e.g. ``"app.name"`` or ``"palette.dark"``).
        default:
            Value returned when key is absent.
        """
        config = self.load_config(config_name)
        keys = key_path.split(".")
        current = config

        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default

        return current

    def save_config(self, config_name: str, config_data: dict[str, Any]) -> bool:
        """Persist a named configuration to the project directory.

        Writes use ``ruamel.yaml`` round-trip mode to preserve existing comments,
        key ordering, and formatting whenever the target file already exists.
        Configuration reads stay on ``PyYAML`` for the current typed read path.

        Parameters
        ----------
        config_name:
            Configuration file name.
        config_data:
            Data to serialise as YAML.

        Returns
        -------
        bool
            ``True`` if the write succeeded.
        """
        config_file: Path
        if config_name in self._config_files:
            # Keep writes consistent with the file originally loaded.
            config_file = self._config_files[config_name]
            config_file.parent.mkdir(parents=True, exist_ok=True)
        else:
            config_dir = get_bin_path() / "config"
            config_dir.mkdir(parents=True, exist_ok=True)
            config_file = config_dir / f"{config_name}.config.yaml"

        try:
            if not self._validate_config_payload(config_name, config_data):
                return False

            existing_doc: MutableMapping[str, Any] | None = None
            if config_file.exists():
                with open(config_file, encoding="utf-8") as f:
                    loaded_doc = self._yaml_writer.load(f)
                if isinstance(loaded_doc, MutableMapping):
                    existing_doc = loaded_doc

            if existing_doc is None:
                payload: MutableMapping[str, Any] = self._to_yaml_mapping(config_data)
            else:
                payload = self._merge_yaml_mapping(existing_doc, config_data)

            with open(config_file, "w", encoding="utf-8") as f:
                self._yaml_writer.dump(payload, f)

            self._config_cache[config_name] = config_data
            self._config_files[config_name] = config_file

            get_printer().verbose_msg(
                f"Configuration '{config_name}' saved: {config_file}"
            )
            return True

        except Exception as e:
            get_printer().error(f"Error saving '{config_name}': {e}")
            return False

    def _validate_config_payload(
        self, config_name: str, config_data: dict[str, Any]
    ) -> bool:
        """Validate known configuration payloads with permissive Pydantic schemas."""
        schema_map: dict[str, type[BaseModel]] = {
            "app": _AppConfigSchema,
            "translation": _TranslationConfigSchema,
            "theme": _ThemeConfigSchema,
        }

        schema = schema_map.get(config_name)
        if schema is None:
            return True

        try:
            schema.model_validate(config_data)
            return True
        except ValidationError as exc:
            warn_user(
                code="config.service.validation_failed",
                user_message=(
                    f"Invalid '{config_name}' configuration; file was not written."
                ),
                log_message=(
                    f"Validation failed for '{config_name}' configuration: {exc}"
                ),
            )
            get_printer().error(
                f"Validation failed for '{config_name}' configuration: {exc}"
            )
            return False

    def _to_yaml_mapping(self, value: Mapping[str, Any]) -> CommentedMap:
        """Convert a standard mapping to a ruamel-compatible ``CommentedMap``."""
        converted = CommentedMap()
        for key, item in value.items():
            converted[key] = self._to_yaml_value(item)
        return converted

    def _to_yaml_value(self, value: Any) -> Any:
        """Recursively convert Python containers to ruamel round-trip containers."""
        if isinstance(value, Mapping):
            return self._to_yaml_mapping(value)
        if isinstance(value, list):
            return [self._to_yaml_value(item) for item in value]
        return value

    def _merge_yaml_mapping(
        self,
        target: MutableMapping[str, Any],
        source: Mapping[str, Any],
    ) -> MutableMapping[str, Any]:
        """Merge ``source`` values into ``target`` while preserving YAML metadata."""
        for existing_key in list(target.keys()):
            if existing_key not in source:
                del target[existing_key]

        for key, source_value in source.items():
            current_value = target.get(key)
            if isinstance(source_value, Mapping) and isinstance(
                current_value, MutableMapping
            ):
                target[key] = self._merge_yaml_mapping(current_value, source_value)
                continue

            if isinstance(source_value, Mapping):
                target[key] = self._to_yaml_mapping(source_value)
                continue

            if isinstance(source_value, list):
                target[key] = [self._to_yaml_value(item) for item in source_value]
                continue

            target[key] = source_value

        return target

    # -----------------------------------------------------------
    # Implementation-specific methods
    # -----------------------------------------------------------

    def get_config_paths(self, config_name: str) -> list[Path]:
        """Return candidate paths for *config_name* in priority order.

        Parameters
        ----------
        config_name:
            Logical configuration name (e.g. ``"app"``, ``"languages"``,
            ``"theme"``). Files are resolved as ``<name>.config.yaml``.
        """
        config_file = f"{config_name}.config.yaml"
        paths: list[Path] = []

        # 1. Configured bin directory
        paths.append(get_bin_path() / "config" / config_file)

        # 3. Package resources — relative to cwd
        paths.append(Path.cwd() / "ezqt_app" / "resources" / "config" / config_file)

        # 4. Package resources — relative to APP_PATH
        paths.append(APP_PATH / "resources" / "config" / config_file)

        return paths

    def copy_package_configs_to_project(self) -> bool:
        """Copy package configuration files into the child project.

        Returns
        -------
        bool
            ``True`` if the operation succeeded.
        """
        if not self._project_root:
            get_printer().error("[ConfigService] No project root defined")
            return False

        package_config_dir = self._find_package_config_dir()

        if not package_config_dir:
            get_printer().error(
                f"[ConfigService] EzQt_App package not found. Tested paths: "
                f"{[str(p) for p in [Path.cwd(), APP_PATH]]}"
            )
            return False

        project_config_dir = get_bin_path() / "config"
        project_config_dir.mkdir(parents=True, exist_ok=True)

        copied_files: list[str] = []

        try:
            for config_file in package_config_dir.glob("*.yaml"):
                target_file = project_config_dir / config_file.name

                if target_file.exists():
                    get_printer().verbose_msg(f"Existing file, ignored: {target_file}")
                    continue

                shutil.copy2(config_file, target_file)
                copied_files.append(config_file.name)
                get_printer().action(
                    f"[ConfigService] Configuration copied: {config_file.name}"
                )

            if copied_files:
                get_printer().action(
                    "[ConfigService] "
                    f"{len(copied_files)} configurations copied to project"
                )

            return True

        except Exception as e:
            get_printer().error(f"Error copying configurations: {e}")
            return False

    def clear_cache(self) -> None:
        """Invalidate the in-memory configuration cache."""
        self._config_cache.clear()
        self._config_files.clear()
        get_printer().verbose_msg("Configuration cache cleared")

    def get_loaded_configs(self) -> dict[str, Path]:
        """Return a snapshot of currently cached configuration paths."""
        return self._config_files.copy()

    # -----------------------------------------------------------
    # Private helpers
    # -----------------------------------------------------------

    def _resolve_config_file(self, config_name: str) -> Path | None:
        """Return the first existing path for *config_name*, or ``None``."""
        for path in self.get_config_paths(config_name):
            if path.exists():
                return path
        return None

    def _find_package_config_dir(self) -> Path | None:
        """Locate the ``resources/config`` directory inside the installed package."""
        package_root = _get_installed_package_root()
        if package_root is not None:
            installed_config_dir = package_root / "resources" / "config"
            if installed_config_dir.exists():
                return installed_config_dir

        # 1. Walk up from cwd looking for an ezqt_app package dir
        current = Path.cwd()
        while current.parent != current:
            candidate = current / "ezqt_app"
            if candidate.exists() and (candidate / "resources" / "config").exists():
                config_dir = candidate / "resources" / "config"
                get_printer().verbose_msg(f"EzQt_App package found: {candidate}")
                get_printer().verbose_msg(f"Configuration directory: {config_dir}")
                return config_dir
            current = current.parent

        # 2. Search sys.path entries
        for path in sys.path:
            candidate = Path(path) / "ezqt_app"
            if candidate.exists() and (candidate / "resources" / "config").exists():
                return candidate / "resources" / "config"

        # 3. Fallback — legacy known paths
        for fallback in [
            Path.cwd() / "ezqt_app" / "resources" / "config",
            APP_PATH / "resources" / "config",
            APP_PATH / "ezqt_app" / "resources" / "config",
        ]:
            if fallback.exists():
                get_printer().verbose_msg(
                    f"Configuration directory found (fallback): {fallback}"
                )
                return fallback

        return None


# ///////////////////////////////////////////////////////////////
# SINGLETONS / FUNCTIONS
# ///////////////////////////////////////////////////////////////


def _get_installed_package_root() -> Path | None:
    """Return installed ``ezqt_app`` package root when discoverable."""
    try:
        import importlib.util

        spec = importlib.util.find_spec("ezqt_app")
        if spec is not None:
            if spec.submodule_search_locations:
                location = next(iter(spec.submodule_search_locations), None)
                if location:
                    candidate = Path(location)
                    if candidate.exists():
                        return candidate
            if spec.origin:
                candidate = Path(spec.origin).resolve().parent
                if candidate.exists():
                    return candidate
    except Exception as e:
        get_printer().verbose_msg(
            f"Could not resolve installed package root for ezqt_app: {e}"
        )

    return None


def _resource_candidates(resource_path: str) -> list[Path]:
    """Build candidate paths for a package resource in priority order."""
    rel_path = Path(resource_path.replace("\\", "/"))
    candidates: list[Path] = []

    package_root = _get_installed_package_root()
    if package_root is not None:
        candidates.append(package_root / rel_path)

    candidates.extend(
        [
            APP_PATH / "ezqt_app" / rel_path,
            APP_PATH / rel_path,
            Path.cwd() / "ezqt_app" / rel_path,
        ]
    )
    return candidates


# ///////////////////////////////////////////////////////////////
# FUNCTIONS
# ///////////////////////////////////////////////////////////////
def get_config_service() -> ConfigService:
    """Return the singleton configuration service instance."""
    from .._registry import ServiceRegistry

    return ServiceRegistry.get(ConfigService, ConfigService)


def get_package_resource(resource_path: str) -> Path:
    """Return the filesystem path of an installed package resource.

    Parameters
    ----------
    resource_path:
        Resource path relative to the ``ezqt_app`` package root.

    Returns
    -------
    Path
        Resolved path to the resource.
    """
    for candidate in _resource_candidates(resource_path):
        if candidate.exists():
            return candidate

    try:
        pkg_candidate = Path(str(_pkg_files("ezqt_app").joinpath(resource_path)))
        if pkg_candidate.exists():
            return pkg_candidate
    except Exception as e:
        get_printer().verbose_msg(
            f"importlib.resources lookup failed for '{resource_path}': {e}"
        )

    package_root = _get_installed_package_root()
    if package_root is not None:
        return package_root / Path(resource_path.replace("\\", "/"))
    return APP_PATH / "ezqt_app" / Path(resource_path.replace("\\", "/"))


def get_package_resource_content(resource_path: str) -> str:
    """Return the decoded UTF-8 content of an installed package resource.

    Parameters
    ----------
    resource_path:
        Resource path relative to the ``ezqt_app`` package root.

    Returns
    -------
    str
        Resource file content.

    Raises
    ------
    FileNotFoundError
        If the resource cannot be located by any strategy.
    """
    try:
        return (
            _pkg_files("ezqt_app").joinpath(resource_path).read_text(encoding="utf-8")
        )
    except Exception:
        file_path = get_package_resource(resource_path)
        if file_path.exists():
            with open(file_path, encoding="utf-8") as f:
                return f.read()
        raise FileNotFoundError(f"Resource not found: {resource_path}") from None
