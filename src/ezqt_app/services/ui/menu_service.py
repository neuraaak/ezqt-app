"""
UI menu service implementation.
"""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Third-party imports
from PySide6.QtWidgets import QToolButton, QWidget

# Local imports
from ...domain.ports.main_window import MainWindowProtocol

# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////


class MenuService:
    """Service responsible for menu item selection state and style refresh."""

    @staticmethod
    def select_menu(window: MainWindowProtocol, widget: str) -> None:
        """Set active class on a menu button identified by its object name."""
        for menu_widget in window.ui.menu_container.top_menu.findChildren(QToolButton):
            if menu_widget.objectName() == widget and isinstance(
                menu_widget, QToolButton
            ):
                menu_widget.setProperty("class", "active")
                MenuService.refresh_style(menu_widget)

    @staticmethod
    def deselect_menu(window: MainWindowProtocol, widget: str) -> None:
        """Set inactive class on all menu buttons except the selected one."""
        for menu_widget in window.ui.menu_container.top_menu.findChildren(QToolButton):
            if menu_widget.objectName() != widget and isinstance(
                menu_widget, QToolButton
            ):
                menu_widget.setProperty("class", "inactive")
                MenuService.refresh_style(menu_widget)

    @staticmethod
    def refresh_style(widget: QWidget) -> None:
        """Re-apply widget style after dynamic property changes."""
        widget.style().unpolish(widget)
        widget.style().polish(widget)
