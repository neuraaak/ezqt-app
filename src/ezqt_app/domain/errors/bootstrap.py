# ///////////////////////////////////////////////////////////////
# DOMAIN.ERRORS.BOOTSTRAP - Bootstrap exceptions
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Typed bootstrap exceptions used by init orchestration."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from .base import EzQtError


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class BootstrapError(EzQtError):
    """Base initialization workflow error."""


class InitAlreadyInitializedError(BootstrapError):
    """Raised when init is re-triggered on an initialized context."""


class InitStepError(BootstrapError):
    """Raised when a required initialization step fails."""
