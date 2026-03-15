# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_APP_WINDOW - EzQt_App window tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for app.py — EzQt_App QMainWindow methods."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from unittest.mock import MagicMock, patch

# Third-party imports
from PySide6.QtWidgets import QMainWindow

# Local imports
from ezqt_app.app import EzQt_App

# ///////////////////////////////////////////////////////////////
# CONSTANTS
# ///////////////////////////////////////////////////////////////

_PATCHES = {
    "load_fonts": "ezqt_app.app.AppService.load_fonts_resources",
    "load_settings": "ezqt_app.app.AppService.load_app_settings",
    "config_svc": "ezqt_app.app.get_config_service",
    "settings_svc": "ezqt_app.app.get_settings_service",
    "translation_svc": "ezqt_app.app.get_translation_service",
    "fonts_init": "ezqt_app.app.Fonts.initFonts",
    "size_init": "ezqt_app.app.SizePolicy.initSizePolicy",
    "theme_svc": "ezqt_app.app.ThemeService.apply_theme",
    "ui_def": "ezqt_app.app.UiDefinitionsService.apply_definitions",
    "setupUi": "ezqt_app.widgets.ui_main.Ui_MainWindow.setupUi",
}

# ///////////////////////////////////////////////////////////////
# FUNCTIONS
# ///////////////////////////////////////////////////////////////


def _make_mock_config() -> MagicMock:
    """
    Create a mock configuration service.

    Returns:
        MagicMock: Configured mock.
    """
    mock = MagicMock()
    mock.load_config.return_value = {}
    return mock


def _make_mock_settings() -> MagicMock:
    """
    Create a mock settings service.

    Returns:
        MagicMock: Configured mock.
    """
    mock = MagicMock()
    mock.app.NAME = "Test App"
    mock.gui.THEME = "dark"
    return mock


def _make_mock_translation() -> MagicMock:
    """
    Create a mock translation service.

    Returns:
        MagicMock: Configured mock.
    """
    mock = MagicMock()
    mock.change_language.return_value = True
    mock.change_language_by_code.return_value = True
    return mock


def _make_instance(_qt_application) -> EzQt_App:
    """
    Return an EzQt_App bypassing all service calls.

    Args:
        _qt_application: The Qt application fixture.

    Returns:
        EzQt_App: Initialized instance with mocked dependencies.
    """

    def fake_setupUi(_self_ui: object, window: EzQt_App, **_kwargs: object) -> None:
        window.ui = MagicMock()

    with (
        patch(_PATCHES["load_fonts"]),
        patch(_PATCHES["load_settings"]),
        patch(_PATCHES["config_svc"], return_value=_make_mock_config()),
        patch(_PATCHES["settings_svc"], return_value=_make_mock_settings()),
        patch(_PATCHES["translation_svc"], return_value=_make_mock_translation()),
        patch(_PATCHES["fonts_init"]),
        patch(_PATCHES["size_init"]),
        patch(_PATCHES["theme_svc"]),
        patch(_PATCHES["ui_def"]),
        patch(_PATCHES["setupUi"], new=fake_setupUi),
    ):
        instance = EzQt_App()
        instance.build()

    return instance


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////


class TestEzQtAppClassStructure:
    """Static class-level assertions — no instantiation required."""

    # ------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------

    def test_should_be_qmainwindow_subclass_when_class_is_loaded(self) -> None:
        """Verify EzQt_App inherits from QMainWindow."""
        assert issubclass(EzQt_App, QMainWindow)

    def test_should_be_importable_when_module_is_loaded(self) -> None:
        """Verify EzQt_App is importable."""
        from ezqt_app.app import EzQt_App as _App

        assert _App is not None

    def test_should_have_init_method_when_class_is_loaded(self) -> None:
        """Verify __init__ is present."""
        assert callable(EzQt_App.__init__)

    def test_should_have_expected_public_methods_when_class_is_loaded(self) -> None:
        """Verify expected public methods are present."""
        for method in (
            "set_app_theme",
            "update_ui",
            "set_app_icon",
            "add_menu",
            "switch_menu",
            "resizeEvent",
        ):
            assert hasattr(EzQt_App, method), f"Missing method: {method}"


class TestEzQtAppInstantiation:
    """Tests that the constructor can complete with mocked services."""

    # ------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------

    def test_should_produce_qmainwindow_instance_when_instantiated_with_mocked_services(
        self, qt_application
    ) -> None:
        """Verify successful instantiation."""
        instance = _make_instance(qt_application)
        assert isinstance(instance, QMainWindow)

    def test_should_have_none_theme_file_when_instantiated_without_theme(
        self, qt_application
    ) -> None:
        """Verify default theme file name is None."""
        instance = _make_instance(qt_application)
        assert instance._theme_file_name is None

    def test_should_store_custom_theme_file_when_theme_filename_is_given(
        self, qt_application
    ) -> None:
        """Verify custom theme file name is stored."""

        def fake_setupUi(_self_ui: object, window: EzQt_App, **_kwargs: object) -> None:
            window.ui = MagicMock()

        with (
            patch(_PATCHES["load_fonts"]),
            patch(_PATCHES["load_settings"]),
            patch(_PATCHES["config_svc"], return_value=_make_mock_config()),
            patch(_PATCHES["settings_svc"], return_value=_make_mock_settings()),
            patch(_PATCHES["translation_svc"], return_value=_make_mock_translation()),
            patch(_PATCHES["fonts_init"]),
            patch(_PATCHES["size_init"]),
            patch(_PATCHES["theme_svc"]),
            patch(_PATCHES["ui_def"]),
            patch(_PATCHES["setupUi"], new=fake_setupUi),
        ):
            instance = EzQt_App(theme_file_name="custom.qss")

        assert instance._theme_file_name == "custom.qss"


class TestEzQtAppMethods:
    """Tests for individual EzQt_App methods via a minimally-constructed instance."""

    # ------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------

    def test_should_delegate_to_header_when_set_app_icon_is_called(
        self, qt_application
    ) -> None:
        """Verify set_app_icon delegation."""
        instance = _make_instance(qt_application)
        instance.ui.header_container.set_app_logo = MagicMock()

        instance.set_app_icon("icon.png", y_shrink=5)

        instance.ui.header_container.set_app_logo.assert_called_once_with(
            logo="icon.png", y_shrink=5, y_offset=0
        )

    def test_should_call_resize_grips_when_resize_event_occurs(
        self, qt_application
    ) -> None:
        """Verify resizeEvent behavior."""
        instance = _make_instance(qt_application)

        with patch("ezqt_app.app.UiDefinitionsService.resize_grips") as mock_resize:
            from unittest.mock import MagicMock as MM

            instance.resizeEvent(MM())

        mock_resize.assert_called_once_with(instance)

    def test_should_apply_theme_when_update_ui_is_called(self, qt_application) -> None:
        """Verify update_ui behavior."""
        instance = _make_instance(qt_application)
        instance.ui.settings_panel.get_theme_selector.return_value = None

        with patch("ezqt_app.app.ThemeService.apply_theme") as mock_theme:
            instance.update_ui()

        mock_theme.assert_called_once_with(instance, instance._theme_file_name)

    def test_should_use_settings_service_theme_when_toggle_has_no_value(
        self, qt_application
    ) -> None:
        """Verify set_app_theme fallback behavior."""
        instance = _make_instance(qt_application)
        mock_settings = MagicMock()
        mock_settings.gui.THEME = "light"
        toggle = MagicMock(spec=[])  # no value_id, no value attributes
        instance.ui.settings_panel.get_theme_selector.return_value = toggle

        with (
            patch("ezqt_app.app.get_settings_service", return_value=mock_settings),
            patch("ezqt_app.app.AppService.write_yaml_config"),
            patch.object(instance, "update_ui"),
        ):
            instance.set_app_theme()

        mock_settings.set_theme.assert_called_once_with("light")
