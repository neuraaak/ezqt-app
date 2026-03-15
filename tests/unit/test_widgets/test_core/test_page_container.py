# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_WIDGETS.TEST_CORE.TEST_PAGE_CONTAINER - Page container tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for the PageContainer class."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Third-party imports
from PySide6.QtWidgets import QFrame, QSizePolicy, QStackedWidget, QWidget

# Local imports
from ezqt_app.widgets.core.page_container import PageContainer

# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////


class TestPageContainer:
    """Tests for the PageContainer class."""

    def test_should_have_pages_container_properties_when_instantiated(
        self, qt_application
    ):
        """Test initialization with default parameters."""
        container = PageContainer()

        # Check basic properties
        assert container.objectName() == "pages_container"
        assert container.frameShape() == QFrame.NoFrame
        assert container.frameShadow() == QFrame.Raised

    def test_should_accept_parent_when_parent_widget_is_given(self, qt_application):
        """Test initialization with parent."""
        parent = QWidget()
        container = PageContainer(parent=parent)

        # Check that parent is correctly defined
        assert container.parent() == parent

    def test_should_have_vertical_layout_when_instantiated(self, qt_application):
        """Test layout structure."""
        container = PageContainer()

        # Check that main layout exists
        assert hasattr(container, "_layout")
        assert container._layout is not None

        # Check layout properties
        assert container._layout.spacing() == 0
        margins = container._layout.contentsMargins()
        assert margins.left() == 10
        assert margins.top() == 10
        assert margins.right() == 10
        assert margins.bottom() == 10

    def test_should_have_stacked_widget_when_instantiated(self, qt_application):
        """Test stacked widget."""
        container = PageContainer()

        # Check that stacked widget exists
        assert hasattr(container, "_stacked_widget")
        assert container._stacked_widget is not None
        assert isinstance(container._stacked_widget, QStackedWidget)

        # Check stacked widget properties
        assert container._stacked_widget.objectName() == "pages_stacked_widget"
        assert container._stacked_widget.styleSheet() == "background: transparent;"

    def test_should_initialize_with_empty_pages_dict_when_instantiated(
        self, qt_application
    ):
        """Test pages dictionary."""
        container = PageContainer()

        # Check that pages dictionary exists
        assert hasattr(container, "pages")
        assert isinstance(container.pages, dict)

    def test_should_create_page_widget_when_add_page_is_called(self, qt_application):
        """Test adding a page."""
        container = PageContainer()

        # Add a page
        page_name = "test_page"
        page = container.add_page(page_name)

        # Check that page was created
        assert page is not None
        assert isinstance(page, QWidget)

        # Check that page was added to stacked widget
        assert page in container.get_stacked_widget().children()

        # Check that page was added to dictionary
        assert page_name in container.pages

    def test_should_create_all_pages_when_add_page_is_called_multiple_times(
        self, qt_application
    ):
        """Test adding multiple pages."""
        container = PageContainer()

        # Add multiple pages
        page_names = ["page1", "page2", "page3"]
        pages = []

        for name in page_names:
            page = container.add_page(name)
            pages.append(page)

        # Check that all pages were created
        assert len(pages) == 3
        for page in pages:
            assert page is not None
            assert isinstance(page, QWidget)

        # Check that all pages are in stacked widget
        for page in pages:
            assert page in container.get_stacked_widget().children()

        # Check that all pages are in dictionary
        for name in page_names:
            assert name in container.pages

    def test_should_assign_page_name_prefix_when_page_is_added(self, qt_application):
        """Test page object names."""
        container = PageContainer()

        # Add a page
        page_name = "test_page"
        page = container.add_page(page_name)

        # Check that object name is correct
        assert page.objectName() == f"page_{page_name}"

    def test_should_start_with_empty_stacked_widget_when_instantiated(
        self, qt_application
    ):
        """Test page container initial state."""
        container = PageContainer()

        # Check that container starts empty
        assert container.get_stacked_widget().count() == 0

    def test_should_be_independent_when_two_containers_are_created(
        self, qt_application
    ):
        """Test page container with existing pages."""
        # Create first container and add pages
        container1 = PageContainer()
        container1.add_page("page1")
        container1.add_page("page2")

        # Create second container
        container2 = PageContainer()

        # Each container owns its own page registry in v6.
        assert "page1" in container1.pages
        assert "page2" in container1.pages
        assert "page1" not in container2.pages
        assert "page2" not in container2.pages

        # Check that each container has its own pages in its stackedWidget.
        assert container1.get_stacked_widget().count() == 2
        assert container2.get_stacked_widget().count() == 0

    def test_should_accept_special_characters_when_page_name_has_hyphens(
        self, qt_application
    ):
        """Test adding page with special characters."""
        container = PageContainer()

        # Add page with special characters
        page_name = "test-page_with_underscores"
        page = container.add_page(page_name)

        # Check that page was created
        assert page is not None
        assert page_name in container.pages

    def test_should_accept_empty_string_when_page_name_is_empty(self, qt_application):
        """Test adding page with empty name."""
        container = PageContainer()

        # Add page with empty name
        page_name = ""
        page = container.add_page(page_name)

        # Check that page was created
        assert page is not None
        assert page_name in container.pages

    def test_should_accept_numeric_name_when_page_name_is_a_number(
        self, qt_application
    ):
        """Test adding page with numeric name."""
        container = PageContainer()

        # Add page with numeric name
        page_name = "123"
        page = container.add_page(page_name)

        # Check that page was created
        assert page is not None
        assert page_name in container.pages

    def test_should_have_10px_margins_when_instantiated(self, qt_application):
        """Test page container layout margins."""
        container = PageContainer()

        # Check layout margins
        margins = container._layout.contentsMargins()
        assert margins.left() == 10
        assert margins.top() == 10
        assert margins.right() == 10
        assert margins.bottom() == 10

    def test_should_have_zero_spacing_when_instantiated(self, qt_application):
        """Test page container layout spacing."""
        container = PageContainer()

        # Check layout spacing
        assert container._layout.spacing() == 0

    def test_should_have_transparent_background_when_stacked_widget_is_created(
        self, qt_application
    ):
        """Test stacked widget style."""
        container = PageContainer()

        # Check stacked widget style
        assert container.get_stacked_widget().styleSheet() == "background: transparent;"

    def test_should_have_no_frame_when_instantiated(self, qt_application):
        """Test page container frame properties."""
        container = PageContainer()

        # Check frame properties
        assert container.frameShape() == QFrame.NoFrame
        assert container.frameShadow() == QFrame.Raised

    def test_should_have_pages_container_object_name_when_instantiated(
        self, qt_application
    ):
        """Test page container object name."""
        container = PageContainer()

        # Check object name
        assert container.objectName() == "pages_container"

    def test_should_be_qframe_instance_when_instantiated(self, qt_application):
        """Test page container inheritance."""
        container = PageContainer()

        # Check inheritance
        assert isinstance(container, QFrame)

    def test_should_have_preferred_size_policy_when_instantiated(self, qt_application):
        """Test page container size policy."""
        container = PageContainer()

        # Check size policy
        assert container.sizePolicy().horizontalPolicy() == QSizePolicy.Policy.Preferred
        assert container.sizePolicy().verticalPolicy() == QSizePolicy.Policy.Preferred
