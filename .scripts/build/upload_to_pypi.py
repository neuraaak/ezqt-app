#!/usr/bin/env python3
# ///////////////////////////////////////////////////////////////
# UPLOAD_TO_PYPI - PyPI Package Uploader
# ///////////////////////////////////////////////////////////////

"""
Upload script for PyPI package.

This script uploads the built package to PyPI or Test PyPI.
It assumes the package has already been built using build_package.py.
"""

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import io
import subprocess
import sys
from pathlib import Path

# Third-party imports
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# ///////////////////////////////////////////////////////////////
# VARIABLES
# ///////////////////////////////////////////////////////////////

project_name = "ezqt_app"

# ///////////////////////////////////////////////////////////////
# GLOBAL CONSOLE
# ///////////////////////////////////////////////////////////////

# Configure console with UTF-8 encoding for Windows emoji support
# Force UTF-8 encoding on Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
console = Console(legacy_windows=False)

# ///////////////////////////////////////////////////////////////
# FUNCTIONS
# ///////////////////////////////////////////////////////////////


def run_command(command: list[str], description: str = "") -> bool:
    """Run a command and return success status.

    Args:
        command: Command to execute as list of strings
        description: Optional description for the command

    Returns:
        bool: True if command succeeded, False otherwise
    """
    if description:
        console.print(f"[cyan]🔄[/cyan] {description}...")

    try:
        result = subprocess.run(  # noqa: S603
            command, check=True, capture_output=True, text=True
        )
        if result.stdout:
            console.print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        console.print(f"[red]❌[/red] Error: {e}")
        if e.stderr:
            console.print(f"[red]Error output:[/red] {e.stderr}")
        return False


def check_dist_exists() -> bool:
    """Check if dist directory exists and contains files.

    Returns:
        bool: True if dist exists and has files, False otherwise
    """
    project_root = Path(__file__).resolve().parents[2]
    dist_path = project_root / "dist"

    if not dist_path.exists():
        console.print("[red]❌[/red] dist/ directory not found")
        console.print("[yellow]💡[/yellow] Please run build_package.py first")
        return False

    dist_files = list(dist_path.glob("*"))
    if not dist_files:
        console.print("[red]❌[/red] No distribution files found in dist/")
        console.print("[yellow]💡[/yellow] Please run build_package.py first")
        return False

    console.print(f"[green]✓[/green] Found {len(dist_files)} distribution file(s)")
    for file in dist_files:
        console.print(f"  [dim]•[/dim] {file.name}")

    return True


def upload_to_test_pypi() -> bool:
    """Upload to Test PyPI.

    Returns:
        bool: True if upload succeeded, False otherwise
    """
    console.print(
        Panel.fit(
            Text("🚀 Uploading to Test PyPI", style="bold cyan"),
            border_style="cyan",
        )
    )

    if not check_dist_exists():
        return False

    project_root = Path(__file__).resolve().parents[2]
    dist_path = project_root / "dist"
    dist_files = list(dist_path.glob("*"))

    commands = [
        [sys.executable, "-m", "twine", "upload", "--repository", "testpypi"]
        + [str(f) for f in dist_files],
    ]

    for command in commands:
        if not run_command(command, "Uploading to Test PyPI"):
            console.print(
                Panel.fit(
                    Text("❌ Upload to Test PyPI failed", style="bold red"),
                    border_style="red",
                )
            )
            return False

    console.print(
        Panel.fit(
            Text("✅ Upload to Test PyPI successful!", style="bold green"),
            border_style="green",
        )
    )
    console.print(
        "[cyan]📦[/cyan] Package available at: "
        f"[link]https://test.pypi.org/project/{project_name}/[/link]"
    )
    return True


def upload_to_pypi() -> bool:
    """Upload to PyPI.

    Returns:
        bool: True if upload succeeded, False otherwise
    """
    console.print(
        Panel.fit(
            Text("🚀 Uploading to PyPI", style="bold cyan"),
            border_style="cyan",
        )
    )

    if not check_dist_exists():
        return False

    # Confirm upload to production PyPI
    console.print(
        "[yellow]⚠️[/yellow]  [bold]You are about to upload to production PyPI![/bold]"
    )
    console.print("[yellow]💡[/yellow] Make sure you have:")
    console.print("  [dim]•[/dim] Tested the package thoroughly")
    console.print("  [dim]•[/dim] Updated the version number")
    console.print("  [dim]•[/dim] Updated the changelog")

    try:
        confirm = input("\n[?] Continue with upload? (yes/no): ").strip().lower()
        if confirm not in ["yes", "y"]:
            console.print("[yellow]⏸️[/yellow]  Upload cancelled by user")
            return False
    except (KeyboardInterrupt, EOFError):
        console.print("\n[yellow]⏸️[/yellow]  Upload cancelled by user")
        return False

    project_root = Path(__file__).resolve().parents[2]
    dist_path = project_root / "dist"
    dist_files = list(dist_path.glob("*"))

    commands = [
        [sys.executable, "-m", "twine", "upload"] + [str(f) for f in dist_files],
    ]

    for command in commands:
        if not run_command(command, "Uploading to PyPI"):
            console.print(
                Panel.fit(
                    Text("❌ Upload to PyPI failed", style="bold red"),
                    border_style="red",
                )
            )
            return False

    console.print(
        Panel.fit(
            Text("✅ Upload to PyPI successful!", style="bold green"),
            border_style="green",
        )
    )
    console.print(
        "[cyan]📦[/cyan] Package available at: "
        f"[link]https://pypi.org/project/{project_name}/[/link]"
    )
    return True


# ///////////////////////////////////////////////////////////////
# MAIN
# ///////////////////////////////////////////////////////////////


def main() -> None:
    """Main function."""
    if len(sys.argv) < 2:
        console.print("[yellow]Usage:[/yellow] python upload_to_pypi.py [test|prod]")
        console.print("  [cyan]test[/cyan]         - Upload to Test PyPI")
        console.print("  [cyan]prod[/cyan]         - Upload to production PyPI")
        console.print()
        console.print(
            "[dim]Note: Package must be built first using build_package.py[/dim]"
        )
        return

    action = sys.argv[1]

    if action in ["test", "test-upload"]:
        if not upload_to_test_pypi():
            sys.exit(1)

    elif action in ["prod", "upload"]:
        if not upload_to_pypi():
            sys.exit(1)

    else:
        console.print(f"[red]❌[/red] Unknown action: [bold]{action}[/bold]")
        console.print("[yellow]💡[/yellow] Use 'test' or 'prod'")
        sys.exit(1)


if __name__ == "__main__":
    main()
