# ///////////////////////////////////////////////////////////////
# DOMAIN.MODELS - Domain models aggregator
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Domain models — pure dataclasses with no infrastructure dependencies."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////
from .runtime import RuntimeStateModel
from .settings import AppSettingsModel, GuiSettingsModel, SettingsStateModel
from .translation import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES
from .ui import FONT_SPECS, SIZE_POLICY_SPECS, FontSpec, SizePolicySpec

# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////
__all__ = [
    "RuntimeStateModel",
    "AppSettingsModel",
    "GuiSettingsModel",
    "SettingsStateModel",
    "FontSpec",
    "SizePolicySpec",
    "FONT_SPECS",
    "SIZE_POLICY_SPECS",
    "SUPPORTED_LANGUAGES",
    "DEFAULT_LANGUAGE",
]
