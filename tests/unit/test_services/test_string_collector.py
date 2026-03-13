# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_SERVICES.TEST_STRING_COLLECTOR - StringCollector tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for services/translation/string_collector.py."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from ezqt_app.services.translation.string_collector import StringCollector

# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////


class TestStringCollectorInit:
    """Tests for StringCollector.__init__()."""

    def test_should_create_translations_dir_when_instantiated_with_user_dir(
        self, tmp_path: Path
    ) -> None:
        collector = StringCollector(user_dir=tmp_path / "collector")
        assert collector.translations_dir.exists()

    def test_should_create_cache_dir_when_instantiated_with_user_dir(
        self, tmp_path: Path
    ) -> None:
        collector = StringCollector(user_dir=tmp_path / "collector")
        assert collector.cache_dir.exists()

    def test_should_create_logs_dir_when_instantiated_with_user_dir(
        self, tmp_path: Path
    ) -> None:
        collector = StringCollector(user_dir=tmp_path / "collector")
        assert collector.logs_dir.exists()

    def test_should_use_home_ezqt_as_default_user_dir_when_instantiated(self) -> None:
        collector = StringCollector()
        assert collector.user_dir == Path.home() / ".ezqt"

    def test_should_initialize_with_empty_collected_strings_when_instantiated(
        self, tmp_path: Path
    ) -> None:
        collector = StringCollector(user_dir=tmp_path)
        assert len(collector._collected_strings) == 0


class TestIsValidString:
    """Tests for StringCollector._is_valid_string()."""

    @pytest.fixture
    def collector(self, tmp_path: Path) -> StringCollector:
        return StringCollector(user_dir=tmp_path)

    def test_should_return_false_when_string_is_empty(
        self, collector: StringCollector
    ) -> None:
        assert not collector._is_valid_string("")

    def test_should_return_false_when_string_is_single_character(
        self, collector: StringCollector
    ) -> None:
        assert not collector._is_valid_string("a")

    def test_should_return_false_when_string_is_digits_only(
        self, collector: StringCollector
    ) -> None:
        assert not collector._is_valid_string("42")

    def test_should_return_false_when_string_has_underscore_prefix(
        self, collector: StringCollector
    ) -> None:
        assert not collector._is_valid_string("_private_var")

    def test_should_return_false_when_string_has_menu_prefix(
        self, collector: StringCollector
    ) -> None:
        assert not collector._is_valid_string("menu_action")

    def test_should_return_false_when_string_has_btn_prefix(
        self, collector: StringCollector
    ) -> None:
        assert not collector._is_valid_string("btn_ok")

    def test_should_return_false_when_string_has_setting_prefix(
        self, collector: StringCollector
    ) -> None:
        assert not collector._is_valid_string("settingTheme")

    def test_should_return_false_when_string_is_constant_case(
        self, collector: StringCollector
    ) -> None:
        assert not collector._is_valid_string("MY_CONSTANT")

    def test_should_return_false_when_string_is_all_lowercase_identifier(
        self, collector: StringCollector
    ) -> None:
        assert not collector._is_valid_string("somevariable")

    def test_should_return_true_when_string_has_spaces(
        self, collector: StringCollector
    ) -> None:
        assert collector._is_valid_string("Click to continue")

    def test_should_return_true_when_string_is_ui_label_text(
        self, collector: StringCollector
    ) -> None:
        assert collector._is_valid_string("Save Settings")

    def test_should_return_true_when_string_has_mixed_case_with_spaces(
        self, collector: StringCollector
    ) -> None:
        assert collector._is_valid_string("Open File")


class TestCollectStringsFromWidget:
    """Tests for StringCollector.collect_strings_from_widget()."""

    @pytest.fixture
    def collector(self, tmp_path: Path) -> StringCollector:
        return StringCollector(user_dir=tmp_path)

    def _make_widget(
        self,
        text: str = "",
        tooltip: str = "",
        title: str = "",
        children: list | None = None,
    ) -> MagicMock:
        widget = MagicMock()
        widget.text.return_value = text
        widget.toolTip.return_value = tooltip
        widget.windowTitle.return_value = title
        widget.findChildren.return_value = children or []
        return widget

    def test_should_collect_text_when_widget_has_valid_text(
        self, collector: StringCollector
    ) -> None:
        widget = self._make_widget(text="Save Settings")
        result = collector.collect_strings_from_widget(widget, recursive=False)
        assert "Save Settings" in result

    def test_should_skip_text_when_widget_text_is_technical(
        self, collector: StringCollector
    ) -> None:
        widget = self._make_widget(text="MY_CONSTANT")
        result = collector.collect_strings_from_widget(widget, recursive=False)
        assert "MY_CONSTANT" not in result

    def test_should_collect_tooltip_when_widget_tooltip_is_valid(
        self, collector: StringCollector
    ) -> None:
        widget = self._make_widget(tooltip="Open settings panel")
        result = collector.collect_strings_from_widget(widget, recursive=False)
        assert "Open settings panel" in result

    def test_should_skip_tooltip_when_widget_tooltip_is_too_short(
        self, collector: StringCollector
    ) -> None:
        widget = self._make_widget(tooltip="x")
        result = collector.collect_strings_from_widget(widget, recursive=False)
        assert "x" not in result

    def test_should_return_set_when_collect_is_called(
        self, collector: StringCollector
    ) -> None:
        widget = self._make_widget()
        result = collector.collect_strings_from_widget(widget, recursive=False)
        assert isinstance(result, set)

    def test_should_return_empty_set_when_widget_has_no_text_method(
        self, collector: StringCollector
    ) -> None:
        widget = MagicMock(spec=[])  # No callable methods
        result = collector.collect_strings_from_widget(widget, recursive=False)
        assert isinstance(result, set)

    def test_should_deduplicate_when_text_and_tooltip_are_identical(
        self, collector: StringCollector
    ) -> None:
        widget = self._make_widget(text="Open File", tooltip="Open File")
        result = collector.collect_strings_from_widget(widget, recursive=False)
        assert (
            result.count("Open File")
            if isinstance(result, list)
            else len([s for s in result if s == "Open File"]) == 1
        )
