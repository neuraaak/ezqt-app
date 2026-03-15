# ///////////////////////////////////////////////////////////////
# MAIN - Application initialization entry point
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Main module — initialization and bootstrap helpers for EzQt_App."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from pathlib import Path
from typing import TYPE_CHECKING

# Local imports
from .services.bootstrap import init as init_app
from .utils.printer import get_printer

if TYPE_CHECKING:
    from ezqt_app.services.application import FileService
    from ezqt_app.services.bootstrap import Initializer, StartupConfig
    from ezqt_app.services.bootstrap.contracts import OverwritePolicy

# ///////////////////////////////////////////////////////////////
# FUNCTIONS
# ///////////////////////////////////////////////////////////////


def init(
    mk_theme: bool = True,
    project_root: str | Path | None = None,
    bin_path: str | Path | None = None,
    overwrite_policy: OverwritePolicy | None = None,
    verbose: bool = True,
) -> dict[str, object]:
    """Initialize the EzQt_App application using the new modular system.

    This function uses the new initialization package to:
    - Configure UTF-8 encoding at system level
    - Load required resources and generate necessary files
    - Setup the complete application environment

    Args:
        mk_theme: Generate theme file. Defaults to True.
        project_root: Project root directory. Defaults to None.
        bin_path: Binary path. Defaults to None.
        overwrite_policy: Policy for overwriting existing files. Defaults to None.
        verbose: Enable verbose output mode. Defaults to True.

    Returns:
        dict[str, object]: Initialization result dictionary.
    """
    from ezqt_app.services.bootstrap.contracts import OverwritePolicy

    resolved_policy = overwrite_policy or OverwritePolicy.ASK
    resolved_project_root = str(project_root) if project_root is not None else None
    resolved_bin_path = str(bin_path) if bin_path is not None else None

    return init_app(
        mk_theme=mk_theme,
        verbose=verbose,
        project_root=resolved_project_root,
        bin_path=resolved_bin_path,
        overwrite_policy=resolved_policy,
    )


def setup_project(base_path: str | None = None) -> bool:
    """Setup a new EzQt_App project using the new modular system.

    Args:
        base_path: Base path for the project. Defaults to current directory.

    Returns:
        bool: True if setup was successful.
    """
    from ezqt_app.services.bootstrap import setup_project as setup_project_app

    return setup_project_app(base_path)


def generate_assets() -> bool:
    """Generate all required assets using the new modular system.

    Returns:
        bool: True if generation was successful.
    """
    from ezqt_app.services.bootstrap import generate_assets as generate_assets_app

    return generate_assets_app()


def configure_startup() -> None:
    """Configure startup settings using the new modular system."""
    from ezqt_app.services.bootstrap import configure_startup as configure_startup_app

    configure_startup_app()


# ///////////////////////////////////////////////////////////////
# UTILITY FUNCTIONS
# ///////////////////////////////////////////////////////////////


def get_initializer() -> Initializer:
    """Get the main initializer instance.

    Returns:
        Initializer: The main initializer instance.
    """
    from ezqt_app.services.bootstrap import Initializer

    return Initializer()


def get_file_service(verbose: bool = False) -> FileService:
    """Get the file service instance.

    Args:
        verbose: Enable verbose output mode. Defaults to False.

    Returns:
        FileService: The file service instance.
    """
    from ezqt_app.services.application import FileService

    return FileService(verbose=verbose)


def get_startup_config() -> StartupConfig:
    """Get the startup configuration instance.

    Returns:
        StartupConfig: The startup configuration instance.
    """
    from ezqt_app.services.bootstrap import StartupConfig

    return StartupConfig()


# ///////////////////////////////////////////////////////////////
# MAIN ENTRY POINT
# ///////////////////////////////////////////////////////////////

if __name__ == "__main__":
    # Example usage of the new initialization system
    printer = get_printer()
    printer.section("EzQt_App - New Initialization System")

    # Initialize the application
    init(mk_theme=True)

    printer.success("Application initialized successfully!")
    printer.info("Ready to create your EzQt_App application!")
