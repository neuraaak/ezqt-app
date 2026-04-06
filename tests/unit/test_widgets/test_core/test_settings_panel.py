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
from unittest.mock import MagicMock, patch

# Third-party imports
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QScrollArea, QSizePolicy, QWidget

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
        assert panel.objectName() == "settings_panel"
        assert panel.frameShape() == QFrame.Shape.NoFrame
        assert panel.frameShadow() == QFrame.Shadow.Raised

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
        assert isinstance(panel._scroll_area, QScrollArea)
        assert panel._scroll_area.objectName() == "settings_scroll_area"
        assert panel._scroll_area.widgetResizable() is True
        assert (
            panel._scroll_area.horizontalScrollBarPolicy()
            == Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        assert (
            panel._scroll_area.verticalScrollBarPolicy()
            == Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

    def test_should_have_content_container_when_instantiated(self, qt_application):
        panel = SettingsPanel()
        assert hasattr(panel, "_content_widget")
        assert panel._content_widget.objectName() == "content_widget"
        assert panel._content_widget.frameShape() == QFrame.Shape.NoFrame
        assert panel._content_layout.spacing() == 0

    def test_should_have_theme_container_and_select_when_instantiated(
        self, qt_application
    ):
        panel = SettingsPanel()
        assert panel._theme_section_frame.objectName() == "theme_section_frame"
        assert hasattr(panel, "_theme_selector")
        assert panel._theme_selector.objectName() == "theme_selector"
        # Bidirectional maps are always initialised (may be empty if config absent)
        assert isinstance(panel._theme_options_map, dict)
        assert isinstance(panel._theme_value_to_display, dict)

    def test_should_have_correct_theme_layout_properties_when_instantiated(
        self, qt_application
    ):
        panel = SettingsPanel()
        assert panel._theme_section_layout.spacing() == 8
        margins = panel._theme_section_layout.contentsMargins()
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

    def test_should_load_non_theme_settings_with_full_app_payload(
        self, qt_application, monkeypatch
    ):
        class _FakeConfigService:
            def load_config(self, _name: str, force_reload: bool = True):
                return {
                    "app": {
                        "name": "MyApplication",
                        "description": "This is an example description",
                        "app_width": 1280,
                        "app_min_width": 940,
                        "app_height": 720,
                        "app_min_height": 560,
                        "debug_printer": False,
                        "menu_panel_shrinked_width": 60,
                        "menu_panel_extended_width": 240,
                        "settings_panel_width": 240,
                        "time_animation": 400,
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
                            "options": ["English", "Français"],
                            "default": "English",
                            "description": "Interface language",
                            "enabled": True,
                        },
                    },
                }

        monkeypatch.setattr(
            config_module,
            "get_config_service",
            lambda: _FakeConfigService(),
        )

        panel = SettingsPanel(load_from_yaml=False)
        panel.load_settings_from_yaml()

        assert "language" in panel._settings


class TestSettingsPanelAdditionalCoverage:
    """Additional coverage tests for SettingsPanel helper methods."""

    def test_should_return_none_when_setting_key_does_not_exist(self, qt_application):
        panel = SettingsPanel(load_from_yaml=False)
        assert panel.get_setting_value("missing") is None

    def test_should_set_and_get_setting_value_for_registered_widget(
        self, qt_application
    ):
        panel = SettingsPanel(load_from_yaml=False)
        widget = MagicMock()
        widget.get_value.return_value = "value"
        panel._settings["x"] = widget

        panel.set_setting_value("x", "updated")

        widget.set_value.assert_called_once_with("updated")
        assert panel.get_setting_value("x") == "value"

    def test_should_collect_all_setting_values(self, qt_application):
        panel = SettingsPanel(load_from_yaml=False)
        w1 = MagicMock()
        w1.get_value.return_value = 1
        w2 = MagicMock()
        w2.get_value.return_value = "ok"
        panel._settings = {"a": w1, "b": w2}

        values = panel.get_all_settings()

        assert values == {"a": 1, "b": "ok"}

    def test_should_continue_save_all_when_one_setting_fails(
        self, qt_application, monkeypatch
    ):
        panel = SettingsPanel(load_from_yaml=False)

        ok_widget = MagicMock()
        ok_widget.get_value.return_value = "ok"
        bad_widget = MagicMock()
        bad_widget.get_value.return_value = "bad"
        panel._settings = {"ok": ok_widget, "bad": bad_widget}

        calls = {"count": 0}

        def _stage(*_args, **_kwargs):
            calls["count"] += 1
            if calls["count"] == 2:
                raise RuntimeError("boom")

        monkeypatch.setattr(
            "ezqt_app.services.application.app_service.AppService.stage_config_value",
            _stage,
        )

        with patch("ezqt_app.widgets.core.settings_panel.warn_tech") as warn:
            panel.save_all_settings_to_yaml()

        assert calls["count"] == 2
        warn.assert_called_once()

    def test_should_retranslate_theme_selector_and_all_widgets(self, qt_application):
        panel = SettingsPanel(load_from_yaml=False)
        panel._theme_selector = MagicMock()

        with_retranslate = MagicMock()
        without_retranslate = object()
        panel._settings = {
            "one": with_retranslate,
            "two": without_retranslate,
        }

        panel.retranslate_ui()

        panel._theme_selector.retranslate_ui.assert_called_once()
        with_retranslate.retranslate_ui.assert_called_once()

    def test_should_update_theme_icons_for_new_and_legacy_patterns(
        self, qt_application, monkeypatch
    ):
        panel = SettingsPanel(load_from_yaml=False)

        class _ThemeAware(QWidget):
            def __init__(self) -> None:
                super().__init__()
                self.theme = None

            def setTheme(self, theme: str) -> None:  # noqa: N802
                self.theme = theme

        class _LegacyThemeAware(QWidget):
            def __init__(self) -> None:
                super().__init__()
                self.called = False

            def update_theme_icon(self) -> None:
                self.called = True

        legacy = _LegacyThemeAware()
        modern = _ThemeAware()
        panel._widgets = [modern, legacy]

        class _FakeSettings:
            class gui:  # noqa: N801
                THEME = "dark"

        monkeypatch.setattr(
            "ezqt_app.widgets.core.settings_panel.get_settings_service",
            lambda: _FakeSettings(),
        )

        panel.update_all_theme_icons()

        assert modern.theme == "dark"
        assert legacy.called is True

    def test_should_stage_and_emit_when_theme_selector_changes(
        self, qt_application, monkeypatch
    ):
        panel = SettingsPanel(load_from_yaml=False)
        panel._theme_options_map = {"Blue Gray - Dark": "blue-gray:dark"}

        class _FakeSettings:
            def set_theme(self, *_args, **_kwargs) -> None:
                return None

        staged: list[tuple[list[str], str]] = []

        def _stage(keys, value):
            staged.append((keys, value))

        emitted: list[tuple[str, str]] = []
        panel.settingChanged.connect(lambda key, value: emitted.append((key, value)))

        monkeypatch.setattr(
            "ezqt_app.widgets.core.settings_panel.get_settings_service",
            lambda: _FakeSettings(),
        )
        monkeypatch.setattr(
            "ezqt_app.services.application.app_service.AppService.stage_config_value",
            _stage,
        )

        panel._on_theme_selector_changed("Blue Gray - Dark")

        assert staged
        assert staged[0][1] == "blue-gray:dark"
        assert ("theme", "blue-gray:dark") in emitted

    def test_should_warn_when_theme_selector_change_raises(
        self, qt_application, monkeypatch
    ):
        panel = SettingsPanel(load_from_yaml=False)
        panel._theme_options_map = {}

        monkeypatch.setattr(
            "ezqt_app.services.settings.get_settings_service",
            lambda: (_ for _ in ()).throw(RuntimeError("boom")),
        )

        with patch("ezqt_app.widgets.core.settings_panel.warn_tech") as warn:
            panel._on_theme_selector_changed("x")

        warn.assert_called_once()

    def test_should_add_section_with_title_and_scroll(self, qt_application):
        panel = SettingsPanel(load_from_yaml=False)

        section = panel.add_setting_section("My Section")
        panel.scroll_to_top()
        panel.scroll_to_bottom()
        panel.scroll_to_widget(section)

        assert isinstance(section, QFrame)
        assert section.objectName() == "settings_section_my_section"
