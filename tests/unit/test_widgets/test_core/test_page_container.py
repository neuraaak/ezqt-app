# ///////////////////////////////////////////////////////////////

"""
Unit tests for the PageContainer class.
"""

import os
import sys

# Add project path to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))

from PySide6.QtWidgets import QFrame, QSizePolicy, QStackedWidget, QWidget

# Direct import of module without going through main package
sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(__file__), "..", "..", "..", "..", "ezqt_app", "widgets", "core"
    ),
)
from ezqt_app.widgets.core.page_container import PageContainer


class TestPageContainer:
    """Tests for the PageContainer class."""

    def test_init_default_parameters(self, qt_application):
        """Test initialization with default parameters."""
        container = PageContainer()

        # Check basic properties
        assert container.objectName() == "pagesContainer"
        assert container.frameShape() == QFrame.NoFrame
        assert container.frameShadow() == QFrame.Raised

    def test_init_with_parent(self, qt_application):
        """Test initialization with parent."""
        parent = QWidget()
        container = PageContainer(parent=parent)

        # Check that parent is correctly defined
        assert container.parent() == parent

    def test_layout_structure(self, qt_application):
        """Test layout structure."""
        container = PageContainer()

        # Check that main layout exists
        assert hasattr(container, "VL_pagesContainer")
        assert container.VL_pagesContainer is not None

        # Check layout properties
        assert container.VL_pagesContainer.spacing() == 0
        margins = container.VL_pagesContainer.contentsMargins()
        assert margins.left() == 10
        assert margins.top() == 10
        assert margins.right() == 10
        assert margins.bottom() == 10

    def test_stacked_widget(self, qt_application):
        """Test stacked widget."""
        container = PageContainer()

        # Check that stacked widget exists
        assert hasattr(container, "stackedWidget")
        assert container.stackedWidget is not None
        assert isinstance(container.stackedWidget, QStackedWidget)

        # Check stacked widget properties
        assert container.stackedWidget.objectName() == "stackedWidget"
        assert container.stackedWidget.styleSheet() == "background: transparent;"

    def test_pages_dictionary(self, qt_application):
        """Test pages dictionary."""
        container = PageContainer()

        # Check that pages dictionary exists
        assert hasattr(container, "pages")
        assert isinstance(container.pages, dict)

    def test_add_page(self, qt_application):
        """Test adding a page."""
        container = PageContainer()

        # Add a page
        page_name = "test_page"
        page = container.add_page(page_name)

        # Check that page was created
        assert page is not None
        assert isinstance(page, QWidget)

        # Check that page was added to stacked widget
        assert page in container.stackedWidget.children()

        # Check that page was added to dictionary
        assert page_name in container.pages

    def test_add_multiple_pages(self, qt_application):
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
            assert page in container.stackedWidget.children()

        # Check that all pages are in dictionary
        for name in page_names:
            assert name in container.pages

    def test_page_object_names(self, qt_application):
        """Test page object names."""
        container = PageContainer()

        # Add a page
        page_name = "test_page"
        page = container.add_page(page_name)

        # Check that object name is correct
        assert page.objectName() == f"page_{page_name}"

    def test_page_container_initial_state(self, qt_application):
        """Test page container initial state."""
        container = PageContainer()

        # Check that container starts empty
        assert container.stackedWidget.count() == 0

    def test_page_container_with_existing_pages(self, qt_application):
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
        assert container1.stackedWidget.count() == 2
        assert container2.stackedWidget.count() == 0

    def test_add_page_with_special_characters(self, qt_application):
        """Test adding page with special characters."""
        container = PageContainer()

        # Add page with special characters
        page_name = "test-page_with_underscores"
        page = container.add_page(page_name)

        # Check that page was created
        assert page is not None
        assert page_name in container.pages

    def test_add_page_with_empty_name(self, qt_application):
        """Test adding page with empty name."""
        container = PageContainer()

        # Add page with empty name
        page_name = ""
        page = container.add_page(page_name)

        # Check that page was created
        assert page is not None
        assert page_name in container.pages

    def test_add_page_with_numeric_name(self, qt_application):
        """Test adding page with numeric name."""
        container = PageContainer()

        # Add page with numeric name
        page_name = "123"
        page = container.add_page(page_name)

        # Check that page was created
        assert page is not None
        assert page_name in container.pages

    def test_page_container_layout_margins(self, qt_application):
        """Test page container layout margins."""
        container = PageContainer()

        # Check layout margins
        margins = container.VL_pagesContainer.contentsMargins()
        assert margins.left() == 10
        assert margins.top() == 10
        assert margins.right() == 10
        assert margins.bottom() == 10

    def test_page_container_layout_spacing(self, qt_application):
        """Test page container layout spacing."""
        container = PageContainer()

        # Check layout spacing
        assert container.VL_pagesContainer.spacing() == 0

    def test_stacked_widget_style(self, qt_application):
        """Test stacked widget style."""
        container = PageContainer()

        # Check stacked widget style
        assert container.stackedWidget.styleSheet() == "background: transparent;"

    def test_page_container_frame_properties(self, qt_application):
        """Test page container frame properties."""
        container = PageContainer()

        # Check frame properties
        assert container.frameShape() == QFrame.NoFrame
        assert container.frameShadow() == QFrame.Raised

    def test_page_container_object_name(self, qt_application):
        """Test page container object name."""
        container = PageContainer()

        # Check object name
        assert container.objectName() == "pagesContainer"

    def test_page_container_inheritance(self, qt_application):
        """Test page container inheritance."""
        container = PageContainer()

        # Check inheritance
        assert isinstance(container, QFrame)

    def test_page_container_size_policy(self, qt_application):
        """Test page container size policy."""
        container = PageContainer()

        # Check size policy
        assert (
            container.sizePolicy().horizontalPolicy() == QSizePolicy.Policy.Preferred
        )
        assert (
            container.sizePolicy().verticalPolicy() == QSizePolicy.Policy.Preferred
        )
