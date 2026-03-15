# ///////////////////////////////////////////////////////////////
# SERVICES.RUNTIME.SERVICE - Runtime state service
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Runtime state service implementation."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Local imports
from ...domain.models.runtime import RuntimeStateModel
from ...domain.ports.runtime_state_service import RuntimeStateServiceProtocol
from .._registry import ServiceRegistry


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class RuntimeStateService(RuntimeStateServiceProtocol):
    """Service managing runtime flags and legacy global UI state."""

    def __init__(self) -> None:
        """Initialize runtime state."""
        self._state = RuntimeStateModel()

    def set_debug_mode(self, enabled: bool = True) -> None:
        self._state.debug_mode = enabled

    def set_verbose_mode(self, enabled: bool = True) -> None:
        self._state.verbose_mode = enabled

    def is_debug_mode(self) -> bool:
        return self._state.debug_mode

    def is_verbose_mode(self) -> bool:
        return self._state.verbose_mode

    def mark_app_initialized(self) -> None:
        self._state.app_initialized = True

    def mark_app_running(self) -> None:
        self._state.app_running = True

    def is_app_initialized(self) -> bool:
        return self._state.app_initialized

    def is_app_running(self) -> bool:
        return self._state.app_running

    def get_global_state(self) -> bool:
        return self._state.global_state

    def set_global_state(self, state: bool) -> None:
        self._state.global_state = state

    def get_global_title_bar(self) -> bool:
        return self._state.global_title_bar

    def set_global_title_bar(self, enabled: bool) -> None:
        self._state.global_title_bar = enabled


# ///////////////////////////////////////////////////////////////
# FUNCTIONS
# ///////////////////////////////////////////////////////////////
def get_runtime_state_service() -> RuntimeStateService:
    """Return the singleton runtime state service."""
    return ServiceRegistry.get(RuntimeStateService, RuntimeStateService)
