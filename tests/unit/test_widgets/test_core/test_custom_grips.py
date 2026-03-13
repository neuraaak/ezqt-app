# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_WIDGETS.TEST_CORE.TEST_CUSTOM_GRIPS - CustomGrip tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for widgets/custom_grips/custom_grips.py."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

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
        assert grip is not None

    def test_should_create_grip_when_bottom_edge_is_given(self, qt_application) -> None:
        parent = _parent_widget(qt_application)
        grip = CustomGrip(parent, Qt.Edge.BottomEdge)
        assert grip is not None

    def test_should_create_grip_when_left_edge_is_given(self, qt_application) -> None:
        parent = _parent_widget(qt_application)
        grip = CustomGrip(parent, Qt.Edge.LeftEdge)
        assert grip is not None

    def test_should_create_grip_when_right_edge_is_given(self, qt_application) -> None:
        parent = _parent_widget(qt_application)
        grip = CustomGrip(parent, Qt.Edge.RightEdge)
        assert grip is not None

    def test_should_store_parent_reference_when_instantiated(
        self, qt_application
    ) -> None:
        parent = _parent_widget(qt_application)
        grip = CustomGrip(parent, Qt.Edge.TopEdge)
        assert grip._parent is parent

    def test_should_return_given_widget_as_parent_when_instantiated(
        self, qt_application
    ) -> None:
        parent = _parent_widget(qt_application)
        grip = CustomGrip(parent, Qt.Edge.BottomEdge)
        assert grip.parent() is parent


class TestCustomGripDisableColor:
    """Tests for the disable_color parameter."""

    def test_should_not_raise_when_top_grip_is_created_with_disable_color(
        self, qt_application
    ) -> None:
        parent = _parent_widget(qt_application)
        grip = CustomGrip(parent, Qt.Edge.TopEdge, disable_color=True)
        assert grip is not None

    def test_should_not_raise_when_bottom_grip_is_created_with_disable_color(
        self, qt_application
    ) -> None:
        parent = _parent_widget(qt_application)
        grip = CustomGrip(parent, Qt.Edge.BottomEdge, disable_color=True)
        assert grip is not None

    def test_should_not_raise_when_left_grip_is_created_with_disable_color(
        self, qt_application
    ) -> None:
        parent = _parent_widget(qt_application)
        grip = CustomGrip(parent, Qt.Edge.LeftEdge, disable_color=True)
        assert grip is not None

    def test_should_not_raise_when_right_grip_is_created_with_disable_color(
        self, qt_application
    ) -> None:
        parent = _parent_widget(qt_application)
        grip = CustomGrip(parent, Qt.Edge.RightEdge, disable_color=True)
        assert grip is not None


class TestCustomGripGeometry:
    """Tests for geometry set during initialization."""

    def test_should_have_max_height_of_10_when_top_grip_is_created(
        self, qt_application
    ) -> None:
        parent = _parent_widget(qt_application)
        grip = CustomGrip(parent, Qt.Edge.TopEdge)
        assert grip.maximumHeight() == 10

    def test_should_have_max_height_of_10_when_bottom_grip_is_created(
        self, qt_application
    ) -> None:
        parent = _parent_widget(qt_application)
        grip = CustomGrip(parent, Qt.Edge.BottomEdge)
        assert grip.maximumHeight() == 10

    def test_should_have_max_width_of_10_when_left_grip_is_created(
        self, qt_application
    ) -> None:
        parent = _parent_widget(qt_application)
        grip = CustomGrip(parent, Qt.Edge.LeftEdge)
        assert grip.maximumWidth() == 10

    def test_should_have_max_width_of_10_when_right_grip_is_created(
        self, qt_application
    ) -> None:
        parent = _parent_widget(qt_application)
        grip = CustomGrip(parent, Qt.Edge.RightEdge)
        assert grip.maximumWidth() == 10
