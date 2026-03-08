# ///////////////////////////////////////////////////////////////
# DOMAIN.ERRORS.BASE - Base domain exceptions
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Base exception hierarchy for ezqt_app."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from dataclasses import dataclass

# Local imports
from ...shared.types import JsonMap


# ///////////////////////////////////////////////////////////////
# DATACLASSES
# ///////////////////////////////////////////////////////////////
@dataclass(slots=True)
class EzQtError(Exception):
    """Base typed exception for all application-specific errors."""

    code: str
    message: str
    context: JsonMap | None = None

    def __str__(self) -> str:
        return self.message


class DomainError(EzQtError):
    """Base domain-layer error."""
