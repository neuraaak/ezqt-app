# ///////////////////////////////////////////////////////////////
# UTILS.QT_RUNTIME - Qt runtime environment helpers
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Low-level Qt environment setup utilities."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import os
import sys


# ///////////////////////////////////////////////////////////////
# FUNCTIONS
# ///////////////////////////////////////////////////////////////
def configure_qt_environment() -> None:
    """Configure Qt environment variables before any Qt imports."""
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCALE_FACTOR_ROUNDING_POLICY"] = "PassThrough"
    os.environ["QT_FONT_DPI"] = "96"
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"

    if sys.platform.startswith("win"):
        os.environ["QT_QPA_PLATFORM"] = "windows:dpiawareness=0"
    elif sys.platform.startswith("linux"):
        os.environ["QT_QPA_PLATFORM"] = "xcb"
    elif sys.platform.startswith("darwin"):
        os.environ["QT_QPA_PLATFORM"] = "cocoa"


def configure_qt_high_dpi() -> bool:
    """Configure Qt High DPI policy when Qt modules are available."""
    try:
        from PySide6.QtCore import Qt
        from PySide6.QtGui import QGuiApplication

        if QGuiApplication.instance() is None:
            QGuiApplication.setHighDpiScaleFactorRoundingPolicy(
                Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
            )
            return True
        return False
    except ImportError:
        return False
    except RuntimeError as error:
        if "QGuiApplication instance" in str(error):
            return False
        raise
    except Exception:
        return False


def configure_qt_high_dpi_early() -> bool:
    """Configure environment and High DPI policy as early as possible."""
    configure_qt_environment()
    return configure_qt_high_dpi()


# Apply environment configuration at import-time for backward compatibility
configure_qt_environment()


# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////
__all__ = [
    "configure_qt_environment",
    "configure_qt_high_dpi",
    "configure_qt_high_dpi_early",
]
