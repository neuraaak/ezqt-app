#!/usr/bin/env python3
# ///////////////////////////////////////////////////////////////
# LINT - Code Quality Checker
# ///////////////////////////////////////////////////////////////

"""
Code quality check script.

Runs Ruff on the codebase.

Usage:
    python .scripts/dev/lint.py [options]

Options:
    --check-only    Only check, don't fix
    --fix          Fix issues automatically (default)
    --verbose      Verbose output
    --help         Show this help
"""

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import argparse
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

project_name = "EzQt-App"

# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////


class CodeQualityChecker:
    """Code quality checker for your project."""

    # ///////////////////////////////////////////////////////////////
    # INIT
    # ///////////////////////////////////////////////////////////////

    def __init__(self, check_only: bool = False, verbose: bool = False) -> None:
        """Initialize the code quality checker.

        Args:
            check_only: If True, only check without fixing
            verbose: If True, show verbose output
        """
        self.check_only = check_only
        self.verbose = verbose
        # Configure console with UTF-8 encoding for Windows emoji support
        # Force UTF-8 encoding on Windows
        if sys.platform == "win32":
            sys.stdout = io.TextIOWrapper(
                sys.stdout.buffer, encoding="utf-8", errors="replace"
            )
        self.console = Console(legacy_windows=False)
        # Project root is 2 levels up from .scripts/dev/lint.py
        self.project_root = Path(__file__).resolve().parents[2]
        # Directories to scan (relative to project root)
        self.scan_dirs = [
            f"src/{project_name.lower().replace('-', '_')}",
            "tests",
            ".scripts",
        ]

    # ///////////////////////////////////////////////////////////////
    # PRIVATE METHODS
    # ///////////////////////////////////////////////////////////////

    def _get_scan_paths(self) -> list[Path]:
        """Get paths to scan (directories or files).

        Returns:
            List[Path]: List of paths to scan
        """
        scan_paths = []
        for scan_dir in self.scan_dirs:
            scan_path = self.project_root / scan_dir
            if scan_path.exists():
                scan_paths.append(scan_path)
            elif self.verbose:
                self.console.print(
                    f"  [yellow]⚠[/yellow]  Warning: {scan_path} does not exist, skipping..."
                )
        return scan_paths

    def _run_command(self, command: list[str], description: str) -> bool:
        """Run a command and return success status.

        Args:
            command: Command to execute as list of strings
            description: Description of the command

        Returns:
            bool: True if command succeeded, False otherwise
        """
        if self.verbose:
            self.console.print(f"[cyan]Running {description}...[/cyan]")
            self.console.print(f"  [dim]Command: {' '.join(command)}[/dim]")

        try:
            result = subprocess.run(  # noqa: S603
                command,
                check=True,
                capture_output=not self.verbose,
                text=True,
                cwd=self.project_root,
            )

        except subprocess.CalledProcessError as e:
            self.console.print(f"[red]❌ ERROR:[/red] {description} failed:")
            if e.stdout:
                self.console.print(f"[dim]STDOUT:[/dim]\n{e.stdout}")
            if e.stderr:
                self.console.print(f"[dim]STDERR:[/dim]\n{e.stderr}")
            return False
        else:
            if self.verbose and result.stdout:
                self.console.print(result.stdout)

            self.console.print(
                f"[green]✓[/green] [green]SUCCESS:[/green] {description} completed successfully"
            )
            return True

    # ///////////////////////////////////////////////////////////////
    # PUBLIC METHODS
    # ///////////////////////////////////////////////////////////////

    def run_import_linter(self) -> bool:
        """Run import-linter to check layer dependency contracts.

        Returns:
            bool: True if contracts are respected, False otherwise
        """
        command = ["lint-imports"]
        env = {"PYTHONPATH": str(self.project_root / "src")}

        if self.verbose:
            self.console.print("[cyan]Running import-linter...[/cyan]")
            self.console.print(
                f"  [dim]Command: PYTHONPATH=src {' '.join(command)}[/dim]"
            )

        try:
            import os

            full_env = {**os.environ, **env}
            result = subprocess.run(  # noqa: S603
                command,
                check=True,
                capture_output=not self.verbose,
                text=True,
                cwd=self.project_root,
                env=full_env,
            )
        except subprocess.CalledProcessError as e:
            self.console.print("[red]❌ ERROR:[/red] import-linter failed:")
            if e.stdout:
                self.console.print(f"[dim]STDOUT:[/dim]\n{e.stdout}")
            if e.stderr:
                self.console.print(f"[dim]STDERR:[/dim]\n{e.stderr}")
            return False
        except FileNotFoundError:
            self.console.print(
                "[yellow]⚠[/yellow]  import-linter not found — skipping (install with: uv add --dev import-linter)"
            )
            return True
        else:
            if self.verbose and result.stdout:
                self.console.print(result.stdout)
            self.console.print(
                "[green]✓[/green] [green]SUCCESS:[/green] import-linter completed successfully"
            )
            return True

    def run_ty(self) -> bool:
        """Run ty type checker.

        Returns:
            bool: True if type checking succeeded, False otherwise
        """
        command = ["ty", "check", "--output-format=concise"]
        command.extend([str(p) for p in self._get_scan_paths()])

        if self.verbose:
            self.console.print("[cyan]Running ty...[/cyan]")
            self.console.print(f"  [dim]Command: {' '.join(command)}[/dim]")

        try:
            result = subprocess.run(  # noqa: S603
                command,
                check=True,
                capture_output=not self.verbose,
                text=True,
                cwd=self.project_root,
            )
        except subprocess.CalledProcessError as e:
            self.console.print("[red]❌ ERROR:[/red] ty type checking failed:")
            if e.stdout:
                self.console.print(f"[dim]STDOUT:[/dim]\n{e.stdout}")
            if e.stderr:
                self.console.print(f"[dim]STDERR:[/dim]\n{e.stderr}")
            return False
        except FileNotFoundError:
            self.console.print(
                "[yellow]⚠[/yellow]  ty not found — skipping (install with: uv add --dev ty)"
            )
            return True
        else:
            if self.verbose and result.stdout:
                self.console.print(result.stdout)
            self.console.print(
                "[green]✓[/green] [green]SUCCESS:[/green] ty type checking completed successfully"
            )
            return True

    def run_ruff(self) -> bool:
        """Run Ruff linter.

        Returns:
            bool: True if linting succeeded, False otherwise
        """
        if self.check_only:
            command = [
                sys.executable,
                "-m",
                "ruff",
                "check",
                "--line-length=88",
                "--output-format=concise",
            ]
        else:
            command = [
                sys.executable,
                "-m",
                "ruff",
                "check",
                "--fix",
                "--line-length=88",
                "--output-format=concise",
            ]

        # Use directories instead of individual files for better performance
        command.extend([str(p) for p in self._get_scan_paths()])

        return self._run_command(command, "Ruff linting")

    def run_ruff_format(self) -> bool:
        """Run Ruff formatter.

        Returns:
            bool: True if formatting succeeded, False otherwise
        """
        mode = "--check" if self.check_only else ""
        command = [sys.executable, "-m", "ruff", "format", "--line-length=88"]

        if mode:
            command.append(mode)

        # Use directories instead of individual files for better performance
        command.extend([str(p) for p in self._get_scan_paths()])

        return self._run_command(command, "Ruff formatting")

    def run_all_checks(self) -> bool:
        """Run all code quality checks.

        Returns:
            bool: True if all checks passed, False otherwise
        """
        # Header with panel
        title = Text("🔍 Code Quality Checker", style="bold cyan")
        subtitle = Text(f"{project_name} Project", style="dim")
        self.console.print(Panel.fit(title, subtitle=subtitle, border_style="cyan"))
        self.console.print()

        if self.verbose:
            self.console.print(f"[dim]Project root:[/dim] {self.project_root}")

        scan_paths = self._get_scan_paths()
        if not scan_paths:
            self.console.print("[red]❌ ERROR:[/red] No directories found to scan!")
            self.console.print(f"  [dim]Project root:[/dim] {self.project_root}")
            self.console.print(f"  [dim]Looking for:[/dim] {', '.join(self.scan_dirs)}")
            sys.exit(1)

        dirs_text = ", ".join(f"[cyan]{p.name}[/cyan]" for p in scan_paths)
        self.console.print(f"[bold]Scanning directories:[/bold] {dirs_text}")
        self.console.print()

        # Order matters: format first, then lint, then types, then architecture contracts
        checks = [
            ("Ruff Format", self.run_ruff_format, "🎨"),
            ("Ruff", self.run_ruff, "🔍"),
            ("Ty", self.run_ty, "🔎"),
            ("Import Linter", self.run_import_linter, "🏗️"),
        ]

        all_passed = True

        for name, check_func, emoji in checks:
            self.console.print(f"[cyan]{emoji} Running {name}...[/cyan]")
            success = check_func()

            if not success:
                all_passed = False
                self.console.print(f"[red]❌ {name} failed[/red]")
            else:
                self.console.print(f"[green]✓ {name} passed[/green]")
            self.console.print()

        if all_passed:
            self.console.print(
                Panel.fit(
                    "[bold green]✓ All code quality checks passed![/bold green]",
                    border_style="green",
                )
            )
        else:
            self.console.print(
                Panel.fit(
                    "[bold red]❌ Some code quality checks failed[/bold red]",
                    border_style="red",
                )
            )
            sys.exit(1)

        return all_passed


# ///////////////////////////////////////////////////////////////
# MAIN
# ///////////////////////////////////////////////////////////////


def main() -> None:
    """Main function."""
    parser = argparse.ArgumentParser(
        description=f"Code quality checker for {project_name} project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python .scripts/dev/lint.py              # Fix all issues
  python .scripts/dev/lint.py --check-only # Only check, don't fix
  python .scripts/dev/lint.py --verbose    # Verbose output
        """,
    )

    parser.add_argument(
        "--check-only", action="store_true", help="Only check, don't fix issues"
    )

    parser.add_argument(
        "--fix", action="store_true", help="Fix issues automatically (default)"
    )

    parser.add_argument("--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    # Default to fix mode unless check-only is specified
    check_only = args.check_only

    checker = CodeQualityChecker(check_only=check_only, verbose=args.verbose)
    checker.run_all_checks()


if __name__ == "__main__":
    main()
