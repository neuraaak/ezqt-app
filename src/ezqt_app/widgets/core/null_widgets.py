# ///////////////////////////////////////////////////////////////
# WIDGETS.CORE.NULL_WIDGETS - Null Object implementations for UI
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Null Object implementations for optional UI components.

These classes satisfy the MainWindowProtocol contracts while performing
no operations and occupying no space. They allow the application to
run without specific components (like the menu) without requiring
conditional logic in services.
"""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from typing import TYPE_CHECKING, Any

# Third-party imports
from PySide6.QtWidgets import QToolButton, QWidget

if TYPE_CHECKING:
    from PySide6.QtWidgets import QPushButton


# ///////////////////////////////////////////////////////////////
# NULL MENU IMPLEMENTATION
# ///////////////////////////////////////////////////////////////


class NullTopMenu(QWidget):
    """Null implementation of _TopMenuProtocol."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.hide()
        self.setMaximumSize(0, 0)


class NullMenuContainer(QWidget):
    """Null implementation of MenuContainerProtocol.

    Occupies 0px width and performs no actions.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.top_menu = NullTopMenu(self)
        self.toggle_button: QPushButton | None = None
        self.menus: dict[str, QToolButton] = {}  # Missing attribute
        self.hide()
        self.setMaximumSize(0, 0)

    def width(self) -> int:
        return 0

    def get_extended_width(self) -> int:
        return 0

    def get_shrink_width(self) -> int:
        return 0

    def update_all_theme_icons(self) -> None:
        """No-op."""

    def add_menu(self, _name: str, _icon: str) -> QToolButton:
        """Return a dummy button to avoid NoneType errors in signals."""
        return QToolButton(self)


# ///////////////////////////////////////////////////////////////
# NULL SETTINGS PANEL IMPLEMENTATION
# ///////////////////////////////////////////////////////////////


class NullSettingsPanel(QWidget):
    """Null implementation of SettingsPanelProtocol."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.hide()
        self.setMaximumSize(0, 0)

    def width(self) -> int:
        return 0

    def get_theme_selector(self) -> Any:
        return None

    def update_all_theme_icons(self) -> None:
        """No-op."""
