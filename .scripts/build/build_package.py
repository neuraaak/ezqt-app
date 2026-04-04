#!/usr/bin/env python3
# ///////////////////////////////////////////////////////////////
# BUILD_PACKAGE - PyPI Package Builder
# ///////////////////////////////////////////////////////////////

"""
Build script for PyPI package.

This script builds the package and optionally checks it.
"""

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import io
import shutil
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

project_name = "EzQt-App"

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
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        if result.stdout:
            console.print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        console.print(f"[red]❌[/red] Error: {e}")
        if e.stderr:
            console.print(f"[red]Error output:[/red] {e.stderr}")
        return False


def clean_build() -> None:
    """Clean previous build artifacts."""
    console.print("[yellow]🧹[/yellow] Cleaning previous build artifacts...")

    project_root = Path(__file__).resolve().parents[2]

    # Remove build directories
    paths_to_clean = [
        project_root / "build",
        project_root / "dist",
    ]

    # Find and remove egg-info directories
    for egg_info in project_root.glob("*.egg-info"):
        paths_to_clean.append(egg_info)

    for path in paths_to_clean:
        if path.exists():
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()

    console.print("[green]✅[/green] Build artifacts cleaned")


def build_package() -> bool:
    """Build the package.

    Returns:
        bool: True if build succeeded, False otherwise
    """
    console.print(
        Panel.fit(
            Text(f"🔨 Building {project_name} package", style="bold cyan"),
            border_style="cyan",
        )
    )

    # Clean previous builds
    clean_build()

    # Build the package
    commands = [
        ["uv", "build", "--wheel"],
        ["uv", "build", "--sdist"],
    ]

    for command in commands:
        if not run_command(command, "Building package"):
            return False

    console.print(
        Panel.fit(
            Text("✅ Package built successfully", style="bold green"),
            border_style="green",
        )
    )
    return True


def check_package() -> bool:
    """Check the built package.

    Returns:
        bool: True if check passed, False otherwise
    """
    console.print("[cyan]🔍[/cyan] Checking package...")

    project_root = Path(__file__).resolve().parents[2]
    dist_path = project_root / "dist"

    # Find all distribution files
    dist_files = list(dist_path.glob("*"))
    if not dist_files:
        console.print("[red]❌[/red] No distribution files found in dist/")
        return False

    commands = [
        ["uv", "run", "twine", "check"] + [str(f) for f in dist_files],
    ]

    for command in commands:
        if not run_command(command, "Checking package"):
            return False

    console.print("[green]✅[/green] Package check passed")
    return True


# ///////////////////////////////////////////////////////////////
# MAIN
# ///////////////////////////////////////////////////////////////


def main() -> None:
    """Main function."""
    if len(sys.argv) < 2:
        console.print("[yellow]Usage:[/yellow] python build_package.py [build|check]")
        console.print("  [cyan]build[/cyan]        - Build the package")
        console.print("  [cyan]check[/cyan]        - Check the built package")
        return

    action = sys.argv[1]

    if action == "build":
        if not build_package():
            sys.exit(1)

    elif action == "check":
        if not build_package():
            sys.exit(1)
        if not check_package():
            sys.exit(1)

    else:
        console.print(f"[red]❌[/red] Unknown action: [bold]{action}[/bold]")
        sys.exit(1)


if __name__ == "__main__":
    main()
