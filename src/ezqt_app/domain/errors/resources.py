# ///////////////////////////////////////////////////////////////
# DOMAIN.ERRORS.RESOURCES - Resource and file generation exceptions
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Typed exceptions for file/resource generation failures."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from .base import EzQtError


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class ResourceError(EzQtError):
    """Base resource generation error."""


class MissingPackageResourceError(ResourceError):
    """Raised when an expected package resource cannot be resolved."""


class ResourceCompilationError(ResourceError):
    """Raised when QRC to Python resource compilation fails."""


class InvalidOverwritePolicyError(ResourceError):
    """Raised when overwrite policy is not recognized."""
