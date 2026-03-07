# ///////////////////////////////////////////////////////////////
# SERVICES.BOOTSTRAP - One-shot application boot sequence
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Bootstrap services — system configuration and initialization sequence."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
from typing import Any

from .initializer import Initializer
from .sequence import InitializationSequence, InitStep, StepStatus
from .startup_config import StartupConfig


# ///////////////////////////////////////////////////////////////
# PUBLIC HELPERS
# ///////////////////////////////////////////////////////////////
def init(mk_theme: bool = True, verbose: bool = True) -> dict[str, Any]:
    """Initialize the EzQt_App application (boot sequence).

    Parameters
    ----------
    mk_theme:
        Generate theme file (default: ``True``).
    verbose:
        Show progress output (default: ``True``).

    Returns
    -------
    dict
        Boot sequence summary.
    """
    return Initializer().initialize(mk_theme, verbose)


def setup_project(base_path: str | None = None) -> bool:
    """Scaffold a new EzQt_App project directory.

    Parameters
    ----------
    base_path:
        Target directory (defaults to current working directory).
    """
    from pathlib import Path

    from ..application.file_service import FileService

    return FileService(Path(base_path) if base_path else None).setup_project()


def generate_assets() -> bool:
    """Generate all required asset files."""
    from ..application.file_service import FileService

    return FileService().generate_all_assets()


def configure_startup() -> None:
    """Run system-level startup configuration (encoding, locale, env)."""
    StartupConfig().configure()


# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////
__all__ = [
    "Initializer",
    "StartupConfig",
    "InitializationSequence",
    "InitStep",
    "StepStatus",
    "init",
    "setup_project",
    "generate_assets",
    "configure_startup",
]
