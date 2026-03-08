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

# Third-party imports
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QSizePolicy


# ///////////////////////////////////////////////////////////////
# PROTOCOLS
# ///////////////////////////////////////////////////////////////
class UiComponentFactoryProtocol(Protocol):
    """Technical contract for reusable UI component factories."""

    def initialize(self) -> None:
        """Initialize all predefined UI components."""

    def get_font(self, name: str) -> QFont | None:
        """Return a predefined font by name."""

    def get_size_policy(self, name: str) -> QSizePolicy | None:
        """Return a predefined size policy by name."""
