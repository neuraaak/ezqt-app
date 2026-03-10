# ///////////////////////////////////////////////////////////////
# DOMAIN.PORTS.UI_COMPONENT_FACTORY - UI component factory port
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Protocol definitions for UI component factories."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from typing import Protocol

# Local imports
from ..models.ui import FontSpec, SizePolicySpec


# ///////////////////////////////////////////////////////////////
# PROTOCOLS
# ///////////////////////////////////////////////////////////////
class UiComponentFactoryProtocol(Protocol):
    """Technical contract for reusable UI component factories."""

    def initialize(self) -> None:
        """Initialize all predefined UI components."""

    def get_font(self, name: str) -> FontSpec | None:
        """Return a predefined font specification by name."""

    def get_size_policy(self, name: str) -> SizePolicySpec | None:
        """Return a predefined size policy specification by name."""
