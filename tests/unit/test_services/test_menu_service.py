# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_SERVICES.TEST_MENU_SERVICE - MenuService tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for services/ui/menu_service.py."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
from types import SimpleNamespace
from unittest.mock import patch

from PySide6.QtWidgets import QToolButton, QWidget

from ezqt_app.services.ui.menu_service import MenuService


def _build_window_with_buttons() -> tuple[SimpleNamespace, QToolButton, QToolButton]:
    top_menu = QWidget()

    button_home = QToolButton(top_menu)
    button_home.setObjectName("home")

    button_settings = QToolButton(top_menu)
    button_settings.setObjectName("settings")

    window = SimpleNamespace(
        ui=SimpleNamespace(menu_container=SimpleNamespace(top_menu=top_menu))
    )
    return window, button_home, button_settings


class TestMenuService:
    """Tests for menu button selection and style refresh."""

    def test_should_set_active_class_for_selected_menu_button(
        self, qt_application
    ) -> None:
        window, home, settings = _build_window_with_buttons()

        with patch.object(MenuService, "refresh_style") as refresh:
            MenuService.select_menu(window, "settings")

        assert settings.property("class") == "active"
        assert home.property("class") != "active"
        refresh.assert_called_once_with(settings)

    def test_should_set_inactive_class_for_non_selected_buttons(
        self, qt_application
    ) -> None:
        window, home, settings = _build_window_with_buttons()

        with patch.object(MenuService, "refresh_style") as refresh:
            MenuService.deselect_menu(window, "settings")

        assert home.property("class") == "inactive"
        assert settings.property("class") != "inactive"
        refresh.assert_called_once_with(home)

    def test_should_unpolish_and_polish_widget_style_when_refreshing(self) -> None:
        widget = QWidget()
        style = widget.style()

        with (
            patch.object(style, "unpolish") as unpolish,
            patch.object(style, "polish") as polish,
        ):
            MenuService.refresh_style(widget)

        unpolish.assert_called_once_with(widget)
        polish.assert_called_once_with(widget)
