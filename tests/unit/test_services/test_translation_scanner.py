# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_SERVICES.TEST_TRANSLATION_SCANNER - Scanner tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for services/translation/_scanner.py."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
from unittest.mock import MagicMock

import pytest

from ezqt_app.services.translation._scanner import (
    TextRole,
    WidgetEntry,
    is_translatable,
    scan_widget,
)

# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////


class TestTextRole:
    """Tests for the TextRole enum."""

    def test_should_have_set_text_value_for_text_role(self) -> None:
        assert TextRole.TEXT == "setText"

    def test_should_have_set_tool_tip_value_for_tooltip_role(self) -> None:
        assert TextRole.TOOLTIP == "setToolTip"

    def test_should_have_set_placeholder_text_value_for_placeholder_role(self) -> None:
        assert TextRole.PLACEHOLDER == "setPlaceholderText"

    def test_should_have_set_title_value_for_title_role(self) -> None:
        assert TextRole.TITLE == "setTitle"

    def test_should_have_set_window_title_value_for_window_title_role(self) -> None:
        assert TextRole.WINDOW_TITLE == "setWindowTitle"

    def test_should_be_usable_as_string_since_it_is_str_enum(self) -> None:
        assert isinstance(TextRole.TEXT, str)
        assert TextRole.TEXT.startswith("set")


class TestWidgetEntry:
    """Tests for the WidgetEntry dataclass."""

    def test_should_store_text_and_role_when_created(self) -> None:
        entry = WidgetEntry(original_text="Hello", role=TextRole.TEXT)
        assert entry.original_text == "Hello"
        assert entry.role == TextRole.TEXT

    def test_should_store_tooltip_role_when_tooltip_entry_is_created(self) -> None:
        entry = WidgetEntry(original_text="Hover for info", role=TextRole.TOOLTIP)
        assert entry.role == TextRole.TOOLTIP

    def test_should_use_slots_for_memory_efficiency(self) -> None:
        assert hasattr(WidgetEntry, "__slots__")


class TestIsTranslatable:
    """Tests for the is_translatable() filter function."""

    # --- Returns False ---

    def test_should_return_false_when_text_is_empty(self) -> None:
        assert not is_translatable("")

    def test_should_return_false_when_text_is_single_char(self) -> None:
        assert not is_translatable("a")

    def test_should_return_false_when_text_is_digits_only(self) -> None:
        assert not is_translatable("123")

    def test_should_return_false_when_text_is_all_caps_constant(self) -> None:
        assert not is_translatable("MY_CONSTANT")
        assert not is_translatable("ENABLED")

    def test_should_return_false_when_text_is_snake_case(self) -> None:
        assert not is_translatable("my_variable")
        assert not is_translatable("some_key")

    def test_should_return_false_when_text_is_camel_case(self) -> None:
        assert not is_translatable("myLabel")
        assert not is_translatable("onChange")

    def test_should_return_false_when_text_is_pascal_case(self) -> None:
        assert not is_translatable("MyWidget")
        assert not is_translatable("UserName")

    def test_should_return_false_when_text_has_technical_prefix(self) -> None:
        assert not is_translatable("_internal")
        assert not is_translatable("btn_submit")
        assert not is_translatable("menu_file")
        assert not is_translatable("setting_theme")

    # --- Returns True ---

    def test_should_return_true_for_human_readable_sentence(self) -> None:
        assert is_translatable("Click here")
        assert is_translatable("Save changes")

    def test_should_return_true_for_capitalized_single_word(self) -> None:
        assert is_translatable("Save")
        assert is_translatable("Cancel")

    def test_should_return_true_for_accented_text(self) -> None:
        assert is_translatable("Paramètres")
        assert is_translatable("Bonjour")


class TestScanWidget:
    """Tests for scan_widget() with mock widgets."""

    def _make_widget(
        self,
        text: str = "",
        tooltip: str = "",
        placeholder: str = "",
        children: list | None = None,
    ) -> MagicMock:
        """Build a MagicMock widget with the given property values."""
        w = MagicMock()
        w.text.return_value = text
        w.toolTip.return_value = tooltip
        w.placeholderText.return_value = placeholder
        w.findChildren.return_value = children or []
        return w

    def test_should_return_empty_when_widget_has_no_translatable_text(self) -> None:
        widget = self._make_widget(text="", tooltip="", placeholder="")
        assert scan_widget(widget) == []

    def test_should_return_text_entry_when_widget_has_translatable_text(self) -> None:
        widget = self._make_widget(text="Click here")
        results = scan_widget(widget)
        assert len(results) == 1
        assert results[0][1].original_text == "Click here"
        assert results[0][1].role == TextRole.TEXT

    def test_should_return_tooltip_entry_when_widget_has_translatable_tooltip(
        self,
    ) -> None:
        widget = self._make_widget(text="", tooltip="Hover for details")
        results = scan_widget(widget, include_tooltips=True)
        tooltip_entries = [r for r in results if r[1].role == TextRole.TOOLTIP]
        assert len(tooltip_entries) == 1
        assert tooltip_entries[0][1].original_text == "Hover for details"

    def test_should_not_return_tooltip_when_include_tooltips_is_false(self) -> None:
        widget = self._make_widget(text="", tooltip="Hover for details")
        results = scan_widget(widget, include_tooltips=False)
        assert all(r[1].role != TextRole.TOOLTIP for r in results)

    def test_should_return_placeholder_entry_when_widget_has_translatable_placeholder(
        self,
    ) -> None:
        widget = self._make_widget(text="", placeholder="Enter your name")
        results = scan_widget(widget, include_placeholders=True)
        placeholder_entries = [r for r in results if r[1].role == TextRole.PLACEHOLDER]
        assert len(placeholder_entries) == 1
        assert placeholder_entries[0][1].original_text == "Enter your name"

    def test_should_not_return_placeholder_when_include_placeholders_is_false(
        self,
    ) -> None:
        widget = self._make_widget(text="", placeholder="Enter your name")
        results = scan_widget(widget, include_placeholders=False)
        assert all(r[1].role != TextRole.PLACEHOLDER for r in results)

    def test_should_return_multiple_entries_when_widget_has_text_and_tooltip(
        self,
    ) -> None:
        widget = self._make_widget(text="Submit", tooltip="Click to submit the form")
        results = scan_widget(widget)
        roles = {r[1].role for r in results}
        assert TextRole.TEXT in roles
        assert TextRole.TOOLTIP in roles

    def test_should_include_child_entries_when_recursive_is_true(self) -> None:
        child = self._make_widget(text="Child label")
        parent = self._make_widget(text="", children=[child])
        results = scan_widget(parent, recursive=True)
        texts = [r[1].original_text for r in results]
        assert "Child label" in texts

    def test_should_not_include_child_entries_when_recursive_is_false(self) -> None:
        child = self._make_widget(text="Child label")
        parent = self._make_widget(text="Parent label", children=[child])
        results = scan_widget(parent, recursive=False)
        texts = [r[1].original_text for r in results]
        assert "Parent label" in texts
        assert "Child label" not in texts

    def test_should_not_visit_widget_twice_when_circular_reference_exists(
        self,
    ) -> None:
        widget = self._make_widget(text="Hello")
        widget.findChildren.return_value = [widget]  # self-reference
        results = scan_widget(widget, recursive=True)
        text_entries = [r for r in results if r[1].role == TextRole.TEXT]
        assert len(text_entries) == 1  # visited exactly once

    def test_should_skip_technical_text_when_scanning(self) -> None:
        widget = self._make_widget(text="myButton")
        results = scan_widget(widget)
        assert results == []

    @pytest.mark.parametrize(
        "role",
        [TextRole.TEXT, TextRole.TOOLTIP, TextRole.PLACEHOLDER],
    )
    def test_should_associate_widget_reference_in_result_tuple(
        self, role: TextRole
    ) -> None:
        if role == TextRole.TEXT:
            widget = self._make_widget(text="Submit")
        elif role == TextRole.TOOLTIP:
            widget = self._make_widget(tooltip="Click to submit")
        else:
            widget = self._make_widget(placeholder="Enter value")

        results = scan_widget(widget)
        matching = [r for r in results if r[1].role == role]
        assert len(matching) == 1
        assert matching[0][0] is widget  # first element is the widget itself
