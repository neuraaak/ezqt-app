# ///////////////////////////////////////////////////////////////
# WIDGETS.CUSTOM_GRIPS.CUSTOM_GRIPS - Custom resize grip widgets
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""CustomGrip — window resize handles for frameless windows."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from typing import Any

# Third-party imports
from PySide6.QtCore import QRect, QSize, Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QFrame, QHBoxLayout, QSizeGrip, QWidget


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class CustomGrip(QWidget):
    """
    Custom resize widget for windows.

    This class provides custom resize handles
    for different window edges (top, bottom, left, right).
    Each handle allows resizing the parent window.
    """

    def __init__(
        self, parent: QWidget, position: Qt.Edge, disable_color: bool = False
    ) -> None:
        """
        Initialize the resize handle.

        Parameters
        ----------
        parent : QWidget
            The parent widget to resize.
        position : Qt.Edge
            The position of the handle (Qt.Edge.TopEdge, Qt.Edge.BottomEdge, etc.).
        disable_color : bool, optional
            Disable handle colors (default: False).
        """
        # ////// SETUP UI
        super().__init__()
        self._parent: QWidget = parent
        self.setParent(parent)
        self.wi = Widgets()

        # ////// SHOW TOP GRIP
        if position == Qt.Edge.TopEdge:
            self.wi.top(self)
            self.setGeometry(0, 0, self._parent.width(), 10)
            self.setMaximumHeight(10)

            # ////// SETUP GRIPS
            _ = QSizeGrip(self.wi.top_left)
            _ = QSizeGrip(self.wi.top_right)

            # ////// RESIZE TOP FUNCTION
            def resize_top(event: Any) -> None:
                delta = event.pos()
                height = max(
                    self._parent.minimumHeight(), self._parent.height() - delta.y()
                )
                geo = self._parent.geometry()
                geo.setTop(geo.bottom() - height)
                self._parent.setGeometry(geo)
                event.accept()

            self.wi.top_center.mouseMoveEvent = resize_top  # type: ignore[method-assign]

            # ////// ENABLE COLOR
            if disable_color:
                self.wi.top_left.setStyleSheet("background: transparent")
                self.wi.top_right.setStyleSheet("background: transparent")
                self.wi.top_center.setStyleSheet("background: transparent")

        # ////// SHOW BOTTOM GRIP
        elif position == Qt.Edge.BottomEdge:
            self.wi.bottom(self)
            self.setGeometry(0, self._parent.height() - 10, self._parent.width(), 10)
            self.setMaximumHeight(10)

            # ////// SETUP GRIPS
            self.bottom_left = QSizeGrip(self.wi.bottom_left)
            self.bottom_right = QSizeGrip(self.wi.bottom_right)

            # ////// RESIZE BOTTOM FUNCTION
            def resize_bottom(event: Any) -> None:
                delta = event.pos()
                height = max(
                    self._parent.minimumHeight(), self._parent.height() + delta.y()
                )
                self._parent.resize(self._parent.width(), height)
                event.accept()

            self.wi.bottom_center.mouseMoveEvent = resize_bottom  # type: ignore[method-assign]

            # ////// ENABLE COLOR
            if disable_color:
                self.wi.bottom_left.setStyleSheet("background: transparent")
                self.wi.bottom_right.setStyleSheet("background: transparent")
                self.wi.bottom_center.setStyleSheet("background: transparent")

        # ////// SHOW LEFT GRIP
        elif position == Qt.Edge.LeftEdge:
            self.wi.left(self)
            self.setGeometry(0, 10, 10, self._parent.height() - 20)
            self.setMaximumWidth(10)

            # ////// RESIZE LEFT FUNCTION
            def resize_left(event: Any) -> None:
                delta = event.pos()
                width = max(
                    self._parent.minimumWidth(), self._parent.width() - delta.x()
                )
                geo = self._parent.geometry()
                geo.setLeft(geo.right() - width)
                self._parent.setGeometry(geo)
                event.accept()

            self.wi.leftgrip.mouseMoveEvent = resize_left  # type: ignore[method-assign]

            # ////// ENABLE COLOR
            if disable_color:
                self.wi.leftgrip.setStyleSheet("background: transparent")

        # ////// SHOW RIGHT GRIP
        elif position == Qt.Edge.RightEdge:
            self.wi.right(self)
            self.setGeometry(
                self._parent.width() - 10, 10, 10, self._parent.height() - 20
            )
            self.setMaximumWidth(10)

            # ////// RESIZE RIGHT FUNCTION
            def resize_right(event: Any) -> None:
                delta = event.pos()
                width = max(self._parent.minimumWidth(), delta.x())
                geo = self._parent.geometry()
                geo.setWidth(width)
                self._parent.setGeometry(geo)
                event.accept()

            self.wi.rightgrip.mouseMoveEvent = resize_right  # type: ignore[method-assign]

            # ////// ENABLE COLOR
            if disable_color:
                self.wi.rightgrip.setStyleSheet("background: transparent")

    # ///////////////////////////////////////////////////////////////
    # EVENT FUNCTIONS

    def mouseReleaseEvent(self, event: Any) -> None:  # noqa: ARG002
        """Handle mouse release event."""
        self.mousePos = None

    def resizeEvent(self, event: Any) -> None:  # noqa: ARG002
        """Handle resize event."""
        if hasattr(self.wi, "container_top"):
            self.wi.container_top.setGeometry(0, 0, self.width(), 10)

        elif hasattr(self.wi, "container_bottom"):
            self.wi.container_bottom.setGeometry(0, 0, self.width(), 10)

        elif hasattr(self.wi, "leftgrip"):
            self.wi.leftgrip.setGeometry(0, 0, 10, self.height() - 20)

        elif hasattr(self.wi, "rightgrip"):
            self.wi.rightgrip.setGeometry(0, 0, 10, self.height() - 20)


# ///////////////////////////////////////////////////////////////
class Widgets:
    """
    Utility class for creating resize handle widgets.

    This class provides methods to create different types
    of handles (top, bottom, left, right) with their layouts and styles.
    """

    def top(self, Form: QWidget) -> None:
        """
        Create a resize handle for the top edge.

        Parameters
        ----------
        Form : QWidget
            The parent widget for the handle.
        """
        if not Form.objectName():
            Form.setObjectName("Form")

        # ////// SETUP CONTAINER
        self.container_top = QFrame(Form)
        self.container_top.setObjectName("container_top")
        self.container_top.setGeometry(QRect(0, 0, 500, 10))
        self.container_top.setMinimumSize(QSize(0, 10))
        self.container_top.setMaximumSize(QSize(16777215, 10))
        self.container_top.setFrameShape(QFrame.Shape.NoFrame)
        self.container_top.setFrameShadow(QFrame.Shadow.Raised)

        # ////// SETUP LAYOUT
        self.top_layout = QHBoxLayout(self.container_top)
        self.top_layout.setSpacing(0)
        self.top_layout.setObjectName("top_layout")
        self.top_layout.setContentsMargins(0, 0, 0, 0)

        # ////// SETUP TOP LEFT GRIP
        self.top_left = QFrame(self.container_top)
        self.top_left.setObjectName("top_left")
        self.top_left.setMinimumSize(QSize(10, 10))
        self.top_left.setMaximumSize(QSize(10, 10))
        self.top_left.setCursor(QCursor(Qt.CursorShape.SizeFDiagCursor))
        self.top_left.setStyleSheet("background-color: rgb(33, 37, 43);")
        self.top_left.setFrameShape(QFrame.Shape.NoFrame)
        self.top_left.setFrameShadow(QFrame.Shadow.Raised)
        self.top_layout.addWidget(self.top_left)

        # ////// SETUP TOP CENTER GRIP
        self.top_center = QFrame(self.container_top)
        self.top_center.setObjectName("top")
        self.top_center.setCursor(QCursor(Qt.CursorShape.SizeVerCursor))
        self.top_center.setStyleSheet("background-color: rgb(85, 255, 255);")
        self.top_center.setFrameShape(QFrame.Shape.NoFrame)
        self.top_center.setFrameShadow(QFrame.Shadow.Raised)
        self.top_layout.addWidget(self.top_center)

        # ////// SETUP TOP RIGHT GRIP
        self.top_right = QFrame(self.container_top)
        self.top_right.setObjectName("top_right")
        self.top_right.setMinimumSize(QSize(10, 10))
        self.top_right.setMaximumSize(QSize(10, 10))
        self.top_right.setCursor(QCursor(Qt.CursorShape.SizeBDiagCursor))
        self.top_right.setStyleSheet("background-color: rgb(33, 37, 43);")
        self.top_right.setFrameShape(QFrame.Shape.NoFrame)
        self.top_right.setFrameShadow(QFrame.Shadow.Raised)
        self.top_layout.addWidget(self.top_right)

    def bottom(self, Form: QWidget) -> None:
        """
        Create a resize handle for the bottom edge.

        Parameters
        ----------
        Form : QWidget
            The parent widget for the handle.
        """
        if not Form.objectName():
            Form.setObjectName("Form")

        # ////// SETUP CONTAINER
        self.container_bottom = QFrame(Form)
        self.container_bottom.setObjectName("container_bottom")
        self.container_bottom.setGeometry(QRect(0, 0, 500, 10))
        self.container_bottom.setMinimumSize(QSize(0, 10))
        self.container_bottom.setMaximumSize(QSize(16777215, 10))
        self.container_bottom.setFrameShape(QFrame.Shape.NoFrame)
        self.container_bottom.setFrameShadow(QFrame.Shadow.Raised)

        # ////// SETUP LAYOUT
        self.bottom_layout = QHBoxLayout(self.container_bottom)
        self.bottom_layout.setSpacing(0)
        self.bottom_layout.setObjectName("bottom_layout")
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)

        # ////// SETUP BOTTOM LEFT GRIP
        self.bottom_left = QFrame(self.container_bottom)
        self.bottom_left.setObjectName("bottom_left")
        self.bottom_left.setMinimumSize(QSize(10, 10))
        self.bottom_left.setMaximumSize(QSize(10, 10))
        self.bottom_left.setCursor(QCursor(Qt.CursorShape.SizeBDiagCursor))
        self.bottom_left.setStyleSheet("background-color: rgb(33, 37, 43);")
        self.bottom_left.setFrameShape(QFrame.Shape.NoFrame)
        self.bottom_left.setFrameShadow(QFrame.Shadow.Raised)
        self.bottom_layout.addWidget(self.bottom_left)

        # ////// SETUP BOTTOM CENTER GRIP
        self.bottom_center = QFrame(self.container_bottom)
        self.bottom_center.setObjectName("bottom")
        self.bottom_center.setCursor(QCursor(Qt.CursorShape.SizeVerCursor))
        self.bottom_center.setStyleSheet("background-color: rgb(85, 170, 0);")
        self.bottom_center.setFrameShape(QFrame.Shape.NoFrame)
        self.bottom_center.setFrameShadow(QFrame.Shadow.Raised)
        self.bottom_layout.addWidget(self.bottom_center)

        # ////// SETUP BOTTOM RIGHT GRIP
        self.bottom_right = QFrame(self.container_bottom)
        self.bottom_right.setObjectName("bottom_right")
        self.bottom_right.setMinimumSize(QSize(10, 10))
        self.bottom_right.setMaximumSize(QSize(10, 10))
        self.bottom_right.setCursor(QCursor(Qt.CursorShape.SizeFDiagCursor))
        self.bottom_right.setStyleSheet("background-color: rgb(33, 37, 43);")
        self.bottom_right.setFrameShape(QFrame.Shape.NoFrame)
        self.bottom_right.setFrameShadow(QFrame.Shadow.Raised)
        self.bottom_layout.addWidget(self.bottom_right)

    def left(self, Form: QWidget) -> None:
        """
        Create a resize handle for the left edge.

        Parameters
        ----------
        Form : QWidget
            The parent widget for the handle.
        """
        if not Form.objectName():
            Form.setObjectName("Form")

        # ////// SETUP LEFT GRIP
        self.leftgrip = QFrame(Form)
        self.leftgrip.setObjectName("left")
        self.leftgrip.setGeometry(QRect(0, 10, 10, 480))
        self.leftgrip.setMinimumSize(QSize(10, 0))
        self.leftgrip.setCursor(QCursor(Qt.CursorShape.SizeHorCursor))
        self.leftgrip.setStyleSheet("background-color: rgb(255, 121, 198);")
        self.leftgrip.setFrameShape(QFrame.Shape.NoFrame)
        self.leftgrip.setFrameShadow(QFrame.Shadow.Raised)

    def right(self, Form: QWidget) -> None:
        """
        Create a resize handle for the right edge.

        Parameters
        ----------
        Form : QWidget
            The parent widget for the handle.
        """
        if not Form.objectName():
            Form.setObjectName("Form")
        Form.resize(500, 500)

        # ////// SETUP RIGHT GRIP
        self.rightgrip = QFrame(Form)
        self.rightgrip.setObjectName("right")
        self.rightgrip.setGeometry(QRect(0, 0, 10, 500))
        self.rightgrip.setMinimumSize(QSize(10, 0))
        self.rightgrip.setCursor(QCursor(Qt.CursorShape.SizeHorCursor))
        self.rightgrip.setStyleSheet("background-color: rgb(255, 0, 127);")
        self.rightgrip.setFrameShape(QFrame.Shape.NoFrame)
        self.rightgrip.setFrameShadow(QFrame.Shadow.Raised)


# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////
__all__ = ["CustomGrip"]
