# ///////////////////////////////////////////////////////////////
# SERVICES.TRANSLATION.AUTO_TRANSLATOR - Automatic translation providers
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Automatic translation via external providers (currently disabled)."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import hashlib
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

# Third-party imports
import requests
from PySide6.QtCore import QObject, QThread, Signal

# Local imports
from ...utils.diagnostics import warn_tech, warn_user
from ...utils.printer import get_printer


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class TranslationProvider:
    """Base translation provider class"""

    def __init__(self, name: str, base_url: str):
        self.name = name
        self.base_url = base_url
        self.timeout = 10
        self.rate_limit_delay = 1.0

    def translate(self, text: str, source_lang: str, target_lang: str) -> str | None:
        raise NotImplementedError

    def is_available(self) -> bool:
        try:
            response = requests.get(self.base_url, timeout=5)
            return response.status_code == 200
        except Exception:
            return False


class LibreTranslateProvider(TranslationProvider):
    """LibreTranslate provider"""

    def __init__(self, api_key: str | None = None, custom_server: str | None = None):
        server = custom_server or "https://libretranslate.com"
        super().__init__("LibreTranslate", server)
        self.api_key = api_key
        self.rate_limit_delay = 1.0

    def translate(self, text: str, source_lang: str, target_lang: str) -> str | None:
        try:
            url = f"{self.base_url}/translate"
            data: dict[str, Any] = {
                "q": text,
                "source": source_lang,
                "target": target_lang,
                "format": "text",
            }
            if self.api_key:
                data["api_key"] = self.api_key

            response = requests.post(
                url,
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=self.timeout,
            )
            if response.status_code == 200:
                return response.json().get("translatedText")
            if self.base_url == "https://libretranslate.com":
                warn_user(
                    code="translation.provider.libretranslate.http_error",
                    user_message=(
                        f"LibreTranslate error: {response.status_code}, "
                        "trying alternative server"
                    ),
                    log_message=(
                        f"LibreTranslate error: {response.status_code}, "
                        "trying alternative server"
                    ),
                )
                return LibreTranslateProvider(
                    custom_server="https://translate.argosopentech.com"
                ).translate(text, source_lang, target_lang)
            warn_tech(
                code="translation.provider.libretranslate.http_error",
                message=f"LibreTranslate error: {response.status_code}",
            )
            return None
        except Exception as e:
            warn_tech(
                code="translation.provider.libretranslate.exception",
                message="LibreTranslate exception",
                error=e,
            )
            return None


class GoogleTranslateProvider(TranslationProvider):
    """Google Translate Web provider (unofficial)"""

    def __init__(self):
        super().__init__("Google Translate", "https://translate.googleapis.com")
        self.rate_limit_delay = 0.5

    def translate(self, text: str, source_lang: str, target_lang: str) -> str | None:
        try:
            response = requests.get(
                f"{self.base_url}/translate_a/single",
                params={
                    "client": "gtx",
                    "sl": source_lang,
                    "tl": target_lang,
                    "dt": "t",
                    "q": text,
                },
                timeout=self.timeout,
            )
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0 and len(data[0]) > 0:
                    return data[0][0][0]
            else:
                warn_tech(
                    code="translation.provider.google.http_error",
                    message=f"Google Translate error: {response.status_code}",
                )
        except Exception as e:
            warn_tech(
                code="translation.provider.google.exception",
                message="Google Translate exception",
                error=e,
            )
        return None


class MyMemoryProvider(TranslationProvider):
    """MyMemory provider (free, no API key required)"""

    def __init__(self):
        super().__init__("MyMemory", "https://api.mymemory.translated.net")

    def translate(self, text: str, source_lang: str, target_lang: str) -> str | None:
        try:
            response = requests.get(
                f"{self.base_url}/get",
                params={"q": text, "langpair": f"{source_lang}|{target_lang}"},
                timeout=self.timeout,
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("responseStatus") == 200:
                    return data.get("responseData", {}).get("translatedText")
            else:
                warn_tech(
                    code="translation.provider.mymemory.http_error",
                    message=f"MyMemory error: {response.status_code}",
                )
        except Exception as e:
            warn_tech(
                code="translation.provider.mymemory.exception",
                message="MyMemory exception",
                error=e,
            )
        return None


class TranslationCache:
    """Translation cache manager"""

    def __init__(self, cache_file: Path):
        self.cache_file = cache_file
        self.cache_data: dict[str, Any] = {}
        self.max_age_days = 30
        self.load_cache()

    def _get_cache_key(self, text: str, source_lang: str, target_lang: str) -> str:
        return hashlib.md5(
            f"{text}|{source_lang}|{target_lang}".encode(), usedforsecurity=False
        ).hexdigest()

    def get(self, text: str, source_lang: str, target_lang: str) -> str | None:
        key = self._get_cache_key(text, source_lang, target_lang)
        entry = self.cache_data.get(key)
        if entry:
            created_time = datetime.fromisoformat(entry["created"])
            if datetime.now() - created_time < timedelta(days=self.max_age_days):
                return entry["translation"]
            del self.cache_data[key]
        return None

    def set(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        translation: str,
        provider: str,
    ) -> None:
        key = self._get_cache_key(text, source_lang, target_lang)
        self.cache_data[key] = {
            "original": text,
            "translation": translation,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "provider": provider,
            "created": datetime.now().isoformat(),
        }
        self.save_cache()

    def load_cache(self) -> None:
        try:
            if self.cache_file.exists():
                with open(self.cache_file, encoding="utf-8") as f:
                    self.cache_data = json.load(f)
        except Exception as e:
            warn_tech(
                code="translation.cache.load_failed",
                message="Error loading cache",
                error=e,
            )
            self.cache_data = {}

    def save_cache(self) -> None:
        try:
            self.cache_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(self.cache_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            warn_tech(
                code="translation.cache.save_failed",
                message="Error saving cache",
                error=e,
            )

    def clear_expired(self) -> None:
        current_time = datetime.now()
        expired_keys = [
            key
            for key, entry in self.cache_data.items()
            if current_time - datetime.fromisoformat(entry["created"])
            > timedelta(days=self.max_age_days)
        ]
        for key in expired_keys:
            del self.cache_data[key]
        if expired_keys:
            self.save_cache()


class AutoTranslationWorker(QThread):
    """Background thread for automatic translations"""

    translation_completed = Signal(str, str, str)
    translation_failed = Signal(str, str)

    def __init__(self, providers: list[TranslationProvider], cache: TranslationCache):
        super().__init__()
        self.providers = providers
        self.cache = cache
        self.running = True

    def translate_text(self, text: str, source_lang: str, target_lang: str) -> None:
        cached = self.cache.get(text, source_lang, target_lang)
        if cached:
            self.translation_completed.emit(text, cached, "cache")
            return

        for provider in self.providers:
            if not self.running:
                break
            try:
                translation = provider.translate(text, source_lang, target_lang)
                if translation:
                    self.cache.set(
                        text, source_lang, target_lang, translation, provider.name
                    )
                    self.translation_completed.emit(text, translation, provider.name)
                    return
                time.sleep(provider.rate_limit_delay)
            except Exception as e:
                warn_tech(
                    code="translation.worker.provider_failed",
                    message=f"Translation error with {provider.name}",
                    error=e,
                )

        self.translation_failed.emit(text, "No translation found")

    def stop(self) -> None:
        self.running = False


class AutoTranslator(QObject):
    """Automatic translation manager (currently disabled)."""

    translation_ready = Signal(str, str)
    translation_error = Signal(str, str)

    def __init__(self, cache_dir: Path | None = None):
        super().__init__()
        if cache_dir is None:
            cache_dir = Path.home() / ".ezqt" / "cache"
        cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache = TranslationCache(cache_dir / "translations.json")
        self.providers: list[TranslationProvider] = []
        self.worker: AutoTranslationWorker | None = None
        # TODO: Réactiver la traduction automatique - DÉSACTIVÉ TEMPORAIREMENT
        self.enabled = False

    def _setup_providers(self) -> None:
        pass  # TODO: Réactiver les fournisseurs - DÉSACTIVÉ TEMPORAIREMENT

    def add_provider(self, provider: TranslationProvider) -> None:
        self.providers.append(provider)

    def remove_provider(self, provider_name: str) -> None:
        self.providers = [p for p in self.providers if p.name != provider_name]

    def translate(self, text: str, source_lang: str, target_lang: str) -> str | None:
        cached = self.cache.get(text, source_lang, target_lang)
        if cached:
            return cached

        if hasattr(self, "_last_request_time"):
            elapsed = time.time() - self._last_request_time
            if elapsed < 1.0:
                time.sleep(1.0 - elapsed)

        if not self.worker or not self.worker.isRunning():
            self.worker = AutoTranslationWorker(self.providers, self.cache)
            self.worker.translation_completed.connect(self._on_translation_completed)
            self.worker.translation_failed.connect(self._on_translation_failed)
            self.worker.start()

        self.worker.translate_text(text, source_lang, target_lang)
        self._last_request_time = time.time()
        return None

    def translate_sync(
        self, text: str, source_lang: str, target_lang: str
    ) -> str | None:
        if not self.enabled:
            return None

        cached = self.cache.get(text, source_lang, target_lang)
        if cached:
            return cached

        for provider in self.providers:
            try:
                translation = provider.translate(text, source_lang, target_lang)
                if translation:
                    self.cache.set(
                        text, source_lang, target_lang, translation, provider.name
                    )
                    return translation
                time.sleep(provider.rate_limit_delay)
            except Exception as e:
                warn_tech(
                    code="translation.sync.provider_failed",
                    message=f"Translation error with {provider.name}",
                    error=e,
                )

        return None

    def _on_translation_completed(
        self, original: str, translated: str, provider: str
    ) -> None:
        get_printer().info(
            f"Automatic translation ({provider}): '{original}' → '{translated}'"
        )
        self.translation_ready.emit(original, translated)

    def _on_translation_failed(self, original: str, error: str) -> None:
        warn_user(
            code="translation.auto.failed",
            user_message=f"Automatic translation failed: '{original}' - {error}",
            log_message=f"Automatic translation failed for '{original}': {error}",
        )
        self.translation_error.emit(original, error)

    def save_translation_to_ts(
        self, original: str, translated: str, target_lang: str, ts_file_path: Path
    ) -> None:
        try:
            ts_data: dict[str, Any] = {}
            if ts_file_path.exists():
                with open(ts_file_path, encoding="utf-8") as f:
                    ts_data = json.load(f)
            if not ts_data:
                ts_data = {
                    "metadata": {
                        "language": target_lang,
                        "created": datetime.now().isoformat(),
                    },
                    "translations": {},
                }
            ts_data["translations"][original] = translated
            ts_file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(ts_file_path, "w", encoding="utf-8") as f:
                json.dump(ts_data, f, indent=2, ensure_ascii=False)
            get_printer().info(f"Translation saved to {ts_file_path}")
        except Exception as e:
            warn_tech(
                code="translation.ts.save_failed",
                message="Error saving translation to .ts file",
                error=e,
            )

    def clear_cache(self) -> None:
        self.cache.cache_data.clear()
        self.cache.save_cache()
        get_printer().info("Translation cache cleared")

    def get_cache_stats(self) -> dict[str, Any]:
        stats: dict[str, Any] = {
            "total_entries": len(self.cache.cache_data),
            "cache_file": str(self.cache.cache_file),
            "max_age_days": self.cache.max_age_days,
        }
        provider_stats: dict[str, int] = {}
        for entry in self.cache.cache_data.values():
            p = entry.get("provider", "unknown")
            provider_stats[p] = provider_stats.get(p, 0) + 1
        stats["by_provider"] = provider_stats
        return stats

    def cleanup(self) -> None:
        if self.worker:
            self.worker.stop()
            self.worker.wait()
        self.cache.clear_expired()


# ///////////////////////////////////////////////////////////////
# SINGLETON
# ///////////////////////////////////////////////////////////////
_auto_translator_instance: AutoTranslator | None = None


def get_auto_translator() -> AutoTranslator:
    """Return the global AutoTranslator singleton."""
    global _auto_translator_instance
    if _auto_translator_instance is None:
        _auto_translator_instance = AutoTranslator()
    return _auto_translator_instance


auto_translator = get_auto_translator  # alias
