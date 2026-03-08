# ///////////////////////////////////////////////////////////////
# DOMAIN.ERRORS - Error objects aggregator
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Domain-level typed exceptions exposed for services and adapters."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
from .base import DomainError, EzQtError
from .bootstrap import BootstrapError, InitAlreadyInitializedError, InitStepError
from .resources import (
    InvalidOverwritePolicyError,
    MissingPackageResourceError,
    ResourceCompilationError,
    ResourceError,
)

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
__all__ = [
    "EzQtError",
    "DomainError",
    "BootstrapError",
    "InitAlreadyInitializedError",
    "InitStepError",
    "ResourceError",
    "MissingPackageResourceError",
    "ResourceCompilationError",
    "InvalidOverwritePolicyError",
]
