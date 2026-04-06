# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_SERVICES.TEST_INIT_SERVICE - InitService tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for services/bootstrap/init_service.py."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
from pathlib import Path
from unittest.mock import patch

from ezqt_app.domain.results import InitResult
from ezqt_app.services.bootstrap.contracts.options import InitOptions, OverwritePolicy
from ezqt_app.services.bootstrap.init_service import InitService


class TestInitService:
    """Tests for InitService orchestration and guard behavior."""

    def test_should_mark_initialized_when_sequence_succeeds(self) -> None:
        service = InitService()
        summary = InitResult(success=True, message="ok")

        with patch(
            "ezqt_app.services.bootstrap.init_service.InitializationSequence"
        ) as mocked_sequence:
            mocked_sequence.return_value.execute.return_value = summary
            result = service.run()

        assert result is summary
        assert service.is_initialized() is True

    def test_should_return_already_initialized_result_on_second_run(self) -> None:
        service = InitService()

        with patch(
            "ezqt_app.services.bootstrap.init_service.InitializationSequence"
        ) as mocked_sequence:
            mocked_sequence.return_value.execute.return_value = InitResult(success=True)
            service.run()

        result = service.run(
            InitOptions(project_root=Path("project"), bin_path=Path("project/bin"))
        )

        assert result.success is True
        assert result.message == "Already initialized"
        assert result.error is not None
        assert result.error.code == "bootstrap.already_initialized"

    def test_should_return_failed_result_when_sequence_raises(self) -> None:
        service = InitService()

        with patch(
            "ezqt_app.services.bootstrap.init_service.InitializationSequence"
        ) as mocked_sequence:
            mocked_sequence.return_value.execute.side_effect = RuntimeError("boom")
            result = service.run(InitOptions(project_root=Path("project")))

        assert result.success is False
        assert result.error is not None
        assert result.error.code == "bootstrap.unexpected_error"
        assert "boom" in result.error.message

    def test_should_generate_main_when_option_is_enabled(self, tmp_path: Path) -> None:
        service = InitService()
        summary = InitResult(success=True)
        options = InitOptions(
            project_root=tmp_path,
            bin_path=tmp_path / "bin",
            generate_main=True,
            verbose=False,
            overwrite_policy=OverwritePolicy.FORCE,
        )

        with (
            patch(
                "ezqt_app.services.bootstrap.init_service.InitializationSequence"
            ) as mocked_sequence,
            patch(
                "ezqt_app.services.bootstrap.init_service.FileService"
            ) as mocked_file,
        ):
            mocked_sequence.return_value.execute.return_value = summary
            service.run(options)

        mocked_file.assert_called_once_with(
            base_path=tmp_path,
            bin_path=tmp_path / "bin",
            verbose=False,
            overwrite_policy="force",
        )
        mocked_file.return_value.make_main_from_template.assert_called_once()

    def test_should_not_generate_main_when_summary_is_failed(
        self, tmp_path: Path
    ) -> None:
        service = InitService()
        options = InitOptions(project_root=tmp_path, generate_main=True)

        with (
            patch(
                "ezqt_app.services.bootstrap.init_service.InitializationSequence"
            ) as mocked_sequence,
            patch(
                "ezqt_app.services.bootstrap.init_service.FileService"
            ) as mocked_file,
        ):
            mocked_sequence.return_value.execute.return_value = InitResult(
                success=False
            )
            service.run(options)

        mocked_file.assert_not_called()

    def test_should_reset_initialized_flag_when_reset_is_called(self) -> None:
        service = InitService()
        service._initialized = True

        service.reset()

        assert service.is_initialized() is False
