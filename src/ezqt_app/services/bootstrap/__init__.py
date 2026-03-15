# ///////////////////////////////////////////////////////////////
# SERVICES.BOOTSTRAP - One-shot application boot sequence
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Bootstrap services — system configuration and initialization sequence."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from pathlib import Path
from typing import Any

# Local imports
from .._registry import ServiceRegistry
from .contracts import InitOptions, InitStep, OverwritePolicy, StepStatus
from .exceptions import BootstrapError, InitAlreadyInitializedError, InitStepError
from .init_service import InitService
from .initializer import Initializer
from .sequence import InitializationSequence
from .startup_config import StartupConfig


# ///////////////////////////////////////////////////////////////
# PUBLIC HELPERS
# ///////////////////////////////////////////////////////////////
def init(
    mk_theme: bool = True,
    verbose: bool = True,
    project_root: str | None = None,
    bin_path: str | None = None,
    overwrite_policy: OverwritePolicy = OverwritePolicy.ASK,
    mk_config: bool = True,
    mk_translations: bool = True,
    build_resources: bool = True,
    generate_main: bool = False,
) -> dict[str, Any]:
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
    options = InitOptions(
        project_root=None if project_root is None else Path(project_root),
        bin_path=None if bin_path is None else Path(bin_path),
        mk_theme=mk_theme,
        mk_config=mk_config,
        mk_translations=mk_translations,
        build_resources=build_resources,
        generate_main=generate_main,
        verbose=verbose,
        overwrite_policy=overwrite_policy,
    )
    return ServiceRegistry.get(InitService, InitService).run(options).to_dict()


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
    "InitOptions",
    "OverwritePolicy",
    "InitService",
    "StartupConfig",
    "InitializationSequence",
    "InitStep",
    "StepStatus",
    "BootstrapError",
    "InitAlreadyInitializedError",
    "InitStepError",
    "init",
    "setup_project",
    "generate_assets",
    "configure_startup",
]
