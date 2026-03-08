# ///////////////////////////////////////////////////////////////
# SERVICES.BOOTSTRAP.INIT_SERVICE - Unified init orchestrator
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unified initialization service used by both Python API and CLI."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from pathlib import Path

# Local imports
from ...domain.errors import InitAlreadyInitializedError
from ...domain.results import InitResult
from ...domain.results.result_error import ResultError
from ..application.file_service import FileService
from .contracts.options import InitOptions
from .sequence import InitializationSequence


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class InitService:
    """Coordinates initialization with a single options object."""

    def __init__(self) -> None:
        self._initialized = False

    def run(self, options: InitOptions | None = None) -> InitResult:
        """Run initialization sequence with normalized options."""
        resolved = (options or InitOptions()).resolve()

        if self._initialized:
            err = InitAlreadyInitializedError(
                code="bootstrap.already_initialized",
                message="Initialization already completed",
                context={
                    "project_root": (
                        str(resolved.project_root) if resolved.project_root else None
                    ),
                    "bin_path": str(resolved.bin_path) if resolved.bin_path else None,
                },
            )
            return InitResult(
                success=True,
                message="Already initialized",
                error=ResultError(
                    code=err.code, message=err.message, context=err.context
                ),
            )

        try:
            sequence = InitializationSequence(resolved)
            summary = sequence.execute(verbose=resolved.verbose)
        except Exception as e:
            return InitResult(
                success=False,
                message="Initialization failed before sequence completion",
                error=ResultError(
                    code="bootstrap.unexpected_error",
                    message=str(e),
                    context={
                        "project_root": (
                            str(resolved.project_root)
                            if resolved.project_root
                            else None
                        ),
                        "bin_path": (
                            str(resolved.bin_path) if resolved.bin_path else None
                        ),
                    },
                ),
            )

        # CLI-only optional step: generate main.py from package template.
        if summary.success and resolved.generate_main and resolved.project_root:
            maker = FileService(
                base_path=Path(resolved.project_root),
                bin_path=resolved.bin_path,
                verbose=resolved.verbose,
                overwrite_policy=resolved.overwrite_policy.value,
            )
            maker.make_main_from_template()

        if summary.success:
            self._initialized = True

        return summary

    def reset(self) -> None:
        """Reset initialization state."""
        self._initialized = False
