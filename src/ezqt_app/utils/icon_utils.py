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
import requests
from PySide6.QtCore import QByteArray, QFile, QObject, QSize, Qt, QThread, Signal
from PySide6.QtGui import QColor, QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class IconLoaderWorker(QThread):
    """Background thread that fetches an icon from a URL.

    Signals
    -------
    icon_loaded:
        Emitted with the resulting ``QIcon`` on success.
    load_failed:
        Emitted when the download or decoding fails.
    """

    icon_loaded = Signal(QIcon)
    load_failed = Signal()

    def __init__(self, url: str, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._url = url

    def run(self) -> None:
        try:
            response = requests.get(self._url, timeout=5)
            response.raise_for_status()
            if "image" not in response.headers.get("Content-Type", ""):
                self.load_failed.emit()
                return
            image_data = response.content
            if self._url.lower().endswith(".svg"):
                renderer = QSvgRenderer(QByteArray(image_data))
                pixmap = QPixmap(QSize(16, 16))
                pixmap.fill(Qt.GlobalColor.transparent)
                painter = QPainter(pixmap)
                renderer.render(painter)
                painter.end()
                self.icon_loaded.emit(QIcon(pixmap))
            else:
                pixmap = QPixmap()
                if not pixmap.loadFromData(image_data):
                    self.load_failed.emit()
                    return
                pixmap = colorize_pixmap(pixmap, "#FFFFFF", 0.5)
                self.icon_loaded.emit(QIcon(pixmap))
        except Exception:
            self.load_failed.emit()


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
    """Load an icon from a local source (QIcon, file path, or Qt resource path).

    Note: URL sources are not supported here — use :func:`load_icon_from_url_async`
    for HTTP/HTTPS URLs to avoid blocking the main thread.

    Args:
        source: QIcon instance or local file/resource path.
    Returns:
        QIcon or None: The loaded icon, or None if loading failed or source is a URL.
    """
    if source is None:
        return None
    if isinstance(source, QIcon):
        return source
    if isinstance(source, str):
        if source.startswith(("http://", "https://")):
            return None
        if source.lower().endswith(".svg"):
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
            except Exception:
                return None
        pixmap = QPixmap(source)
        if pixmap.isNull():
            return None
        pixmap = colorize_pixmap(pixmap, "#FFFFFF", 0.5)
        return QIcon(pixmap)
    return None


def load_icon_from_url_async(
    url: str, parent: QObject | None = None
) -> IconLoaderWorker:
    """Start an asynchronous icon download from a URL.

    The caller must connect to the worker's signals before the download
    completes, and must keep a reference to the returned worker to prevent
    garbage collection.

    Args:
        url: HTTP/HTTPS URL pointing to an image (PNG, JPEG, SVG, …).
        parent: Optional Qt parent for the worker thread.
    Returns:
        IconLoaderWorker: Running worker. Connect ``icon_loaded(QIcon)`` and
        ``load_failed()`` to react to the result.

    Example::

        worker = load_icon_from_url_async("https://example.com/icon.png", parent=self)
        worker.icon_loaded.connect(self._on_icon_ready)
        worker.load_failed.connect(self._on_icon_error)
    """
    worker = IconLoaderWorker(url, parent)
    worker.start()
    return worker
