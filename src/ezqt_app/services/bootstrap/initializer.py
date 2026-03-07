# ///////////////////////////////////////////////////////////////
# SERVICES.BOOTSTRAP.INITIALIZER - Main application initializer
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""High-level initializer that coordinates the complete EzQt_App boot sequence."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from pathlib import Path
from typing import Any

# Local imports
from ..application.app_service import AppService
from ..application.file_service import FileService
from .init_options import InitOptions, OverwritePolicy
from .init_service import InitService
from .sequence import InitializationSequence
from .startup_config import StartupConfig


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class Initializer:
    """Coordinates the complete EzQt_App initialization process.

    Orchestrates:
    - Startup configuration (encoding, locale, env)
    - Asset and file generation via :class:`FileService`
    - Application requirements via :class:`AppService`
    - Idempotent guard (subsequent :meth:`initialize` calls are no-ops)
    """

    def __init__(self) -> None:
        self._startup_config = StartupConfig()
        self._file_service = FileService()
        self._sequence = InitializationSequence()
        self._init_service = InitService()
        self._initialized = False

    # ------------------------------------------------------------------
    # Main entry points
    # ------------------------------------------------------------------

    def initialize(
        self,
        _mk_theme: bool = True,
        verbose: bool = True,
        options: InitOptions | None = None,
    ) -> dict[str, Any]:
        """Run the complete boot sequence (idempotent).

        Parameters
        ----------
        mk_theme:
            Generate theme files (default: ``True``).
        verbose:
            Print progress information (default: ``True``).

        Returns
        -------
        dict
            Initialization summary (see :meth:`InitializationSequence.execute`).
        """
        resolved = options or InitOptions(
            mk_theme=_mk_theme,
            verbose=verbose,
            overwrite_policy=OverwritePolicy.ASK,
        )
        return self._init_service.run(resolved)

    def setup_project(self, base_path: str | None = None) -> bool:
        """Configure startup then scaffold a new project directory.

        Parameters
        ----------
        base_path:
            Root directory for the new project.  Defaults to ``cwd``.
        """
        self._startup_config.configure()
        return FileService(Path(base_path) if base_path else None).setup_project()

    # ------------------------------------------------------------------
    # Granular helpers
    # ------------------------------------------------------------------

    def configure_startup(self) -> None:
        """Run system-level startup configuration only."""
        self._startup_config.configure()

    def generate_assets(self) -> bool:
        """Generate all required asset files."""
        return self._file_service.generate_all_assets()

    def check_requirements(self) -> bool:
        """Return ``True`` if asset requirements are satisfied."""
        try:
            AppService.check_assets_requirements()
            return True
        except Exception:
            return False

    def make_required_files(self, mk_theme: bool = True) -> None:
        """Generate required config/resource files."""
        AppService.make_required_files(mk_theme)

    # ------------------------------------------------------------------
    # State
    # ------------------------------------------------------------------

    def is_initialized(self) -> bool:
        return self._initialized

    def reset(self) -> None:
        self._initialized = False
        self._init_service.reset()
        self._startup_config.reset()
        self._sequence.reset()

    # ------------------------------------------------------------------
    # Accessors (kept for compat)
    # ------------------------------------------------------------------

    def get_startup_config(self) -> StartupConfig:
        return self._startup_config

    def get_file_service(self) -> FileService:
        return self._file_service

    def get_sequence(self) -> InitializationSequence:
        return self._sequence
