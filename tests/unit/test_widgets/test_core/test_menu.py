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

    def test_init_default_parameters(self, qt_application):
        """Test initialization with default parameters."""
        menu = Menu()

        # Check basic properties
        assert menu.objectName() == "menuContainer"
        assert menu.frameShape() == QFrame.NoFrame
        assert menu.frameShadow() == QFrame.Raised

        # Check default widths
        assert menu._shrink_width == 60
        assert menu._extended_width == 240

    def test_init_with_custom_widths(self, qt_application):
        """Test initialization with custom widths."""
        shrink_width = 80
        extended_width = 300

        menu = Menu(shrink_width=shrink_width, extended_width=extended_width)

        # Check that custom widths are used
        assert menu._shrink_width == shrink_width
        assert menu._extended_width == extended_width

        # Check that minimum width is set
        assert menu.minimumSize().width() == shrink_width

    def test_layout_structure(self, qt_application):
        """Test layout structure."""
        menu = Menu()

        # Check that main layout exists
        assert hasattr(menu, "VL_menuContainer")
        assert menu.VL_menuContainer is not None

        # Check layout properties
        assert menu.VL_menuContainer.spacing() == 0
        margins = menu.VL_menuContainer.contentsMargins()
        assert margins.left() == 0
        assert margins.top() == 0
        assert margins.right() == 0
        assert margins.bottom() == 0

    def test_main_menu_frame(self, qt_application):
        """Test main menu frame."""
        menu = Menu()

        # Check that main frame exists
        assert hasattr(menu, "mainMenuFrame")
        assert menu.mainMenuFrame is not None

        # Check frame properties
        assert menu.mainMenuFrame.objectName() == "mainMenuFrame"
        assert menu.mainMenuFrame.frameShape() == QFrame.NoFrame
        assert menu.mainMenuFrame.frameShadow() == QFrame.Raised

    def test_main_menu_layout(self, qt_application):
        """Test main menu layout."""
        menu = Menu()

        # Check that main layout exists
        assert hasattr(menu, "VL_mainMenuFrame")
        assert menu.VL_mainMenuFrame is not None

        # Check layout properties
        assert menu.VL_mainMenuFrame.spacing() == 0
        margins = menu.VL_mainMenuFrame.contentsMargins()
        assert margins.left() == 0
        assert margins.top() == 0
        assert margins.right() == 0
        assert margins.bottom() == 0

    def test_toggle_container(self, qt_application):
        """Test toggle container."""
        menu = Menu()

        # Check that toggle container exists
        assert hasattr(menu, "toggleBox")
        assert menu.toggleBox is not None

        # Check container properties
        assert menu.toggleBox.objectName() == "toggleBox"
        assert menu.toggleBox.frameShape() == QFrame.NoFrame
        assert menu.toggleBox.frameShadow() == QFrame.Raised

    def test_toggle_layout(self, qt_application):
        """Test toggle layout."""
        menu = Menu()

        # Check that toggle layout exists
        assert hasattr(menu, "VL_toggleBox")
        assert menu.VL_toggleBox is not None

        # Check layout properties
        assert menu.VL_toggleBox.spacing() == 0
        margins = menu.VL_toggleBox.contentsMargins()
        assert margins.left() == 0
        assert margins.top() == 0
        assert margins.right() == 0
        assert margins.bottom() == 0

    def test_toggle_button(self, qt_application):
        """Test toggle button."""
        menu = Menu()

        # Check that toggle button exists
        assert hasattr(menu, "toggleButton")
        assert menu.toggleButton is not None
        assert isinstance(menu.toggleButton, MenuButton)

        # Check button properties
        assert menu.toggleButton.objectName() == "toggleButton"

    def test_menu_dictionary(self, qt_application):
        """Test menu dictionary."""
        menu = Menu()

        # Check that menu dictionary exists
        assert hasattr(menu, "menus")
        assert isinstance(menu.menus, dict)

    def test_button_list_management(self, qt_application):
        """Test button list management."""
        menu = Menu()

        # Check that button list exists
        assert hasattr(menu, "_buttons")
        assert isinstance(menu._buttons, list)

    def test_icon_list_management(self, qt_application):
        """Test icon list management."""
        menu = Menu()

        # Check that icon list exists
        assert hasattr(menu, "_icons")
        assert isinstance(menu._icons, list)

    def test_size_constraints(self, qt_application):
        """Test size constraints."""
        menu = Menu()

        # Check size constraints
        assert menu.minimumSize().width() == 60
        assert menu.maximumSize().width() == 60
        assert menu.sizePolicy().horizontalPolicy() == QSizePolicy.Policy.Preferred
        assert menu.sizePolicy().verticalPolicy() == QSizePolicy.Policy.Preferred

    def test_toggle_button_properties(self, qt_application):
        """Test toggle button properties."""
        menu = Menu()

        # Check toggle button properties
        assert menu.toggleButton.objectName() == "toggleButton"
        assert menu.toggleButton.icon is not None
        assert menu.toggleButton.icon_size == QSize(20, 20)

    def test_toggle_button_signal(self, qt_application):
        """Test that toggle button emits signals."""
        menu = Menu()

        # Check that toggle button has signal
        assert hasattr(menu.toggleButton, "clicked")
        assert callable(menu.toggleButton.clicked)

    def test_menu_expansion_capability(self, qt_application):
        """Test menu expansion capability."""
        menu = Menu()

        # Check that menu can expand
        assert menu.get_extended_width() > menu.get_shrink_width()
        assert menu.maximumSize().width() == menu._shrink_width

    def test_menu_initial_state(self, qt_application):
        """Test menu initial state."""
        menu = Menu()

        # Check initial state
        assert menu.width() == menu._shrink_width
        assert menu.minimumSize().width() == menu._shrink_width

    def test_menu_with_different_widths(self, qt_application):
        """Test menu with different widths."""
        shrink_width = 50
        extended_width = 200

        menu = Menu(shrink_width=shrink_width, extended_width=extended_width)

        # Check that custom widths are applied
        assert menu._shrink_width == shrink_width
        assert menu._extended_width == extended_width
        assert menu.minimumSize().width() == shrink_width
        assert menu.maximumSize().width() == shrink_width

    def test_menu_frame_properties(self, qt_application):
        """Test menu frame properties."""
        menu = Menu()

        # Check that all frames have correct properties
        assert menu.frameShape() == QFrame.NoFrame
        assert menu.frameShadow() == QFrame.Raised
        assert menu.mainMenuFrame.frameShape() == QFrame.NoFrame
        assert menu.mainMenuFrame.frameShadow() == QFrame.Raised
        assert menu.toggleBox.frameShape() == QFrame.NoFrame
        assert menu.toggleBox.frameShadow() == QFrame.Raised

    def test_menu_layout_properties(self, qt_application):
        """Test menu layout properties."""
        menu = Menu()

        # Check that all layouts have correct properties
        assert menu.VL_menuContainer.spacing() == 0
        assert menu.VL_mainMenuFrame.spacing() == 0
        assert menu.VL_toggleBox.spacing() == 0

        margins = menu.VL_menuContainer.contentsMargins()
        assert margins.left() == 0
        assert margins.top() == 0
        assert margins.right() == 0
        assert margins.bottom() == 0

        margins = menu.VL_mainMenuFrame.contentsMargins()
        assert margins.left() == 0
        assert margins.top() == 0
        assert margins.right() == 0
        assert margins.bottom() == 0

        margins = menu.VL_toggleBox.contentsMargins()
        assert margins.left() == 0
        assert margins.top() == 0
        assert margins.right() == 0
        assert margins.bottom() == 0

    def test_menu_object_names(self, qt_application):
        """Test menu object names."""
        menu = Menu()

        # Check that all objects have correct names
        assert menu.objectName() == "menuContainer"
        assert menu.mainMenuFrame.objectName() == "mainMenuFrame"
        assert menu.toggleBox.objectName() == "toggleBox"
        assert menu.toggleButton.objectName() == "toggleButton"

    def test_menu_size_policy(self, qt_application):
        """Test menu size policy."""
        menu = Menu()

        # Check size policy
        assert menu.sizePolicy().horizontalPolicy() == QSizePolicy.Policy.Preferred
        assert menu.sizePolicy().verticalPolicy() == QSizePolicy.Policy.Preferred
