# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_WIDGETS.TEST_CORE.TEST_MENU - Menu widget tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for the Menu class."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Third-party imports
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QFrame, QSizePolicy

# Local imports
from ezqt_app.widgets.core.menu import Menu
from ezqt_app.widgets.extended.menu_button import MenuButton

# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////


class TestMenu:
    """Tests for the Menu class."""

    def test_should_have_default_menu_properties_when_instantiated(
        self, qt_application
    ):
        """Test initialization with default parameters."""
        menu = Menu()

        # Check basic properties
        assert menu.objectName() == "menu_container"
        assert menu.frameShape() == QFrame.NoFrame
        assert menu.frameShadow() == QFrame.Raised

        # Check default widths
        assert menu._shrink_width == 60
        assert menu._extended_width == 240

    def test_should_use_custom_widths_when_shrink_and_extended_widths_are_given(
        self, qt_application
    ):
        """Test initialization with custom widths."""
        shrink_width = 80
        extended_width = 300

        menu = Menu(shrink_width=shrink_width, extended_width=extended_width)

        # Check that custom widths are used
        assert menu._shrink_width == shrink_width
        assert menu._extended_width == extended_width

        # Check that minimum width is set
        assert menu.minimumSize().width() == shrink_width

    def test_should_have_vertical_layout_when_instantiated(self, qt_application):
        """Test layout structure."""
        menu = Menu()

        # Check that main layout exists
        assert hasattr(menu, "_menu_layout")
        assert menu._menu_layout is not None

        # Check layout properties
        assert menu._menu_layout.spacing() == 0
        margins = menu._menu_layout.contentsMargins()
        assert margins.left() == 0
        assert margins.top() == 0
        assert margins.right() == 0
        assert margins.bottom() == 0

    def test_should_have_main_menu_frame_when_instantiated(self, qt_application):
        """Test main menu frame."""
        menu = Menu()

        # Check that main frame exists
        assert hasattr(menu, "_main_menu_frame")
        assert menu._main_menu_frame is not None

        # Check frame properties
        assert menu._main_menu_frame.objectName() == "main_menu_frame"
        assert menu._main_menu_frame.frameShape() == QFrame.NoFrame
        assert menu._main_menu_frame.frameShadow() == QFrame.Raised

    def test_should_have_main_menu_layout_when_instantiated(self, qt_application):
        """Test main menu layout."""
        menu = Menu()

        # Check that main layout exists
        assert hasattr(menu, "_main_menu_layout")
        assert menu._main_menu_layout is not None

        # Check layout properties
        assert menu._main_menu_layout.spacing() == 0
        margins = menu._main_menu_layout.contentsMargins()
        assert margins.left() == 0
        assert margins.top() == 0
        assert margins.right() == 0
        assert margins.bottom() == 0

    def test_should_have_toggle_container_when_instantiated(self, qt_application):
        """Test toggle container."""
        menu = Menu()

        # Check that toggle container exists
        assert hasattr(menu, "_toggle_container")
        assert menu._toggle_container is not None

        # Check container properties
        assert menu._toggle_container.objectName() == "toggle_container"
        assert menu._toggle_container.frameShape() == QFrame.NoFrame
        assert menu._toggle_container.frameShadow() == QFrame.Raised

    def test_should_have_toggle_layout_when_instantiated(self, qt_application):
        """Test toggle layout."""
        menu = Menu()

        # Check that toggle layout exists
        assert hasattr(menu, "_toggle_layout")
        assert menu._toggle_layout is not None

        # Check layout properties
        assert menu._toggle_layout.spacing() == 0
        margins = menu._toggle_layout.contentsMargins()
        assert margins.left() == 0
        assert margins.top() == 0
        assert margins.right() == 0
        assert margins.bottom() == 0

    def test_should_have_toggle_button_when_instantiated(self, qt_application):
        """Test toggle button."""
        menu = Menu()

        # Check that toggle button exists
        assert hasattr(menu, "toggle_button")
        assert menu.toggle_button is not None
        assert isinstance(menu.toggle_button, MenuButton)

        # Check button properties
        assert menu.toggle_button.objectName() == "toggle_button"

    def test_should_initialize_with_empty_menus_dict_when_instantiated(
        self, qt_application
    ):
        """Test menu dictionary."""
        menu = Menu()

        # Check that menu dictionary exists
        assert hasattr(menu, "menus")
        assert isinstance(menu.menus, dict)

    def test_should_initialize_with_empty_button_list_when_instantiated(
        self, qt_application
    ):
        """Test button list management."""
        menu = Menu()

        # Check that button list exists
        assert hasattr(menu, "_buttons")
        assert isinstance(menu._buttons, list)

    def test_should_initialize_with_empty_icon_list_when_instantiated(
        self, qt_application
    ):
        """Test icon list management."""
        menu = Menu()

        # Check that icon list exists
        assert hasattr(menu, "_icons")
        assert isinstance(menu._icons, list)

    def test_should_have_shrink_width_as_size_constraint_when_instantiated(
        self, qt_application
    ):
        """Test size constraints."""
        menu = Menu()

        # Check size constraints
        assert menu.minimumSize().width() == 60
        assert menu.maximumSize().width() == 60
        assert menu.sizePolicy().horizontalPolicy() == QSizePolicy.Policy.Preferred
        assert menu.sizePolicy().verticalPolicy() == QSizePolicy.Policy.Preferred

    def test_should_have_toggle_button_with_icon_when_instantiated(
        self, qt_application
    ):
        """Test toggle button properties."""
        menu = Menu()

        # Check toggle button properties
        assert menu.toggle_button.objectName() == "toggle_button"
        assert menu.toggle_button.icon is not None
        assert menu.toggle_button.icon_size == QSize(20, 20)

    def test_should_expose_clicked_signal_on_toggle_button_when_instantiated(
        self, qt_application
    ):
        """Test that toggle button emits signals."""
        menu = Menu()

        # Check that toggle button has signal
        assert hasattr(menu.toggle_button, "clicked")
        assert callable(menu.toggle_button.clicked)

    def test_should_have_extended_width_greater_than_shrink_width_when_instantiated(
        self, qt_application
    ):
        """Test menu expansion capability."""
        menu = Menu()

        # Check that menu can expand
        assert menu.get_extended_width() > menu.get_shrink_width()
        assert menu.maximumSize().width() == menu._shrink_width

    def test_should_start_at_shrink_width_when_instantiated(self, qt_application):
        """Test menu initial state."""
        menu = Menu()

        # Check initial state
        assert menu.width() == menu._shrink_width
        assert menu.minimumSize().width() == menu._shrink_width

    def test_should_apply_custom_widths_when_different_widths_are_provided(
        self, qt_application
    ):
        """Test menu with different widths."""
        shrink_width = 50
        extended_width = 200

        menu = Menu(shrink_width=shrink_width, extended_width=extended_width)

        # Check that custom widths are applied
        assert menu._shrink_width == shrink_width
        assert menu._extended_width == extended_width
        assert menu.minimumSize().width() == shrink_width
        assert menu.maximumSize().width() == shrink_width

    def test_should_have_no_frame_on_all_frames_when_instantiated(self, qt_application):
        """Test menu frame properties."""
        menu = Menu()

        # Check that all frames have correct properties
        assert menu.frameShape() == QFrame.NoFrame
        assert menu.frameShadow() == QFrame.Raised
        assert menu._main_menu_frame.frameShape() == QFrame.NoFrame
        assert menu._main_menu_frame.frameShadow() == QFrame.Raised
        assert menu._toggle_container.frameShape() == QFrame.NoFrame
        assert menu._toggle_container.frameShadow() == QFrame.Raised

    def test_should_have_zero_spacing_and_margins_on_all_layouts_when_instantiated(
        self, qt_application
    ):
        """Test menu layout properties."""
        menu = Menu()

        # Check that all layouts have correct properties
        assert menu._menu_layout.spacing() == 0
        assert menu._main_menu_layout.spacing() == 0
        assert menu._toggle_layout.spacing() == 0

        margins = menu._menu_layout.contentsMargins()
        assert margins.left() == 0
        assert margins.top() == 0
        assert margins.right() == 0
        assert margins.bottom() == 0

        margins = menu._main_menu_layout.contentsMargins()
        assert margins.left() == 0
        assert margins.top() == 0
        assert margins.right() == 0
        assert margins.bottom() == 0

        margins = menu._toggle_layout.contentsMargins()
        assert margins.left() == 0
        assert margins.top() == 0
        assert margins.right() == 0
        assert margins.bottom() == 0

    def test_should_have_correct_object_names_when_instantiated(self, qt_application):
        """Test menu object names."""
        menu = Menu()

        # Check that all objects have correct names
        assert menu.objectName() == "menu_container"
        assert menu._main_menu_frame.objectName() == "main_menu_frame"
        assert menu._toggle_container.objectName() == "toggle_container"
        assert menu.toggle_button.objectName() == "toggle_button"

    def test_should_have_preferred_size_policy_when_instantiated(self, qt_application):
        """Test menu size policy."""
        menu = Menu()

        # Check size policy
        assert menu.sizePolicy().horizontalPolicy() == QSizePolicy.Policy.Preferred
        assert menu.sizePolicy().verticalPolicy() == QSizePolicy.Policy.Preferred
