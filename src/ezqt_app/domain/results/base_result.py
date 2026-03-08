# ///////////////////////////////////////////////////////////////
# DOMAIN.RESULTS.BASE_RESULT - Generic operation result model
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Generic typed result model for service orchestration."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
from dataclasses import dataclass
from typing import Generic, TypeVar

from .result_error import ResultError

T = TypeVar("T")


# ///////////////////////////////////////////////////////////////
# DATACLASSES
# ///////////////////////////////////////////////////////////////
@dataclass(slots=True)
class BaseResult(Generic[T]):
    """Typed generic operation result."""

    success: bool
    value: T | None = None
    error: ResultError | None = None

    @classmethod
    def ok(cls, value: T | None = None) -> BaseResult[T]:
        """Build a successful result."""
        return cls(success=True, value=value, error=None)

    @classmethod
    def fail(cls, code: str, message: str) -> BaseResult[T]:
        """Build a failed result."""
        return cls(
            success=False, value=None, error=ResultError(code=code, message=message)
        )
