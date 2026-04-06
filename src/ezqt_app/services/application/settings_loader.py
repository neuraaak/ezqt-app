# ///////////////////////////////////////////////////////////////
# SERVICES.APPLICATION.SETTINGS_LOADER - Settings loader service
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Loads application settings from YAML and applies them to SettingsService."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from pathlib import Path
from typing import Any

# Third-party imports
import yaml
from pydantic import BaseModel, ConfigDict, ValidationError

from ...utils.printer import get_printer, set_global_debug

# Local imports
from ..config.config_service import get_config_service
from ..settings import get_settings_service


# ///////////////////////////////////////////////////////////////
# PYDANTIC RUNTIME SCHEMAS
# ///////////////////////////////////////////////////////////////
class _RuntimeAppSectionSchema(BaseModel):
    """Strict runtime schema for required app settings."""

    model_config = ConfigDict(extra="forbid")

    name: str
    description: str
    app_width: int
    app_min_width: int
    app_height: int
    app_min_height: int
    menu_panel_shrinked_width: int
    menu_panel_extended_width: int
    settings_panel_width: int
    time_animation: int
    debug_printer: bool = False
    settings_storage_root: str | None = None
    config_version: int | None = None


class _RuntimeSettingsPanelOptionSchema(BaseModel):
    """Schema for one settings panel option entry."""

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


class _RuntimeSettingsPanelSchema(BaseModel):
    """Schema for settings panel section used at startup."""

    model_config = ConfigDict(extra="forbid")

    theme: _RuntimeSettingsPanelOptionSchema | None = None
    language: _RuntimeSettingsPanelOptionSchema | None = None
    notifications: _RuntimeSettingsPanelOptionSchema | None = None
    auto_save: _RuntimeSettingsPanelOptionSchema | None = None
    save_interval: _RuntimeSettingsPanelOptionSchema | None = None


class _RuntimeAppConfigSchema(BaseModel):
    """Top-level runtime schema for app configuration payload."""

    model_config = ConfigDict(extra="forbid")

    app: _RuntimeAppSectionSchema
    settings_panel: _RuntimeSettingsPanelSchema | None = None


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class SettingsLoader:
    """Loads ``app.config.yaml`` and populates the settings service.

    Reads the YAML configuration file, extracts application and GUI
    parameters, and injects them into the singleton ``SettingsService``.
    """

    # -----------------------------------------------------------
    # Static API
    # -----------------------------------------------------------

    @staticmethod
    def load_app_settings(
        yaml_file: Path | None = None,
    ) -> dict:
        """Load application settings from YAML and apply to SettingsService.

        Parameters
        ----------
        yaml_file:
            Path to the YAML file. Defaults to the package ``app.config.yaml``.

        Returns
        -------
        dict
            Raw ``app`` section from the YAML file.
        """
        if yaml_file is None:
            raw_data = get_config_service().load_config("app", force_reload=True)
        else:
            with open(yaml_file, encoding="utf-8") as file:
                raw_data = yaml.safe_load(file)

        if not isinstance(raw_data, dict):
            raw_data = {}

        try:
            config = _RuntimeAppConfigSchema.model_validate(raw_data)
        except ValidationError as e:
            get_printer().error(f"Invalid app runtime configuration: {e}")
            raise

        app_data = config.app.model_dump(mode="python")

        settings_service = get_settings_service()
        debug_printer_enabled = bool(config.app.debug_printer)

        # App identity
        settings_service.set_app_name(app_data["name"])
        settings_service.set_app_description(app_data["description"])
        settings_service.set_custom_title_bar_enabled(True)
        settings_service.set_debug_enabled(debug_printer_enabled)
        set_global_debug(debug_printer_enabled)

        # Window dimensions
        settings_service.set_app_min_size(
            width=app_data["app_min_width"],
            height=app_data["app_min_height"],
        )
        settings_service.set_app_dimensions(
            width=app_data["app_width"],
            height=app_data["app_height"],
        )

        # GUI settings
        theme_default = "dark"
        if (
            config.settings_panel is not None
            and config.settings_panel.theme is not None
            and isinstance(config.settings_panel.theme.default, str)
        ):
            theme_default = config.settings_panel.theme.default
        settings_service.set_theme(theme_default)

        settings_service.set_menu_widths(
            shrinked=app_data["menu_panel_shrinked_width"],
            extended=app_data["menu_panel_extended_width"],
        )
        settings_service.set_settings_panel_width(app_data["settings_panel_width"])
        settings_service.set_time_animation(app_data["time_animation"])

        # Display summary through the globally configured printer instance.
        get_printer().config_display(app_data)

        return app_data
