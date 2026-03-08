# ///////////////////////////////////////////////////////////////

"""
Unit tests for extended setting widgets.
"""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox, QLabel, QLineEdit, QSlider

from ezqt_app.widgets.extended.setting_widgets import (
    BaseSettingWidget,
    SettingCheckbox,
    SettingSelect,
    SettingSlider,
    SettingText,
    SettingToggle,
)


class TestBaseSettingWidget:
    """Tests for the BaseSettingWidget class."""

    def test_init(self, qt_application):
        """Test initialization."""
        widget = BaseSettingWidget("Test Label", "Test Description")

        # Check basic properties
        assert widget._label == "Test Label"
        assert widget._description == "Test Description"
        assert widget._key is None
        assert widget.objectName() == "BaseSettingWidget"

    def test_set_key(self, qt_application):
        """Test key definition."""
        widget = BaseSettingWidget("Test Label")

        # Define a key
        widget.set_key("test_key")
        assert widget._key == "test_key"


class TestSettingToggle:
    """Tests for the SettingToggle class."""

    def test_init_default(self, qt_application):
        """Test initialization with default values."""
        widget = SettingToggle("Test Toggle")

        # Check basic properties
        assert widget._label == "Test Toggle"
        assert widget._description == ""
        assert not widget._value
        assert widget.objectName() == "SettingToggle"
        assert widget.property("type") == "SettingToggle"

    def test_init_with_description(self, qt_application):
        """Test initialization with description."""
        widget = SettingToggle("Test Toggle", "Test Description", True)

        # Check properties
        assert widget._label == "Test Toggle"
        assert widget._description == "Test Description"
        assert widget._value

    def test_ui_components(self, qt_application):
        """Test user interface components."""
        widget = SettingToggle("Test Toggle")

        # Check that components exist
        assert hasattr(widget, "label")
        assert hasattr(widget, "toggle")
        assert isinstance(widget.label, QLabel)

        # Check label text
        assert widget.label.text() == "Test Toggle"

    def test_toggle_value(self, qt_application):
        """Test toggle value."""
        widget = SettingToggle("Test Toggle", default=True)

        # Check initial value
        assert widget.value
        assert widget.get_value()

    def test_set_value(self, qt_application):
        """Test value definition."""
        widget = SettingToggle("Test Toggle")

        # Define a new value
        widget.value = True
        assert widget._value
        assert widget.value

    def test_signal(self, qt_application):
        """Test signal."""
        widget = SettingToggle("Test Toggle")

        # Check that the signal exists
        assert hasattr(widget, "valueChanged")
        assert isinstance(widget.valueChanged, Signal)


class TestSettingSelect:
    """Tests for the SettingSelect class."""

    def test_init_default(self, qt_application):
        """Test initialization with default values."""
        widget = SettingSelect("Test Select", options=["Option 1", "Option 2"])

        # Check basic properties
        assert widget._label == "Test Select"
        assert widget._description == ""
        assert widget._value == "Option 1"  # First option by default
        assert widget.objectName() == "SettingSelect"
        assert widget.property("type") == "SettingSelect"

    def test_init_with_default(self, qt_application):
        """Test initialization with a default value."""
        widget = SettingSelect(
            "Test Select", options=["Option 1", "Option 2"], default="Option 2"
        )

        # Check default value
        assert widget._value == "Option 2"

    def test_ui_components(self, qt_application):
        """Test user interface components."""
        widget = SettingSelect("Test Select", options=["Option 1", "Option 2"])

        # Check that components exist
        assert hasattr(widget, "label")
        assert hasattr(widget, "combo")
        assert isinstance(widget.label, QLabel)
        assert isinstance(widget.combo, QComboBox)

        # Check label text
        assert widget.label.text() == "Test Select"

        # Check combo options
        assert widget.combo.count() == 2
        assert widget.combo.itemText(0) == "Option 1"
        assert widget.combo.itemText(1) == "Option 2"

    def test_value_property(self, qt_application):
        """Test value property."""
        widget = SettingSelect("Test Select", options=["Option 1", "Option 2"])

        # Check initial value
        assert widget.value == "Option 1"

        # Define a new value
        widget.value = "Option 2"
        assert widget._value == "Option 2"

    def test_get_set_value(self, qt_application):
        """Test get_value and set_value methods."""
        widget = SettingSelect("Test Select", options=["Option 1", "Option 2"])

        # Check get_value
        assert widget.get_value() == "Option 1"

        # Check set_value
        widget.set_value("Option 2")
        assert widget.get_value() == "Option 2"

    def test_signal(self, qt_application):
        """Test signal."""
        widget = SettingSelect("Test Select", options=["Option 1", "Option 2"])

        # Check that the signal exists
        assert hasattr(widget, "valueChanged")
        assert isinstance(widget.valueChanged, Signal)


class TestSettingSlider:
    """Tests for the SettingSlider class."""

    def test_init_default(self, qt_application):
        """Test initialization with default values."""
        widget = SettingSlider("Test Slider")

        # Check basic properties
        assert widget._label == "Test Slider"
        assert widget._description == ""
        assert widget._value == 50
        assert widget.objectName() == "SettingSlider"
        assert widget.property("type") == "SettingSlider"

    def test_init_with_custom_values(self, qt_application):
        """Test initialization with custom values."""
        widget = SettingSlider("Test Slider", min_val=10, max_val=100, default=50)

        # Check custom values
        assert widget._value == 50

    def test_ui_components(self, qt_application):
        """Test user interface components."""
        widget = SettingSlider("Test Slider")

        # Check that components exist
        assert hasattr(widget, "label")
        assert hasattr(widget, "slider")
        assert hasattr(widget, "value_label")
        assert isinstance(widget.label, QLabel)
        assert isinstance(widget.slider, QSlider)
        assert isinstance(widget.value_label, QLabel)

        # Check label text
        assert widget.label.text() == "Test Slider"

        # Check displayed value
        assert widget.value_label.text() == "50"

    def test_slider_properties(self, qt_application):
        """Test slider properties."""
        widget = SettingSlider("Test Slider", min_val=10, max_val=100)

        # Check slider properties
        assert widget.slider.minimum() == 10
        assert widget.slider.maximum() == 100
        assert widget.slider.value() == 50

    def test_value_property(self, qt_application):
        """Test value property."""
        widget = SettingSlider("Test Slider")

        # Check initial value
        assert widget.value == 50

        # Define a new value
        widget.value = 50
        assert widget._value == 50

    def test_get_set_value(self, qt_application):
        """Test get_value and set_value methods."""
        widget = SettingSlider("Test Slider")

        # Check get_value
        assert widget.get_value() == 50

        # Check set_value
        widget.set_value(50)
        assert widget.get_value() == 50

    def test_signal(self, qt_application):
        """Test signal."""
        widget = SettingSlider("Test Slider")

        # Check that the signal exists
        assert hasattr(widget, "valueChanged")
        assert isinstance(widget.valueChanged, Signal)


class TestSettingText:
    """Tests for the SettingText class."""

    def test_init_default(self, qt_application):
        """Test initialization with default values."""
        widget = SettingText("Test Text")

        # Check basic properties
        assert widget._label == "Test Text"
        assert widget._description == ""
        assert widget._value == ""
        assert widget.objectName() == "SettingText"
        assert widget.property("type") == "SettingText"

    def test_init_with_default(self, qt_application):
        """Test initialization with a default value."""
        widget = SettingText("Test Text", default="Default Text")

        # Check default value
        assert widget._value == "Default Text"

    def test_ui_components(self, qt_application):
        """Test user interface components."""
        widget = SettingText("Test Text")

        # Check that components exist
        assert hasattr(widget, "label")
        assert hasattr(widget, "text_edit")
        assert isinstance(widget.label, QLabel)
        assert isinstance(widget.text_edit, QLineEdit)

        # Check label text
        assert widget.label.text() == "Test Text"

    def test_value_property(self, qt_application):
        """Test value property."""
        widget = SettingText("Test Text")

        # Check initial value
        assert widget.value == ""

        # Define a new value
        widget.value = "New Text"
        assert widget._value == "New Text"

    def test_get_set_value(self, qt_application):
        """Test get_value and set_value methods."""
        widget = SettingText("Test Text")

        # Check get_value
        assert widget.get_value() == ""

        # Check set_value
        widget.set_value("New Text")
        assert widget.get_value() == "New Text"

    def test_signal(self, qt_application):
        """Test signal."""
        widget = SettingText("Test Text")

        # Check that the signal exists
        assert hasattr(widget, "valueChanged")
        assert isinstance(widget.valueChanged, Signal)


class TestSettingCheckbox:
    """Tests for the SettingCheckbox class."""

    def test_init_default(self, qt_application):
        """Test initialization with default values."""
        widget = SettingCheckbox("Test Checkbox")

        # Check basic properties
        assert widget._label == "Test Checkbox"
        assert widget._description == ""
        assert not widget._value
        assert widget.objectName() == "SettingCheckbox"
        assert widget.property("type") == "SettingCheckbox"

    def test_init_with_default(self, qt_application):
        """Test initialization with a default value."""
        widget = SettingCheckbox("Test Checkbox", default=True)

        # Check default value
        assert widget._value

    def test_ui_components(self, qt_application):
        """Test user interface components."""
        widget = SettingCheckbox("Test Checkbox")

        # Check that components exist
        assert hasattr(widget, "label")
        assert hasattr(widget, "checkbox")
        assert isinstance(widget.label, QLabel)

        # Check label text
        assert widget.label.text() == "Test Checkbox"

    def test_value_property(self, qt_application):
        """Test value property."""
        widget = SettingCheckbox("Test Checkbox")

        # Check initial value
        assert not widget.value

        # Define a new value
        widget.value = True
        assert widget._value

    def test_get_set_value(self, qt_application):
        """Test get_value and set_value methods."""
        widget = SettingCheckbox("Test Checkbox")

        # Check get_value
        assert not widget.get_value()

        # Check set_value
        widget.set_value(True)
        assert widget.get_value()

    def test_signal(self, qt_application):
        """Test signal."""
        widget = SettingCheckbox("Test Checkbox")

        # Check that the signal exists
        assert hasattr(widget, "valueChanged")
        assert isinstance(widget.valueChanged, Signal)
