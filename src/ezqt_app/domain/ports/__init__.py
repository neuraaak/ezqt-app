# ///////////////////////////////////////////////////////////////
# DOMAIN.PORTS - Domain ports aggregator
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Domain ports — abstract contracts (Protocols) for all application services."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////
from .config_service import ConfigServiceProtocol
from .runtime_state_service import RuntimeStateServiceProtocol
from .settings_service import SettingsServiceProtocol
from .translation_service import TranslationServiceProtocol
from .ui_component_factory import UiComponentFactoryProtocol

# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////
__all__ = [
    "ConfigServiceProtocol",
    "RuntimeStateServiceProtocol",
    "SettingsServiceProtocol",
    "TranslationServiceProtocol",
    "UiComponentFactoryProtocol",
]
