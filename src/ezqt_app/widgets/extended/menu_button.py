# ///////////////////////////////////////////////////////////////
# WIDGETS.EXTENDED.MENU_BUTTON - Animated menu button widget
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""MenuButton — expandable/shrinkable button for navigation menus."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from typing import Any

# Third-party imports
from PySide6.QtCore import QEasingCurve, QPropertyAnimation, QSize, Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QToolButton

# Local imports
from ezqt_app.utils.diagnostics import warn_tech
from ezqt_app.utils.icon_utils import colorize_pixmap, load_icon_from_source


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class MenuButton(QToolButton):
    """
    Enhanced menu button with automatic shrink/extended state management.

    Features:
        - Automatic shrink/extended state management
        - Icon support from various sources (QIcon, path, URL, SVG)
        - Text visibility based on state (visible in extended, hidden in shrink)
        - Customizable shrink size and icon positioning
        - Property access to icon and text
        - Signals for state changes and interactions
        - Hover and click effects
    """

    iconChanged = Signal(QIcon)
    textChanged = Signal(str)
    stateChanged = Signal(bool)  # True for extended, False for shrink

    def __init__(
        self,
        parent: Any | None = None,
        icon: QIcon | str | None = None,
        text: str = "",
        icon_size: QSize | tuple[int, int] = QSize(20, 20),
        shrink_size: int = 60,  # Will be overridden by Menu class
        spacing: int = 10,
        min_height: int | None = None,
        duration: int = 300,  # Animation duration in milliseconds
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the menu button.

        Parameters
        ----------
        parent : Any, optional
            The parent widget (default: None).
        icon : QIcon or str, optional
            The icon to display (default: None).
        text : str, optional
            The button text (default: "").
        icon_size : QSize or tuple, optional
            Icon size (default: QSize(20, 20)).
        shrink_size : int, optional
            Width in shrink state (default: 60).
        spacing : int, optional
            Spacing between icon and text (default: 10).
        min_height : int, optional
            Minimum button height (default: None).
        duration : int, optional
            Animation duration in milliseconds (default: 300).
        *args : Any
            Additional positional arguments.
        **kwargs : Any
            Additional keyword arguments.
        """
        super().__init__(parent, *args, **kwargs)
        self.setProperty("type", "MenuButton")

        # ////// INITIALIZE VARIABLES
        self._icon_size: QSize = (
            QSize(*icon_size)
            if isinstance(icon_size, (tuple, list))
            else QSize(icon_size)
        )
        self._shrink_size: int = shrink_size
        self._spacing: int = spacing
        self._min_height: int | None = min_height
        self._duration: int = duration
        self._current_icon: QIcon | None = None
        self._is_extended: bool = (
            False  # Start in shrink state (menu is shrinked at startup)
        )

        # ////// CALCULATE ICON POSITION
        # Calculate the ideal icon position so it stays fixed when menu expands
        # In shrink mode: icon should be centered in shrink_size
        # In extended mode: icon should stay at the same absolute position
        self._icon_x_position = (self._shrink_size - self._icon_size.width()) // 2

        # ////// SETUP UI COMPONENTS
        self.icon_label = QLabel()
        self.text_label = QLabel()

        # ////// CONFIGURE ICON LABEL
        self.icon_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter
        )
        self.icon_label.setStyleSheet("background-color: transparent;")

        # ////// CONFIGURE TEXT LABEL
        self.text_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        self.text_label.setWordWrap(True)
        self.text_label.setStyleSheet("background-color: transparent;")

        # ////// SETUP LAYOUT
        layout = QHBoxLayout(self)
        layout.setContentsMargins(
            0, 0, 0, 0
        )  # No margins, we'll handle positioning manually
        layout.setSpacing(0)  # No spacing, we'll handle it manually
        layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)  # Always center vertically
        layout.addWidget(self.icon_label)
        layout.addWidget(self.text_label)

        # ////// CONFIGURE SIZE POLICY
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # ////// SET INITIAL VALUES
        if icon:
            self.icon = icon
        if text:
            self.text = text

        # ////// INITIALIZE STATE
        self._update_state_display(animate=False)

    # ///////////////////////////////////////////////////////////////
    # PROPERTY FUNCTIONS

    @property
    def icon(self) -> QIcon | None:
        """Get or set the button icon."""
        return self._current_icon

    @icon.setter
    def icon(self, value: QIcon | str | None) -> None:
        """Set the button icon from various sources."""
        icon = load_icon_from_source(value)
        if icon:
            self._current_icon = icon
            self.icon_label.setPixmap(icon.pixmap(self._icon_size))
            self.icon_label.setFixedSize(self._icon_size)
            # Recalculate icon position when icon changes
            self._icon_x_position = (self._shrink_size - self._icon_size.width()) // 2
            self.iconChanged.emit(icon)
        elif value is not None:
            warn_tech(
                code="widgets.menu_button.icon_load_failed",
                message=f"Could not load icon from source: {value}",
            )

    @property
    def text(self) -> str:
        """Get or set the button text."""
        return self.text_label.text()

    @text.setter
    def text(self, value: str) -> None:
        """Set the button text."""
        if value != self.text_label.text():
            self.text_label.setText(str(value))
            self.textChanged.emit(str(value))

    @property
    def icon_size(self) -> QSize:
        """Get or set the icon size."""
        return self._icon_size

    @icon_size.setter
    def icon_size(self, value: QSize | tuple[int, int]) -> None:
        """Set the icon size."""
        self._icon_size = (
            QSize(*value) if isinstance(value, (tuple, list)) else QSize(value)
        )
        if self._current_icon:
            self.icon_label.setPixmap(self._current_icon.pixmap(self._icon_size))
            self.icon_label.setFixedSize(self._icon_size)
        # Recalculate icon position when icon size changes
        self._icon_x_position = (self._shrink_size - self._icon_size.width()) // 2

    @property
    def shrink_size(self) -> int:
        """Get or set the shrink width."""
        return self._shrink_size

    @shrink_size.setter
    def shrink_size(self, value: int) -> None:
        """Set the shrink width."""
        self._shrink_size = int(value)
        # Recalculate icon position
        self._icon_x_position = (self._shrink_size - self._icon_size.width()) // 2
        self._update_state_display(animate=False)

    @property
    def is_extended(self) -> bool:
        """Get the current state (True for extended, False for shrink)."""
        return self._is_extended

    @property
    def spacing(self) -> int:
        """Get or set the spacing between icon and text."""
        return self._spacing

    @spacing.setter
    def spacing(self, value: int) -> None:
        """Set the spacing between icon and text."""
        self._spacing = int(value)
        layout = self.layout()
        if layout:
            layout.setSpacing(self._spacing)

    @property
    def min_height(self) -> int | None:
        """Get or set the minimum button height."""
        return self._min_height

    @min_height.setter
    def min_height(self, value: int | None) -> None:
        """Set the minimum button height."""
        self._min_height = value
        self.updateGeometry()

    @property
    def duration(self) -> int:
        """Get or set the animation duration in milliseconds."""
        return self._duration

    @duration.setter
    def duration(self, value: int) -> None:
        """Set the animation duration in milliseconds."""
        self._duration = int(value)

    # ///////////////////////////////////////////////////////////////
    # UTILITY FUNCTIONS

    def clear_icon(self) -> None:
        """Remove the current icon."""
        self._current_icon = None
        self.icon_label.clear()
        self.iconChanged.emit(QIcon())

    def clear_text(self) -> None:
        """Clear the button text."""
        self.text = ""

    def toggle_state(self) -> None:
        """Toggle the button state."""
        self.set_state(not self._is_extended)

    def set_state(self, extended: bool) -> None:
        """
        Set the button state.

        Parameters
        ----------
        extended : bool
            True for extended, False for shrink.
        """
        if extended != self._is_extended:
            self._is_extended = extended
            self._update_state_display()
            self.stateChanged.emit(extended)

    def set_icon_color(self, color: str = "#FFFFFF", opacity: float = 0.5) -> None:
        """
        Apply a color and opacity to the current icon.

        Parameters
        ----------
        color : str, optional
            The color to apply (default: "#FFFFFF").
        opacity : float, optional
            The opacity to apply (default: 0.5).
        """
        if self._current_icon:
            pixmap = self._current_icon.pixmap(self._icon_size)
            colored_pixmap = colorize_pixmap(pixmap, color, opacity)
            self.icon_label.setPixmap(colored_pixmap)

    def update_theme_icon(self, theme_icon: QIcon) -> None:
        """
        Update the icon with a theme icon.

        Parameters
        ----------
        theme_icon : QIcon
            The new theme icon.
        """
        if theme_icon:
            self.icon_label.setPixmap(theme_icon.pixmap(self._icon_size))

    def _update_state_display(self, animate: bool = True) -> None:
        """
        Update the display based on current state.

        Parameters
        ----------
        animate : bool, optional
            Enable animation (default: True).
        """
        layout = self.layout()

        if self._is_extended:
            # ////// EXTENDED STATE
            self.text_label.show()
            # Remove maximum width constraint
            self.setMaximumWidth(16777215)  # Qt's maximum value
            # Set minimum width to accommodate icon + text + spacing
            min_width = self._icon_size.width() + self._spacing + 20  # margins
            if self.text:
                min_width += self.text_label.fontMetrics().horizontalAdvance(self.text)
            self.setMinimumWidth(min_width)
            # Set layout alignment to left (icon stays in position, text appears to the right)
            if layout:
                layout.setAlignment(
                    Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
                )
                # Extended mode: position icon at calculated position, text to the right
                left_margin = self._icon_x_position
                layout.setContentsMargins(left_margin, 2, 8, 2)
                layout.setSpacing(self._spacing)
        else:
            # ////// SHRINK STATE
            self.text_label.hide()
            self.setMinimumWidth(self._shrink_size)
            self.setMaximumWidth(self._shrink_size)
            # Set layout alignment to center for shrink state
            if layout:
                layout.setAlignment(
                    Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter
                )
                # Perfect centering: calculate exact margins
                icon_center = self._shrink_size // 2
                icon_left = icon_center - (self._icon_size.width() // 2)
                layout.setContentsMargins(icon_left, 2, icon_left, 2)
                layout.setSpacing(0)

        # Apply animation if requested
        if animate:
            self._animate_state_change()

    def _animate_state_change(self) -> None:
        """
        Animate the state change.
        """
        # Stop any ongoing animation
        if (
            hasattr(self, "animation")
            and self.animation.state() == QPropertyAnimation.State.Running
        ):
            self.animation.stop()

        # Get current and target geometries
        current_rect = self.geometry()

        if self._is_extended:
            # Animate to extended state
            # Calculate target width based on content
            icon_width = self._icon_size.width() if self._current_icon else 0
            text_width = 0
            if self.text:
                text_width = self.text_label.fontMetrics().horizontalAdvance(self.text)
            target_width = (
                self._icon_x_position + icon_width + self._spacing + text_width + 8
            )
        else:
            # Animate to shrink state
            target_width = self._shrink_size

        target_rect = current_rect
        target_rect.setWidth(target_width)

        # Start animation
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(self._duration)
        self.animation.setStartValue(current_rect)
        self.animation.setEndValue(target_rect)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.start()

    # ///////////////////////////////////////////////////////////////
    # OVERRIDE FUNCTIONS

    def sizeHint(self) -> QSize:
        """Get the recommended size for the button."""
        return QSize(100, 40)

    def minimumSizeHint(self) -> QSize:
        """Get the minimum recommended size for the button."""
        # ////// CALCULATE BASE SIZE
        base_size = super().minimumSizeHint()

        # ////// CALCULATE WIDTH BASED ON STATE
        if self._is_extended:
            # Extended state: calculate full width
            # Icon position + icon width + spacing + text width + right margin
            icon_width = self._icon_size.width() if self._current_icon else 0
            text_width = 0
            if self.text:
                text_width = self.text_label.fontMetrics().horizontalAdvance(self.text)
            total_width = (
                self._icon_x_position + icon_width + self._spacing + text_width + 8
            )  # right margin
        else:
            # Shrink state: use shrink_size
            total_width = self._shrink_size

        # ////// CALCULATE HEIGHT
        min_height = (
            self._min_height
            if self._min_height is not None
            else max(base_size.height(), self._icon_size.height() + 8)
        )

        return QSize(total_width, min_height)

    # ///////////////////////////////////////////////////////////////
    # STYLE FUNCTIONS

    def refresh_style(self) -> None:
        """Refresh the widget style (useful after dynamic stylesheet changes)."""
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()


# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////
__all__ = ["MenuButton"]
