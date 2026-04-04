"""
UI panel animation service implementation.
"""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from typing import cast

# Third-party imports
from PySide6.QtCore import QEasingCurve, QObject, QPropertyAnimation

# Local imports
from ...domain.ports.main_window import MainWindowProtocol
from ...utils.diagnostics import warn_tech
from ..settings import get_settings_service


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class PanelService:
    """Service responsible for menu and settings panel animations."""

    @staticmethod
    def toggle_menu_panel(window: MainWindowProtocol, enable: bool) -> None:
        """Animate the left menu panel between shrink and extended widths."""
        if not enable:
            return

        settings_service = get_settings_service()
        width = window.ui.menu_container.width()
        max_extend = window.ui.menu_container.get_extended_width()
        standard = window.ui.menu_container.get_shrink_width()
        width_extended = max_extend if width == standard else standard

        window.menu_animation = QPropertyAnimation(
            cast(QObject, window.ui.menu_container),
            b"minimumWidth",
        )
        window.menu_animation.setDuration(settings_service.gui.TIME_ANIMATION)
        window.menu_animation.setStartValue(width)
        window.menu_animation.setEndValue(width_extended)
        window.menu_animation.setEasingCurve(QEasingCurve.Type.InOutQuart)
        window.menu_animation.start()

    @staticmethod
    def toggle_settings_panel(window: MainWindowProtocol, enable: bool) -> None:
        """Animate the right settings panel and synchronize theme toggle."""
        if not enable:
            return

        settings_service = get_settings_service()
        width = window.ui.settings_panel.width()
        max_extend = settings_service.gui.SETTINGS_PANEL_WIDTH
        standard = 0
        is_opening = width == 0
        width_extended = max_extend if is_opening else standard

        window.ui.header_container.set_settings_panel_open(is_opening)

        window.settings_animation = QPropertyAnimation(
            cast(QObject, window.ui.settings_panel),
            b"minimumWidth",
        )
        window.settings_animation.setDuration(settings_service.gui.TIME_ANIMATION)
        window.settings_animation.setStartValue(width)
        window.settings_animation.setEndValue(width_extended)
        window.settings_animation.setEasingCurve(QEasingCurve.Type.InOutQuart)
        window.settings_animation.start()

        theme_toggle = window.ui.settings_panel.get_theme_selector()
        if theme_toggle and hasattr(theme_toggle, "set_value"):
            try:
                gui = settings_service.gui
                internal = f"{gui.THEME_PRESET}:{gui.THEME}"
                value_to_display = getattr(
                    window.ui.settings_panel, "_theme_value_to_display", {}
                )
                display = value_to_display.get(internal, "")
                if display:
                    theme_toggle.set_value(display)
            except Exception as error:
                warn_tech(
                    code="ui.panel.theme_selector_sync_failed",
                    message="Theme selector sync failed on panel open",
                    error=error,
                )
