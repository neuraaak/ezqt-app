# ///////////////////////////////////////////////////////////////
# DOMAIN.RESULTS.INIT_RESULT - Initialization aggregate result model
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Typed aggregate result for initialization workflows."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from dataclasses import dataclass, field

# Local imports
from ...shared.types import JsonMap
from .init_step_result import InitStepResult
from .result_error import ResultError


# ///////////////////////////////////////////////////////////////
# DATACLASSES
# ///////////////////////////////////////////////////////////////
@dataclass(slots=True)
class InitResult:
    """Aggregate initialization result consumed by API/CLI façades."""

    success: bool
    message: str | None = None
    total_steps: int = 0
    successful: int = 0
    failed: int = 0
    skipped: int = 0
    total_time: float = 0.0
    steps: list[InitStepResult] = field(default_factory=list)
    error: ResultError | None = None

    def to_dict(self) -> JsonMap:
        """Convert to a dictionary for backward-compatible public API."""
        return {
            "success": self.success,
            "message": self.message,
            "total_steps": self.total_steps,
            "successful": self.successful,
            "failed": self.failed,
            "skipped": self.skipped,
            "total_time": self.total_time,
            "steps": [
                {
                    "name": step.name,
                    "description": step.description,
                    "required": step.required,
                    "status": step.status,
                    "error_message": step.error_message,
                    "duration": step.duration,
                }
                for step in self.steps
            ],
            "error": (
                {
                    "code": self.error.code,
                    "message": self.error.message,
                    "context": self.error.context,
                }
                if self.error is not None
                else None
            ),
        }
