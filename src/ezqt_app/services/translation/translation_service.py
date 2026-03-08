# ///////////////////////////////////////////////////////////////
# SERVICES.TRANSLATION.SERVICE - Translation service
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Translation service implementation."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Local imports
from ...domain.ports.translation_service import TranslationServiceProtocol
from .manager import get_translation_manager


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class TranslationService(TranslationServiceProtocol):
    """Service wrapper around translation management."""

    def change_language(self, language_name: str) -> bool:
        """Switch application language using its display name."""
        return get_translation_manager().load_language(language_name)

    def change_language_by_code(self, language_code: str) -> bool:
        """Switch application language using ISO code (e.g. ``"fr"``)."""
        return get_translation_manager().load_language_by_code(language_code)

    def get_available_languages(self) -> list[str]:
        """Return available language codes."""
        return get_translation_manager().get_available_languages()

    def get_current_language_name(self) -> str:
        """Return the current language display name."""
        return get_translation_manager().get_current_language_name()

    def get_current_language_code(self) -> str:
        """Return the current language code."""
        return get_translation_manager().get_current_language_code()

    def translate(self, text: str) -> str:
        """Translate a text using the active language context."""
        return get_translation_manager().translate(text)


# ///////////////////////////////////////////////////////////////
# SINGLETONS
# ///////////////////////////////////////////////////////////////
_translation_service = TranslationService()


# ///////////////////////////////////////////////////////////////
# FUNCTIONS
# ///////////////////////////////////////////////////////////////
def get_translation_service() -> TranslationService:
    """Return the singleton translation service."""
    return _translation_service
