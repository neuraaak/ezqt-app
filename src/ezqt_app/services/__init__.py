# ///////////////////////////////////////////////////////////////
# SERVICES - Logique métier
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""
Ce module regroupe les services métier pour la bibliothèque ezqt_app.
"""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Local imports
from ._registry import ServiceRegistry
from .config import ConfigService, get_config_service
from .runtime import RuntimeStateService, get_runtime_state_service
from .settings import SettingsService, get_settings_service
from .translation import TranslationService, get_translation_service
from .ui import Fonts, SizePolicy, UiComponentFactory, get_ui_component_factory

# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////
__all__ = [
    "ServiceRegistry",
    "ConfigService",
    "get_config_service",
    "RuntimeStateService",
    "get_runtime_state_service",
    "SettingsService",
    "get_settings_service",
    "TranslationService",
    "get_translation_service",
    "UiComponentFactory",
    "get_ui_component_factory",
    "Fonts",
    "SizePolicy",
]
