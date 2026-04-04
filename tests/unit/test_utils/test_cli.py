# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_UTILS.TEST_CLI - CLI tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""CLI tests aligned with the v6 command structure."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Third-party imports
from click.testing import CliRunner

# Local imports
from ezqt_app.cli.main import cli

# ///////////////////////////////////////////////////////////////
# FUNCTIONS
# ///////////////////////////////////////////////////////////////


def test_should_be_importable_and_callable_when_cli_is_loaded() -> None:
    """CLI object is importable and callable."""
    assert cli is not None
    assert callable(cli)


def test_should_expose_expected_commands_when_cli_is_loaded() -> None:
    """Top-level CLI exposes the expected command names."""
    expected_commands = {
        "init",
        "convert",
        "docs",
        "info",
        "create",
    }
    assert expected_commands.issubset(set(cli.commands))


def test_should_render_help_page_when_help_flag_is_given() -> None:
    """The CLI help page can be rendered."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])

    assert result.exit_code == 0
    assert "Usage:" in result.output
