# ///////////////////////////////////////////////////////////////
# EZQT_APP - CLI Version Command
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""
CLI command for displaying version information.

This module provides the version command for EzQt_App.
"""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Third-party imports
import click
from rich.panel import Panel
from rich.text import Text

# Local imports
import ezqt_app

from .._console import console

# ///////////////////////////////////////////////////////////////
# COMMANDS
# ///////////////////////////////////////////////////////////////


@click.command(name="version", help="Display version information")
@click.option(
    "--full",
    "-f",
    is_flag=True,
    help="Display full version information",
)
def version_command(full: bool) -> None:
    """Display version information.

    Show the current version of EzQt_App.
    Use --full for detailed version information.
    """
    version = getattr(ezqt_app, "__version__", "unknown")
    author = getattr(ezqt_app, "__author__", "unknown")

    if full:
        # Full version info
        text = Text()
        text.append("EzQt_App ", style="bold bright_blue")
        text.append(f"v{version}", style="bold green")
        text.append("\n\n", style="reset")

        text.append("Author: ", style="dim")
        text.append(f"{author}\n", style="white")

        url = getattr(ezqt_app, "__url__", None)
        if url:
            text.append("URL: ", style="dim")
            text.append(f"{url}\n", style="white")

        panel = Panel(
            text,
            title="[bold bright_blue]Version Information[/bold bright_blue]",
            border_style="bright_blue",
            padding=(1, 2),
        )
        console.print(panel)
    else:
        # Simple version
        console.print(
            f"[bold bright_blue]EzQt_App[/bold bright_blue] v[bold green]{version}[/bold green]"
        )
