# ///////////////////////////////////////////////////////////////
# DOMAIN.PORTS.RUNTIME_STATE_SERVICE - Runtime state port
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Protocol definitions for runtime state services."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from typing import Protocol


# ///////////////////////////////////////////////////////////////
# PROTOCOLS
# ///////////////////////////////////////////////////////////////
class RuntimeStateServiceProtocol(Protocol):
    """Technical contract for runtime state management."""

    def set_debug_mode(self, enabled: bool = True) -> None:
        """Enable or disable debug mode."""

    def set_verbose_mode(self, enabled: bool = True) -> None:
        """Enable or disable verbose mode."""

    def is_debug_mode(self) -> bool:
        """Return debug mode status."""

    def is_verbose_mode(self) -> bool:
        """Return verbose mode status."""

    def mark_app_initialized(self) -> None:
        """Mark application as initialized."""

    def mark_app_running(self) -> None:
        """Mark application as running."""

    def is_app_initialized(self) -> bool:
        """Return app initialized status."""

    def is_app_running(self) -> bool:
        """Return app running status."""

    def get_global_state(self) -> bool:
        """Return legacy window global state."""

    def set_global_state(self, state: bool) -> None:
        """Set legacy window global state."""

    def get_global_title_bar(self) -> bool:
        """Return legacy title bar status."""

    def set_global_title_bar(self, enabled: bool) -> None:
        """Set legacy title bar status."""
