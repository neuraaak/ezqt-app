# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_SERVICES.TEST_AUTO_TRANSLATOR - AutoTranslator tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for services/translation/auto_translator.py."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from ezqt_app.services.translation.auto_translator import (
    AutoTranslator,
    GoogleTranslateProvider,
    LibreTranslateProvider,
    MyMemoryProvider,
    TranslationCache,
    TranslationProvider,
)

# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////


class TestTranslationCache:
    """Tests for TranslationCache (pure file I/O logic)."""

    def test_should_return_none_when_cache_entry_is_missing(
        self, tmp_path: Path
    ) -> None:
        cache = TranslationCache(tmp_path / "cache.json")
        assert cache.get("hello", "en", "fr") is None

    def test_should_return_translation_when_cache_entry_is_set(
        self, tmp_path: Path
    ) -> None:
        cache = TranslationCache(tmp_path / "cache.json")
        cache.set("hello", "en", "fr", "bonjour", "test-provider")
        result = cache.get("hello", "en", "fr")
        assert result == "bonjour"

    def test_should_return_none_when_language_pair_does_not_match(
        self, tmp_path: Path
    ) -> None:
        cache = TranslationCache(tmp_path / "cache.json")
        cache.set("hello", "en", "fr", "bonjour", "test")
        assert cache.get("hello", "en", "de") is None

    def test_should_persist_entry_when_new_cache_instance_is_created(
        self, tmp_path: Path
    ) -> None:
        cache_file = tmp_path / "cache.json"
        cache1 = TranslationCache(cache_file)
        cache1.set("hello", "en", "fr", "bonjour", "test")

        cache2 = TranslationCache(cache_file)
        assert cache2.get("hello", "en", "fr") == "bonjour"

    def test_should_return_none_when_cache_entry_is_expired(
        self, tmp_path: Path
    ) -> None:
        cache = TranslationCache(tmp_path / "cache.json")
        key = cache._get_cache_key("old", "en", "fr")
        old_date = (datetime.now() - timedelta(days=60)).isoformat()
        cache.cache_data[key] = {
            "original": "old",
            "translation": "vieux",
            "source_lang": "en",
            "target_lang": "fr",
            "provider": "test",
            "created": old_date,
        }
        assert cache.get("old", "en", "fr") is None

    def test_should_remove_old_entries_when_clear_expired_is_called(
        self, tmp_path: Path
    ) -> None:
        cache = TranslationCache(tmp_path / "cache.json")
        key = cache._get_cache_key("old", "en", "fr")
        old_date = (datetime.now() - timedelta(days=60)).isoformat()
        cache.cache_data[key] = {
            "original": "old",
            "translation": "vieux",
            "source_lang": "en",
            "target_lang": "fr",
            "provider": "test",
            "created": old_date,
        }
        cache.clear_expired()
        assert key not in cache.cache_data

    def test_should_keep_fresh_entries_when_clear_expired_is_called(
        self, tmp_path: Path
    ) -> None:
        cache = TranslationCache(tmp_path / "cache.json")
        cache.set("fresh", "en", "fr", "frais", "test")
        initial_count = len(cache.cache_data)
        cache.clear_expired()
        assert len(cache.cache_data) == initial_count

    def test_should_return_empty_dict_when_cache_file_is_corrupt(
        self, tmp_path: Path
    ) -> None:
        cache_file = tmp_path / "corrupt.json"
        cache_file.write_text("this is not valid json", encoding="utf-8")
        cache = TranslationCache(cache_file)
        assert cache.cache_data == {}

    def test_should_return_empty_dict_when_cache_file_is_missing(
        self, tmp_path: Path
    ) -> None:
        cache = TranslationCache(tmp_path / "nonexistent.json")
        assert cache.cache_data == {}

    def test_should_return_same_key_when_same_inputs_are_given(
        self, tmp_path: Path
    ) -> None:
        cache = TranslationCache(tmp_path / "cache.json")
        key1 = cache._get_cache_key("hello", "en", "fr")
        key2 = cache._get_cache_key("hello", "en", "fr")
        assert key1 == key2

    def test_should_return_different_keys_when_inputs_differ(
        self, tmp_path: Path
    ) -> None:
        cache = TranslationCache(tmp_path / "cache.json")
        key1 = cache._get_cache_key("hello", "en", "fr")
        key2 = cache._get_cache_key("world", "en", "fr")
        assert key1 != key2


class TestLibreTranslateProvider:
    """Tests for LibreTranslateProvider.translate()."""

    def test_should_return_translated_text_when_status_is_200(self) -> None:
        provider = LibreTranslateProvider()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"translatedText": "Bonjour"}

        with patch(
            "ezqt_app.services.translation.auto_translator.requests.post",
            return_value=mock_response,
        ):
            result = provider.translate("Hello", "en", "fr")

        assert result == "Bonjour"

    def test_should_return_none_when_network_exception_occurs(self) -> None:
        provider = LibreTranslateProvider()
        with patch(
            "ezqt_app.services.translation.auto_translator.requests.post",
            side_effect=Exception("connection refused"),
        ):
            result = provider.translate("Hello", "en", "fr")

        assert result is None

    def test_should_send_translate_url_when_translate_is_called(self) -> None:
        provider = LibreTranslateProvider()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"translatedText": "ok"}

        with patch(
            "ezqt_app.services.translation.auto_translator.requests.post",
            return_value=mock_response,
        ) as mock_post:
            provider.translate("hi", "en", "fr")

        call_kwargs = mock_post.call_args
        assert "translate" in call_kwargs[0][0]

    def test_should_use_custom_server_url_when_custom_server_is_given(self) -> None:
        provider = LibreTranslateProvider(custom_server="https://custom.server.example")
        assert "custom.server.example" in provider.base_url


class TestGoogleTranslateProvider:
    """Tests for GoogleTranslateProvider.translate()."""

    def test_should_return_translated_text_when_google_response_is_200(self) -> None:
        provider = GoogleTranslateProvider()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [[["Bonjour", "Hello", None, None, 1]]]

        with patch(
            "ezqt_app.services.translation.auto_translator.requests.get",
            return_value=mock_response,
        ):
            result = provider.translate("Hello", "en", "fr")

        assert result == "Bonjour"

    def test_should_return_none_when_google_raises_exception(self) -> None:
        provider = GoogleTranslateProvider()
        with patch(
            "ezqt_app.services.translation.auto_translator.requests.get",
            side_effect=Exception("network error"),
        ):
            result = provider.translate("Hello", "en", "fr")

        assert result is None

    def test_should_return_none_when_google_status_is_not_200(self) -> None:
        provider = GoogleTranslateProvider()
        mock_response = MagicMock()
        mock_response.status_code = 429  # rate limited
        with patch(
            "ezqt_app.services.translation.auto_translator.requests.get",
            return_value=mock_response,
        ):
            result = provider.translate("Hello", "en", "fr")
        assert result is None


class TestMyMemoryProvider:
    """Tests for MyMemoryProvider.translate()."""

    def test_should_return_translated_text_when_mymemory_response_is_200(self) -> None:
        provider = MyMemoryProvider()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "responseStatus": 200,
            "responseData": {"translatedText": "Bonjour"},
        }

        with patch(
            "ezqt_app.services.translation.auto_translator.requests.get",
            return_value=mock_response,
        ):
            result = provider.translate("Hello", "en", "fr")

        assert result == "Bonjour"

    def test_should_return_none_when_mymemory_raises_exception(self) -> None:
        provider = MyMemoryProvider()
        with patch(
            "ezqt_app.services.translation.auto_translator.requests.get",
            side_effect=Exception("timeout"),
        ):
            result = provider.translate("Hello", "en", "fr")

        assert result is None

    def test_should_return_none_when_mymemory_response_status_is_not_200(self) -> None:
        provider = MyMemoryProvider()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"responseStatus": 500}
        with patch(
            "ezqt_app.services.translation.auto_translator.requests.get",
            return_value=mock_response,
        ):
            result = provider.translate("Hello", "en", "fr")
        assert result is None


class TestTranslationProviderBase:
    """Tests for the base TranslationProvider class."""

    def test_should_raise_not_implemented_when_translate_is_called_on_base(
        self,
    ) -> None:
        provider = TranslationProvider("test", "http://example.com")
        with pytest.raises(NotImplementedError):
            provider.translate("text", "en", "fr")

    def test_should_return_false_when_is_available_raises_exception(self) -> None:
        provider = TranslationProvider("test", "http://unreachable.invalid")
        with patch(
            "ezqt_app.services.translation.auto_translator.requests.get",
            side_effect=Exception("unreachable"),
        ):
            assert provider.is_available() is False


class TestAutoTranslator:
    """Tests for AutoTranslator orchestration."""

    def test_should_initialize_with_three_providers_when_created(
        self, tmp_path: Path
    ) -> None:
        translator = AutoTranslator(cache_dir=tmp_path)
        assert len(translator.providers) == 3

    def test_should_be_disabled_when_created_without_explicit_enable(
        self, tmp_path: Path
    ) -> None:
        translator = AutoTranslator(cache_dir=tmp_path)
        assert translator.enabled is False

    def test_should_return_none_when_translator_is_disabled(
        self, tmp_path: Path
    ) -> None:
        translator = AutoTranslator(cache_dir=tmp_path)
        translator.enabled = False
        result = translator.translate_sync("Hello", "en", "fr")
        assert result is None

    def test_should_return_cached_value_when_translation_is_in_cache(
        self, tmp_path: Path
    ) -> None:
        translator = AutoTranslator(cache_dir=tmp_path)
        translator.enabled = True
        translator.cache.set("Hello", "en", "fr", "Bonjour", "test")
        result = translator.translate_sync("Hello", "en", "fr")
        assert result == "Bonjour"

    def test_should_increase_provider_count_when_provider_is_added(
        self, tmp_path: Path
    ) -> None:
        translator = AutoTranslator(cache_dir=tmp_path)
        initial = len(translator.providers)
        translator.add_provider(MagicMock(name="extra"))
        assert len(translator.providers) == initial + 1

    def test_should_remove_provider_when_name_matches(self, tmp_path: Path) -> None:
        translator = AutoTranslator(cache_dir=tmp_path)
        initial = len(translator.providers)
        mock_provider = MagicMock()
        mock_provider.name = "SpecialProvider"
        translator.add_provider(mock_provider)
        translator.remove_provider("SpecialProvider")
        assert len(translator.providers) == initial

    def test_should_return_provider_result_when_enabled_and_cache_misses(
        self, tmp_path: Path
    ) -> None:
        translator = AutoTranslator(cache_dir=tmp_path)
        translator.enabled = True
        mock_provider = MagicMock()
        mock_provider.translate.return_value = "Hola"
        mock_provider.rate_limit_delay = 0
        translator.providers = [mock_provider]

        result = translator.translate_sync("Hello", "en", "es")

        assert result == "Hola"
        mock_provider.translate.assert_called_once_with("Hello", "en", "es")
