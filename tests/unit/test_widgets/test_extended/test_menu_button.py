# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_WIDGETS.TEST_EXTENDED.TEST_MENU_BUTTON - Menu button tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for the MenuButton class."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Third-party imports
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QLabel

# Local imports
from ezqt_app.widgets.extended.menu_button import MenuButton

# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////


class TestMenuButton:
    """Tests for the MenuButton class."""

    def test_should_have_default_properties_when_instantiated(self, qt_application):
        """Test initialization with default parameters."""
        button = MenuButton(text="Test Button")

        # Check basic properties
        assert button.property("type") == "MenuButton"
        assert button.text == "Test Button"
        assert button._is_extended is False  # Should start shrunk
        assert button.shrink_size == 60
        assert button.icon_size == QSize(20, 20)

    def test_should_have_protected_ui_components_when_instantiated(
        self, qt_application
    ):
        """Test that UI components are correctly initialized and protected."""
        button = MenuButton()

        assert hasattr(button, "_icon_label")
        assert hasattr(button, "_text_label")
        assert isinstance(button._icon_label, QLabel)
        assert isinstance(button._text_label, QLabel)
        assert button._icon_label.styleSheet() == "background-color: transparent;"

    def test_should_calculate_correct_icon_position_when_instantiated(
        self, qt_application
    ):
        """Test the mathematical calculation for icon centering."""
        shrink_size = 60
        icon_width = 20
        expected_pos = (shrink_size - icon_width) // 2

        button = MenuButton(shrink_size=shrink_size, icon_size=QSize(icon_width, 20))
        assert button._icon_x_position == expected_pos

    def test_should_update_text_label_when_text_property_is_set(self, qt_application):
        """Test text property and signal."""
        button = MenuButton()

        # Connect to signal
        received_text = []
        button.textChanged.connect(lambda t: received_text.append(t))

        button.text = "New Navigation"
        assert button._text_label.text() == "New Navigation"
        assert "New Navigation" in received_text

    def test_should_handle_state_change_when_set_state_is_called(self, qt_application):
        """Test transition between shrink and extended states."""
        button = MenuButton(text="Home")
        assert button._text_label.isHidden()

        # Switch to extended
        button.set_state(True)
        assert button.is_extended is True
        # Use isHidden() check instead of isVisible() for unit tests environment
        assert not button._text_label.isHidden()
        assert button.maximumWidth() == 16777215

        # Switch back to shrink
        button.set_state(False)
        assert button.is_extended is False
        assert button._text_label.isHidden()
        assert button.maximumWidth() == button.shrink_size

    def test_should_emit_state_changed_signal_when_state_changes(self, qt_application):
        """Test stateChanged signal."""
        button = MenuButton()
        states = []
        button.stateChanged.connect(lambda s: states.append(s))

        button.set_state(True)
        assert states == [True]

        button.set_state(False)
        assert states == [True, False]

    def test_should_update_margins_when_switching_states(self, qt_application):
        """Test that layout margins are adjusted for perfect centering."""
        button = MenuButton(shrink_size=60, icon_size=QSize(20, 20))
        layout = button.layout()

        # Shrink state margins (centered)
        button.set_state(False)
        margins = layout.contentsMargins()
        # (60 - 20) // 2 = 20
        assert margins.left() == 20
        assert margins.right() == 20

        # Extended state margins (fixed icon position)
        button.set_state(True)
        margins = layout.contentsMargins()
        assert margins.left() == button._icon_x_position
        assert margins.right() == 8

    def test_should_toggle_state_when_toggle_state_is_called(self, qt_application):
        """Test the toggle logic."""
        button = MenuButton()
        initial_state = button.is_extended

        button.toggle_state()
        assert button.is_extended != initial_state

        button.toggle_state()
        assert button.is_extended == initial_state

    def test_should_update_icon_size_and_recalculate_position(self, qt_application):
        """Test icon size change impact."""
        button = MenuButton(shrink_size=100, icon_size=QSize(20, 20))
        assert button._icon_x_position == 40  # (100-20)//2

        button.icon_size = QSize(40, 40)
        assert button._icon_x_position == 30  # (100-40)//2
        assert button.icon_size == QSize(40, 40)

    def test_should_have_minimum_size_hint_based_on_state(self, qt_application):
        """Test size hints for layout engine."""
        button = MenuButton(shrink_size=60, text="Very Long Menu Item Name")

        # Shrunk hint
        button.set_state(False)
        assert button.minimumSizeHint().width() == 60

        # Extended hint
        button.set_state(True)
        extended_width = button.minimumSizeHint().width()
        assert extended_width > 60
