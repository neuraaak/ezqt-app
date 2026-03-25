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
from PySide6.QtCore import QCoreApplication, QEvent, QSize, Qt
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
        self.setObjectName("menu_container")
        self.setMinimumSize(QSize(self._shrink_width, 0))
        self.setMaximumSize(QSize(self._shrink_width, 16777215))
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setFrameShadow(QFrame.Shadow.Raised)

        # ////// SETUP MAIN LAYOUT
        self._menu_layout = QVBoxLayout(self)
        self._menu_layout.setSpacing(0)
        self._menu_layout.setObjectName("menu_layout")
        self._menu_layout.setContentsMargins(0, 0, 0, 0)

        # ////// SETUP MAIN MENU FRAME
        self._main_menu_frame = QFrame(self)
        self._main_menu_frame.setObjectName("main_menu_frame")
        self._main_menu_frame.setFrameShape(QFrame.Shape.NoFrame)
        self._main_menu_frame.setFrameShadow(QFrame.Shadow.Raised)
        self._menu_layout.addWidget(self._main_menu_frame)

        # ////// SETUP MAIN MENU LAYOUT
        self._main_menu_layout = QVBoxLayout(self._main_menu_frame)
        self._main_menu_layout.setSpacing(0)
        self._main_menu_layout.setObjectName("main_menu_layout")
        self._main_menu_layout.setContentsMargins(0, 0, 0, 0)

        # ////// SETUP TOGGLE CONTAINER
        self._toggle_container = QFrame(self._main_menu_frame)
        self._toggle_container.setObjectName("toggle_container")
        self._toggle_container.setMaximumSize(QSize(16777215, 45))
        self._toggle_container.setFrameShape(QFrame.Shape.NoFrame)
        self._toggle_container.setFrameShadow(QFrame.Shadow.Raised)
        self._main_menu_layout.addWidget(self._toggle_container)

        # ////// SETUP TOGGLE LAYOUT
        self._toggle_layout = QVBoxLayout(self._toggle_container)
        self._toggle_layout.setSpacing(0)
        self._toggle_layout.setObjectName("toggle_layout")
        self._toggle_layout.setContentsMargins(0, 0, 0, 0)

        # ////// SETUP TOGGLE BUTTON
        # Lazy import to avoid circular imports
        from ezqt_widgets import ThemeIcon

        from ...widgets.extended.menu_button import MenuButton

        settings_service = get_settings_service()

        # Store the toggle button label so retranslate_ui() can re-apply it.
        self._toggle_text: str = "Hide"

        self.toggle_button = MenuButton(
            parent=self._toggle_container,
            icon=Icons.icon_menu,
            text=self._toggle_text,
            shrink_size=self._shrink_width,
            spacing=15,
            duration=settings_service.gui.TIME_ANIMATION,
        )
        self.toggle_button.setObjectName("toggle_button")
        _sp = SizePolicy.H_EXPANDING_V_FIXED
        if _sp is not None:
            _sp.setHeightForWidth(self.toggle_button.sizePolicy().hasHeightForWidth())
            self.toggle_button.setSizePolicy(_sp)
        self.toggle_button.setMinimumSize(QSize(0, 45))
        if Fonts.SEGOE_UI_10_REG is not None:
            self.toggle_button.setFont(Fonts.SEGOE_UI_10_REG)
        self.toggle_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.toggle_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        icon_menu = ThemeIcon(Icons.icon_menu, theme=settings_service.gui.THEME)
        self._buttons.append(self.toggle_button)
        self._icons.append(icon_menu)
        # Connect to the toggle_state method
        self.toggle_button.clicked.connect(self.toggle_button.toggle_state)

        self._toggle_layout.addWidget(self.toggle_button)

        # ////// SETUP TOP MENU
        self.top_menu = QFrame(self._main_menu_frame)
        self.top_menu.setObjectName("top_menu")
        self.top_menu.setFrameShape(QFrame.Shape.NoFrame)
        self.top_menu.setFrameShadow(QFrame.Shadow.Raised)
        self._main_menu_layout.addWidget(self.top_menu, 0, Qt.AlignmentFlag.AlignTop)

        # ////// SETUP TOP MENU LAYOUT
        self._top_menu_layout = QVBoxLayout(self.top_menu)
        self._top_menu_layout.setSpacing(0)
        self._top_menu_layout.setObjectName("top_menu_layout")
        self._top_menu_layout.setContentsMargins(0, 0, 0, 0)

        # ////// SYNC INITIAL STATE
        self._sync_initial_state()

    # ///////////////////////////////////////////////////////////////
    # UTILITY FUNCTIONS

    def _tr(self, text: str) -> str:
        """Shortcut for translation with global context."""
        return QCoreApplication.translate("EzQt_App", text)

    def retranslate_ui(self) -> None:
        """Apply current translations to all owned text labels and tooltips."""
        # The buttons are now autonomous and know how to retranslate themselves
        # as they store their original untranslated text.
        if hasattr(self.toggle_button, "retranslate_ui"):
            self.toggle_button.retranslate_ui()
            # Dynamic tooltip for the toggle button
            self.toggle_button.setToolTip(self._tr(self._toggle_text))

        for menu_btn in self.menus.values():
            if hasattr(menu_btn, "retranslate_ui"):
                menu_btn.retranslate_ui()
                # Dynamic tooltip: very useful when the menu is shrunk
                # menu_btn._original_text contains the key (e.g. "Home")
                original_text = getattr(menu_btn, "_original_text", "")
                if original_text:
                    menu_btn.setToolTip(self._tr(original_text))

    def changeEvent(self, event: QEvent) -> None:
        """Handle Qt change events, triggering UI retranslation on language change."""
        if event.type() == QEvent.Type.LanguageChange:
            self.retranslate_ui()
        super().changeEvent(event)

    def _sync_initial_state(self) -> None:
        """Sync the initial state of all buttons with the container state."""
        if hasattr(self, "toggle_button"):
            self.toggle_button.set_state(False)
            self.sync_all_menu_states(False)

    def add_menu(self, name: str, icon: QIcon | str | None = None):
        """Add a menu item to the container."""
        # Lazy import to avoid circular imports
        from ezqt_widgets import ThemeIcon

        from ...widgets.extended.menu_button import MenuButton

        current_theme = get_settings_service().gui.THEME

        menu = MenuButton(
            parent=self.top_menu,
            icon=icon,
            text=name,
            shrink_size=self._shrink_width,
            spacing=15,
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
        theme_icon = ThemeIcon(icon, theme=current_theme) if icon is not None else None
        self._buttons.append(menu)
        self._icons.append(theme_icon)

        # Connect to the toggle button to sync state
        self.toggle_button.stateChanged.connect(menu.set_state)

        self._top_menu_layout.addWidget(menu)
        self.menus[name] = menu

        return menu

    def update_all_theme_icons(self) -> None:
        """Update theme icons for all buttons."""
        current_theme = get_settings_service().gui.THEME
        for i, btn in enumerate(self._buttons):
            icon = self._icons[i]
            setter = getattr(icon, "setTheme", None)
            if callable(setter):
                setter(current_theme)
            updater = getattr(btn, "update_theme_icon", None)
            if icon is not None and callable(updater):
                updater(icon)

    def sync_all_menu_states(self, extended: bool) -> None:
        """Sync all menu buttons to the given state."""
        for btn in self._buttons:
            setter = getattr(btn, "set_state", None)
            if btn != self.toggle_button and callable(setter):
                setter(extended)

    def get_menu_state(self) -> bool:
        """Get the current menu state."""
        if hasattr(self, "toggle_button"):
            return self.toggle_button.is_extended
        return False

    def get_shrink_width(self) -> int:
        """Get the configured shrink width."""
        return self._shrink_width

    def get_extended_width(self) -> int:
        """Get the configured extended width."""
        return self._extended_width


# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////
__all__ = ["Menu"]
