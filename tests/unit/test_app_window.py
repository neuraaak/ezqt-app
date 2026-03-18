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

    def test_should_emit_deprecation_when_theme_file_name_is_given(
        self, qt_application
    ) -> None:
        """Passing theme_file_name emits a deprecation warning."""

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
            patch("ezqt_app.app.warn_tech") as mock_warn,
        ):
            EzQt_App(theme_file_name="custom.qss")

        mock_warn.assert_called_once()
        call_kwargs = mock_warn.call_args
        assert "theme_file_name" in call_kwargs.kwargs.get(
            "code", call_kwargs.args[0] if call_kwargs.args else ""
        )


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
        """Verify update_ui calls ThemeService.apply_theme with the window."""
        instance = _make_instance(qt_application)
        instance.ui.settings_panel.get_theme_selector = MagicMock(return_value=None)

        with patch("ezqt_app.app.ThemeService.apply_theme") as mock_theme:
            instance.update_ui()

        mock_theme.assert_called_once_with(instance)

    def test_should_delegate_to_update_ui_when_set_app_theme_is_called(
        self, qt_application
    ) -> None:
        """set_app_theme() delegates to update_ui(); theme is already set by the selector."""
        instance = _make_instance(qt_application)

        with patch.object(instance, "update_ui") as mock_update:
            instance.set_app_theme()

        mock_update.assert_called_once()
