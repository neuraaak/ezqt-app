# ///////////////////////////////////////////////////////////////
# WIDGETS.CORE.MENU - Menu container widget
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Menu container with toggle button and expandable navigation."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from typing import Any

# Third-party imports
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QCursor, QIcon
from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget

# Local imports
from ...services.settings import get_settings_service
from ...services.ui import Fonts, SizePolicy
from ...shared.resources import Icons


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class Menu(QFrame):
    """
    Menu container with expansion/reduction support.

    This class provides a menu container with a toggle button
    to expand or reduce the menu width. The menu contains an upper
    section for menu items and a lower section for the toggle button.
    """

    def __init__(
        self,
        parent: QWidget | None = None,
        shrink_width: int = 60,
        extended_width: int = 240,
    ) -> None:
        """
        Initialize the menu container.

        Parameters
        ----------
        parent : QWidget, optional
            The parent widget (default: None).
        shrink_width : int, optional
            Width when menu is shrunk (default: 60).
        extended_width : int, optional
            Width when menu is extended (default: 240).
        """
        super().__init__(parent)

        # ////// STORE CONFIGURATION
        self._shrink_width = shrink_width
        self._extended_width = extended_width
        self.menus: dict[str, Any] = {}
        self._buttons: list[Any] = []
        self._icons: list[Any | None] = []

        # ////// SETUP WIDGET PROPERTIES
        self.setObjectName("menuContainer")
        self.setMinimumSize(QSize(self._shrink_width, 0))
        self.setMaximumSize(QSize(self._shrink_width, 16777215))
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setFrameShadow(QFrame.Shadow.Raised)

        # ////// SETUP MAIN LAYOUT
        self.VL_menuContainer = QVBoxLayout(self)
        self.VL_menuContainer.setSpacing(0)
        self.VL_menuContainer.setObjectName("VL_menuContainer")
        self.VL_menuContainer.setContentsMargins(0, 0, 0, 0)

        # ////// SETUP MAIN MENU FRAME
        self.mainMenuFrame = QFrame(self)
        self.mainMenuFrame.setObjectName("mainMenuFrame")
        self.mainMenuFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.mainMenuFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.VL_menuContainer.addWidget(self.mainMenuFrame)

        # ////// SETUP MAIN MENU LAYOUT
        self.VL_mainMenuFrame = QVBoxLayout(self.mainMenuFrame)
        self.VL_mainMenuFrame.setSpacing(0)
        self.VL_mainMenuFrame.setObjectName("VL_mainMenuFrame")
        self.VL_mainMenuFrame.setContentsMargins(0, 0, 0, 0)

        # ////// SETUP TOGGLE CONTAINER
        self.toggleBox = QFrame(self.mainMenuFrame)
        self.toggleBox.setObjectName("toggleBox")
        self.toggleBox.setMaximumSize(QSize(16777215, 45))
        self.toggleBox.setFrameShape(QFrame.Shape.NoFrame)
        self.toggleBox.setFrameShadow(QFrame.Shadow.Raised)
        self.VL_mainMenuFrame.addWidget(self.toggleBox)

        # ////// SETUP TOGGLE LAYOUT
        self.VL_toggleBox = QVBoxLayout(self.toggleBox)
        self.VL_toggleBox.setSpacing(0)
        self.VL_toggleBox.setObjectName("VL_toggleBox")
        self.VL_toggleBox.setContentsMargins(0, 0, 0, 0)

        # ////// SETUP TOGGLE BUTTON
        # Lazy import to avoid circular imports
        from ...widgets.extended.menu_button import MenuButton
        from ...widgets.extended.theme_icon import ThemeIcon

        settings_service = get_settings_service()

        self.toggleButton = MenuButton(
            parent=self.toggleBox,
            icon=Icons.icon_menu,
            text="Hide",
            shrink_size=self._shrink_width,
            spacing=15,  # Reduced from 35 to 15 for better alignment
            duration=settings_service.gui.TIME_ANIMATION,
        )
        self.toggleButton.setObjectName("toggleButton")
        _sp = SizePolicy.H_EXPANDING_V_FIXED
        if _sp is not None:
            _sp.setHeightForWidth(self.toggleButton.sizePolicy().hasHeightForWidth())
            self.toggleButton.setSizePolicy(_sp)
        self.toggleButton.setMinimumSize(QSize(0, 45))
        if Fonts.SEGOE_UI_10_REG is not None:
            self.toggleButton.setFont(Fonts.SEGOE_UI_10_REG)
        self.toggleButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.toggleButton.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        # Don't set contents margins here - MenuButton handles its own positioning
        # self.toggleButton.setContentsMargins(20, 0, 0, 0)
        #
        icon_menu = ThemeIcon(Icons.icon_menu)
        self._buttons.append(self.toggleButton)
        self._icons.append(icon_menu)
        # Connect to the new toggle_state method
        self.toggleButton.clicked.connect(self.toggleButton.toggle_state)
        #
        self.VL_toggleBox.addWidget(self.toggleButton)

        # ////// SETUP TOP MENU
        self.topMenu = QFrame(self.mainMenuFrame)
        self.topMenu.setObjectName("topMenu")
        self.topMenu.setFrameShape(QFrame.Shape.NoFrame)
        self.topMenu.setFrameShadow(QFrame.Shadow.Raised)
        self.VL_mainMenuFrame.addWidget(self.topMenu, 0, Qt.AlignmentFlag.AlignTop)

        # ////// SETUP TOP MENU LAYOUT
        self.VL_topMenu = QVBoxLayout(self.topMenu)
        self.VL_topMenu.setSpacing(0)
        self.VL_topMenu.setObjectName("VL_topMenu")
        self.VL_topMenu.setContentsMargins(0, 0, 0, 0)

        # ////// SYNC INITIAL STATE
        self._sync_initial_state()

    # ///////////////////////////////////////////////////////////////
    # UTILITY FUNCTIONS

    def _sync_initial_state(self) -> None:
        """
        Sync the initial state of all buttons with the container state.

        The menu container starts shrunk, so all buttons
        must start in the shrunk state.
        """
        if hasattr(self, "toggleButton"):
            # Force toggle button to shrink state
            self.toggleButton.set_state(False)  # False = shrink state
            # Sync all existing menu buttons
            self.sync_all_menu_states(False)

    def add_menu(self, name: str, icon: QIcon | str | None = None):
        """
        Add a menu item to the container.

        Parameters
        ----------
        name : str
            The name of the menu item.
        icon : str or Icons, optional
            The icon for the menu item (default: None).

        Returns
        -------
        MenuButton
            The created menu button.
        """
        # Lazy import to avoid circular imports
        from ...widgets.extended.menu_button import MenuButton
        from ...widgets.extended.theme_icon import ThemeIcon

        menu = MenuButton(
            parent=self.topMenu,
            icon=icon,
            text=name,
            shrink_size=self._shrink_width,
            spacing=15,  # Reduced from 35 to 15 for better alignment
            duration=get_settings_service().gui.TIME_ANIMATION,
        )
        menu.setObjectName(f"menu_{name}")
        menu.setProperty("class", "inactive")
        _sp = SizePolicy.H_EXPANDING_V_FIXED
        if _sp is not None:
            _sp.setHeightForWidth(menu.sizePolicy().hasHeightForWidth())
            menu.setSizePolicy(_sp)
        menu.setMinimumSize(QSize(0, 45))
        if Fonts.SEGOE_UI_10_REG is not None:
            menu.setFont(Fonts.SEGOE_UI_10_REG)
        menu.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        menu.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        # ////// SETUP THEME ICON
        theme_icon = ThemeIcon(icon) if icon is not None else None
        self._buttons.append(menu)
        self._icons.append(theme_icon)

        # Connect to the toggle button to sync state
        self.toggleButton.stateChanged.connect(menu.set_state)

        self.VL_topMenu.addWidget(menu)
        self.menus[name] = menu

        return menu

    def update_all_theme_icons(self) -> None:
        """Update theme icons for all buttons."""
        for i, btn in enumerate(self._buttons):
            icon = self._icons[i]
            updater = getattr(btn, "update_theme_icon", None)
            if icon is not None and callable(updater):
                updater(icon)

    def sync_all_menu_states(self, extended: bool) -> None:
        """
        Sync all menu buttons to the given state.

        Parameters
        ----------
        extended : bool
            True for extended, False for shrunk.
        """
        for btn in self._buttons:
            setter = getattr(btn, "set_state", None)
            if btn != self.toggleButton and callable(setter):
                setter(extended)

    def get_menu_state(self) -> bool:
        """
        Get the current menu state.

        Returns
        -------
        bool
            True if extended, False if shrunk.
        """
        if hasattr(self, "toggleButton"):
            return self.toggleButton.is_extended
        return False

    def get_shrink_width(self) -> int:
        """
        Get the configured shrink width.

        Returns
        -------
        int
            The shrink width.
        """
        return self._shrink_width

    def get_extended_width(self) -> int:
        """
        Get the configured extended width.

        Returns
        -------
        int
            The extended width.
        """
        return self._extended_width


# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////
__all__ = ["Menu"]
