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
from typing import TYPE_CHECKING

# Local imports
from .services.bootstrap import init as init_app
from .utils.printer import get_printer

if TYPE_CHECKING:
    from ezqt_app.services.application import FileService
    from ezqt_app.services.bootstrap import Initializer, StartupConfig

# ///////////////////////////////////////////////////////////////
# FUNCTIONS
# ///////////////////////////////////////////////////////////////


def init(mk_theme: bool = True) -> None:
    """
    Initialize the EzQt_App application using the new modular system.

    This function uses the new initialization package to:
    - Configure UTF-8 encoding at system level
    - Load required resources and generate necessary files
    - Setup the complete application environment

    Parameters
    ----------
    mk_theme : bool, optional
        Generate theme file (default: True).
    """
    init_app(mk_theme)


def setup_project(base_path: str | None = None) -> bool:
    """
    Setup a new EzQt_App project using the new modular system.

    Parameters
    ----------
    base_path : str, optional
        Base path for the project (default: current directory).

    Returns
    -------
    bool
        True if setup was successful.
    """
    from ezqt_app.services.bootstrap import setup_project as setup_project_app

    return setup_project_app(base_path)


def generate_assets() -> bool:
    """
    Generate all required assets using the new modular system.

    Returns
    -------
    bool
        True if generation was successful.
    """
    from ezqt_app.services.bootstrap import generate_assets as generate_assets_app

    return generate_assets_app()


def configure_startup() -> None:
    """
    Configure startup settings using the new modular system.
    """
    from ezqt_app.services.bootstrap import configure_startup as configure_startup_app

    configure_startup_app()


# ///////////////////////////////////////////////////////////////
# UTILITY FUNCTIONS
# ///////////////////////////////////////////////////////////////


def get_initializer() -> Initializer:
    """
    Get the main initializer instance.

    Returns
    -------
    Initializer
        The main initializer instance.
    """
    from ezqt_app.services.bootstrap import Initializer

    return Initializer()


def get_file_service(verbose: bool = False) -> FileService:
    """
    Get the file service instance.

    Parameters
    ----------
    verbose : bool, optional
        Enable verbose output mode, default False

    Returns
    -------
    FileService
        The file service instance.
    """
    from ezqt_app.services.application import FileService

    return FileService(verbose=verbose)


def get_startup_config() -> StartupConfig:
    """
    Get the startup configuration instance.

    Returns
    -------
    StartupConfig
        The startup configuration instance.
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
