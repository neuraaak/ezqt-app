"""CLI tests aligned with the v6 command structure."""

from click.testing import CliRunner

from ezqt_app.cli.main import cli


def test_cli_initialization() -> None:
    """CLI object is importable and callable."""
    assert cli is not None
    assert callable(cli)


def test_cli_lists_expected_commands() -> None:
    """Top-level CLI exposes the expected command names."""
    expected_commands = {
        "init",
        "convert",
        "mkqm",
        "test",
        "docs",
        "info",
        "create",
    }
    assert expected_commands.issubset(set(cli.commands))


def test_cli_help_runs_successfully() -> None:
    """The CLI help page can be rendered."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])

    assert result.exit_code == 0
    assert "Usage:" in result.output
