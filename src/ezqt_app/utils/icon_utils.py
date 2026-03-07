# ///////////////////////////////////////////////////////////////
# ICON_UTILS - Icon and pixmap utility functions
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////
"""
Utility functions for manipulating icons and QPixmap objects.
Migrated from widgets/extended/menu_button.py.
"""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Third-party imports
from PySide6.QtCore import QByteArray, QFile, QSize, Qt
from PySide6.QtGui import QColor, QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer

# Local imports
from ezqt_app.utils.printer import get_printer

# ///////////////////////////////////////////////////////////////
# FUNCTIONS
# ///////////////////////////////////////////////////////////////


def colorize_pixmap(
    pixmap: QPixmap, color: str = "#FFFFFF", opacity: float = 0.5
) -> QPixmap:
    """
    Colorize a QPixmap with the given color and opacity.
    Args:
        pixmap: QPixmap to colorize.
        color: Color to apply (default: "#FFFFFF").
        opacity: Opacity to apply (default: 0.5).
    Returns:
        QPixmap: The colorized pixmap.
    """
    result = QPixmap(pixmap.size())
    result.fill(Qt.GlobalColor.transparent)
    painter = QPainter(result)
    painter.setOpacity(opacity)
    painter.drawPixmap(0, 0, pixmap)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
    painter.fillRect(result.rect(), QColor(color))
    painter.end()
    return result


def load_icon_from_source(source: QIcon | str | None) -> QIcon | None:
    """
    Load an icon from various sources (QIcon, path, URL, etc.).
    Args:
        source: QIcon, file path, or URL.
    Returns:
        QIcon or None: The loaded icon or None if loading failed.
    """
    if source is None:
        return None
    elif isinstance(source, QIcon):
        return source
    elif isinstance(source, str):
        if source.startswith(("http://", "https://")):
            try:
                import requests

                response = requests.get(source, timeout=5)
                response.raise_for_status()
                if "image" not in response.headers.get("Content-Type", ""):
                    raise ValueError("URL does not point to an image file.")
                image_data = response.content
                if source.lower().endswith(".svg"):
                    renderer = QSvgRenderer(QByteArray(image_data))
                    pixmap = QPixmap(QSize(16, 16))
                    pixmap.fill(Qt.GlobalColor.transparent)
                    painter = QPainter(pixmap)
                    renderer.render(painter)
                    painter.end()
                    return QIcon(pixmap)
                else:
                    pixmap = QPixmap()
                    if not pixmap.loadFromData(image_data):
                        raise ValueError("Failed to load image data from URL.")
                    pixmap = colorize_pixmap(pixmap, "#FFFFFF", 0.5)
                    return QIcon(pixmap)
            except Exception as e:
                get_printer().warning(f"Failed to load icon from URL: {e}")
                return None
        elif source.lower().endswith(".svg"):
            try:
                file = QFile(source)
                if not file.open(QFile.OpenModeFlag.ReadOnly):
                    raise ValueError("Failed to open SVG file.")
                renderer = QSvgRenderer(file)
                pixmap = QPixmap(QSize(16, 16))
                pixmap.fill(Qt.GlobalColor.transparent)
                painter = QPainter(pixmap)
                renderer.render(painter)
                painter.end()
                return QIcon(pixmap)
            except Exception as e:
                get_printer().warning(f"Failed to load local SVG: {e}")
                return None
        else:
            pixmap = QPixmap(source)
            if pixmap.isNull():
                get_printer().warning(f"Failed to load pixmap from path: {source}")
                return None
            pixmap = colorize_pixmap(pixmap, "#FFFFFF", 0.5)
            return QIcon(pixmap)
    return None
