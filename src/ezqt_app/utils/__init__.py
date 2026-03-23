# ///////////////////////////////////////////////////////////////
# UTILS - Fonctions utilitaires
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""
Ce module regroupe les fonctions utilitaires pour la bibliothèque ezqt_app.
"""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Local imports
from .diagnostics import info_user, warn_tech, warn_user
from .printer import get_printer
from .qt_runtime import (
    configure_qt_environment,
    configure_qt_high_dpi,
    configure_qt_high_dpi_early,
)
from .runtime_paths import APP_PATH

# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////
__all__ = [
    "APP_PATH",
    "configure_qt_environment",
    "configure_qt_high_dpi",
    "configure_qt_high_dpi_early",
    "info_user",
    "get_printer",
    "warn_tech",
    "warn_user",
]
