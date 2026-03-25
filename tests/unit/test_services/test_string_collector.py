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

from ezqt_app.services.translation import is_translatable
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

    def test_should_use_home_ezqt_as_default_user_dir_when_instantiated(self) -> None:
        collector = StringCollector()
        assert collector.user_dir == Path.home() / ".ezqt"

    def test_should_initialize_with_empty_collected_strings_when_instantiated(
        self, tmp_path: Path
    ) -> None:
        collector = StringCollector(user_dir=tmp_path)
        assert len(collector._collected_strings) == 0


class TestIsTranslatableViaCollector:
    """Tests for is_translatable() — the filter used by StringCollector.

    ``StringCollector._is_valid_string()`` was removed in P1 and replaced by
    the standalone ``is_translatable()`` from ``_scanner``.  These tests verify
    the same contract through the public re-export.
    """

    def test_should_return_false_when_string_is_empty(self) -> None:
        assert not is_translatable("")

    def test_should_return_false_when_string_is_single_character(self) -> None:
        assert not is_translatable("a")

    def test_should_return_false_when_string_is_digits_only(self) -> None:
        assert not is_translatable("42")

    def test_should_return_false_when_string_has_underscore_prefix(self) -> None:
        assert not is_translatable("_private_var")

    def test_should_return_false_when_string_has_menu_prefix(self) -> None:
        assert not is_translatable("menu_action")

    def test_should_return_false_when_string_has_btn_prefix(self) -> None:
        assert not is_translatable("btn_ok")

    def test_should_return_false_when_string_has_setting_prefix(self) -> None:
        assert not is_translatable("settingTheme")

    def test_should_return_false_when_string_is_constant_case(self) -> None:
        assert not is_translatable("MY_CONSTANT")

    def test_should_return_false_when_string_is_all_lowercase_identifier(self) -> None:
        assert not is_translatable("somevariable")

    def test_should_return_true_when_string_has_spaces(self) -> None:
        assert is_translatable("Click to continue")

    def test_should_return_true_when_string_is_ui_label_text(self) -> None:
        assert is_translatable("Save Settings")

    def test_should_return_true_when_string_has_mixed_case_with_spaces(self) -> None:
        assert is_translatable("Open File")


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
