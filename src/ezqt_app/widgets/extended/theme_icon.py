# ///////////////////////////////////////////////////////////////
# WIDGETS.EXTENDED.THEME_ICON - Theme-aware icon widget
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""ThemeIcon — QIcon subclass that adapts to the current application theme."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Third-party imports
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QIcon, QPainter, QPixmap

# Local imports
from ...services.settings import get_settings_service
from ...utils.diagnostics import warn_tech


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class ThemeIcon(QIcon):
    """
    Icon with automatic theme support.

    This class extends QIcon to provide an icon that adapts
    automatically to the current theme (light/dark). The icon changes
    color based on the application theme.
    """

    def __init__(self, original_icon: QIcon | str) -> None:
        """
        Initialize icon with theme support.

        Parameters
        ----------
        original_icon : QIcon or str
            The original icon or path to the icon.
        """
        super().__init__()
        self.original_icon = (
            QIcon(original_icon) if isinstance(original_icon, str) else original_icon
        )
        self.updateIcon()
        self._connect_theme_changed()

    # ///////////////////////////////////////////////////////////////
    # UTILITY FUNCTIONS

    def _connect_theme_changed(self) -> None:
        """
        Connect to theme change signal.

        Uses lazy import to avoid circular imports.
        """
        try:
            # Lazy import to avoid circular import
            from ...widgets.core.ez_app import EzApplication

            app = EzApplication.instance()
            if isinstance(app, EzApplication):
                app.themeChanged.connect(self.updateIcon)
        except ImportError:
            # Fallback if import fails
            warn_tech(
                code="widgets.theme_icon.connect_theme_signal_failed",
                message="Could not connect to EzApplication theme signal",
            )

    def updateIcon(self) -> None:
        """
        Update icon based on current theme.

        Changes icon color based on theme:
        - Dark theme: light icon
        - Light theme: dark icon
        """
        icon_color = "light" if get_settings_service().gui.THEME == "dark" else "dark"

        # ////// GET ORIGINAL PIXMAP
        pixmap = self.original_icon.pixmap(self.original_icon.availableSizes()[0])

        # ////// CREATE IMAGE FOR MANIPULATION
        image = pixmap.toImage()

        # ////// DETERMINE NEW COLOR
        new_color = QColor(
            Qt.GlobalColor.white if icon_color == "light" else Qt.GlobalColor.black
        )

        # ////// CREATE NEW PIXMAP
        new_pixmap = QPixmap(image.size())
        new_pixmap.fill(Qt.GlobalColor.transparent)

        # ////// DRAW COLORED ICON
        painter = QPainter(new_pixmap)
        painter.drawImage(0, 0, image)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        painter.fillRect(image.rect(), new_color)
        painter.end()

        self.addPixmap(new_pixmap)


# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////
__all__ = ["ThemeIcon"]
