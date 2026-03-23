# ///////////////////////////////////////////////////////////////
# CLI.MAIN - Command-line interface entry point
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""EzQt_App CLI — main entry point and command definitions."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import sys
from pathlib import Path

# Third-party imports
import click

# Local imports
from ezqt_app.services.bootstrap import OverwritePolicy
from ezqt_app.services.bootstrap import init as bootstrap_init
from ezqt_app.utils.diagnostics import warn_tech

from ..version import __version__
from .runner import ProjectRunner


# ///////////////////////////////////////////////////////////////
# CLI GROUP
# ///////////////////////////////////////////////////////////////
@click.group()
@click.version_option(version=__version__, prog_name="EzQt_App CLI")
def cli():
    """EzQt_App CLI - Framework utilities and project management.

    A command-line interface for managing EzQt_App projects
    and framework utilities.
    """


# ///////////////////////////////////////////////////////////////
# COMMANDS
# ///////////////////////////////////////////////////////////////
@cli.command()
@click.option("--force", "-f", is_flag=True, help="Force overwrite of existing files")
@click.option(
    "--verbose", "-v", is_flag=True, help="Verbose output with detailed information"
)
@click.option("--no-main", is_flag=True, help="Skip main.py generation")
def init(force, verbose, no_main):
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
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
def convert(verbose: bool) -> None:  # noqa: ARG001
    """Convert translation files.

    Convert .ts files to .qm format for Qt applications.
    """
    try:
        from ezqt_app.cli.create_qm_files import main as convert_main

        convert_main()
    except ImportError:
        warn_tech(
            "cli.convert.module_missing",
            "Translation conversion module import failed",
        )
        click.echo(click.style("Translation conversion module not found", fg="red"))
        sys.exit(1)
    except Exception as e:
        warn_tech(
            "cli.convert.failed",
            "Translation conversion command failed",
            error=e,
        )
        click.echo(click.style(f"Error during conversion: {e}", fg="red"))
        sys.exit(1)


@cli.command()
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
def mkqm(verbose):
    """Convert translation files (alias for convert).

    Convert .ts files to .qm format for Qt applications.
    """
    if verbose:
        click.echo("Verbose mode enabled")

    try:
        from ezqt_app.cli.create_qm_files import main as convert_main

        convert_main()
    except ImportError:
        warn_tech(
            "cli.mkqm.module_missing",
            "Translation conversion module import failed",
        )
        click.echo(click.style("Translation conversion module not found", fg="red"))
        sys.exit(1)
    except Exception as e:
        warn_tech(
            "cli.mkqm.failed",
            "Translation conversion alias command failed",
            error=e,
        )
        click.echo(click.style(f"Error during conversion: {e}", fg="red"))
        sys.exit(1)


@cli.command()
@click.option("--unit", "-u", is_flag=True, help="Run unit tests")
@click.option("--integration", "-i", is_flag=True, help="Run integration tests")
@click.option("--coverage", "-c", is_flag=True, help="Run tests with coverage")
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
def test(unit, integration, coverage, verbose):
    """Run tests.

    Execute the test suite for EzQt_App framework.
    """
    import subprocess

    if not any([unit, integration, coverage]):
        unit = True

    try:
        if unit:
            click.echo("Running unit tests...")
            cmd = ["python", "tests/run_tests.py", "--type", "unit"]
            if verbose:
                cmd.append("--verbose")
            subprocess.run(cmd, check=True)

        if integration:
            click.echo("Running integration tests...")
            cmd = ["python", "tests/run_tests.py", "--type", "integration"]
            if verbose:
                cmd.append("--verbose")
            subprocess.run(cmd, check=True)

        if coverage:
            click.echo("Running tests with coverage...")
            cmd = ["python", "tests/run_tests.py", "--coverage"]
            if verbose:
                cmd.append("--verbose")
            subprocess.run(cmd, check=True)
            click.echo("Coverage report generated in htmlcov/")

        click.echo("Tests completed successfully!")

    except subprocess.CalledProcessError as e:
        click.echo(click.style(f"Tests failed: {e}", fg="red"))
        sys.exit(1)
    except FileNotFoundError:
        click.echo(
            click.style(
                "Test runner not found. Make sure you're in the project root.",
                fg="red",
            )
        )
        sys.exit(1)


@cli.command()
@click.option("--serve", "-s", is_flag=True, help="Serve documentation locally")
@click.option("--port", "-p", default=8000, help="Port for documentation server")
def docs(serve, port):
    """Documentation utilities.

    Access and manage EzQt_App documentation.
    """
    if serve:
        try:
            import http.server
            import os
            import socketserver

            docs_dir = os.path.join(os.path.dirname(__file__), "..", "..", "docs")
            if os.path.exists(docs_dir):
                os.chdir(docs_dir)
                click.echo(f"Serving documentation at http://localhost:{port}")
                click.echo("Press Ctrl+C to stop the server")

                with socketserver.TCPServer(
                    ("", port), http.server.SimpleHTTPRequestHandler
                ) as httpd:
                    httpd.serve_forever()
            else:
                click.echo(click.style("Documentation directory not found", fg="red"))

        except KeyboardInterrupt:
            click.echo("\nDocumentation server stopped")
        except Exception as e:
            warn_tech(
                "cli.docs.serve_failed",
                "Documentation local server failed",
                error=e,
            )
            click.echo(click.style(f"Error serving documentation: {e}", fg="red"))
    else:
        click.echo("Documentation options:")
        click.echo("  --serve, -s     Serve documentation locally")
        click.echo("  --port, -p      Specify port (default: 8000)")
        click.echo("\nExample: ezqt docs --serve --port 8080")


@cli.command()
def info():
    """Show package information.

    Display information about EzQt_App installation.
    """
    try:
        import ezqt_app

        click.echo("EzQt_App Information")
        click.echo("=" * 40)
        click.echo(f"Version: {getattr(ezqt_app, '__version__', '5.0.0')}")
        click.echo(f"Location: {ezqt_app.__file__}")

        try:
            import PySide6

            click.echo(f"PySide6: {PySide6.__version__}")
        except ImportError:
            click.echo("PySide6: Not installed")

        try:
            import yaml

            click.echo(f"PyYaml: {yaml.__version__}")
        except ImportError:
            click.echo("PyYaml: Not installed")

        try:
            import ezpl  # noqa: F401

            click.echo(f"ezplog: {ezpl.__version__}")
        except ImportError:
            click.echo("ezplog: Not installed")

        runner = ProjectRunner()
        try:
            project_info = runner.get_project_info()
            click.echo(f"Project structure: {project_info['status']}")
        except FileNotFoundError:
            click.echo("Project structure: Not initialized")

        click.echo("=" * 40)

    except ImportError:
        click.echo(click.style("EzQt_App not found in current environment", fg="red"))


@cli.command()
@click.option("--template", "-t", help="Template type (basic, advanced)")
@click.option("--name", "-n", help="Project name")
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
def create(template, name, verbose):
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
# PUBLIC API
# ///////////////////////////////////////////////////////////////
__all__ = ["cli"]

if __name__ == "__main__":
    cli()
