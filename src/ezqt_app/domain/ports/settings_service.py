# ///////////////////////////////////////////////////////////////
# DOMAIN.PORTS.SETTINGS_SERVICE - Settings service port
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Protocol definitions for settings services."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from typing import Protocol

# Local imports
from ...domain.models.settings import AppSettingsModel, GuiSettingsModel


# ///////////////////////////////////////////////////////////////
# PROTOCOLS
# ///////////////////////////////////////////////////////////////
class SettingsServiceProtocol(Protocol):
    """Technical contract for mutable application settings state."""

    @property
    def app(self) -> AppSettingsModel:
        """Return mutable application settings."""
        ...

    @property
    def gui(self) -> GuiSettingsModel:
        """Return mutable GUI settings."""
        ...

    def set_app_name(self, name: str) -> None:
        """Set application name."""
        ...

    def set_app_description(self, description: str) -> None:
        """Set application description."""
        ...

    def set_custom_title_bar_enabled(self, enabled: bool) -> None:
        """Enable or disable custom title bar."""
        ...

    def set_app_min_size(self, width: int, height: int) -> None:
        """Set minimum window size as (width, height) integers."""
        ...

    def set_app_dimensions(self, width: int, height: int) -> None:
        """Set default window dimensions."""
        ...

    def set_debug_enabled(self, enabled: bool) -> None:
        """Enable or disable debug console output."""
        ...

    def set_theme(self, theme: str) -> None:
        """Set active theme."""
        ...

    def set_menu_widths(self, shrinked: int, extended: int) -> None:
        """Set menu panel widths."""
        ...

    def set_settings_panel_width(self, width: int) -> None:
        """Set settings panel width."""
        ...

    def set_time_animation(self, duration: int) -> None:
        """Set animation duration in milliseconds."""
        ...
