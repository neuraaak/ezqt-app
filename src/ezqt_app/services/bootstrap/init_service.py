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
from typing import Any

# Local imports
from ..application.file_service import FileService
from .init_options import InitOptions
from .sequence import InitializationSequence


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class InitService:
    """Coordinates initialization with a single options object."""

    def __init__(self) -> None:
        self._initialized = False

    def run(self, options: InitOptions | None = None) -> dict[str, Any]:
        """Run initialization sequence with normalized options."""
        resolved = (options or InitOptions()).resolve()

        if self._initialized:
            return {"success": True, "message": "Already initialized"}

        sequence = InitializationSequence(resolved)
        summary = sequence.execute(verbose=resolved.verbose)

        # CLI-only optional step: generate main.py from package template.
        if summary.get("success") and resolved.generate_main and resolved.project_root:
            maker = FileService(
                base_path=Path(resolved.project_root),
                bin_path=resolved.bin_path,
                verbose=resolved.verbose,
                overwrite_policy=resolved.overwrite_policy.value,
            )
            maker.make_main_from_template()

        if summary.get("success"):
            self._initialized = True

        return summary

    def reset(self) -> None:
        """Reset initialization state."""
        self._initialized = False
