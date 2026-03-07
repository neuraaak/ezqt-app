# ///////////////////////////////////////////////////////////////
# DOMAIN.PORTS.TRANSLATION_SERVICE - Translation service port
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Protocol definitions for translation services."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from typing import Protocol


# ///////////////////////////////////////////////////////////////
# PROTOCOLS
# ///////////////////////////////////////////////////////////////
class TranslationServiceProtocol(Protocol):
    """Technical contract for translation services."""

    def change_language(self, language_name: str) -> bool:
        """Switch application language using its display name."""

    def get_available_languages(self) -> list[str]:
        """Return available language codes."""

    def get_current_language_name(self) -> str:
        """Return the current language display name."""

    def get_current_language_code(self) -> str:
        """Return the current language code."""

    def translate(self, text: str) -> str:
        """Translate a text using the active language context."""
