# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_UTILS.TEST_PRINTER - Printer utility tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for utils/printer.py."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
from unittest.mock import patch

from ezqt_app.utils import printer as printer_module


class TestPrinter:
    """Tests for Printer formatting and gating behaviors."""

    def test_should_print_info_and_success_messages(self) -> None:
        printer = printer_module.Printer(verbose=False, debug=False)

        with patch("builtins.print") as mocked_print:
            printer.info("hello")
            printer.success("done")

        assert mocked_print.call_count == 2

    def test_should_not_print_verbose_when_verbose_is_disabled(self) -> None:
        printer = printer_module.Printer(verbose=False, debug=False)

        with patch("builtins.print") as mocked_print:
            printer.verbose_msg("hidden")

        mocked_print.assert_not_called()

    def test_should_print_verbose_when_verbose_is_enabled(self) -> None:
        printer = printer_module.Printer(verbose=True, debug=False)

        with patch("builtins.print") as mocked_print:
            printer.verbose_msg("shown")

        mocked_print.assert_called_once()

    def test_should_print_debug_when_debug_is_enabled(self) -> None:
        printer = printer_module.Printer(verbose=False, debug=True)

        with patch("builtins.print") as mocked_print:
            printer.debug_msg("dbg")

        mocked_print.assert_called_once()

    def test_should_not_print_debug_when_only_verbose_is_enabled(self) -> None:
        printer = printer_module.Printer(verbose=True, debug=False)

        with patch("builtins.print") as mocked_print:
            printer.debug_msg("dbg")

        mocked_print.assert_not_called()

    def test_should_print_truncated_list_when_items_exceed_max(self) -> None:
        printer = printer_module.Printer(verbose=True, debug=False)

        with patch("builtins.print") as mocked_print:
            printer.list_items(["a", "b", "c", "d"], max_items=2)

        assert mocked_print.called

    def test_should_route_file_operation_by_status(self) -> None:
        printer = printer_module.Printer(verbose=False, debug=False)

        with (
            patch.object(printer, "info") as info,
            patch.object(printer, "error") as error,
            patch.object(printer, "warning") as warning,
        ):
            printer.file_operation("COPY", "x.txt", status="completed")
            printer.file_operation("COPY", "x.txt", status="error")
            printer.file_operation("COPY", "x.txt", status="warning")

        info.assert_called_once()
        error.assert_called_once()
        warning.assert_called_once()

    def test_should_print_section_and_raw_and_custom(self) -> None:
        printer = printer_module.Printer(verbose=False, debug=False)

        with patch("builtins.print") as mocked_print:
            printer.section("Demo")
            printer.custom_print("hello", color="GREEN", prefix="*")
            printer.raw_print("plain")

        assert mocked_print.call_count >= 5

    def test_should_print_config_display_box(self) -> None:
        printer = printer_module.Printer(verbose=False, debug=False)

        with patch("builtins.print") as mocked_print:
            printer.config_display({"name": "Demo", "debug_printer": False})

        assert mocked_print.call_count >= 4

    def test_should_print_qrc_compilation_result_for_failure(self) -> None:
        printer = printer_module.Printer(verbose=True, debug=True)

        with (
            patch.object(printer, "warning") as warning,
            patch.object(printer, "debug_msg") as debug,
        ):
            printer.qrc_compilation_result(False, "oops")

        warning.assert_called_once()
        debug.assert_called_once()


class TestPrinterGlobals:
    """Tests for module-level printer singleton helpers."""

    def test_should_return_default_singleton_when_no_overrides(self) -> None:
        base = printer_module.get_printer()
        assert base is printer_module.get_printer()

    def test_should_return_new_instance_when_overrides_differ(self) -> None:
        base = printer_module.get_printer()
        custom = printer_module.get_printer(verbose=not base.verbose)

        assert custom is not base

    def test_should_update_global_verbose_and_debug(self) -> None:
        printer_module.set_global_verbose(True)
        assert printer_module.get_printer().verbose is True

        printer_module.set_global_debug(True)
        assert printer_module.get_printer().debug is True
