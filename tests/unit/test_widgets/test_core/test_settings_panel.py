# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_WIDGETS.TEST_CORE.TEST_SETTINGS_PANEL - Settings panel tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for the SettingsPanel class."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from unittest.mock import MagicMock

# Third-party imports
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QScrollArea, QSizePolicy, QWidget

import ezqt_app.services.config as config_module

# Local imports
from ezqt_app.widgets.core.settings_panel import SettingsPanel

# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////


class TestSettingsPanel:
    """Tests for the SettingsPanel class."""

    def test_should_have_default_frame_properties_when_instantiated(
        self, qt_application
    ):
        panel = SettingsPanel()
        assert panel.objectName() == "settingsPanel"
        assert panel.frameShape() == QFrame.NoFrame
        assert panel.frameShadow() == QFrame.Raised

    def test_should_use_custom_width_when_width_is_given(self, qt_application):
        panel = SettingsPanel(width=300)
        assert panel.get_width() == 300

    def test_should_accept_parent_when_parent_is_given(self, qt_application):
        parent = QWidget()
        panel = SettingsPanel(parent=parent)
        assert panel.parent() == parent

    def test_should_have_correctly_configured_scroll_area_when_instantiated(
        self, qt_application
    ):
        panel = SettingsPanel()
        assert isinstance(panel.settingsScrollArea, QScrollArea)
        assert panel.settingsScrollArea.objectName() == "settingsScrollArea"
        assert panel.settingsScrollArea.widgetResizable() is True
        assert (
            panel.settingsScrollArea.horizontalScrollBarPolicy()
            == Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        assert (
            panel.settingsScrollArea.verticalScrollBarPolicy()
            == Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

    def test_should_have_content_container_when_instantiated(self, qt_application):
        panel = SettingsPanel()
        assert hasattr(panel, "contentSettings")
        assert panel.contentSettings.objectName() == "contentSettings"
        assert panel.contentSettings.frameShape() == QFrame.NoFrame
        assert panel.VL_contentSettings.spacing() == 0

    def test_should_have_theme_container_and_label_when_instantiated(
        self, qt_application
    ):
        panel = SettingsPanel()
        assert panel.themeSettingsContainer.objectName() == "themeSettingsContainer"
        assert panel.themeLabel.objectName() == "themeLabel"
        assert isinstance(panel.themeLabel, QLabel)
        assert panel._theme_label_text == "Active Theme"

    def test_should_have_correct_theme_layout_properties_when_instantiated(
        self, qt_application
    ):
        panel = SettingsPanel()
        assert panel.VL_themeSettingsContainer.spacing() == 8
        margins = panel.VL_themeSettingsContainer.contentsMargins()
        assert margins.left() == 10
        assert margins.top() == 10
        assert margins.right() == 10
        assert margins.bottom() == 10

    def test_should_have_setting_and_language_signals_when_instantiated(
        self, qt_application
    ):
        panel = SettingsPanel()
        assert hasattr(panel, "settingChanged")
        assert hasattr(panel, "languageChanged")

    def test_should_initialize_with_empty_internal_collections_when_loaded_without_yaml(
        self, qt_application
    ):
        panel = SettingsPanel(load_from_yaml=False)
        assert isinstance(panel._widgets, list)
        assert isinstance(panel._settings, dict)

    def test_should_have_zero_size_constraints_when_instantiated(self, qt_application):
        panel = SettingsPanel()
        assert panel.minimumSize().width() == 0
        assert panel.maximumSize().width() == 0
        assert panel.sizePolicy().horizontalPolicy() == QSizePolicy.Policy.Preferred
        assert panel.sizePolicy().verticalPolicy() == QSizePolicy.Policy.Preferred

    def test_should_update_width_when_set_width_is_called(self, qt_application):
        panel = SettingsPanel()
        panel.set_width(350)
        assert panel.get_width() == 350

    def test_should_have_empty_settings_when_loaded_without_yaml(self, qt_application):
        panel = SettingsPanel(load_from_yaml=False)
        assert panel._settings == {}

    def test_should_prefer_legacy_root_when_legacy_root_key_exists(
        self, qt_application, monkeypatch
    ):
        # settings_storage_root points to "app.settings_panel" but config["app"] has no
        # "settings_panel" sub-key → _exists fails → fallback returns ["app", "settings_panel"].
        class _FakeConfigService:
            def load_config(self, _name: str):
                return {
                    "app": {"settings_storage_root": "app.settings_panel"},
                    "settings_panel": {},
                }

        monkeypatch.setattr(
            config_module,
            "get_config_service",
            lambda: _FakeConfigService(),
        )

        panel = SettingsPanel(load_from_yaml=False)
        # First element is always the config file name ("app").
        assert panel._settings_storage_prefix() == ["app", "settings_panel"]

    def test_should_use_configured_root_when_settings_storage_root_is_available(
        self, qt_application, monkeypatch
    ):
        class _FakeConfigService:
            def load_config(self, _name: str):
                return {
                    "app": {"settings_storage_root": "app.settings_panel"},
                    "settings_panel": {},
                    "app_settings": {},
                }

        monkeypatch.setattr(
            config_module,
            "get_config_service",
            lambda: _FakeConfigService(),
        )

        panel = SettingsPanel(load_from_yaml=False)
        # _exists(["app", "settings_panel"]) is False (no nested key) → fallback.
        assert panel._settings_storage_prefix() == ["app", "settings_panel"]

    def test_should_accept_nested_root_when_mapping_exists_in_config(
        self, qt_application, monkeypatch
    ):
        # settings_panel is nested under app → _exists(["app", "settings_panel"]) succeeds.
        # Result prepends config name: ["app", "app", "settings_panel"] so that
        # stage_config_value navigates config["app"]["settings_panel"].
        class _FakeConfigService:
            def load_config(self, _name: str):
                return {
                    "app": {
                        "settings_storage_root": "app.settings_panel",
                        "settings_panel": {},
                    }
                }

        monkeypatch.setattr(
            config_module,
            "get_config_service",
            lambda: _FakeConfigService(),
        )

        panel = SettingsPanel(load_from_yaml=False)
        assert panel._settings_storage_prefix() == ["app", "app", "settings_panel"]

    def test_should_resync_theme_selector_when_language_is_changed(
        self, qt_application, monkeypatch
    ):
        class _FakeTranslationService:
            def get_current_language_name(self) -> str:
                return "English"

            def change_language(self, _name: str) -> bool:
                return True

        monkeypatch.setattr(
            "ezqt_app.widgets.core.settings_panel.get_translation_service",
            lambda: _FakeTranslationService(),
        )

        panel = SettingsPanel(load_from_yaml=False)
        panel._sync_theme_selector_with_settings = MagicMock()

        panel._on_setting_changed("language", "Français")

        panel._sync_theme_selector_with_settings.assert_called_once()
