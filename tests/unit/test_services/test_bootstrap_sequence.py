# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_SERVICES.TEST_BOOTSTRAP_SEQUENCE - Sequence orchestration tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for services/bootstrap/sequence.py — InitializationSequence."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
from unittest.mock import patch

from ezqt_app.services.bootstrap.contracts.steps import StepStatus
from ezqt_app.services.bootstrap.sequence import InitializationSequence

# ///////////////////////////////////////////////////////////////
# HELPERS
# ///////////////////////////////////////////////////////////////


def _empty_sequence() -> InitializationSequence:
    """Return an InitializationSequence with no default steps registered."""
    with patch.object(InitializationSequence, "_setup_steps"):
        seq = InitializationSequence()
    return seq


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////


class TestInitializationSequenceStepManagement:
    """Tests for step registration and introspection."""

    def test_should_append_one_step_when_add_step_is_called(self) -> None:
        seq = _empty_sequence()
        assert len(seq.steps) == 0
        seq.add_step("my-step", "A test step", lambda: None, required=True)
        assert len(seq.steps) == 1

    def test_should_store_name_and_description_when_step_is_added(self) -> None:
        seq = _empty_sequence()
        seq.add_step("init", "Initialize", lambda: None)
        step = seq.steps[0]
        assert step.name == "init"
        assert step.description == "Initialize"

    def test_should_store_required_flag_when_step_is_added(self) -> None:
        seq = _empty_sequence()
        seq.add_step("opt", "Optional", lambda: None, required=False)
        assert seq.steps[0].required is False

    def test_should_return_none_when_step_name_is_unknown(self) -> None:
        seq = _empty_sequence()
        assert seq.get_step_status("nonexistent") is None

    def test_should_normalize_spaces_and_case_when_error_code_is_generated(
        self,
    ) -> None:
        seq = _empty_sequence()
        code = seq._error_code_for_step("Configure Startup")
        assert code == "bootstrap.step.configure_startup.failed"

    def test_should_handle_single_word_when_error_code_is_generated(self) -> None:
        seq = _empty_sequence()
        code = seq._error_code_for_step("encoding")
        assert code == "bootstrap.step.encoding.failed"


class TestInitializationSequenceExecution:
    """Tests for execute() flow."""

    def test_should_run_all_steps_when_execute_is_called(self) -> None:
        seq = _empty_sequence()
        results: list[int] = []
        seq.add_step("s1", "Step 1", lambda: results.append(1))
        seq.add_step("s2", "Step 2", lambda: results.append(2))

        summary = seq.execute(verbose=False)

        assert results == [1, 2]
        assert summary.success is True

    def test_should_return_init_result_when_execute_is_called(self) -> None:
        from ezqt_app.domain.results import InitResult

        seq = _empty_sequence()
        seq.add_step("ok", "ok", lambda: None)
        summary = seq.execute(verbose=False)
        assert isinstance(summary, InitResult)

    def test_should_mark_step_as_success_when_step_completes(self) -> None:
        seq = _empty_sequence()
        seq.add_step("good", "Good step", lambda: None)
        seq.execute(verbose=False)
        assert seq.get_step_status("good") == StepStatus.SUCCESS

    def test_should_mark_step_as_failed_when_required_step_raises(self) -> None:
        seq = _empty_sequence()

        def failing() -> None:
            raise RuntimeError("step failed")

        seq.add_step("bad", "Bad step", failing, required=True)
        summary = seq.execute(verbose=False)

        assert summary.success is False
        assert seq.get_step_status("bad") == StepStatus.FAILED

    def test_should_stop_execution_when_required_step_fails(self) -> None:
        seq = _empty_sequence()
        executed: list[str] = []

        def failing() -> None:
            raise RuntimeError("boom")

        seq.add_step("fail-me", "d", failing, required=True)
        seq.add_step(
            "should-not-run", "d", lambda: executed.append("ran"), required=True
        )

        seq.execute(verbose=False)

        assert "ran" not in executed

    def test_should_continue_execution_when_optional_step_fails(self) -> None:
        seq = _empty_sequence()
        results: list[str] = []

        def optional_fail() -> None:
            raise RuntimeError("optional fails")

        seq.add_step("bad-opt", "d", optional_fail, required=False)
        seq.add_step("next", "d", lambda: results.append("ok"), required=True)

        seq.execute(verbose=False)

        assert "ok" in results

    def test_should_include_error_info_in_summary_when_step_fails(self) -> None:
        seq = _empty_sequence()

        def failing() -> None:
            raise RuntimeError("specific message")

        seq.add_step("err-step", "d", failing, required=True)
        summary = seq.execute(verbose=False)

        assert summary.error is not None
        assert "specific message" in summary.error.message

    def test_should_succeed_when_sequence_is_empty(self) -> None:
        seq = _empty_sequence()
        summary = seq.execute(verbose=False)
        assert summary.success is True


class TestInitializationSequenceIntrospection:
    """Tests for get_failed_steps / get_successful_steps."""

    def test_should_return_failed_steps_when_required_step_fails(self) -> None:
        seq = _empty_sequence()

        def fail() -> None:
            raise RuntimeError("fail")

        seq.add_step("bad", "d", fail, required=True)
        seq.execute(verbose=False)

        failed = seq.get_failed_steps()
        assert len(failed) == 1
        assert failed[0].name == "bad"

    def test_should_return_successful_steps_when_steps_complete(self) -> None:
        seq = _empty_sequence()
        seq.add_step("good1", "d", lambda: None)
        seq.add_step("good2", "d", lambda: None)
        seq.execute(verbose=False)

        successful = seq.get_successful_steps()
        assert len(successful) == 2

    def test_should_return_empty_list_when_all_steps_succeed(self) -> None:
        seq = _empty_sequence()
        seq.add_step("ok", "d", lambda: None)
        seq.execute(verbose=False)
        assert seq.get_failed_steps() == []
