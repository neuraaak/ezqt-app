# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_WIDGETS.TEST_UI_MAIN - Ui_MainWindow tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for widgets/ui_main.py — Ui_MainWindow.setupUi()."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
from unittest.mock import MagicMock, patch

from PySide6.QtWidgets import QMainWindow

from ezqt_app.widgets.ui_main import Ui_MainWindow

# ///////////////////////////////////////////////////////////////
# HELPERS
# ///////////////////////////////////////////////////////////////

_SETTINGS_PATH = "ezqt_app.widgets.ui_main.get_settings_service"


def _mock_settings() -> MagicMock:
    mock = MagicMock()
    mock.gui.MENU_PANEL_SHRINKED_WIDTH = 50
    mock.gui.MENU_PANEL_EXTENDED_WIDTH = 200
    mock.gui.SETTINGS_PANEL_WIDTH = 240
    return mock


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////


class TestUiMainWindowInstantiation:
    """Tests for Ui_MainWindow class-level behavior."""

    def test_should_be_instantiable_when_ui_main_window_is_created(self) -> None:
        ui = Ui_MainWindow()
        assert ui is not None

    def test_should_have_setup_ui_method_when_class_is_loaded(self) -> None:
        assert callable(Ui_MainWindow.setupUi)


class TestUiMainWindowSetupUi:
    """Tests for Ui_MainWindow.setupUi()."""

    def test_should_set_central_widget_when_setup_ui_is_called(
        self, qt_application
    ) -> None:
        main_window = QMainWindow()
        ui = Ui_MainWindow()
        with patch(_SETTINGS_PATH, return_value=_mock_settings()):
            ui.setupUi(main_window)
        assert main_window.centralWidget() is not None

    def test_should_create_header_container_when_setup_ui_is_called(
        self, qt_application
    ) -> None:
        main_window = QMainWindow()
        ui = Ui_MainWindow()
        with patch(_SETTINGS_PATH, return_value=_mock_settings()):
            ui.setupUi(main_window)
        assert hasattr(ui, "headerContainer")
        assert ui.headerContainer is not None

    def test_should_create_menu_container_when_setup_ui_is_called(
        self, qt_application
    ) -> None:
        main_window = QMainWindow()
        ui = Ui_MainWindow()
        with patch(_SETTINGS_PATH, return_value=_mock_settings()):
            ui.setupUi(main_window)
        assert hasattr(ui, "menuContainer")
        assert ui.menuContainer is not None

    def test_should_create_pages_container_when_setup_ui_is_called(
        self, qt_application
    ) -> None:
        main_window = QMainWindow()
        ui = Ui_MainWindow()
        with patch(_SETTINGS_PATH, return_value=_mock_settings()):
            ui.setupUi(main_window)
        assert hasattr(ui, "pagesContainer")
        assert ui.pagesContainer is not None

    def test_should_create_settings_panel_when_setup_ui_is_called(
        self, qt_application
    ) -> None:
        main_window = QMainWindow()
        ui = Ui_MainWindow()
        with patch(_SETTINGS_PATH, return_value=_mock_settings()):
            ui.setupUi(main_window)
        assert hasattr(ui, "settingsPanel")
        assert ui.settingsPanel is not None

    def test_should_create_bottom_bar_when_setup_ui_is_called(
        self, qt_application
    ) -> None:
        main_window = QMainWindow()
        ui = Ui_MainWindow()
        with patch(_SETTINGS_PATH, return_value=_mock_settings()):
            ui.setupUi(main_window)
        assert hasattr(ui, "bottomBar")
        assert ui.bottomBar is not None

    def test_should_set_minimum_window_size_when_setup_ui_is_called(
        self, qt_application
    ) -> None:
        main_window = QMainWindow()
        ui = Ui_MainWindow()
        with patch(_SETTINGS_PATH, return_value=_mock_settings()):
            ui.setupUi(main_window)
        # setupUi resizes to 1280×720 and sets minimumSize to 940×560
        assert main_window.minimumWidth() == 940
        assert main_window.minimumHeight() == 560

    def test_should_create_app_margins_layout_when_setup_ui_is_called(
        self, qt_application
    ) -> None:
        main_window = QMainWindow()
        ui = Ui_MainWindow()
        with patch(_SETTINGS_PATH, return_value=_mock_settings()):
            ui.setupUi(main_window)
        assert hasattr(ui, "appMargins")
        assert ui.appMargins is not None
