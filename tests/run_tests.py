#!/usr/bin/env python
# ///////////////////////////////////////////////////////////////
# RUN_TESTS - Test runner script
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""
Test runner script for EzQt_App.

Provides a convenient CLI wrapper around pytest for executing different
types of tests (unit, integration, robustness) with various configurations.

Supports:
    - Running specific test types or all tests
    - Coverage reporting
    - Verbose output
    - Parallel execution via pytest-xdist
    - Marker-based filtering
    - Fast mode (excluding slow tests)

Example:
    python run_tests.py --type unit --verbose --coverage
    python run_tests.py --type all --parallel
    python run_tests.py --marker qt --fast
"""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import argparse
import logging
import subprocess
import sys
from pathlib import Path

# ///////////////////////////////////////////////////////////////
# HELPER FUNCTIONS
# ///////////////////////////////////////////////////////////////

logger = logging.getLogger(__name__)


def run_command(cmd: list[str], description: str) -> bool:
    """
    Execute a command and display output in real-time.

    Args:
        cmd: Command and arguments as list of strings
        description: Human-readable description of what's running

    Returns:
        bool: True if command succeeded (exit code 0), False otherwise
    """
    logger.info("\n%s", "=" * 60)
    logger.info("%s", description)
    logger.info("%s", "=" * 60)
    try:
        result = subprocess.run(cmd, check=False)  # noqa: S603
        return result.returncode == 0
    except KeyboardInterrupt:
        logger.warning("Interrupted by user (Ctrl+C)")
        return False
    except Exception as e:
        logger.exception("Execution error: %s", e)
        return False


def main() -> None:
    """
    Main entry point for the test runner.

    Parses CLI arguments and executes pytest with appropriate configuration.
    Validates that pyproject.toml exists before running tests.

    Exit codes:
        0: All tests passed
        1: Tests failed or pyproject.toml not found
    """
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

    parser = argparse.ArgumentParser(
        description="Test runner for EzQt_App with flexible configuration"
    )
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
        logger.error("pyproject.toml not found. Run this script from the project root.")
        sys.exit(1)

    # Build pytest command
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
            [
                "--cov=src/ezqt_app",
                "--cov-report=term-missing",
                "--cov-report=html:htmlcov",
            ]
        )

    success = run_command(cmd_parts, f"Running {args.type} tests")

    if success:
        logger.info("Tests passed successfully")
        if args.coverage:
            logger.info("Coverage report generated in htmlcov/")
            logger.info("Open htmlcov/index.html in your browser")
    else:
        logger.error("Tests failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
