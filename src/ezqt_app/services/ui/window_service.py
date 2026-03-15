"""
Window state service implementation for UI runtime interactions.
"""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Third-party imports
from PySide6.QtGui import QIcon

# Local imports
from ...domain.ports.main_window import MainWindowProtocol
from ..runtime import get_runtime_state_service


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class WindowService:
    """Service responsible for maximize/restore and window state flags."""

    @staticmethod
    def maximize_restore(window: MainWindowProtocol) -> None:
        """Toggle between maximized and restored window state."""
        runtime_state_service = get_runtime_state_service()
        is_maximized = runtime_state_service.get_global_state()

        if not is_maximized:
            window.showMaximized()
            runtime_state_service.set_global_state(True)
            window.ui.app_margins_layout.setContentsMargins(0, 0, 0, 0)
            window.ui.header_container.maximize_restore_btn.setToolTip("Restore")
            window.ui.header_container.maximize_restore_btn.setIcon(
                QIcon(":/icons/icons/icon_restore.png")
            )
            window.ui.bottom_bar.size_grip_spacer.hide()
            window.left_grip.hide()
            window.right_grip.hide()
            window.top_grip.hide()
            window.bottom_grip.hide()
            return

        runtime_state_service.set_global_state(False)
        window.showNormal()
        window.resize(window.width() + 1, window.height() + 1)
        window.ui.app_margins_layout.setContentsMargins(10, 10, 10, 10)
        window.ui.header_container.maximize_restore_btn.setToolTip("Maximize")
        window.ui.header_container.maximize_restore_btn.setIcon(
            QIcon(":/icons/icons/icon_maximize.png")
        )
        window.ui.bottom_bar.size_grip_spacer.show()
        window.left_grip.show()
        window.right_grip.show()
        window.top_grip.show()
        window.bottom_grip.show()

    @staticmethod
    def get_status() -> bool:
        """Return the current maximize/restore status."""
        return get_runtime_state_service().get_global_state()

    @staticmethod
    def set_status(status: bool) -> None:
        """Persist the current maximize/restore status."""
        get_runtime_state_service().set_global_state(status)
