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
from pathlib import Path
from typing import Any

# Third-party imports
import yaml

# Local imports
from ...domain.ports.config_service import ConfigServiceProtocol
from ...utils.diagnostics import warn_user
from ...utils.printer import get_printer
from ...utils.runtime_paths import APP_PATH


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class ConfigService(ConfigServiceProtocol):
    """Modular configuration service for EzQt_App."""

    def __init__(self):
        self._config_cache: dict[str, Any] = {}
        self._config_files: dict[str, Path] = {}
        self._project_root: Path | None = None

    # -----------------------------------------------------------
    # Port methods (ConfigServiceProtocol)
    # -----------------------------------------------------------

    def set_project_root(self, project_root: Path | str) -> None:
        """Set the active project root directory."""
        self._project_root = (
            project_root if isinstance(project_root, Path) else Path(project_root)
        )

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
        if not self._project_root:
            get_printer().error("No project root defined")
            return False

        config_dir = self._project_root / "bin" / "config"
        config_dir.mkdir(parents=True, exist_ok=True)
        config_file = config_dir / f"{config_name}.config.yaml"

        try:
            with open(config_file, "w", encoding="utf-8") as f:
                yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True)

            self._config_cache[config_name] = config_data
            self._config_files[config_name] = config_file

            get_printer().verbose_msg(
                f"Configuration '{config_name}' saved: {config_file}"
            )
            return True

        except Exception as e:
            get_printer().error(f"Error saving '{config_name}': {e}")
            return False

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

        # 1. Child project (bin/config/)
        if self._project_root:
            paths.append(self._project_root / "bin" / "config" / config_file)

        # 2. Current directory (bin/config/)
        paths.append(Path.cwd() / "bin" / "config" / config_file)

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
            get_printer().error("No project root defined")
            return False

        package_config_dir = self._find_package_config_dir()

        if not package_config_dir:
            get_printer().error(
                f"EzQt_App package not found. Tested paths: "
                f"{[str(p) for p in [Path.cwd(), APP_PATH]]}"
            )
            return False

        project_config_dir = self._project_root / "bin" / "config"
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
                get_printer().info(f"Configuration copied: {config_file.name}")

            if copied_files:
                get_printer().info(
                    f"✅ {len(copied_files)} configurations copied to project"
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
# SINGLETONS
# ///////////////////////////////////////////////////////////////
_config_service: ConfigService | None = None


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
    global _config_service
    if _config_service is None:
        _config_service = ConfigService()
    return _config_service


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
        import pkg_resources  # type: ignore[import-untyped]

        pkg_candidate = Path(pkg_resources.resource_filename("ezqt_app", resource_path))
        if pkg_candidate.exists():
            return pkg_candidate
    except Exception as e:
        get_printer().verbose_msg(
            f"pkg_resources lookup failed for '{resource_path}': {e}"
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
        import pkg_resources  # type: ignore[import-untyped]

        return pkg_resources.resource_string("ezqt_app", resource_path).decode("utf-8")
    except Exception:
        file_path = get_package_resource(resource_path)
        if file_path.exists():
            with open(file_path, encoding="utf-8") as f:
                return f.read()
        raise FileNotFoundError(f"Resource not found: {resource_path}") from None
