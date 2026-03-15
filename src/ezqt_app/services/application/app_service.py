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
# MODULE-LEVEL STATE
# ///////////////////////////////////////////////////////////////

# Config names that have been mutated in-memory and need to be flushed to disk.
_dirty: set[str] = set()

# Guard against double-registration of the aboutToQuit signal.
_quit_signal_connected: bool = False


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////


class AppService:
    """
    Central orchestration service for application lifecycle.

    Aggregates config, asset, resource and settings operations into a
    single cohesive snake_case API used by widgets, CLI and bootstrap.
    """

    # ///////////////////////////////////////////////////////////////
    # PUBLIC METHODS
    # ///////////////////////////////////////////////////////////////

    # ------------------------------------------------
    # ASSETS
    # ------------------------------------------------

    @staticmethod
    def check_assets_requirements(
        base_path: Path | None = None,
        bin_path: Path | None = None,
        overwrite_policy: str = "ask",
    ) -> None:
        """
        Generate asset binaries, QRC and RC files at APP_PATH.

        Args:
            base_path: Optional base path for assets.
            bin_path: Optional binary path.
            overwrite_policy: Policy for overwriting existing files (default: "ask").
        """
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
        """
        Copy YAML, QSS theme and translation files into project directories.

        Args:
            mk_theme: When True also copies the QSS theme file.
            mk_config: When True copies configuration files.
            mk_translations: When True copies translation files.
            base_path: Optional base path.
            bin_path: Optional binary path.
            overwrite_policy: Policy for overwriting (default: "ask").
        """
        AssetsService.make_required_files(
            mk_theme=mk_theme,
            mk_config=mk_config,
            mk_translations=mk_translations,
            base_path=base_path,
            bin_path=bin_path,
            overwrite_policy=overwrite_policy,
        )

    # ------------------------------------------------
    # CONFIGURATION
    # ------------------------------------------------

    @staticmethod
    def set_project_root(project_root: Path) -> None:
        """
        Set the project root directory used by the config service.

        Args:
            project_root: The Path to the project root.
        """
        get_config_service().set_project_root(project_root)

    @staticmethod
    def load_config(config_name: str) -> dict[str, Any]:
        """
        Load a named configuration from its YAML file.

        Args:
            config_name: Logical name of the configuration (e.g. "app").

        Returns:
            dict: The loaded configuration data.
        """
        return get_config_service().load_config(config_name)

    @staticmethod
    def get_config_value(config_name: str, key_path: str, default: Any = None) -> Any:
        """
        Get a value from a named configuration using dot-separated path.

        Args:
            config_name: Logical name of the configuration.
            key_path: Dot-separated key path, e.g. "app.name".
            default: Value returned when the path is absent.

        Returns:
            Any: The configuration value or default.
        """
        return get_config_service().get_config_value(config_name, key_path, default)

    @staticmethod
    def save_config(config_name: str, data: dict[str, Any]) -> None:
        """
        Persist a named configuration to its YAML file.

        Args:
            config_name: Logical name of the configuration.
            data: Full configuration dict to write.
        """
        get_config_service().save_config(config_name, data)

    @staticmethod
    def write_yaml_config(keys: list[str], val: Any) -> None:
        """
        Write a single value into a YAML config using a key list immediately.

        Args:
            keys: List where keys[0] is config name and keys[1:] is the path.
            val: Value to assign at the leaf key.
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
    def stage_config_value(keys: list[str], val: Any) -> None:
        """
        Mutate a config value in the shared cache and mark it dirty for flush.

        Args:
            keys: List where keys[0] is config name and keys[1:] is the path.
            val: Value to assign at the leaf key.
        """
        if not keys:
            return

        global _quit_signal_connected  # noqa: PLW0603

        config_name = keys[0]
        config_service = get_config_service()

        config: dict[str, Any] = config_service.load_config(config_name)
        current: dict[str, Any] = config
        for key in keys[1:-1]:
            if key not in current or not isinstance(current[key], dict):
                current[key] = {}
            current = current[key]

        current[keys[-1]] = val
        _dirty.add(config_name)

        if not _quit_signal_connected:
            from PySide6.QtCore import QCoreApplication

            app = QCoreApplication.instance()
            if app is not None:
                app.aboutToQuit.connect(AppService.flush_all)
                _quit_signal_connected = True

    @staticmethod
    def flush_all() -> None:
        """Write all dirty configs to disk and clear the dirty set."""
        if not _dirty:
            return

        config_service = get_config_service()
        for config_name in list(_dirty):
            config_data = config_service.load_config(config_name)
            config_service.save_config(config_name, config_data)

        _dirty.clear()

    @staticmethod
    def copy_package_configs_to_project() -> None:
        """Copy package default configs into the child project directory."""
        get_config_service().copy_package_configs_to_project()

    # ------------------------------------------------
    # PACKAGE RESOURCES
    # ------------------------------------------------

    @staticmethod
    def get_package_resource(resource_path: str) -> Path:
        """
        Return a Path to an installed package resource.

        Args:
            resource_path: Relative path inside the package.

        Returns:
            Path: Absolute path to the resource.
        """
        return get_package_resource(resource_path)

    @staticmethod
    def get_package_resource_content(resource_path: str) -> str:
        """
        Return the text content of an installed package resource.

        Args:
            resource_path: Relative path inside the package.

        Returns:
            str: Content of the resource.
        """
        return get_package_resource_content(resource_path)

    # ------------------------------------------------
    # RESOURCES (FONTS)
    # ------------------------------------------------

    @staticmethod
    def load_fonts_resources(app: bool = False) -> None:
        """
        Load .ttf font files into Qt's font database.

        Args:
            app: Whether to also load fonts from the bin/fonts/ directory.
        """
        ResourceService.load_fonts_resources(app)

    # ------------------------------------------------
    # SETTINGS
    # ------------------------------------------------

    @staticmethod
    def load_app_settings(
        logs_dir_override: str | Path | None = None,
        log_file_name_override: str | None = None,
    ) -> dict[str, Any]:
        """
        Load app settings and configure logger.

        Args:
            logs_dir_override: Optional custom logs directory.
            log_file_name_override: Optional custom log file name.

        Returns:
            dict: Loaded settings.
        """
        return SettingsLoader.load_app_settings(
            logs_dir_override=logs_dir_override,
            log_file_name_override=log_file_name_override,
        )
