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
from PySide6.QtCore import QMargins, QRect, QSize, Qt
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

        Parameters
        ----------
        app_name : str, optional
            Application name (default: "").
        description : str, optional
            Application description (default: "").
        parent : QWidget, optional
            The parent widget (default: None).
        *args : Any
            Additional positional arguments.
        **kwargs : Any
            Additional keyword arguments.
        """
        super().__init__(parent, *args, **kwargs)
        self._buttons: list[QPushButton] = []
        self._icons: list[Any] = []

        # ////// SETUP WIDGET PROPERTIES
        self.setObjectName("headerContainer")
        self.setFixedHeight(50)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setFrameShadow(QFrame.Shadow.Raised)

        # Check if SizePolicy is initialized, otherwise use default policy
        if (
            hasattr(SizePolicy, "H_EXPANDING_V_PREFERRED")
            and SizePolicy.H_EXPANDING_V_PREFERRED is not None
        ):
            self.setSizePolicy(SizePolicy.H_EXPANDING_V_PREFERRED)
            SizePolicy.H_EXPANDING_V_PREFERRED.setHeightForWidth(
                self.sizePolicy().hasHeightForWidth()
            )
        else:
            # Use default size policy if SizePolicy is not initialized
            default_policy = QSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
            )
            default_policy.setHorizontalStretch(0)
            default_policy.setVerticalStretch(0)
            self.setSizePolicy(default_policy)

        # ////// SETUP MAIN LAYOUT
        self.HL_headerContainer = QHBoxLayout(self)
        self.HL_headerContainer.setSpacing(0)
        self.HL_headerContainer.setObjectName("HL_headerContainer")
        self.HL_headerContainer.setContentsMargins(0, 0, 10, 0)

        # ////// SETUP META INFO SECTION
        self.headerMetaInfo = QFrame(self)
        self.headerMetaInfo.setObjectName("headerMetaInfo")
        self.headerMetaInfo.setMinimumSize(QSize(0, 50))
        self.headerMetaInfo.setMaximumSize(QSize(16777215, 50))
        self.headerMetaInfo.setFrameShape(QFrame.Shape.NoFrame)
        self.headerMetaInfo.setFrameShadow(QFrame.Shadow.Raised)
        self.HL_headerContainer.addWidget(self.headerMetaInfo)

        # ////// SETUP APP LOGO
        self.headerAppLogo = QLabel(self.headerMetaInfo)
        self.headerAppLogo.setObjectName("headerAppLogo")
        self.headerAppLogo.setGeometry(QRect(10, 4, 40, 40))
        self.headerAppLogo.setMinimumSize(QSize(40, 40))
        self.headerAppLogo.setMaximumSize(QSize(40, 40))
        self.headerAppLogo.setFrameShape(QFrame.Shape.NoFrame)
        self.headerAppLogo.setFrameShadow(QFrame.Shadow.Raised)

        # ////// SETUP APP NAME
        self.headerAppName = QLabel(app_name, self.headerMetaInfo)
        self.headerAppName.setObjectName("headerAppName")
        self.headerAppName.setGeometry(QRect(65, 6, 160, 20))

        # Check if Fonts is initialized, otherwise use default font
        if hasattr(Fonts, "SEGOE_UI_12_SB") and Fonts.SEGOE_UI_12_SB is not None:
            self.headerAppName.setFont(Fonts.SEGOE_UI_12_SB)
        else:
            try:
                from PySide6.QtGui import QFont

                default_font = QFont()
                default_font.setFamily("Segoe UI")
                default_font.setPointSize(12)
                self.headerAppName.setFont(default_font)
            except ImportError:
                # If QFont is not available, ignore font
                pass

        self.headerAppName.setAlignment(
            Qt.AlignmentFlag.AlignLeading
            | Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignTop
        )
        # //////
        self.headerAppDescription = QLabel(description, self.headerMetaInfo)
        self.headerAppDescription.setObjectName("headerAppDescription")
        self.headerAppDescription.setGeometry(QRect(65, 26, 240, 16))
        self.headerAppDescription.setMaximumSize(QSize(16777215, 16))

        # Check if Fonts is initialized, otherwise use default font
        if hasattr(Fonts, "SEGOE_UI_8_REG") and Fonts.SEGOE_UI_8_REG is not None:
            self.headerAppDescription.setFont(Fonts.SEGOE_UI_8_REG)
        else:
            try:
                from PySide6.QtGui import QFont

                default_font = QFont()
                default_font.setFamily("Segoe UI")
                default_font.setPointSize(8)
                self.headerAppDescription.setFont(default_font)
            except ImportError:
                # If QFont is not available, ignore font
                pass

        self.headerAppDescription.setAlignment(
            Qt.AlignmentFlag.AlignLeading
            | Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignTop
        )

        # /////////////////////////////////////////////////////////////////////
        self.headerHSpacer = QSpacerItem(
            20, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        #
        self.HL_headerContainer.addItem(self.headerHSpacer)

        # /////////////////////////////////////////////////////////////////////

        self.headerButtons = QFrame(self)
        self.headerButtons.setObjectName("headerButtons")
        self.headerButtons.setMinimumSize(QSize(0, 28))
        self.headerButtons.setFrameShape(QFrame.Shape.NoFrame)
        self.headerButtons.setFrameShadow(QFrame.Shadow.Raised)
        #
        self.HL_headerContainer.addWidget(
            self.headerButtons, 0, Qt.AlignmentFlag.AlignRight
        )
        # //////
        self.HL_headerButtons = QHBoxLayout(self.headerButtons)
        self.HL_headerButtons.setSpacing(5)
        self.HL_headerButtons.setObjectName("HL_headerButtons")
        self.HL_headerButtons.setContentsMargins(0, 0, 0, 0)

        # /////////////////////////////////////////////////////////////////////

        # Lazy import to avoid circular imports
        from ...widgets.extended.theme_icon import ThemeIcon

        self.settingsTopBtn = QPushButton(self.headerButtons)
        self._buttons.append(self.settingsTopBtn)
        self.settingsTopBtn.setObjectName("settingsTopBtn")
        self.settingsTopBtn.setMinimumSize(QSize(28, 28))
        self.settingsTopBtn.setMaximumSize(QSize(28, 28))
        self.settingsTopBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        #
        icon_settings = ThemeIcon(Icons.icon_settings)
        self._icons.append(icon_settings)
        self.settingsTopBtn.setIcon(icon_settings)
        self.settingsTopBtn.setIconSize(QSize(20, 20))
        #
        self.HL_headerButtons.addWidget(self.settingsTopBtn)
        # //////
        self.minimizeAppBtn = QPushButton(self.headerButtons)
        self._buttons.append(self.minimizeAppBtn)
        self.minimizeAppBtn.setObjectName("minimizeAppBtn")
        self.minimizeAppBtn.setMinimumSize(QSize(28, 28))
        self.minimizeAppBtn.setMaximumSize(QSize(28, 28))
        self.minimizeAppBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        #
        icon_minimize = ThemeIcon(Icons.icon_minimize)
        self._icons.append(icon_minimize)
        self.minimizeAppBtn.setIcon(icon_minimize)
        self.minimizeAppBtn.setIconSize(QSize(20, 20))
        #
        self.HL_headerButtons.addWidget(self.minimizeAppBtn)
        # //////
        self.maximizeRestoreAppBtn = QPushButton(self.headerButtons)
        self._buttons.append(self.maximizeRestoreAppBtn)
        self.maximizeRestoreAppBtn.setObjectName("maximizeRestoreAppBtn")
        self.maximizeRestoreAppBtn.setMinimumSize(QSize(28, 28))
        self.maximizeRestoreAppBtn.setMaximumSize(QSize(28, 28))

        # Check if Fonts is initialized, otherwise use default font
        if hasattr(Fonts, "SEGOE_UI_10_REG") and Fonts.SEGOE_UI_10_REG is not None:
            self.maximizeRestoreAppBtn.setFont(Fonts.SEGOE_UI_10_REG)
        else:
            try:
                from PySide6.QtGui import QFont

                default_font = QFont()
                default_font.setFamily("Segoe UI")
                default_font.setPointSize(10)
                self.maximizeRestoreAppBtn.setFont(default_font)
            except ImportError:
                # If QFont is not available, ignore font
                pass

        self.maximizeRestoreAppBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        #
        icon_maximize = ThemeIcon(Icons.icon_maximize)
        self._icons.append(icon_maximize)
        self.maximizeRestoreAppBtn.setIcon(icon_maximize)
        self.maximizeRestoreAppBtn.setIconSize(QSize(20, 20))
        #
        self.HL_headerButtons.addWidget(self.maximizeRestoreAppBtn)
        # //////
        self.closeAppBtn = QPushButton(self.headerButtons)
        self._buttons.append(self.closeAppBtn)
        self.closeAppBtn.setObjectName("closeAppBtn")
        self.closeAppBtn.setMinimumSize(QSize(28, 28))
        self.closeAppBtn.setMaximumSize(QSize(28, 28))
        self.closeAppBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        #
        icon_close = ThemeIcon(Icons.icon_close)
        self._icons.append(icon_close)
        self.closeAppBtn.setIcon(icon_close)
        self.closeAppBtn.setIconSize(QSize(20, 20))
        #
        self.HL_headerButtons.addWidget(self.closeAppBtn)

    # ///////////////////////////////////////////////////////////////
    # UTILITY FUNCTIONS

    def set_app_name(self, app_name: str) -> None:
        """
        Set the application name in the header.

        Parameters
        ----------
        app_name : str
            The new application name.
        """
        self.headerAppName.setText(app_name)

    def set_app_description(self, description: str) -> None:
        """
        Set the application description in the header.

        Parameters
        ----------
        description : str
            The new application description.
        """
        self.headerAppDescription.setText(description)

    def set_app_logo(
        self, logo: str | QPixmap, y_shrink: int = 0, y_offset: int = 0
    ) -> None:
        """
        Set the application logo in the header.

        Parameters
        ----------
        logo : str or QPixmap
            The logo to display (file path or QPixmap).
        y_shrink : int, optional
            Vertical reduction of the logo (default: 0).
        y_offset : int, optional
            Vertical offset of the logo (default: 0).
        """

        def offsetY(y_offset: int = 0, x_offset: int = 0) -> None:
            """Apply offset to logo."""
            current_rect = self.headerAppLogo.geometry()
            new_rect = QRect(
                current_rect.x() + x_offset,
                current_rect.y() + y_offset,
                current_rect.width(),
                current_rect.height(),
            )
            self.headerAppLogo.setGeometry(new_rect)

        # ////// PROCESS LOGO
        pixmap_logo = QPixmap(logo) if isinstance(logo, str) else logo
        if pixmap_logo.size() != self.headerAppLogo.minimumSize():
            pixmap_logo = pixmap_logo.scaled(
                self.headerAppLogo.minimumSize().shrunkBy(
                    QMargins(0, y_shrink, 0, y_shrink)
                ),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

        self.headerAppLogo.setPixmap(pixmap_logo)
        offsetY(y_offset, y_shrink)

    def update_all_theme_icons(self) -> None:
        """Update all button icons according to current theme."""
        for i, btn in enumerate(self._buttons):
            btn.setIcon(self._icons[i])


# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////
__all__ = ["Header"]
