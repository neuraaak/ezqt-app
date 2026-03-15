# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_WIDGETS.TEST_CORE.TEST_CUSTOM_GRIPS - CustomGrip tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for the CustomGrip class and its internal structure."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSizeGrip, QWidget

from ezqt_app.utils.custom_grips import CustomGrip

# ///////////////////////////////////////////////////////////////
# HELPERS
# ///////////////////////////////////////////////////////////////


def _parent_widget(_qt_application) -> QWidget:
    parent = QWidget()
    parent.resize(400, 300)
    return parent


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////


class TestCustomGripCreation:
    """Tests for CustomGrip instantiation with each edge."""

    def test_should_create_grip_when_top_edge_is_given(self, qt_application) -> None:
        parent = _parent_widget(qt_application)
        grip = CustomGrip(parent, Qt.Edge.TopEdge)
        assert grip.objectName() == "custom_grip_topedge"
        assert hasattr(grip, "_container")
        assert grip._container.objectName() == "grip_container_top"

    def test_should_create_grip_when_bottom_edge_is_given(self, qt_application) -> None:
        parent = _parent_widget(qt_application)
        grip = CustomGrip(parent, Qt.Edge.BottomEdge)
        assert grip.objectName() == "custom_grip_bottomedge"
        assert hasattr(grip, "_container")
        assert grip._container.objectName() == "grip_container_bottom"

    def test_should_create_grip_when_left_edge_is_given(self, qt_application) -> None:
        parent = _parent_widget(qt_application)
        grip = CustomGrip(parent, Qt.Edge.LeftEdge)
        assert grip.objectName() == "custom_grip_leftedge"
        assert hasattr(grip, "_center_grip")
        assert grip._center_grip.objectName() == "grip_left"

    def test_should_create_grip_when_right_edge_is_given(self, qt_application) -> None:
        parent = _parent_widget(qt_application)
        grip = CustomGrip(parent, Qt.Edge.RightEdge)
        assert grip.objectName() == "custom_grip_rightedge"
        assert hasattr(grip, "_center_grip")
        assert grip._center_grip.objectName() == "grip_right"

    def test_should_store_parent_reference_when_instantiated(
        self, qt_application
    ) -> None:
        parent = _parent_widget(qt_application)
        grip = CustomGrip(parent, Qt.Edge.TopEdge)
        assert grip._parent is parent

    def test_should_have_protected_members_for_internal_frames(
        self, qt_application
    ) -> None:
        """Test that internal structure uses the new snake_case protected members."""
        parent = _parent_widget(qt_application)
        grip = CustomGrip(parent, Qt.Edge.TopEdge)

        # Check for top-specific frames
        assert hasattr(grip, "_left_frame")
        assert hasattr(grip, "_right_frame")
        assert hasattr(grip, "_center_grip")
        assert isinstance(grip._left_grip, QSizeGrip)
        assert isinstance(grip._right_grip, QSizeGrip)


class TestCustomGripGeometry:
    """Tests for geometry and resize logic."""

    def test_should_have_max_height_of_10_when_top_grip_is_created(
        self, qt_application
    ) -> None:
        parent = _parent_widget(qt_application)
        grip = CustomGrip(parent, Qt.Edge.TopEdge)
        assert grip.maximumHeight() == 10

    def test_should_update_container_geometry_when_resized(
        self, qt_application
    ) -> None:
        """Test that internal container follows the widget resize."""
        parent = _parent_widget(qt_application)
        grip = CustomGrip(parent, Qt.Edge.TopEdge)

        # Resize and manually trigger event processing for the test environment
        grip.resize(500, 10)
        from PySide6.QtCore import QSize
        from PySide6.QtGui import QResizeEvent

        event = QResizeEvent(QSize(500, 10), QSize(400, 10))
        grip.resizeEvent(event)

        assert grip._container.width() == 500

    def test_should_have_correct_cursors_for_top_corners(self, qt_application) -> None:
        """Test that resize cursors are correctly assigned."""
        parent = _parent_widget(qt_application)
        grip = CustomGrip(parent, Qt.Edge.TopEdge)

        assert grip._left_frame.cursor().shape() == Qt.CursorShape.SizeFDiagCursor
        assert grip._right_frame.cursor().shape() == Qt.CursorShape.SizeBDiagCursor
        assert grip._center_grip.cursor().shape() == Qt.CursorShape.SizeVerCursor
