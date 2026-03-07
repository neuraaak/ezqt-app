# ///////////////////////////////////////////////////////////////
# WIDGETS.CORE.EZ_APP - Extended QApplication
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""EzApplication — QApplication subclass with theme and UTF-8 support."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import contextlib
import locale
import os
import time
from typing import Any

# Third-party imports
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QApplication

# Local imports
from ...utils.qt_runtime import configure_qt_high_dpi

# Configure High DPI before any QApplication instance is created
with contextlib.suppress(ImportError, RuntimeError, Exception):
    configure_qt_high_dpi()


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class EzApplication(QApplication):
    """
    Extended main application with theme and UTF-8 encoding support.

    This class inherits from QApplication and adds functionality
    for theme management and UTF-8 encoding.
    """

    themeChanged = Signal()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initialize the application with UTF-8 and high resolution support.

        Parameters
        ----------
        *args : Any
            Positional arguments passed to QApplication.
        **kwargs : Any
            Keyword arguments passed to QApplication.
        """
        with contextlib.suppress(ImportError, RuntimeError, Exception):
            if QGuiApplication.instance() is None:
                QGuiApplication.setHighDpiScaleFactorRoundingPolicy(
                    Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
                )

        existing_app = QApplication.instance()
        if existing_app and not isinstance(existing_app, EzApplication):
            raise RuntimeError(
                "Please destroy the QApplication singleton before creating a new EzApplication instance."
            )

        super().__init__(*args, **kwargs)

        with contextlib.suppress(locale.Error):
            locale.setlocale(locale.LC_ALL, "")

        os.environ["PYTHONIOENCODING"] = "utf-8"
        os.environ["QT_FONT_DPI"] = "96"

    @classmethod
    def create_for_testing(cls, *args: Any, **kwargs: Any) -> EzApplication:
        """
        Create an EzApplication instance for testing, bypassing singleton checks.
        """
        with contextlib.suppress(ImportError, RuntimeError, Exception):
            if QGuiApplication.instance() is None:
                QGuiApplication.setHighDpiScaleFactorRoundingPolicy(
                    Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
                )

        existing_app = QApplication.instance()
        if existing_app:
            if isinstance(existing_app, cls):
                return existing_app
            existing_app.quit()
            existing_app.deleteLater()
            time.sleep(0.2)

            if nested_app := QApplication.instance():
                nested_app.quit()
                nested_app.deleteLater()
                time.sleep(0.2)

        try:
            instance = cls(*args, **kwargs)
        except RuntimeError as e:
            if "QApplication singleton" in str(e):
                app = QApplication.instance()
                if app:
                    app.quit()
                    app.deleteLater()
                    time.sleep(0.3)
                instance = cls(*args, **kwargs)
            else:
                raise

        with contextlib.suppress(locale.Error):
            locale.setlocale(locale.LC_ALL, "")

        os.environ["PYTHONIOENCODING"] = "utf-8"
        os.environ["QT_FONT_DPI"] = "96"

        return instance


# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////
__all__ = ["EzApplication"]
