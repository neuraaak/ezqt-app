# ///////////////////////////////////////////////////////////////
# EZQT_APP - CLI Info Command
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""
CLI command for displaying package information.

This module provides the info command for EzQt_App.
"""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

# Third-party imports
import click
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

# Local imports
import ezqt_app

from .._console import console
from ._runner import ProjectRunner

# ///////////////////////////////////////////////////////////////
# COMMANDS
# ///////////////////////////////////////////////////////////////


@click.command(name="info", help="Display package information")
def info_command() -> None:
    """Display package information.

    Show detailed information about the EzQt_App package including
    version, location, dependencies, and current project structure.
    """
    try:
        # Package metadata
        pkg_version = getattr(ezqt_app, "__version__", "unknown")
        author = getattr(ezqt_app, "__author__", "unknown")
        maintainer = getattr(ezqt_app, "__maintainer__", "unknown")
        description = getattr(ezqt_app, "__description__", "unknown")
        url = getattr(ezqt_app, "__url__", "unknown")

        try:
            package_path = (
                Path(ezqt_app.__file__).parent
                if hasattr(ezqt_app, "__file__")
                else None
            )
        except (AttributeError, TypeError, OSError):
            package_path = None

        try:
            runner = ProjectRunner()
            project_info = runner.get_project_info()
            project_status: str | None = project_info.get("status", "unknown")
        except Exception:
            project_status = None

        # Build info text
        text = Text()
        text.append("Package Information\n", style="bold bright_blue")
        text.append("=" * 50 + "\n\n", style="dim")

        # Version
        text.append("Version: ", style="bold")
        text.append(f"{pkg_version}\n", style="white")

        # Author
        text.append("Author: ", style="bold")
        text.append(f"{author}\n", style="white")

        if maintainer != author:
            text.append("Maintainer: ", style="bold")
            text.append(f"{maintainer}\n", style="white")

        # Description
        text.append("\nDescription:\n", style="bold")
        text.append(f"  {description}\n", style="dim white")

        # URL
        text.append("\nURL: ", style="bold")
        text.append(f"{url}\n", style="cyan")

        # Package location
        if package_path:
            text.append("\nPackage Location: ", style="bold")
            text.append(f"{package_path}\n", style="dim white")

        if project_status is not None:
            text.append("\nProject Structure: ", style="bold")
            text.append(f"{project_status}\n", style="white")

        # Display panel
        panel = Panel(
            text,
            title="[bold bright_blue]EzQt_App Information[/bold bright_blue]",
            border_style="bright_blue",
            padding=(1, 2),
        )
        console.print(panel)

        # Dependencies table
        try:
            import PySide6
            import rich

            def _get_version(pkg: str) -> str:
                try:
                    return version(pkg)
                except PackageNotFoundError:
                    return "unknown"

            deps_table = Table(
                title="Dependencies", show_header=True, header_style="bold blue"
            )
            deps_table.add_column("Package", style="cyan")
            deps_table.add_column("Version", style="green")

            deps_table.add_row("PySide6", getattr(PySide6, "__version__", "unknown"))
            deps_table.add_row("rich", getattr(rich, "__version__", "unknown"))
            deps_table.add_row("click", _get_version("click"))
            deps_table.add_row("PyYAML", _get_version("PyYAML"))

            console.print("\n")
            console.print(deps_table)
        except (ImportError, OSError, RuntimeError, ValueError) as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

    except click.ClickException:
        raise
    except (OSError, RuntimeError, ValueError, TypeError, AttributeError) as e:
        raise click.ClickException(str(e)) from e
