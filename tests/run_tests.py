# ///////////////////////////////////////////////////////////////
# Test Runner Script
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Test runner script for ezqt_app.

This script provides a convenient way to run tests with various options:
- Unit, integration, or robustness tests
- Coverage reports
- Parallel execution
- Custom markers
"""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import argparse
import subprocess
import sys
from pathlib import Path

# ///////////////////////////////////////////////////////////////
# FUNCTIONS
# ///////////////////////////////////////////////////////////////


def run_command(cmd, description):
    """Execute a command and display the result."""
    print(f"\n{'=' * 60}")
    print(f"🚀 {description}")
    print(f"{'=' * 60}")

    try:
        # Stream stdout/stderr in real time instead of buffering everything.
        result = subprocess.run(cmd, shell=True, check=False)
        return result.returncode == 0
    except KeyboardInterrupt:
        print("\n⚠️  User interruption (Ctrl+C)")
        return False
    except Exception as e:
        print(f"❌ Error during execution: {e}")
        return False


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Test runner for EzQt_App")
    parser.add_argument(
        "--type",
        choices=["unit", "integration", "robustness", "all"],
        default="unit",
        help="Type of tests to run",
    )
    parser.add_argument(
        "--coverage", action="store_true", help="Generate coverage report"
    )
    parser.add_argument("--verbose", action="store_true", help="Mode verbeux")
    parser.add_argument("--fast", action="store_true", help="Exclure les tests lents")
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Execute tests in parallel (pytest-xdist)",
    )
    parser.add_argument(
        "--marker",
        type=str,
        help="Execute only tests with this marker (e.g., wizard, config)",
    )
    args = parser.parse_args()

    # ////// CHECK THAT WE ARE IN THE RIGHT DIRECTORY
    if not Path("pyproject.toml").exists():
        print(
            "❌ Error: pyproject.toml not found. Run this script from the project root."
        )
        sys.exit(1)

    cmd_parts = [sys.executable, "-m", "pytest"]
    if args.verbose:
        cmd_parts.append("-v")
    if args.fast:
        cmd_parts.extend(["-m", "not slow"])
    if args.marker:
        cmd_parts.extend(["-m", args.marker])
    if args.parallel:
        cmd_parts.extend(["-n", "auto"])
    if args.type == "unit":
        cmd_parts.append("tests/unit/")
    elif args.type == "integration":
        cmd_parts.append("tests/integration/")
    elif args.type == "robustness":
        cmd_parts.append("tests/robustness/")
    else:
        cmd_parts.append("tests/")
    if args.coverage:
        cmd_parts.extend(
            ["--cov=ezqt_app", "--cov-report=term-missing", "--cov-report=html:htmlcov"]
        )

    cmd = " ".join(cmd_parts)

    # ////// RUN THE TESTS
    success = run_command(cmd, f"Running {args.type} tests")

    if success:
        print("\n✅ Tests executed successfully!")

        if args.coverage:
            print("\n📊 Coverage report generated in htmlcov/")
            print("   Open htmlcov/index.html in your browser")
    else:
        print("\n❌ Test failure")
        sys.exit(1)


if __name__ == "__main__":
    main()
