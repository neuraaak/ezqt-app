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
        result = subprocess.run(
            cmd, shell=True, check=False, capture_output=True, text=True
        )
        print(result.stdout)
        if result.stderr:
            print(f"⚠️  Warnings/Errors: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error during execution: {e}")
        return False


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Test runner for EzQt_App")
    parser.add_argument(
        "--type",
        choices=["unit", "integration", "all"],
        default="unit",
        help="Type of tests to run",
    )
    parser.add_argument(
        "--coverage", action="store_true", help="Generate coverage report"
    )
    parser.add_argument("--verbose", action="store_true", help="Verbose mode")
    parser.add_argument("--fast", action="store_true", help="Exclude slow tests")

    args = parser.parse_args()

    # ////// CHECK THAT WE ARE IN THE RIGHT DIRECTORY
    if not Path("pyproject.toml").exists():
        print(
            "❌ Error: pyproject.toml not found. Run this script from the project root."
        )
        sys.exit(1)

    # ////// BUILD THE PYTEST COMMAND
    cmd_parts = ["python", "-m", "pytest"]

    if args.verbose:
        cmd_parts.append("-v")

    if args.fast:
        cmd_parts.extend(["-m", "not slow"])

    if args.type == "unit":
        cmd_parts.append("tests/unit/")
    elif args.type == "integration":
        cmd_parts.append("tests/integration/")
    else:  # "all"
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
