# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_SERVICES.TEST_SETTINGS_LOADER - SettingsLoader tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for services/application/settings_loader.py."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from pydantic import ValidationError

from ezqt_app.services.application.settings_loader import SettingsLoader


def _valid_runtime_config() -> dict:
    return {
        "app": {
            "name": "Demo",
            "description": "Demo app",
            "app_width": 1280,
            "app_min_width": 940,
            "app_height": 720,
            "app_min_height": 560,
            "menu_panel_shrinked_width": 60,
            "menu_panel_extended_width": 240,
            "settings_panel_width": 280,
            "time_animation": 400,
            "debug_printer": True,
        },
        "settings_panel": {"theme": {"default": "light"}},
    }


class TestSettingsLoader:
    """Tests for strict runtime loading and settings application."""

    def test_should_apply_settings_from_config_service_when_yaml_is_none(self) -> None:
        settings_service = MagicMock()
        printer = MagicMock()
        config_service = MagicMock()
        config_service.load_config.return_value = _valid_runtime_config()

        with (
            patch(
                "ezqt_app.services.application.settings_loader.get_config_service",
                return_value=config_service,
            ),
            patch(
                "ezqt_app.services.application.settings_loader.get_settings_service",
                return_value=settings_service,
            ),
            patch(
                "ezqt_app.services.application.settings_loader.get_printer",
                return_value=printer,
            ),
            patch(
                "ezqt_app.services.application.settings_loader.set_global_debug"
            ) as dbg,
        ):
            result = SettingsLoader.load_app_settings()

        assert result["name"] == "Demo"
        settings_service.set_app_name.assert_called_once_with("Demo")
        settings_service.set_theme.assert_called_once_with("light")
        dbg.assert_called_once_with(True)
        printer.config_display.assert_called_once()

    def test_should_apply_default_theme_when_settings_panel_is_missing(self) -> None:
        settings_service = MagicMock()
        printer = MagicMock()
        config = _valid_runtime_config()
        config.pop("settings_panel")

        with (
            patch(
                "ezqt_app.services.application.settings_loader.get_config_service"
            ) as cfg,
            patch(
                "ezqt_app.services.application.settings_loader.get_settings_service",
                return_value=settings_service,
            ),
            patch(
                "ezqt_app.services.application.settings_loader.get_printer",
                return_value=printer,
            ),
            patch("ezqt_app.services.application.settings_loader.set_global_debug"),
        ):
            cfg.return_value.load_config.return_value = config
            SettingsLoader.load_app_settings()

        settings_service.set_theme.assert_called_once_with("dark")

    def test_should_accept_full_runtime_payload_from_shipped_app_config(self) -> None:
        settings_service = MagicMock()
        printer = MagicMock()
        config_service = MagicMock()
        config_service.load_config.return_value = {
            "app": {
                "name": "Demo",
                "description": "Demo app",
                "app_width": 1280,
                "app_min_width": 940,
                "app_height": 720,
                "app_min_height": 560,
                "menu_panel_shrinked_width": 60,
                "menu_panel_extended_width": 240,
                "settings_panel_width": 280,
                "time_animation": 400,
                "debug_printer": False,
                "settings_storage_root": "settings_panel",
                "config_version": 1,
            },
            "settings_panel": {
                "theme": {
                    "type": "select",
                    "label": "Active Theme",
                    "default": "blue-gray:dark",
                    "description": "Choose the application theme",
                    "enabled": True,
                },
                "language": {
                    "type": "select",
                    "label": "Language",
                    "options": ["English", "Francais"],
                    "default": "English",
                    "description": "Interface language",
                    "enabled": True,
                },
            },
        }

        with (
            patch(
                "ezqt_app.services.application.settings_loader.get_config_service",
                return_value=config_service,
            ),
            patch(
                "ezqt_app.services.application.settings_loader.get_settings_service",
                return_value=settings_service,
            ),
            patch(
                "ezqt_app.services.application.settings_loader.get_printer",
                return_value=printer,
            ),
            patch(
                "ezqt_app.services.application.settings_loader.set_global_debug"
            ) as dbg,
        ):
            result = SettingsLoader.load_app_settings()

        assert result["name"] == "Demo"
        settings_service.set_theme.assert_called_once_with("blue-gray:dark")
        dbg.assert_called_once_with(False)
        printer.config_display.assert_called_once()

    def test_should_load_from_explicit_yaml_file_when_path_is_given(
        self, tmp_path: Path
    ) -> None:
        yaml_file = tmp_path / "app.config.yaml"
        yaml_file.write_text(
            """
app:
  name: Demo
  description: Demo app
  app_width: 1280
  app_min_width: 940
  app_height: 720
  app_min_height: 560
  menu_panel_shrinked_width: 60
  menu_panel_extended_width: 240
  settings_panel_width: 280
  time_animation: 400
  debug_printer: false
settings_panel:
  theme:
    default: dark
""".strip(),
            encoding="utf-8",
        )

        with (
            patch(
                "ezqt_app.services.application.settings_loader.get_settings_service",
                return_value=MagicMock(),
            ),
            patch(
                "ezqt_app.services.application.settings_loader.get_printer",
                return_value=MagicMock(),
            ),
            patch("ezqt_app.services.application.settings_loader.set_global_debug"),
        ):
            result = SettingsLoader.load_app_settings(yaml_file=yaml_file)

        assert result["description"] == "Demo app"

    def test_should_raise_validation_error_when_payload_is_invalid(self) -> None:
        bad_payload = {"app": {"name": "Demo"}}
        printer = MagicMock()

        with (
            patch(
                "ezqt_app.services.application.settings_loader.get_config_service"
            ) as cfg,
            patch(
                "ezqt_app.services.application.settings_loader.get_printer",
                return_value=printer,
            ),
            pytest.raises(ValidationError),
        ):
            cfg.return_value.load_config.return_value = bad_payload
            SettingsLoader.load_app_settings()

        printer.error.assert_called_once()
