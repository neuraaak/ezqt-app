# ///////////////////////////////////////////////////////////////
# SERVICES.BOOTSTRAP.CONTRACTS.STEPS - Initialization step contracts
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Contracts describing initialization sequence steps."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum


# ///////////////////////////////////////////////////////////////
# TYPES
# ///////////////////////////////////////////////////////////////
class StepStatus(Enum):
    """Execution status of a single initialization step."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass(slots=True)
class InitStep:
    """Descriptor for a single initialization step."""

    name: str
    description: str
    function: Callable[[], None]
    required: bool = True
    status: StepStatus = StepStatus.PENDING
    error_message: str | None = None
    duration: float | None = None
