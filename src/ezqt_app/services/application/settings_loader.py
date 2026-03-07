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

# Third-party imports
import yaml

from ...utils.printer import Printer

# Local imports
from ..config.config_service import get_package_resource
from ..settings import get_settings_service


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class SettingsLoader:
    """Loads ``app.yaml`` and populates the settings service.

    Reads the YAML configuration file, extracts application and GUI
    parameters, and injects them into the singleton ``SettingsService``.
    """

    # -----------------------------------------------------------
    # Static API
    # -----------------------------------------------------------

    @staticmethod
    def load_app_settings(yaml_file: Path | None = None) -> dict:
        """Load application settings from YAML and apply to SettingsService.

        Parameters
        ----------
        yaml_file:
            Path to the YAML file. Defaults to the package ``app.yaml``.

        Returns
        -------
        dict
            Raw ``app`` section from the YAML file.
        """
        if not yaml_file:
            yaml_file = get_package_resource("app.yaml")

        with open(yaml_file, encoding="utf-8") as file:
            data = yaml.safe_load(file)
            app_data = data.get("app", {})

        settings_service = get_settings_service()

        # App identity
        settings_service.set_app_name(app_data["name"])
        settings_service.set_app_description(app_data["description"])
        settings_service.set_custom_title_bar_enabled(True)

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
        try:
            settings_panel = data.get("settings_panel", {})
            settings_service.set_theme(
                settings_panel.get("theme", {}).get("default", app_data["theme"])
            )
        except KeyError:
            settings_service.set_theme(app_data["theme"])

        settings_service.set_menu_widths(
            shrinked=app_data["menu_panel_shrinked_width"],
            extended=app_data["menu_panel_extended_width"],
        )
        settings_service.set_settings_panel_width(app_data["settings_panel_width"])
        settings_service.set_time_animation(app_data["time_animation"])

        # Display summary (force verbose to show ASCII frame)
        Printer(verbose=True).config_display(app_data)

        return app_data
