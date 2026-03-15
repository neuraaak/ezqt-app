# ///////////////////////////////////////////////////////////////
# SERVICES.UI.UI_FUNCTIONS - Unified UI facade class
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Legacy UIFunctions facade providing a unified camelCase interface to UI services."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from typing import cast

# Local imports
from ...domain.ports.main_window import MainWindowProtocol
from .definitions_service import UiDefinitionsService
from .menu_service import MenuService
from .panel_service import PanelService
from .theme_service import ThemeService
from .window_service import WindowService


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class UIFunctions:
    """Unified UI functions facade (legacy camelCase API).

    Combines all specialized UI services to provide a single interface
    for user interface management. Kept for backward compatibility.
    """

    def __init__(self) -> None:
        pass

    # ///////////////////////////////////////////////////////////////
    # WINDOW MANAGEMENT

    def _w(self) -> MainWindowProtocol:
        """Cast self to MainWindowProtocol (UIFunctions is a QMainWindow mixin)."""
        return cast(MainWindowProtocol, self)

    def maximize_restore(self) -> None:
        """Maximize or restore window based on current state."""
        WindowService.maximize_restore(self._w())

    def returnStatus(self):
        """Return current window state."""
        return WindowService.get_status()

    def setStatus(self, status) -> None:
        """Set window state."""
        WindowService.set_status(status)

    # ///////////////////////////////////////////////////////////////
    # PANEL MANAGEMENT

    def toggleMenuPanel(self, enable) -> None:
        """Toggle menu panel display."""
        PanelService.toggle_menu_panel(self._w(), enable)

    def toggleSettingsPanel(self, enable) -> None:
        """Toggle settings panel display."""
        PanelService.toggle_settings_panel(self._w(), enable)

    # ///////////////////////////////////////////////////////////////
    # MENU MANAGEMENT

    def selectMenu(self, widget) -> None:
        """Select a menu item."""
        MenuService.select_menu(self._w(), widget)

    def deselectMenu(self, widget) -> None:
        """Deselect a menu item."""
        MenuService.deselect_menu(self._w(), widget)

    def refreshStyle(self, w):
        """Refresh widget style."""
        MenuService.refresh_style(w)

    # ///////////////////////////////////////////////////////////////
    # THEME MANAGEMENT

    def theme(self, customThemeFile: str | None = None) -> None:
        """Load and apply theme to interface."""
        ThemeService.apply_theme(self._w(), customThemeFile)

    # ///////////////////////////////////////////////////////////////
    # UI DEFINITIONS

    def uiDefinitions(self) -> None:
        """Configure and initialize all user interface elements."""
        UiDefinitionsService.apply_definitions(self)

    def resize_grips(self) -> None:
        """Resize window resize grips."""
        UiDefinitionsService.resize_grips(self._w())


# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////
__all__ = ["UIFunctions"]
