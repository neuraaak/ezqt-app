# ///////////////////////////////////////////////////////////////
# SERVICES.TRANSLATION.AUTO_TRANSLATOR - Automatic translation providers
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Automatic translation via external providers (disabled by default)."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import hashlib
import json
import threading
import time
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

# Third-party imports
import requests
from pydantic import BaseModel, ConfigDict, RootModel, ValidationError
from PySide6.QtCore import QObject, Signal

# Local imports
from ...utils.diagnostics import warn_tech, warn_user
from ...utils.printer import get_printer


# ///////////////////////////////////////////////////////////////
# PYDANTIC RESPONSE SCHEMAS
# ///////////////////////////////////////////////////////////////
class _LibreTranslateResponseSchema(BaseModel):
    """Expected response payload for LibreTranslate provider."""

    model_config = ConfigDict(extra="forbid")

    translatedText: str


class _GoogleTranslateResponseSchema(RootModel[list[Any]]):
    """Root response payload for Google Translate unofficial endpoint."""


class _MyMemoryResponseDataSchema(BaseModel):
    """Nested MyMemory response data payload."""

    model_config = ConfigDict(extra="forbid")

    translatedText: str | None = None


class _MyMemoryResponseSchema(BaseModel):
    """Expected response payload for MyMemory provider."""

    model_config = ConfigDict(extra="forbid")

    responseStatus: int
    responseData: _MyMemoryResponseDataSchema | None = None


class _TranslationCacheEntrySchema(BaseModel):
    """Strict schema for one translation cache entry."""

    model_config = ConfigDict(extra="forbid")

    original: str
    translation: str
    source_lang: str
    target_lang: str
    provider: str
    created: datetime


class _TranslationCacheFileSchema(RootModel[dict[str, _TranslationCacheEntrySchema]]):
    """Strict schema for translation cache file content."""


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class TranslationProvider(ABC):
    """Base translation provider class"""

    def __init__(self, name: str, base_url: str):
        self.name = name
        self.base_url = base_url
        self.timeout = 10
        self.rate_limit_delay = 1.0

    @abstractmethod
    def translate(
        self, text: str, source_lang: str, target_lang: str
    ) -> str | None: ...

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
                payload = _LibreTranslateResponseSchema.model_validate(response.json())
                return payload.translatedText
            warn_tech(
                code="translation.provider.libretranslate.http_error",
                message=f"LibreTranslate error: {response.status_code}",
            )
            return None
        except ValidationError as e:
            warn_tech(
                code="translation.provider.libretranslate.invalid_payload",
                message="LibreTranslate returned an invalid payload",
                error=e,
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
                payload = _GoogleTranslateResponseSchema.model_validate(response.json())
                data = payload.root
                if (
                    data
                    and len(data) > 0
                    and isinstance(data[0], list)
                    and len(data[0]) > 0
                ):
                    first_entry = data[0][0]
                    if isinstance(first_entry, list) and first_entry:
                        translated = first_entry[0]
                        if isinstance(translated, str):
                            return translated

                warn_tech(
                    code="translation.provider.google.invalid_payload",
                    message="Google Translate returned an unexpected payload shape",
                )
            else:
                warn_tech(
                    code="translation.provider.google.http_error",
                    message=f"Google Translate error: {response.status_code}",
                )
        except ValidationError as e:
            warn_tech(
                code="translation.provider.google.invalid_payload",
                message="Google Translate returned an invalid payload",
                error=e,
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
                payload = _MyMemoryResponseSchema.model_validate(response.json())
                if payload.responseStatus == 200 and payload.responseData is not None:
                    return payload.responseData.translatedText
            else:
                warn_tech(
                    code="translation.provider.mymemory.http_error",
                    message=f"MyMemory error: {response.status_code}",
                )
        except ValidationError as e:
            warn_tech(
                code="translation.provider.mymemory.invalid_payload",
                message="MyMemory returned an invalid payload",
                error=e,
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
        entry_raw = self.cache_data.get(key)
        if entry_raw:
            try:
                entry = _TranslationCacheEntrySchema.model_validate(entry_raw)
            except ValidationError:
                del self.cache_data[key]
                return None

            if datetime.now() - entry.created < timedelta(days=self.max_age_days):
                return entry.translation
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
                    raw_data = json.load(f)
                validated = _TranslationCacheFileSchema.model_validate(raw_data)
                self.cache_data = {
                    key: entry.model_dump(mode="json")
                    for key, entry in validated.root.items()
                }
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
            validated = _TranslationCacheFileSchema.model_validate(self.cache_data)
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(
                    validated.model_dump(mode="json"), f, indent=2, ensure_ascii=False
                )
        except Exception as e:
            warn_tech(
                code="translation.cache.save_failed",
                message="Error saving cache",
                error=e,
            )

    def clear_expired(self) -> None:
        current_time = datetime.now()
        expired_keys: list[str] = []
        for key, entry_raw in self.cache_data.items():
            try:
                entry = _TranslationCacheEntrySchema.model_validate(entry_raw)
            except ValidationError:
                expired_keys.append(key)
                continue

            if current_time - entry.created > timedelta(days=self.max_age_days):
                expired_keys.append(key)

        for key in expired_keys:
            del self.cache_data[key]
        if expired_keys:
            self.save_cache()


class AutoTranslator(QObject):
    """Automatic translation manager (disabled by default).

    Each call to :meth:`translate` spawns a lightweight daemon thread that
    performs the HTTP round-trip in the background.  Signals are emitted from
    that thread; Qt automatically delivers them via a queued connection to
    slots that live in the main thread, so the UI is never blocked.

    A ``_pending`` set (guarded by ``_lock``) deduplicates in-flight requests:
    if the same source string is requested while a thread for it is still
    running, no second thread is spawned.
    """

    translation_ready = Signal(str, str)
    translation_error = Signal(str, str)

    def __init__(self, cache_dir: Path | None = None):
        super().__init__()
        if cache_dir is None:
            cache_dir = Path.home() / ".ezqt" / "cache"
        cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache = TranslationCache(cache_dir / "translations.json")
        self.providers: list[TranslationProvider] = []
        self._pending: set[str] = set()
        self._lock = threading.Lock()
        self._setup_providers()
        self.enabled = False

    def _setup_providers(self) -> None:
        # Order matters: fastest/unofficial first, then free fallback providers.
        # is_available() performs a synchronous HTTP GET; calling it at setup time
        # would block the Qt main thread. Provider availability checking requires
        # a dedicated health-check mechanism before it can be integrated.
        self.providers = [
            GoogleTranslateProvider(),
            MyMemoryProvider(),
            LibreTranslateProvider(),
        ]

    def add_provider(self, provider: TranslationProvider) -> None:
        self.providers.append(provider)

    def remove_provider(self, provider_name: str) -> None:
        self.providers = [p for p in self.providers if p.name != provider_name]

    def translate(self, text: str, source_lang: str, target_lang: str) -> str | None:
        """Schedule an async translation and return ``None`` immediately.

        If *source_lang* equals *target_lang* the method returns *text*
        immediately (identity translation — no HTTP request is made).
        If *text* is already cached the cached value is returned immediately.
        Otherwise a daemon thread is started and ``None`` is returned; the
        caller receives the result via :attr:`translation_ready`.
        """
        if source_lang == target_lang:
            return text

        cached = self.cache.get(text, source_lang, target_lang)
        if cached:
            return cached

        with self._lock:
            if text in self._pending:
                return None
            self._pending.add(text)

        t = threading.Thread(
            target=self._do_translate,
            args=(text, source_lang, target_lang),
            daemon=True,
            name=f"ez-translate:{text[:30]}",
        )
        t.start()
        return None

    def _do_translate(self, text: str, source_lang: str, target_lang: str) -> None:
        """Blocking translation worker — runs in a background daemon thread."""
        try:
            for provider in self.providers:
                try:
                    translation = provider.translate(text, source_lang, target_lang)
                    if translation:
                        self.cache.set(
                            text, source_lang, target_lang, translation, provider.name
                        )
                        get_printer().debug_msg(
                            "[TranslationService] Automatic translation "
                            f"({provider.name}): '{text}' -> '{translation}'"
                        )
                        # Signal is delivered to the main thread via queued connection.
                        self.translation_ready.emit(text, translation)
                        return
                    time.sleep(provider.rate_limit_delay)
                except Exception as e:
                    warn_tech(
                        code="translation.worker.provider_failed",
                        message=f"Translation error with {provider.name}",
                        error=e,
                    )

            warn_user(
                code="translation.auto.failed",
                user_message=f"Automatic translation failed: '{text}'",
                log_message=f"All providers failed for '{text}'",
            )
            self.translation_error.emit(text, "No translation found")
        finally:
            with self._lock:
                self._pending.discard(text)

    def translate_sync(
        self, text: str, source_lang: str, target_lang: str
    ) -> str | None:
        """Translate text synchronously, blocking until a result is obtained.

        Intended for use in CLI scripts, test helpers, and offline batch-processing
        tools that run outside the Qt event loop. Each provider call is a blocking
        HTTP request; the total wait time can reach ``len(providers) × timeout``
        seconds if all providers fail.

        Warning:
            **Never call this method from the Qt main (UI) thread.** Doing so
            blocks the event loop for the entire duration of the HTTP round-trips,
            freezing the application UI. For in-app translation use
            :meth:`translate` instead, which runs the request in a daemon thread.

        Example::

            # Appropriate usage — called from a CLI script, not from a Qt slot:
            translator = get_auto_translator()
            translator.enabled = True
            result = translator.translate_sync("Hello", "en", "fr")
            print(result)  # "Bonjour"

        Args:
            text: The source text to translate.
            source_lang: BCP-47 language code of the source text (e.g. ``"en"``).
            target_lang: BCP-47 language code of the desired output (e.g. ``"fr"``).

        Returns:
            The translated string, or ``None`` if the translator is disabled or
            all providers fail.
        """
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

    def save_translation_to_ts(
        self, original: str, translated: str, target_lang: str, ts_file_path: Path
    ) -> None:
        """Append a single translation entry to a Qt Linguist .ts XML file."""
        from xml.etree.ElementTree import Element, ElementTree, SubElement  # nosec B405

        import defusedxml.ElementTree as ET  # type: ignore[import-untyped]

        try:
            if ts_file_path.exists():
                try:
                    tree = ET.parse(ts_file_path)
                    root = tree.getroot()
                    if root is None:
                        raise ET.ParseError("Empty document")
                except ET.ParseError:
                    root = Element("TS", {"language": target_lang, "version": "2.1"})
                    tree = ElementTree(root)
            else:
                root = Element("TS", {"language": target_lang, "version": "2.1"})
                tree = ElementTree(root)

            context = root.find("context")
            if context is None:
                context = SubElement(root, "context")
                SubElement(context, "name").text = "ezqt_app"

            # Update existing entry if source already present, otherwise append.
            for msg in context.findall("message"):
                src = msg.find("source")
                if src is not None and src.text == original:
                    trans = msg.find("translation")
                    if trans is not None:
                        trans.text = translated
                    break
            else:
                msg = SubElement(context, "message")
                SubElement(msg, "source").text = original
                SubElement(msg, "translation").text = translated

            ts_file_path.parent.mkdir(parents=True, exist_ok=True)
            tree.write(ts_file_path, encoding="unicode", xml_declaration=True)
            get_printer().debug_msg(
                f"[TranslationService] Translation saved to {ts_file_path}"
            )
        except Exception as e:
            warn_tech(
                code="translation.ts.save_failed",
                message="Error saving translation to .ts file",
                error=e,
            )

    def clear_cache(self) -> None:
        self.cache.cache_data.clear()
        self.cache.save_cache()
        get_printer().debug_msg("[TranslationService] Translation cache cleared")

    def get_cache_stats(self) -> dict[str, Any]:
        stats: dict[str, Any] = {
            "total_entries": len(self.cache.cache_data),
            "cache_file": str(self.cache.cache_file),
            "max_age_days": self.cache.max_age_days,
        }
        provider_stats: dict[str, int] = {}
        for entry_raw in self.cache.cache_data.values():
            try:
                entry = _TranslationCacheEntrySchema.model_validate(entry_raw)
                p = entry.provider
            except ValidationError:
                p = "invalid"
            provider_stats[p] = provider_stats.get(p, 0) + 1
        stats["by_provider"] = provider_stats
        return stats

    def cleanup(self) -> None:
        # Background threads are daemon threads — they exit automatically when
        # the process exits.  We only need to flush the on-disk cache.
        self.cache.clear_expired()


# ///////////////////////////////////////////////////////////////
# FUNCTIONS
# ///////////////////////////////////////////////////////////////
def get_auto_translator() -> AutoTranslator:
    """Return the global AutoTranslator singleton."""
    from .._registry import ServiceRegistry

    return ServiceRegistry.get(AutoTranslator, AutoTranslator)
