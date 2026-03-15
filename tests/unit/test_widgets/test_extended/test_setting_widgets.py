# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_WIDGETS.TEST_EXTENDED.TEST_SETTING_WIDGETS - Setting widget tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for extended setting widgets."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Third-party imports
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox, QLabel, QLineEdit, QSlider

# Local imports
from ezqt_app.widgets.extended.setting_widgets import (
    BaseSettingWidget,
    SettingCheckbox,
    SettingSelect,
    SettingSlider,
    SettingText,
    SettingToggle,
)

# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////


class TestBaseSettingWidget:
    """Tests for the BaseSettingWidget class."""

    def test_should_have_default_properties_when_instantiated(self, qt_application):
        """Test initialization."""
        widget = BaseSettingWidget("Test Label", "Test Description")

        # Check basic properties
        assert widget._label_text == "Test Label"
        assert widget._description_text == "Test Description"
        assert widget._key is None
        assert widget.objectName() == "base_setting_widget"

    def test_should_store_key_when_set_key_is_called(self, qt_application):
        """Test key definition."""
        widget = BaseSettingWidget("Test Label")

        # Define a key
        widget.set_key("test_key")
        assert widget._key == "test_key"


class TestSettingToggle:
    """Tests for the SettingToggle class."""

    def test_should_have_default_toggle_properties_when_instantiated(
        self, qt_application
    ):
        """Test initialization with default values."""
        widget = SettingToggle("Test Toggle")

        # Check basic properties
        assert widget._label_text == "Test Toggle"
        assert widget._description_text == ""
        assert not widget._value
        assert widget.objectName() == "setting_toggle_container"
        assert widget.property("type") == "setting_toggle"

    def test_should_accept_description_when_instantiated_with_description(
        self, qt_application
    ):
        """Test initialization with description."""
        widget = SettingToggle("Test Toggle", "Test Description", True)

        # Check properties
        assert widget._label_text == "Test Toggle"
        assert widget._description_text == "Test Description"
        assert widget._value

    def test_should_have_label_and_toggle_switch_when_instantiated(
        self, qt_application
    ):
        """Test user interface components."""
        widget = SettingToggle("Test Toggle")

        # Check that components exist
        assert hasattr(widget, "_label_widget")
        assert hasattr(widget, "_control_widget")
        assert isinstance(widget._label_widget, QLabel)

        # Check label text
        assert widget._label_widget.text() == "Test Toggle"

    def test_should_return_checked_when_default_is_true(self, qt_application):
        """Test toggle value."""
        widget = SettingToggle("Test Toggle", default=True)

        # Check initial value
        assert widget.value
        assert widget.get_value()

    def test_should_update_value_when_set_value_is_called(self, qt_application):
        """Test value definition."""
        widget = SettingToggle("Test Toggle")

        # Define a new value
        widget.value = True
        assert widget._value
        assert widget.value

    def test_should_have_value_changed_signal_when_toggle_is_instantiated(
        self, qt_application
    ):
        """Test signal."""
        widget = SettingToggle("Test Toggle")

        # Check that the signal exists
        assert hasattr(widget, "valueChanged")
        assert isinstance(widget.valueChanged, Signal)


class TestSettingSelect:
    """Tests for the SettingSelect class."""

    def test_should_have_default_select_properties_when_instantiated(
        self, qt_application
    ):
        """Test initialization with default values."""
        widget = SettingSelect("Test Select", options=["Option 1", "Option 2"])

        # Check basic properties
        assert widget._label_text == "Test Select"
        assert widget._description_text == ""
        assert widget._value == "Option 1"  # First option by default
        assert widget.objectName() == "setting_select_container"
        assert widget.property("type") == "setting_select"

    def test_should_use_given_default_when_default_option_is_given(
        self, qt_application
    ):
        """Test initialization with a default value."""
        widget = SettingSelect(
            "Test Select", options=["Option 1", "Option 2"], default="Option 2"
        )

        # Check default value
        assert widget._value == "Option 2"

    def test_should_have_label_and_combo_box_when_instantiated(self, qt_application):
        """Test user interface components."""
        widget = SettingSelect("Test Select", options=["Option 1", "Option 2"])

        # Check that components exist
        assert hasattr(widget, "_label_widget")
        assert hasattr(widget, "_control_widget")
        assert isinstance(widget._label_widget, QLabel)
        assert isinstance(widget._control_widget, QComboBox)

        # Check label text
        assert widget._label_widget.text() == "Test Select"

        # Check combo options
        assert widget._control_widget.count() == 2
        assert widget._control_widget.itemText(0) == "Option 1"
        assert widget._control_widget.itemText(1) == "Option 2"

    def test_should_update_value_when_select_value_is_set(self, qt_application):
        """Test value property."""
        widget = SettingSelect("Test Select", options=["Option 1", "Option 2"])

        # Check initial value
        assert widget.value == "Option 1"

        # Define a new value
        widget.value = "Option 2"
        assert widget._value == "Option 2"

    def test_should_get_and_set_value_when_select_methods_are_called(
        self, qt_application
    ):
        """Test get_value and set_value methods."""
        widget = SettingSelect("Test Select", options=["Option 1", "Option 2"])

        # Check get_value
        assert widget.get_value() == "Option 1"

        # Check set_value
        widget.set_value("Option 2")
        assert widget.get_value() == "Option 2"

    def test_should_have_value_changed_signal_when_select_is_instantiated(
        self, qt_application
    ):
        """Test signal."""
        widget = SettingSelect("Test Select", options=["Option 1", "Option 2"])

        # Check that the signal exists
        assert hasattr(widget, "valueChanged")
        assert isinstance(widget.valueChanged, Signal)


class TestSettingSlider:
    """Tests for the SettingSlider class."""

    def test_should_have_default_slider_properties_when_instantiated(
        self, qt_application
    ):
        """Test initialization with default values."""
        widget = SettingSlider("Test Slider")

        # Check basic properties
        assert widget._label_text == "Test Slider"
        assert widget._description_text == ""
        assert widget._value == 50
        assert widget.objectName() == "setting_slider_container"
        assert widget.property("type") == "setting_slider"

    def test_should_accept_custom_range_when_min_and_max_are_given(
        self, qt_application
    ):
        """Test initialization with custom values."""
        widget = SettingSlider("Test Slider", min_val=10, max_val=100, default=50)

        # Check custom values
        assert widget._value == 50

    def test_should_have_label_slider_and_value_label_when_instantiated(
        self, qt_application
    ):
        """Test user interface components."""
        widget = SettingSlider("Test Slider")

        # Check that components exist
        assert hasattr(widget, "_label_widget")
        assert hasattr(widget, "_control_widget")
        assert hasattr(widget, "_value_label")
        assert isinstance(widget._label_widget, QLabel)
        assert isinstance(widget._control_widget, QSlider)
        assert isinstance(widget._value_label, QLabel)

        # Check label text
        assert widget._label_widget.text() == "Test Slider"

        # Check displayed value
        assert widget._value_label.text() == "50"

    def test_should_have_correct_range_when_instantiated_with_custom_values(
        self, qt_application
    ):
        """Test slider properties."""
        widget = SettingSlider("Test Slider", min_val=10, max_val=100)

        # Check slider properties
        assert widget._control_widget.minimum() == 10
        assert widget._control_widget.maximum() == 100
        assert widget._control_widget.value() == 50

    def test_should_update_value_when_slider_value_is_set(self, qt_application):
        """Test value property."""
        widget = SettingSlider("Test Slider")

        # Check initial value
        assert widget.value == 50

        # Define a new value
        widget.value = 50
        assert widget._value == 50

    def test_should_get_and_set_slider_value_when_slider_methods_are_called(
        self, qt_application
    ):
        """Test get_value and set_value methods."""
        widget = SettingSlider("Test Slider")

        # Check get_value
        assert widget.get_value() == 50

        # Check set_value
        widget.set_value(50)
        assert widget.get_value() == 50

    def test_should_have_value_changed_signal_when_slider_is_instantiated(
        self, qt_application
    ):
        """Test signal."""
        widget = SettingSlider("Test Slider")

        # Check that the signal exists
        assert hasattr(widget, "valueChanged")
        assert isinstance(widget.valueChanged, Signal)


class TestSettingText:
    """Tests for the SettingText class."""

    def test_should_have_default_text_properties_when_instantiated(
        self, qt_application
    ):
        """Test initialization with default values."""
        widget = SettingText("Test Text")

        # Check basic properties
        assert widget._label_text == "Test Text"
        assert widget._description_text == ""
        assert widget._value == ""
        assert widget.objectName() == "setting_text_container"
        assert widget.property("type") == "setting_text"

    def test_should_use_given_default_when_default_text_is_given(self, qt_application):
        """Test initialization with a default value."""
        widget = SettingText("Test Text", default="Default Text")

        # Check default value
        assert widget._value == "Default Text"

    def test_should_have_label_and_line_edit_when_instantiated(self, qt_application):
        """Test user interface components."""
        widget = SettingText("Test Text")

        # Check that components exist
        assert hasattr(widget, "_label_widget")
        assert hasattr(widget, "_control_widget")
        assert isinstance(widget._label_widget, QLabel)
        assert isinstance(widget._control_widget, QLineEdit)

        # Check label text
        assert widget._label_widget.text() == "Test Text"

    def test_should_update_value_when_text_value_is_set(self, qt_application):
        """Test value property."""
        widget = SettingText("Test Text")

        # Check initial value
        assert widget.value == ""

        # Define a new value
        widget.value = "New Text"
        assert widget._value == "New Text"

    def test_should_get_and_set_text_value_when_text_methods_are_called(
        self, qt_application
    ):
        """Test get_value and set_value methods."""
        widget = SettingText("Test Text")

        # Check get_value
        assert widget.get_value() == ""

        # Check set_value
        widget.set_value("New Text")
        assert widget.get_value() == "New Text"

    def test_should_have_value_changed_signal_when_text_is_instantiated(
        self, qt_application
    ):
        """Test signal."""
        widget = SettingText("Test Text")

        # Check that the signal exists
        assert hasattr(widget, "valueChanged")
        assert isinstance(widget.valueChanged, Signal)


class TestSettingCheckbox:
    """Tests for the SettingCheckbox class."""

    def test_should_have_default_checkbox_properties_when_instantiated(
        self, qt_application
    ):
        """Test initialization with default values."""
        widget = SettingCheckbox("Test Checkbox")

        # Check basic properties
        assert widget._label_text == "Test Checkbox"
        assert widget._description_text == ""
        assert not widget._value
        assert widget.objectName() == "setting_checkbox_container"
        assert widget.property("type") == "setting_checkbox"

    def test_should_use_given_default_when_default_checkbox_value_is_given(
        self, qt_application
    ):
        """Test initialization with a default value."""
        widget = SettingCheckbox("Test Checkbox", default=True)

        # Check default value
        assert widget._value

    def test_should_have_label_and_checkbox_when_instantiated(self, qt_application):
        """Test user interface components."""
        widget = SettingCheckbox("Test Checkbox")

        # Check that components exist
        assert hasattr(widget, "_label_widget")
        assert hasattr(widget, "_control_widget")
        assert isinstance(widget._label_widget, QLabel)

        # Check label text
        assert widget._label_widget.text() == "Test Checkbox"

    def test_should_update_value_when_checkbox_value_is_set(self, qt_application):
        """Test value property."""
        widget = SettingCheckbox("Test Checkbox")

        # Check initial value
        assert not widget.value

        # Define a new value
        widget.value = True
        assert widget._value

    def test_should_get_and_set_checkbox_value_when_checkbox_methods_are_called(
        self, qt_application
    ):
        """Test get_value and set_value methods."""
        widget = SettingCheckbox("Test Checkbox")

        # Check get_value
        assert not widget.get_value()

        # Check set_value
        widget.set_value(True)
        assert widget.get_value()

    def test_should_have_value_changed_signal_when_checkbox_is_instantiated(
        self, qt_application
    ):
        """Test signal."""
        widget = SettingCheckbox("Test Checkbox")

        # Check that the signal exists
        assert hasattr(widget, "valueChanged")
        assert isinstance(widget.valueChanged, Signal)
