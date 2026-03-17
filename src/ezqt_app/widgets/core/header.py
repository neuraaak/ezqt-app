# ///////////////////////////////////////////////////////////////
# WIDGETS.CORE.HEADER - Application header widget
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Header widget with logo, application name, and window control buttons."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from typing import Any

# Third-party imports
from PySide6.QtCore import QCoreApplication, QEvent, QMargins, QRect, QSize, Qt
from PySide6.QtGui import QCursor, QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QWidget,
)

# Local imports
from ...services.settings import get_settings_service
from ...services.ui import Fonts, SizePolicy
from ...shared.resources import Icons

# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////


class Header(QFrame):
    """
    Application header with logo, name and control buttons.

    This class provides a customizable header bar with
    the application logo, its name, description and window
    control buttons (minimize, maximize, close).
    """

    # ///////////////////////////////////////////////////////////////
    # INIT
    # ///////////////////////////////////////////////////////////////

    def __init__(
        self,
        app_name: str = "",
        description: str = "",
        parent: QWidget | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the application header.

        Args:
            app_name: Application name (default: "").
            description: Application description (default: "").
            parent: The parent widget (default: None).
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(parent, *args, **kwargs)
        self._buttons: list[QPushButton] = []
        self._icons: list[Any] = []

        # Store originals for retranslation
        self._app_name: str = app_name
        self._description: str = description

        # Widget properties
        self.setObjectName("header_container")
        self.setFixedHeight(50)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setFrameShadow(QFrame.Shadow.Raised)

        # Size policy initialization
        if (
            hasattr(SizePolicy, "H_EXPANDING_V_PREFERRED")
            and SizePolicy.H_EXPANDING_V_PREFERRED is not None
        ):
            self.setSizePolicy(SizePolicy.H_EXPANDING_V_PREFERRED)
            SizePolicy.H_EXPANDING_V_PREFERRED.setHeightForWidth(
                self.sizePolicy().hasHeightForWidth()
            )
        else:
            default_policy = QSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
            )
            default_policy.setHorizontalStretch(0)
            default_policy.setVerticalStretch(0)
            self.setSizePolicy(default_policy)

        # Main layout
        self._layout = QHBoxLayout(self)
        self._layout.setSpacing(0)
        self._layout.setObjectName("header_layout")
        self._layout.setContentsMargins(0, 0, 10, 0)

        # Meta info section
        self._info_frame = QFrame(self)
        self._info_frame.setObjectName("info_frame")
        self._info_frame.setMinimumSize(QSize(0, 50))
        self._info_frame.setMaximumSize(QSize(16777215, 50))
        self._info_frame.setFrameShape(QFrame.Shape.NoFrame)
        self._info_frame.setFrameShadow(QFrame.Shadow.Raised)
        self._layout.addWidget(self._info_frame)

        # App logo
        self._logo_label = QLabel(self._info_frame)
        self._logo_label.setObjectName("app_logo")
        self._logo_label.setGeometry(QRect(10, 4, 40, 40))
        self._logo_label.setMinimumSize(QSize(40, 40))
        self._logo_label.setMaximumSize(QSize(40, 40))
        self._logo_label.setFrameShape(QFrame.Shape.NoFrame)
        self._logo_label.setFrameShadow(QFrame.Shadow.Raised)

        # App title
        self._title_label = QLabel(app_name, self._info_frame)
        self._title_label.setObjectName("app_title")
        self._title_label.setGeometry(QRect(65, 6, 160, 20))

        if hasattr(Fonts, "SEGOE_UI_12_SB") and Fonts.SEGOE_UI_12_SB is not None:
            self._title_label.setFont(Fonts.SEGOE_UI_12_SB)
        else:
            try:
                from PySide6.QtGui import QFont

                default_font = QFont()
                default_font.setFamily("Segoe UI")
                default_font.setPointSize(12)
                self._title_label.setFont(default_font)
            except ImportError:
                pass

        self._title_label.setAlignment(
            Qt.AlignmentFlag.AlignLeading
            | Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignTop
        )

        # App subtitle
        self._subtitle_label = QLabel(description, self._info_frame)
        self._subtitle_label.setObjectName("app_subtitle")
        self._subtitle_label.setGeometry(QRect(65, 26, 16777215, 16))
        self._subtitle_label.setMaximumSize(QSize(16777215, 16))

        if hasattr(Fonts, "SEGOE_UI_8_REG") and Fonts.SEGOE_UI_8_REG is not None:
            self._subtitle_label.setFont(Fonts.SEGOE_UI_8_REG)
        else:
            try:
                from PySide6.QtGui import QFont

                default_font = QFont()
                default_font.setFamily("Segoe UI")
                default_font.setPointSize(8)
                self._subtitle_label.setFont(default_font)
            except ImportError:
                pass

        self._subtitle_label.setAlignment(
            Qt.AlignmentFlag.AlignLeading
            | Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignTop
        )

        # Spacer
        self._spacer = QSpacerItem(
            20, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        self._layout.addItem(self._spacer)

        # Buttons frame
        self._buttons_frame = QFrame(self)
        self._buttons_frame.setObjectName("buttons_frame")
        self._buttons_frame.setMinimumSize(QSize(0, 28))
        self._buttons_frame.setFrameShape(QFrame.Shape.NoFrame)
        self._buttons_frame.setFrameShadow(QFrame.Shadow.Raised)
        self._layout.addWidget(self._buttons_frame, 0, Qt.AlignmentFlag.AlignRight)

        self._buttons_layout = QHBoxLayout(self._buttons_frame)
        self._buttons_layout.setSpacing(5)
        self._buttons_layout.setObjectName("buttons_layout")
        self._buttons_layout.setContentsMargins(0, 0, 0, 0)

        # Theme buttons
        from ezqt_widgets import ThemeIcon

        current_theme = get_settings_service().gui.THEME

        # Settings button
        self.settings_btn = QPushButton(self._buttons_frame)
        self._buttons.append(self.settings_btn)
        self.settings_btn.setObjectName("settings_btn")
        self.settings_btn.setMinimumSize(QSize(28, 28))
        self.settings_btn.setMaximumSize(QSize(28, 28))
        self.settings_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        icon_settings = ThemeIcon(Icons.icon_settings, theme=current_theme)
        self._icons.append(icon_settings)
        self.settings_btn.setIcon(icon_settings)
        self.settings_btn.setIconSize(QSize(20, 20))
        self._buttons_layout.addWidget(self.settings_btn)

        # Minimize button
        self.minimize_btn = QPushButton(self._buttons_frame)
        self._buttons.append(self.minimize_btn)
        self.minimize_btn.setObjectName("minimize_btn")
        self.minimize_btn.setMinimumSize(QSize(28, 28))
        self.minimize_btn.setMaximumSize(QSize(28, 28))
        self.minimize_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        icon_minimize = ThemeIcon(Icons.icon_minimize, theme=current_theme)
        self._icons.append(icon_minimize)
        self.minimize_btn.setIcon(icon_minimize)
        self.minimize_btn.setIconSize(QSize(20, 20))
        self._buttons_layout.addWidget(self.minimize_btn)

        # Maximize button
        self.maximize_restore_btn = QPushButton(self._buttons_frame)
        self._buttons.append(self.maximize_restore_btn)
        self.maximize_restore_btn.setObjectName("maximize_restore_btn")
        self.maximize_restore_btn.setMinimumSize(QSize(28, 28))
        self.maximize_restore_btn.setMaximumSize(QSize(28, 28))

        if hasattr(Fonts, "SEGOE_UI_10_REG") and Fonts.SEGOE_UI_10_REG is not None:
            self.maximize_restore_btn.setFont(Fonts.SEGOE_UI_10_REG)
        else:
            try:
                from PySide6.QtGui import QFont

                default_font = QFont()
                default_font.setFamily("Segoe UI")
                default_font.setPointSize(10)
                self.maximize_restore_btn.setFont(default_font)
            except ImportError:
                pass

        self.maximize_restore_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon_maximize = ThemeIcon(Icons.icon_maximize, theme=current_theme)
        self._icons.append(icon_maximize)
        self.maximize_restore_btn.setIcon(icon_maximize)
        self.maximize_restore_btn.setIconSize(QSize(20, 20))
        self._buttons_layout.addWidget(self.maximize_restore_btn)

        # Close button
        self.close_btn = QPushButton(self._buttons_frame)
        self._buttons.append(self.close_btn)
        self.close_btn.setObjectName("close_btn")
        self.close_btn.setMinimumSize(QSize(28, 28))
        self.close_btn.setMaximumSize(QSize(28, 28))
        self.close_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        icon_close = ThemeIcon(Icons.icon_close, theme=current_theme)
        self._icons.append(icon_close)
        self.close_btn.setIcon(icon_close)
        self.close_btn.setIconSize(QSize(20, 20))
        self._buttons_layout.addWidget(self.close_btn)

        self.retranslate_ui()

    # ///////////////////////////////////////////////////////////////
    # PUBLIC METHODS
    # ///////////////////////////////////////////////////////////////

    def set_app_name(self, app_name: str) -> None:
        """
        Set the application name in the header.

        Args:
            app_name: The new application name.
        """
        self._app_name = app_name
        self._title_label.setText(QCoreApplication.translate("EzQt_App", app_name))

    def set_app_description(self, description: str) -> None:
        """
        Set the application description in the header.

        Args:
            description: The new application description.
        """
        self._description = description
        self._subtitle_label.setText(
            QCoreApplication.translate("EzQt_App", description)
        )

    def retranslate_ui(self) -> None:
        """Apply current translations to all owned text labels and tooltips."""
        self._title_label.setText(
            QCoreApplication.translate("EzQt_App", self._app_name)
        )
        self._subtitle_label.setText(
            QCoreApplication.translate("EzQt_App", self._description)
        )

        self.settings_btn.setToolTip(QCoreApplication.translate("EzQt_App", "Settings"))
        self.minimize_btn.setToolTip(QCoreApplication.translate("EzQt_App", "Minimize"))
        self.maximize_restore_btn.setToolTip(
            QCoreApplication.translate("EzQt_App", "Maximize")
        )
        self.close_btn.setToolTip(QCoreApplication.translate("EzQt_App", "Close"))

    def changeEvent(self, event: QEvent) -> None:
        """
        Handle Qt change events, triggering UI retranslation on language change.

        Args:
            event: The QEvent instance.
        """
        if event.type() == QEvent.Type.LanguageChange:
            self.retranslate_ui()
        super().changeEvent(event)

    def set_app_logo(
        self, logo: str | QPixmap, y_shrink: int = 0, y_offset: int = 0
    ) -> None:
        """
        Set the application logo in the header.

        Args:
            logo: The logo to display (file path or QPixmap).
            y_shrink: Vertical reduction of the logo (default: 0).
            y_offset: Vertical offset of the logo (default: 0).
        """

        def offsetY(y_offset: int = 0, x_offset: int = 0) -> None:
            """Apply offset to logo."""
            current_rect = self._logo_label.geometry()
            new_rect = QRect(
                current_rect.x() + x_offset,
                current_rect.y() + y_offset,
                current_rect.width(),
                current_rect.height(),
            )
            self._logo_label.setGeometry(new_rect)

        # Process logo
        pixmap_logo = QPixmap(logo) if isinstance(logo, str) else logo
        if pixmap_logo.size() != self._logo_label.minimumSize():
            pixmap_logo = pixmap_logo.scaled(
                self._logo_label.minimumSize().shrunkBy(
                    QMargins(0, y_shrink, 0, y_shrink)
                ),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

        self._logo_label.setPixmap(pixmap_logo)
        offsetY(y_offset, y_shrink)

    def update_all_theme_icons(self) -> None:
        """Update all button icons according to current theme."""
        current_theme = get_settings_service().gui.THEME
        for i, btn in enumerate(self._buttons):
            icon = self._icons[i]
            setter = getattr(icon, "set_theme", None)
            if callable(setter):
                setter(current_theme)
            btn.setIcon(icon)


# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////

__all__ = ["Header"]
