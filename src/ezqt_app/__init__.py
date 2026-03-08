# ///////////////////////////////////////////////////////////////
# EZQT_APP - Main Module
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""
ezqt_app - Lightweight framework to quickly build modern Qt desktop applications.

ezqt_app is a PySide6-based framework providing a complete application shell
with integrated resource management, theming, translation, and reusable
UI components.

**Main Features:**
    - Ready-to-use application window (EzQt_App) with frameless design
    - Integrated theme system with QSS support
    - Built-in translation engine (multi-language support)
    - Modular initialization and asset generation
    - Settings persistence via YAML
    - Reusable core widgets (Header, Menu, PageContainer, SettingsPanel)

**Quick Start:**
    >>> from ezqt_app import EzApplication, EzQt_App, init
    >>> import sys
    >>>
    >>> app = EzApplication(sys.argv)
    >>> init()
    >>>
    >>> window = EzQt_App()
    >>> window.show()
    >>>
    >>> sys.exit(app.exec())
"""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import sys

# Local imports
from .app import EzApplication, EzQt_App
from .main import configure_startup, generate_assets, init, setup_project
from .services.settings import SettingsService, get_settings_service
from .services.translation import (
    change_language,
    change_language_by_code,
    get_available_languages,
    get_current_language,
    register_tr,
    set_tr,
    tr,
    unregister_tr,
)
from .services.ui import UIFunctions
from .widgets.core.header import Header
from .widgets.core.menu import Menu
from .widgets.core.page_container import PageContainer
from .widgets.core.settings_panel import SettingsPanel
from .widgets.ui_main import Ui_MainWindow

# ///////////////////////////////////////////////////////////////
# META INFORMATIONS
# ///////////////////////////////////////////////////////////////

__version__ = "5.0.0"
__author__ = "Neuraaak"
__maintainer__ = "Neuraaak"
__description__ = (
    "Lightweight framework based on PySide6 to quickly build modern desktop "
    "applications, with integrated resource, theme, and reusable component management."
)
__python_requires__ = ">=3.10"
__keywords__ = ["qt", "pyside6", "application", "framework", "gui", "desktop"]
__url__ = "https://github.com/neuraaak/ezqt-app"
__repository__ = "https://github.com/neuraaak/ezqt-app"

# ///////////////////////////////////////////////////////////////
# PYTHON VERSION CHECK
# ///////////////////////////////////////////////////////////////

if sys.version_info < (3, 10):  # noqa: UP036
    raise RuntimeError(
        f"ezqt_app {__version__} requires Python 3.10 or higher. "
        f"Current version: {sys.version}"
    )

# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////

__all__ = [
    # Application
    "EzApplication",
    "EzQt_App",
    # Bootstrap
    "init",
    "setup_project",
    "generate_assets",
    "configure_startup",
    # UI
    "UIFunctions",
    "Ui_MainWindow",
    # Settings
    "SettingsService",
    "get_settings_service",
    # Translation
    "tr",
    "set_tr",
    "register_tr",
    "unregister_tr",
    "change_language",
    "change_language_by_code",
    "get_available_languages",
    "get_current_language",
    # CLI
    "cli",
    # Widgets
    "Header",
    "Menu",
    "PageContainer",
    "SettingsPanel",
    # Metadata
    "__version__",
    "__author__",
    "__maintainer__",
    "__description__",
    "__python_requires__",
    "__keywords__",
    "__url__",
    "__repository__",
]


def __getattr__(name: str):
    """Lazy-load optional CLI entrypoint to avoid hard dependency at import time."""
    if name == "cli":
        from .cli.main import cli

        return cli
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
