# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_SERVICES.TEST_TRANSLATION_HELPERS - Translation helper tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for services/translation/helpers.py — thin wrappers on TranslationManager."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
from typing import Any
from unittest.mock import MagicMock, patch

from ezqt_app.services.translation.helpers import (
    change_language,
    change_language_by_code,
    clear_auto_translation_cache,
    enable_auto_translation,
    get_auto_translation_stats,
    get_available_languages,
    get_current_language,
    tr,
)

# ///////////////////////////////////////////////////////////////
# CONSTANTS
# ///////////////////////////////////////////////////////////////

_MANAGER_PATH = "ezqt_app.services.translation.helpers.get_translation_manager"


def _mock_manager(**attrs: Any) -> MagicMock:
    m = MagicMock()
    for key, value in attrs.items():
        setattr(m, key, value)
    return m


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////


class TestTr:
    """Tests for tr()."""

    def test_should_delegate_to_manager_translate_when_tr_is_called(self) -> None:
        mock = _mock_manager()
        mock.translate.return_value = "bonjour"
        with patch(_MANAGER_PATH, return_value=mock):
            result = tr("hello")
        mock.translate.assert_called_once_with("hello")
        assert result == "bonjour"

    def test_should_return_original_text_when_no_translation_exists(self) -> None:
        mock = _mock_manager()
        mock.translate.return_value = "hello"
        with patch(_MANAGER_PATH, return_value=mock):
            result = tr("hello")
        assert result == "hello"


class TestChangeLanguage:
    """Tests for change_language() and change_language_by_code()."""

    def test_should_delegate_and_return_bool_when_change_language_is_called(
        self,
    ) -> None:
        mock = _mock_manager()
        mock.load_language.return_value = True
        with patch(_MANAGER_PATH, return_value=mock):
            result = change_language("Français")
        mock.load_language.assert_called_once_with("Français")
        assert result is True

    def test_should_return_false_when_language_is_unknown(self) -> None:
        mock = _mock_manager()
        mock.load_language.return_value = False
        with patch(_MANAGER_PATH, return_value=mock):
            result = change_language("Unknown")
        assert result is False

    def test_should_delegate_when_change_language_by_code_is_called(self) -> None:
        mock = _mock_manager()
        mock.load_language_by_code.return_value = True
        with patch(_MANAGER_PATH, return_value=mock):
            result = change_language_by_code("fr")
        mock.load_language_by_code.assert_called_once_with("fr")
        assert result is True


class TestGetAvailableLanguages:
    """Tests for get_available_languages() and get_current_language()."""

    def test_should_return_list_when_get_available_languages_is_called(self) -> None:
        mock = _mock_manager()
        mock.get_available_languages.return_value = ["en", "fr", "de"]
        with patch(_MANAGER_PATH, return_value=mock):
            result = get_available_languages()
        assert result == ["en", "fr", "de"]

    def test_should_return_language_name_when_get_current_language_is_called(
        self,
    ) -> None:
        mock = _mock_manager()
        mock.get_current_language_name.return_value = "English"
        with patch(_MANAGER_PATH, return_value=mock):
            result = get_current_language()
        assert result == "English"


class TestAutoTranslationHelpers:
    """Tests for enable/stats/clear auto-translation helpers."""

    def test_should_delegate_with_true_when_enable_auto_translation_is_called(
        self,
    ) -> None:
        mock = _mock_manager()
        with patch(_MANAGER_PATH, return_value=mock):
            enable_auto_translation(True)
        mock.enable_auto_translation.assert_called_once_with(True)

    def test_should_delegate_with_false_when_disable_auto_translation_is_called(
        self,
    ) -> None:
        mock = _mock_manager()
        with patch(_MANAGER_PATH, return_value=mock):
            enable_auto_translation(False)
        mock.enable_auto_translation.assert_called_once_with(False)

    def test_should_return_dict_when_get_auto_translation_stats_is_called(self) -> None:
        mock = _mock_manager()
        mock.get_auto_translation_stats.return_value = {"cached": 5}
        with patch(_MANAGER_PATH, return_value=mock):
            result = get_auto_translation_stats()
        assert isinstance(result, dict)
        assert result == {"cached": 5}

    def test_should_delegate_when_clear_auto_translation_cache_is_called(self) -> None:
        mock = _mock_manager()
        with patch(_MANAGER_PATH, return_value=mock):
            clear_auto_translation_cache()
        mock.clear_auto_translation_cache.assert_called_once()
