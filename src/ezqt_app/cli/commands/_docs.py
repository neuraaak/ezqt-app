# ///////////////////////////////////////////////////////////////
# EZQT_APP - CLI Docs Command
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""CLI command for opening EzQt_App online documentation."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import webbrowser

# Third-party imports
import click

# ///////////////////////////////////////////////////////////////
# CONSTANTS
# ///////////////////////////////////////////////////////////////

DOCS_URL = "https://neuraaak.github.io/ezqt-app/"


# ///////////////////////////////////////////////////////////////
# COMMANDS
# ///////////////////////////////////////////////////////////////


@click.command(name="docs", help="Open the online documentation")
def docs_command() -> None:
    """Open the EzQt_App documentation website in the default browser."""
    try:
        opened = webbrowser.open(DOCS_URL, new=2)
    except (OSError, RuntimeError, webbrowser.Error) as e:
        raise click.ClickException(str(e)) from e

    if opened:
        click.echo(f"Opened documentation: {DOCS_URL}")
        return

    # Fallback for environments where a browser cannot be opened.
    click.echo(DOCS_URL)
