# ///////////////////////////////////////////////////////////////
# SERVICES.APPLICATION.APP_SERVICE - Application orchestration service
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Central application service — orchestrates config, assets, resources and settings."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from pathlib import Path
from typing import Any

# Local imports
from ..config.config_service import (
    get_config_service,
    get_package_resource,
    get_package_resource_content,
)
from .assets_service import AssetsService
from .resource_service import ResourceService
from .settings_loader import SettingsLoader


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class AppService:
    """Central orchestration service for application lifecycle.

    Aggregates config, asset, resource and settings operations into a
    single cohesive snake_case API used by widgets, CLI and bootstrap.
    """

    # ------------------------------------------------------------------
    # Assets
    # ------------------------------------------------------------------

    @staticmethod
    def check_assets_requirements(
        base_path: Path | None = None,
        bin_path: Path | None = None,
        overwrite_policy: str = "ask",
    ) -> None:
        """Generate asset binaries, QRC and RC files at APP_PATH."""
        AssetsService.check_assets_requirements(
            base_path=base_path,
            bin_path=bin_path,
            overwrite_policy=overwrite_policy,
        )

    @staticmethod
    def make_required_files(
        mk_theme: bool = True,
        mk_config: bool = True,
        mk_translations: bool = True,
        base_path: Path | None = None,
        bin_path: Path | None = None,
        overwrite_policy: str = "ask",
    ) -> None:
        """Copy YAML, QSS theme and translation files into ``cwd/bin/``.

        Parameters
        ----------
        mk_theme:
            When ``True`` (default) also copies the QSS theme file.
        """
        AssetsService.make_required_files(
            mk_theme=mk_theme,
            mk_config=mk_config,
            mk_translations=mk_translations,
            base_path=base_path,
            bin_path=bin_path,
            overwrite_policy=overwrite_policy,
        )

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    @staticmethod
    def set_project_root(project_root: Path) -> None:
        """Set the project root directory used by the config service."""
        get_config_service().set_project_root(project_root)

    @staticmethod
    def load_config(config_name: str) -> dict[str, Any]:
        """Load a named configuration from its YAML file.

        Parameters
        ----------
        config_name:
            Logical name of the configuration (e.g. ``"app"``).
        """
        return get_config_service().load_config(config_name)

    @staticmethod
    def get_config_value(config_name: str, key_path: str, default: Any = None) -> Any:
        """Get a value from a named configuration using dot-separated path.

        Parameters
        ----------
        config_name:
            Logical name of the configuration.
        key_path:
            Dot-separated key path, e.g. ``"app.name"``.
        default:
            Value returned when the path is absent.
        """
        return get_config_service().get_config_value(config_name, key_path, default)

    @staticmethod
    def save_config(config_name: str, data: dict[str, Any]) -> None:
        """Persist a named configuration to its YAML file.

        Parameters
        ----------
        config_name:
            Logical name of the configuration.
        data:
            Full configuration dict to write.
        """
        get_config_service().save_config(config_name, data)

    @staticmethod
    def write_yaml_config(keys: list[str], val: Any) -> None:
        """Write a single value into a YAML config using a key list.

        The first element of *keys* is the config name; remaining elements
        form the nested path to the value.

        Parameters
        ----------
        keys:
            List of keys where ``keys[0]`` is the config name and
            ``keys[1:]`` is the path inside that config.
        val:
            Value to assign at the leaf key.
        """
        if not keys:
            return

        config_name = keys[0]
        config_service = get_config_service()
        config = config_service.load_config(config_name)

        current = config
        for key in keys[1:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]

        current[keys[-1]] = val
        config_service.save_config(config_name, config)

    @staticmethod
    def copy_package_configs_to_project() -> None:
        """Copy package default configs into the child project directory."""
        get_config_service().copy_package_configs_to_project()

    # ------------------------------------------------------------------
    # Package resources
    # ------------------------------------------------------------------

    @staticmethod
    def get_package_resource(resource_path: str) -> Path:
        """Return a :class:`~pathlib.Path` to an installed package resource.

        Parameters
        ----------
        resource_path:
            Relative path inside the package (e.g. ``"resources/themes/main_theme.qss"``).
        """
        return get_package_resource(resource_path)

    @staticmethod
    def get_package_resource_content(resource_path: str) -> str:
        """Return the text content of an installed package resource.

        Parameters
        ----------
        resource_path:
            Relative path inside the package.
        """
        return get_package_resource_content(resource_path)

    # ------------------------------------------------------------------
    # Resources (fonts)
    # ------------------------------------------------------------------

    @staticmethod
    def load_fonts_resources(app: bool = False) -> None:
        """Load ``.ttf`` font files into Qt's font database.

        Parameters
        ----------
        app:
            When ``False`` loads from the installed package fonts then
            recurses with ``True`` to also load from ``bin/fonts/``.
        """
        ResourceService.load_fonts_resources(app)

    # ------------------------------------------------------------------
    # Settings
    # ------------------------------------------------------------------

    @staticmethod
    def load_app_settings() -> dict[str, Any]:
        """Load application settings from the project YAML file."""
        return SettingsLoader.load_app_settings()
