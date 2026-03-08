# ///////////////////////////////////////////////////////////////
# DOMAIN.MODELS.TRANSLATION - Translation domain constants
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Pure domain constants for the translation system."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# CONSTANTS
# ///////////////////////////////////////////////////////////////
SUPPORTED_LANGUAGES: dict[str, dict[str, str]] = {
    "en": {"name": "English", "native_name": "English", "file": "ezqt_app_en.ts"},
    "fr": {"name": "Français", "native_name": "Français", "file": "ezqt_app_fr.ts"},
    "es": {"name": "Español", "native_name": "Español", "file": "ezqt_app_es.ts"},
    "de": {"name": "Deutsch", "native_name": "Deutsch", "file": "ezqt_app_de.ts"},
}

DEFAULT_LANGUAGE: str = "en"
