#!/usr/bin/env python3
# ///////////////////////////////////////////////////////////////
# UPDATE_VERSION - Sync version.py and README badge from pyproject.toml
# ///////////////////////////////////////////////////////////////

"""Update version.py from the version defined in pyproject.toml.

pyproject.toml [project].version is the single source of truth.
The README version badge is dynamic (shields.io PyPI) and does not need updating.
"""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import io
import re
import sys
import tomllib
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

# Force UTF-8 encoding on Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
console = Console(legacy_windows=False)

# ///////////////////////////////////////////////////////////////
# PUBLIC METHODS
# ///////////////////////////////////////////////////////////////


def read_version() -> str:
    """Read version from pyproject.toml [project].version.

    This is the canonical source of truth for the package version.
    """
    project_root = Path(__file__).resolve().parents[2]
    pyproject_path = project_root / "pyproject.toml"

    with pyproject_path.open("rb") as f:
        data = tomllib.load(f)

    version: str = data["project"]["version"]
    console.print(f"[cyan]📖[/cyan] Found version: [bold green]{version}[/bold green]")
    return version


def update_version_py(version: str) -> None:
    """Update __version__ in src/{project_name}/version.py."""
    project_root = Path(__file__).resolve().parents[2]
    version_path = (
        project_root / "src" / project_name.lower().replace("-", "_") / "version.py"
    )
    content = version_path.read_text(encoding="utf-8")

    new_content = re.sub(
        r'(__version__\s*=\s*)["\'][^"\']+["\']',
        rf'\g<1>"{version}"',
        content,
    )
    if new_content == content:
        console.print(f"[dim]✓ version.py already at {version} — no change[/dim]")
        return
    version_path.write_text(new_content, encoding="utf-8")
    console.print(
        f"[green]✓[/green] Updated [cyan]version.py[/cyan] to [bold]{version}[/bold]"
    )


def main() -> None:
    """Entry point."""
    title = Text("🔄 Version Synchronization", style="bold cyan")
    subtitle = Text(f"{project_name} Project", style="dim")
    console.print(Panel.fit(title, subtitle=subtitle, border_style="cyan"))
    console.print()

    try:
        version = read_version()
        update_version_py(version)

        console.print()
        console.print(
            Panel.fit(
                f"[bold green]✓ Version synchronization completed![/bold green]\n"
                f"[dim]version.py updated to {version}[/dim]",
                border_style="green",
            )
        )
    except (FileNotFoundError, KeyError) as e:
        console.print()
        console.print(
            Panel.fit(
                f"[bold red]❌ Version synchronization failed![/bold red]\n"
                f"[red]{str(e)}[/red]",
                border_style="red",
            )
        )
        sys.exit(1)


# ///////////////////////////////////////////////////////////////
# MAIN
# ///////////////////////////////////////////////////////////////

if __name__ == "__main__":
    main()
