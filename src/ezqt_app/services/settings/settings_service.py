# ///////////////////////////////////////////////////////////////
# SERVICES.SETTINGS.SERVICE - Settings service
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Settings service implementation."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Third-party imports
from PySide6.QtCore import QSize

from ...domain.models.settings import (
    AppSettingsModel,
    GuiSettingsModel,
    SettingsStateModel,
)
from ...domain.ports.settings_service import SettingsServiceProtocol

# Local imports
from .._registry import ServiceRegistry


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class SettingsService(SettingsServiceProtocol):
    """Service managing mutable application settings state."""

    def __init__(self) -> None:
        """Initialize settings state container."""
        self._state = SettingsStateModel()

    @property
    def app(self) -> AppSettingsModel:
        """Return mutable application settings."""
        return self._state.app

    @property
    def gui(self) -> GuiSettingsModel:
        """Return mutable GUI settings."""
        return self._state.gui

    def set_app_name(self, name: str) -> None:
        """Set application name."""
        self.app.NAME = name

    def set_app_description(self, description: str) -> None:
        """Set application description."""
        self.app.DESCRIPTION = description

    def set_custom_title_bar_enabled(self, enabled: bool) -> None:
        """Enable or disable custom title bar."""
        self.app.ENABLE_CUSTOM_TITLE_BAR = enabled

    def set_app_min_size(self, width: int, height: int) -> None:
        """Set minimum window size."""
        self.app.APP_MIN_SIZE = (width, height)

    def set_app_min_size_qsize(self, size: QSize) -> None:
        """Set minimum window size from QSize (convenience, not part of the port)."""
        self.app.APP_MIN_SIZE = (size.width(), size.height())

    def set_app_dimensions(self, width: int, height: int) -> None:
        """Set default window dimensions."""
        self.app.APP_WIDTH = width
        self.app.APP_HEIGHT = height

    def set_debug_enabled(self, enabled: bool) -> None:
        """Enable or disable debug console output."""
        self.app.DEBUG = enabled

    def set_theme(self, theme: str) -> None:
        """Set active theme.

        Accepts either a ``'preset:variant'`` string (e.g. ``'blue_gray:dark'``)
        or a bare variant (e.g. ``'dark'``, ``'light'``) for backward compat.
        A bare variant keeps the current ``THEME_PRESET`` unchanged.
        """
        value = theme.lower().strip()
        if ":" in value:
            preset, _, variant = value.partition(":")
            self.gui.THEME_PRESET = preset.strip()
            self.gui.THEME = variant.strip()
        else:
            self.gui.THEME = value

    def set_menu_widths(self, shrinked: int, extended: int) -> None:
        """Set menu panel widths."""
        self.gui.MENU_PANEL_SHRINKED_WIDTH = shrinked
        self.gui.MENU_PANEL_EXTENDED_WIDTH = extended

    def set_settings_panel_width(self, width: int) -> None:
        """Set settings panel width."""
        self.gui.SETTINGS_PANEL_WIDTH = width

    def set_time_animation(self, duration: int) -> None:
        """Set animation duration in milliseconds."""
        self.gui.TIME_ANIMATION = duration


# ///////////////////////////////////////////////////////////////
# FUNCTIONS
# ///////////////////////////////////////////////////////////////
def get_settings_service() -> SettingsService:
    """Return the singleton settings service."""
    return ServiceRegistry.get(SettingsService, SettingsService)
