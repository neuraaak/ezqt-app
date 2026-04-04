# ///////////////////////////////////////////////////////////////
# UTILS.CUSTOM_GRIPS - Custom resize grip widgets
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
from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QCursor, QMouseEvent
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
        super().__init__(parent)
        self._parent = parent
        self._position = position
        self._disable_color = disable_color

        # Initialize internal members
        self._container = None
        self._left_grip = None
        self._right_grip = None
        self._center_grip = None

        self.setObjectName(f"custom_grip_{str(position).split('.')[-1].lower()}")
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Configure the user interface based on position."""
        if self._position == Qt.Edge.TopEdge:
            self._setup_top_grip()
        elif self._position == Qt.Edge.BottomEdge:
            self._setup_bottom_grip()
        elif self._position == Qt.Edge.LeftEdge:
            self._setup_left_grip()
        elif self._position == Qt.Edge.RightEdge:
            self._setup_right_grip()

    def _setup_top_grip(self) -> None:
        """Configure the handle for the top edge."""
        self.setGeometry(0, 0, self._parent.width(), 10)
        self.setMaximumHeight(10)

        self._container = QFrame(self)
        self._container.setObjectName("grip_container_top")
        self._container.setGeometry(QRect(0, 0, self._parent.width(), 10))
        self._container.setFrameShape(QFrame.Shape.NoFrame)
        self._container.setFrameShadow(QFrame.Shadow.Raised)

        layout = QHBoxLayout(self._container)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # Top Left
        self._left_frame = QFrame(self._container)
        self._left_frame.setObjectName("grip_top_left")
        self._left_frame.setFixedSize(10, 10)
        self._left_frame.setCursor(QCursor(Qt.CursorShape.SizeFDiagCursor))
        self._left_grip = QSizeGrip(self._left_frame)
        layout.addWidget(self._left_frame)

        # Top Center
        self._center_grip = QFrame(self._container)
        self._center_grip.setObjectName("grip_top_center")
        self._center_grip.setCursor(QCursor(Qt.CursorShape.SizeVerCursor))
        self._center_grip.mouseMoveEvent = self._resize_top  # type: ignore
        layout.addWidget(self._center_grip)

        # Top Right
        self._right_frame = QFrame(self._container)
        self._right_frame.setObjectName("grip_top_right")
        self._right_frame.setFixedSize(10, 10)
        self._right_frame.setCursor(QCursor(Qt.CursorShape.SizeBDiagCursor))
        self._right_grip = QSizeGrip(self._right_frame)
        layout.addWidget(self._right_frame)

        if self._disable_color:
            self._container.setStyleSheet("background: transparent")
            self._left_frame.setStyleSheet("background: transparent")
            self._right_frame.setStyleSheet("background: transparent")
            self._center_grip.setStyleSheet("background: transparent")

    def _setup_bottom_grip(self) -> None:
        """Configure the handle for the bottom edge."""
        self.setGeometry(0, self._parent.height() - 10, self._parent.width(), 10)
        self.setMaximumHeight(10)

        self._container = QFrame(self)
        self._container.setObjectName("grip_container_bottom")
        self._container.setGeometry(QRect(0, 0, self._parent.width(), 10))
        self._container.setFrameShape(QFrame.Shape.NoFrame)
        self._container.setFrameShadow(QFrame.Shadow.Raised)

        layout = QHBoxLayout(self._container)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # Bottom Left
        self._left_frame = QFrame(self._container)
        self._left_frame.setObjectName("grip_bottom_left")
        self._left_frame.setFixedSize(10, 10)
        self._left_frame.setCursor(QCursor(Qt.CursorShape.SizeBDiagCursor))
        self._left_grip = QSizeGrip(self._left_frame)
        layout.addWidget(self._left_frame)

        # Bottom Center
        self._center_grip = QFrame(self._container)
        self._center_grip.setObjectName("grip_bottom_center")
        self._center_grip.setCursor(QCursor(Qt.CursorShape.SizeVerCursor))
        self._center_grip.mouseMoveEvent = self._resize_bottom  # type: ignore
        layout.addWidget(self._center_grip)

        # Bottom Right
        self._right_frame = QFrame(self._container)
        self._right_frame.setObjectName("grip_bottom_right")
        self._right_frame.setFixedSize(10, 10)
        self._right_frame.setCursor(QCursor(Qt.CursorShape.SizeFDiagCursor))
        self._right_grip = QSizeGrip(self._right_frame)
        layout.addWidget(self._right_frame)

        if self._disable_color:
            self._container.setStyleSheet("background: transparent")
            self._left_frame.setStyleSheet("background: transparent")
            self._right_frame.setStyleSheet("background: transparent")
            self._center_grip.setStyleSheet("background: transparent")

    def _setup_left_grip(self) -> None:
        """Configure the handle for the left edge."""
        self.setGeometry(0, 10, 10, self._parent.height() - 20)
        self.setMaximumWidth(10)

        self._center_grip = QFrame(self)
        self._center_grip.setObjectName("grip_left")
        self._center_grip.setCursor(QCursor(Qt.CursorShape.SizeHorCursor))
        self._center_grip.setFrameShape(QFrame.Shape.NoFrame)
        self._center_grip.setFrameShadow(QFrame.Shadow.Raised)
        self._center_grip.mouseMoveEvent = self._resize_left  # type: ignore

        if self._disable_color:
            self._center_grip.setStyleSheet("background: transparent")

    def _setup_right_grip(self) -> None:
        """Configure the handle for the right edge."""
        self.setGeometry(self._parent.width() - 10, 10, 10, self._parent.height() - 20)
        self.setMaximumWidth(10)

        self._center_grip = QFrame(self)
        self._center_grip.setObjectName("grip_right")
        self._center_grip.setCursor(QCursor(Qt.CursorShape.SizeHorCursor))
        self._center_grip.setFrameShape(QFrame.Shape.NoFrame)
        self._center_grip.setFrameShadow(QFrame.Shadow.Raised)
        self._center_grip.mouseMoveEvent = self._resize_right  # type: ignore

        if self._disable_color:
            self._center_grip.setStyleSheet("background: transparent")

    # ///////////////////////////////////////////////////////////////
    # RESIZE LOGIC

    def _resize_top(self, event: QMouseEvent) -> None:
        delta = event.pos()
        height = max(self._parent.minimumHeight(), self._parent.height() - delta.y())
        geo = self._parent.geometry()
        geo.setTop(geo.bottom() - height)
        self._parent.setGeometry(geo)
        event.accept()

    def _resize_bottom(self, event: QMouseEvent) -> None:
        delta = event.pos()
        height = max(self._parent.minimumHeight(), self._parent.height() + delta.y())
        self._parent.resize(self._parent.width(), height)
        event.accept()

    def _resize_left(self, event: QMouseEvent) -> None:
        delta = event.pos()
        width = max(self._parent.minimumWidth(), self._parent.width() - delta.x())
        geo = self._parent.geometry()
        geo.setLeft(geo.right() - width)
        self._parent.setGeometry(geo)
        event.accept()

    def _resize_right(self, event: QMouseEvent) -> None:
        delta = event.pos()
        width = max(self._parent.minimumWidth(), delta.x())
        geo = self._parent.geometry()
        geo.setWidth(width)
        self._parent.setGeometry(geo)
        event.accept()

    # ///////////////////////////////////////////////////////////////
    # EVENT OVERRIDES

    def resizeEvent(self, event: Any) -> None:
        """Handle widget resize by updating internal container geometry."""
        if self._container:
            self._container.setGeometry(0, 0, self.width(), 10)
        elif self._center_grip:
            # For side grips, update the center frame height
            self._center_grip.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)


# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////
__all__ = ["CustomGrip"]
