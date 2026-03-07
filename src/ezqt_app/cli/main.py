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
import importlib.resources
import sys
from pathlib import Path

# Third-party imports
import click
from colorama import Fore, Style

# Local imports
from ezqt_app.services.application import FileService as FileMaker

from .runner import ProjectRunner


# ///////////////////////////////////////////////////////////////
# CLI GROUP
# ///////////////////////////////////////////////////////////////
@click.group()
@click.version_option(version="5.0.0", prog_name="EzQt_App CLI")
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

        maker = FileMaker(base_path=Path.cwd(), verbose=verbose)

        if verbose:
            click.echo("Generating assets...")

        maker.make_assets_binaries()
        maker.make_qrc()
        maker.make_rc_py()
        maker.make_app_resources_module()

        if not no_main:
            template_path = Path(
                str(
                    importlib.resources.files("ezqt_app")
                    .joinpath("resources")
                    .joinpath("templates")
                    .joinpath("main.py.template")
                )
            )

            if template_path.exists():
                main_py = Path.cwd() / "main.py"

                if main_py.exists() and not force:
                    if click.confirm("main.py already exists. Overwrite?"):
                        maker.make_main_from_template(template_path)
                        click.echo("main.py overwritten")
                    else:
                        click.echo(f"{Fore.YELLOW}main.py preserved{Style.RESET_ALL}")
                else:
                    maker.make_main_from_template(template_path)
                    click.echo("main.py generated")
            else:
                click.echo(
                    f"{Fore.RED}Template main.py.template not found{Style.RESET_ALL}"
                )

        click.echo("Project initialization completed!")

        if verbose:
            click.echo("\nGenerated files:")
            click.echo("  - assets/ (icons, images, themes)")
            click.echo("  - base_resources.qrc")
            click.echo("  - base_resources_rc.py")
            click.echo("  - shared resources via ezqt_app.shared.resources")
            if not no_main:
                click.echo("  - main.py (example)")

    except Exception as e:
        click.echo(f"{Fore.RED}Error during initialization: {e}{Style.RESET_ALL}")
        if verbose:
            import traceback

            click.echo(traceback.format_exc())
        sys.exit(1)


@cli.command()
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
def convert(verbose):  # noqa: ARG001
    """Convert translation files.

    Convert .ts files to .qm format for Qt applications.
    """
    try:
        from ezqt_app.cli.create_qm_files import main as convert_main

        convert_main()
    except ImportError:
        click.echo(
            f"{Fore.RED}Translation conversion module not found{Style.RESET_ALL}"
        )
        sys.exit(1)
    except Exception as e:
        click.echo(f"{Fore.RED}Error during conversion: {e}{Style.RESET_ALL}")
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
        click.echo(
            f"{Fore.RED}Translation conversion module not found{Style.RESET_ALL}"
        )
        sys.exit(1)
    except Exception as e:
        click.echo(f"{Fore.RED}Error during conversion: {e}{Style.RESET_ALL}")
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
        click.echo(f"{Fore.RED}Tests failed: {e}{Style.RESET_ALL}")
        sys.exit(1)
    except FileNotFoundError:
        click.echo(
            f"{Fore.RED}Test runner not found. Make sure you're in the project root.{Style.RESET_ALL}"
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
                click.echo(
                    f"{Fore.RED}Documentation directory not found{Style.RESET_ALL}"
                )

        except KeyboardInterrupt:
            click.echo("\nDocumentation server stopped")
        except Exception as e:
            click.echo(f"{Fore.RED}Error serving documentation: {e}{Style.RESET_ALL}")
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
            import yaml  # noqa: F401

            click.echo("PyYaml: Available")
        except ImportError:
            click.echo("PyYaml: Not installed")

        try:
            import colorama  # noqa: F401

            click.echo("Colorama: Available")
        except ImportError:
            click.echo("Colorama: Not installed")

        runner = ProjectRunner()
        try:
            project_info = runner.get_project_info()
            click.echo(f"Project structure: {project_info['status']}")
        except FileNotFoundError:
            click.echo("Project structure: Not initialized")

        click.echo("=" * 40)

    except ImportError:
        click.echo(
            f"{Fore.RED}EzQt_App not found in current environment{Style.RESET_ALL}"
        )


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
            click.echo(f"{Fore.RED}Failed to create project template{Style.RESET_ALL}")
            sys.exit(1)
    except Exception as e:
        click.echo(f"{Fore.RED}Error creating template: {e}{Style.RESET_ALL}")
        sys.exit(1)


# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////
__all__ = ["cli"]

if __name__ == "__main__":
    cli()
