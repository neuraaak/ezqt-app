#!/usr/bin/env python3
# ///////////////////////////////////////////////////////////////
# UPDATE_README_VERSION - Sync README badge and pyproject.toml with __init__.py version
# ///////////////////////////////////////////////////////////////

"""Update the version badge in README.md and pyproject.toml from your-project/__init__.py.

This keeps the visible version in sync with the canonical __version__ value
defined in your-project/__init__.py, which is the single source of truth.
"""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import io
import re
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
# PUBLIC METHODS
# ///////////////////////////////////////////////////////////////


def read_version() -> str:
    """Read version from {project_name}/__init__.py __version__.

    This is the canonical source of truth for the package version.
    """
    # Project root is the parent of the .scripts/dev directory
    project_root = Path(__file__).resolve().parents[2]
    init_path = project_root / "src" / project_name.lower() / "__init__.py"
    content = init_path.read_text(encoding="utf-8")

    # Match __version__ = "X.Y.Z"
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if match:
        version = match.group(1)
        console.print(
            f"[cyan]📖[/cyan] Found version: [bold green]{version}[/bold green]"
        )
        return version

    error_msg = f"Unable to find __version__ in {project_name}/__init__.py"
    console.print(f"[red]❌[/red] {error_msg}")
    raise RuntimeError(error_msg)


def update_pyproject(version: str) -> None:
    """Update version in pyproject.toml [project].version."""
    project_root = Path(__file__).resolve().parents[2]
    pyproject_path = project_root / "pyproject.toml"
    content = pyproject_path.read_text(encoding="utf-8")

    # Match version = "X.Y.Z" in [project] section
    in_project_section = False
    lines = content.splitlines()
    new_lines = []

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("[project]"):
            in_project_section = True
            new_lines.append(line)
            continue

        if (
            in_project_section
            and stripped.startswith("[")
            and not stripped.startswith("[project]")
        ):
            in_project_section = False

        if in_project_section and stripped.startswith("version"):
            # Replace the version line
            match = re.match(r'version\s*=\s*["\']([^"\']+)["\']', stripped)
            if match:
                # Preserve the original formatting (quotes style)
                quote_char = '"' if '"' in stripped else "'"
                indent = len(line) - len(line.lstrip())
                new_lines.append(
                    f"{indent * ' '}version = {quote_char}{version}{quote_char}"
                )
                continue

        new_lines.append(line)

    pyproject_path.write_text("\n".join(new_lines), encoding="utf-8")
    console.print(
        f"[green]✓[/green] Updated [cyan]pyproject.toml[/cyan] version to [bold]{version}[/bold]"
    )


def update_readme(version: str) -> None:
    """Replace version badge in README.md with the given version."""
    project_root = Path(__file__).resolve().parents[2]
    readme_path = project_root / "README.md"
    content = readme_path.read_text(encoding="utf-8")

    # Match shields.io badge: Version-X.Y.Z-orange.svg?style=for-the-badge
    # Format: [![Version](https://img.shields.io/badge/Version-3.1.0-orange.svg?style=for-the-badge)]
    # Pattern matches: Version-<version>-orange.svg?style=for-the-badge)
    pattern = r"(Version-)(\d+\.\d+\.\d+)(-orange\.svg\?style=for-the-badge\))"
    new_content, count = re.subn(
        pattern,
        rf"\g<1>{version}\g<3>",
        content,
        count=1,
    )

    if count == 0:
        error_msg = "Version badge not found in README.md"
        console.print(f"[red]❌[/red] {error_msg}")
        console.print(
            "[yellow]💡[/yellow] Expected format: "
            "[![Version](.../Version-X.Y.Z-orange.svg?style=for-the-badge)]"
        )
        raise RuntimeError(error_msg)

    readme_path.write_text(new_content, encoding="utf-8")
    console.print(
        f"[green]✓[/green] Updated [cyan]README.md[/cyan] badge to version [bold]{version}[/bold]"
    )


def main() -> None:
    """Entry point."""
    title = Text("🔄 Version Synchronization", style="bold cyan")
    subtitle = Text(f"{project_name} Project", style="dim")
    console.print(Panel.fit(title, subtitle=subtitle, border_style="cyan"))
    console.print()

    try:
        version = read_version()
        update_pyproject(version)
        update_readme(version)

        console.print()
        console.print(
            Panel.fit(
                f"[bold green]✓ Version synchronization completed![/bold green]\n"
                f"[dim]All files updated to version {version}[/dim]",
                border_style="green",
            )
        )
    except (RuntimeError, FileNotFoundError) as e:
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
