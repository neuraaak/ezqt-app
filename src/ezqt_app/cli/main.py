# ///////////////////////////////////////////////////////////////
# CLI.MAIN - CLI Main Entry Point
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""
EzQt_App CLI - Main entry point.

Command-line interface for managing EzQt_App projects
and framework utilities.
"""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import sys
from pathlib import Path

# Third-party imports
import click
from rich.panel import Panel
from rich.text import Text

# Local imports
from ezqt_app.services.bootstrap import OverwritePolicy
from ezqt_app.services.bootstrap import init as bootstrap_init
from ezqt_app.utils.diagnostics import warn_tech

from .._version import __version__
from ._console import console
from .commands import (
    ProjectRunner,
    convert_qm,
    docs_command,
    info_command,
    version_command,
)

# ///////////////////////////////////////////////////////////////
# CLI GROUP
# ///////////////////////////////////////////////////////////////


@click.group(
    name="ezqt-app",
    invoke_without_command=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.version_option(
    __version__,
    "-v",
    "--version",
    prog_name="EzQt_App CLI",
    message="%(prog)s version %(version)s",
)
@click.pass_context
def cli(ctx: click.Context) -> None:
    """EzQt_App CLI - Framework utilities and project management.

    A command-line interface for managing EzQt_App projects
    and framework utilities.
    """
    if ctx.invoked_subcommand is None:
        _display_welcome()
        click.echo(ctx.get_help())


def _display_welcome() -> None:
    """Display a welcome message."""
    try:
        welcome_text = Text()
        welcome_text.append("EzQt_App CLI", style="bold bright_blue")
        welcome_text.append(" - Qt Application Framework", style="dim white")

        panel = Panel(
            welcome_text,
            title="[bold bright_blue]Welcome[/bold bright_blue]",
            border_style="bright_blue",
            padding=(1, 2),
        )
        console.print(panel)
    except (OSError, RuntimeError, ValueError):
        click.echo("EzQt_App CLI - Qt Application Framework")


# ///////////////////////////////////////////////////////////////
# COMMAND GROUPS
# ///////////////////////////////////////////////////////////////

# Register commands and groups
cli.add_command(docs_command)
cli.add_command(info_command)
cli.add_command(version_command)


# ///////////////////////////////////////////////////////////////
# COMMANDS
# ///////////////////////////////////////////////////////////////


@cli.command()
@click.option("--force", "-f", is_flag=True, help="Force overwrite of existing files")
@click.option(
    "--verbose", "-v", is_flag=True, help="Verbose output with detailed information"
)
@click.option("--no-main", is_flag=True, help="Skip main.py generation")
def init(force: bool, verbose: bool, no_main: bool) -> None:
    """Initialize a new EzQt_App project.

    Create a new EzQt_App project with all required assets and files.
    """
    if verbose:
        click.echo("Verbose mode enabled")
        click.echo(f"Current directory: {Path.cwd()}")

    try:
        click.echo("Initializing EzQt_App project...")
        policy = OverwritePolicy.FORCE if force else OverwritePolicy.ASK

        if verbose:
            click.echo("Running unified initialization workflow...")

        summary = bootstrap_init(
            mk_theme=True,
            verbose=verbose,
            project_root=str(Path.cwd()),
            bin_path=str(Path.cwd() / "bin"),
            overwrite_policy=policy,
            mk_config=True,
            mk_translations=True,
            build_resources=True,
            generate_main=not no_main,
        )

        if not summary.get("success", False):
            click.echo(click.style("Initialization failed", fg="red"))
            sys.exit(1)

        click.echo("Project initialization completed!")

        if verbose:
            click.echo("\nGenerated files:")
            click.echo("  - bin/config/app.config.yaml")
            click.echo("  - bin/themes/*.qss")
            click.echo("  - bin/translations/*.ts")
            click.echo("  - bin/resources.qrc")
            click.echo("  - bin/resources_rc.py (if pyside6-rcc available)")
            if not no_main:
                click.echo("  - main.py (example)")

    except Exception as e:
        warn_tech(
            "cli.init.failed",
            "Project initialization command failed",
            error=e,
        )
        click.echo(click.style(f"Error during initialization: {e}", fg="red"))
        if verbose:
            import traceback

            click.echo(traceback.format_exc())
        sys.exit(1)


@cli.command()
def convert() -> None:
    """Convert translation files.

    Convert .ts files to .qm format for Qt applications.
    """
    try:
        convert_qm()
    except Exception as e:
        warn_tech(
            "cli.convert.failed",
            "Translation conversion command failed",
            error=e,
        )
        click.echo(click.style(f"Error during conversion: {e}", fg="red"))
        sys.exit(1)


@cli.command()
@click.option("--template", "-t", help="Template type (basic, advanced)")
@click.option("--name", "-n", help="Project name")
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
def create(template: str | None, name: str | None, verbose: bool) -> None:
    """Create project template.

    Create a new project with predefined templates.
    """
    if verbose:
        click.echo("Verbose mode enabled")

    runner = ProjectRunner(verbose)

    try:
        success = runner.create_project_template(template, name)
        if success:
            click.echo("Project template created successfully!")
        else:
            click.echo(click.style("Failed to create project template", fg="red"))
            sys.exit(1)
    except Exception as e:
        warn_tech(
            "cli.create.failed",
            "Project template creation command failed",
            error=e,
        )
        click.echo(click.style(f"Error creating template: {e}", fg="red"))
        sys.exit(1)


# ///////////////////////////////////////////////////////////////
# MAIN ENTRY POINT
# ///////////////////////////////////////////////////////////////


def main() -> None:
    """Main entry point for the CLI."""
    try:
        cli()
    except click.ClickException as e:
        e.show()
        raise SystemExit(e.exit_code) from e
    except KeyboardInterrupt as e:
        console.print("\n[yellow]Interrupted by user[/yellow]")
        raise SystemExit(1) from e
    except (OSError, RuntimeError, ValueError) as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise SystemExit(1) from e


if __name__ == "__main__":
    main()
