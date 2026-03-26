# ///////////////////////////////////////////////////////////////
# SERVICES.TRANSLATION.MANAGER - Translation engine
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Core translation manager — QTranslator wrapper with Qt-native language change propagation."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import sys
from pathlib import Path
from typing import Any

# Third-party imports
from PySide6.QtCore import QCoreApplication, QObject, QTranslator, Signal

# Local imports
from ...domain.models.translation import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES
from ...services.config import get_config_service
from ...utils.diagnostics import warn_tech, warn_user
from ...utils.printer import get_printer
from ...utils.runtime_paths import get_bin_path
from .auto_translator import get_auto_translator


# ///////////////////////////////////////////////////////////////
# HELPERS
# ///////////////////////////////////////////////////////////////
def _parse_bool(raw: object) -> bool:
    """Parse a config value as bool, supporting string representations."""
    if isinstance(raw, str):
        return raw.strip().lower() in {"1", "true", "yes", "on"}
    return bool(raw)


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class EzTranslator(QTranslator):
    """Qt translator that intercepts unknown strings for auto-translation.

    This translator is installed alongside the compiled ``.qm`` translator.
    Qt calls ``translate()`` on every installed translator in LIFO order until
    one returns a non-empty string.  When *source_text* is not yet known,
    ``EzTranslator`` fires the async auto-translation pipeline and returns an
    empty string so Qt falls back to the source text for this render cycle.
    On the next ``LanguageChange`` (triggered once the translation arrives) the
    string is found in ``_ts_translations`` and returned immediately.

    Args:
        manager: The owning :class:`TranslationManager` instance.
    """

    _CONTEXT = "EzQt_App"

    def __init__(self, manager: TranslationManager) -> None:
        super().__init__()
        self._manager = manager

    # ------------------------------------------------------------------
    # QTranslator virtual override
    # ------------------------------------------------------------------

    def translate(  # type: ignore[override]
        self,
        context: str,
        source_text: str,
        _disambiguation: str | None = None,
        _n: int = -1,
    ) -> str | None:
        """Return the translation for *source_text*, or ``None`` if unknown.

        PySide6 maps a ``None`` return value to a null ``QString``, which tells
        Qt to continue querying the next installed translator and ultimately to
        fall back to the source text.  Returning ``""`` (an empty but non-null
        ``QString``) would be interpreted as "the translation is an empty
        string", which is incorrect for strings not yet translated.

        When the string is absent from the in-memory cache and auto-translation
        is active, an async translation request is fired so the string will be
        available on the next ``LanguageChange`` cycle.

        Args:
            context: Qt translation context (only ``"EzQt_App"`` is handled).
            source_text: The English source string to translate.
            _disambiguation: Optional disambiguation hint (unused).
            _n: Plural form selector (unused).

        Returns:
            The translated string if already cached, ``None`` otherwise.
        """
        if context != self._CONTEXT or not source_text:
            return None

        cached = self._manager._ts_translations.get(source_text)
        if cached:
            return cached

        # String is unknown — fire auto-translation if enabled.
        # auto_translator.translate() handles all cases uniformly:
        #   • source == target  → returns text immediately (identity, no HTTP)
        #   • cache hit         → returns cached value immediately
        #   • cache miss        → spawns a daemon thread, returns None
        # All languages including English are processed so that every .ts file
        # is populated with real entries and compiled to a valid .qm.
        if (
            self._manager.auto_translation_enabled
            and self._manager.auto_translator.enabled
        ):
            result = self._manager.auto_translator.translate(
                source_text, DEFAULT_LANGUAGE, self._manager.current_language
            )
            if result is not None:
                # Immediate result (identity or cache hit): populate in-memory
                # cache and persist to .ts so the string survives the next load.
                self._manager._ts_translations[source_text] = result
                self._manager._persist_translation(source_text, result)
                return result
            # Async request dispatched — a thread is running the HTTP round-trip.
            self._manager._increment_pending()

        # Return None so Qt falls back to the .qm translator or source text.
        return None


class TranslationManager(QObject):
    """Core translation engine for EzQt_App.

    Handles .ts file loading, language switching, Qt translator installation
    and automatic widget retranslation on language change.
    """

    languageChanged = Signal(str)
    # Emitted when the first pending auto-translation is enqueued (count > 0).
    # Consumers (e.g. BottomBar) use this to show a progress indicator.
    translation_started = Signal()
    # Emitted when all pending auto-translations have been resolved (count == 0).
    # Consumers use this to hide the progress indicator.
    translation_finished = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.translator = QTranslator()
        self.current_language = DEFAULT_LANGUAGE

        self._ts_translations: dict[str, str] = {}

        # Count of async auto-translation requests that have been fired but
        # for which no result (ready or error) has arrived yet.  Incremented
        # each time a new request is dispatched; decremented on every outcome.
        # When the count transitions 0 → 1 we emit translation_started; when
        # it transitions 1 → 0 we emit translation_finished.
        self._pending_auto_translations: int = 0

        # EzTranslator intercepts QCoreApplication.translate("EzQt_App", text)
        # calls for strings absent from the compiled .qm file (e.g. developer
        # custom strings not yet added to the .ts).  It is installed once and
        # kept across language switches; only the .qm-backed translator is
        # swapped on each language change.
        self._ez_translator = EzTranslator(self)

        self.auto_translator = get_auto_translator()
        self.auto_translation_enabled = False
        self.auto_save_translations = False

        try:
            translation_cfg = (
                get_config_service().load_config("translation").get("translation", {})
            )
            if isinstance(translation_cfg, dict):
                self.auto_translation_enabled = _parse_bool(
                    translation_cfg.get("auto_translation_enabled", False)
                )
                self.auto_save_translations = _parse_bool(
                    translation_cfg.get("save_to_ts_files", False)
                )
        except Exception as e:
            warn_tech(
                code="translation.manager.config_load_failed",
                message="Could not load translation config; using defaults (disabled)",
                error=e,
            )

        self.auto_translator.enabled = self.auto_translation_enabled
        self.auto_translator.translation_ready.connect(self._on_auto_translation_ready)
        self.auto_translator.translation_error.connect(self._on_auto_translation_error)

        # Register cleanup on application exit: stop the worker thread and purge
        # the expired cache entries. Guard against QCoreApplication not yet existing
        # (e.g., when the manager is instantiated in a test context without a Qt app).
        # Also install EzTranslator so it begins intercepting QCoreApplication.translate()
        # calls immediately — even before the first explicit language switch.
        _qapp = QCoreApplication.instance()
        if _qapp is not None:
            _qapp.aboutToQuit.connect(self.auto_translator.cleanup)
            QCoreApplication.installTranslator(self._ez_translator)

        # Resolve translations directory
        if hasattr(sys, "_MEIPASS"):
            self.translations_dir: Path | None = (
                Path(sys._MEIPASS)  # pyright: ignore[reportAttributeAccessIssue]
                / "ezqt_app"
                / "resources"
                / "translations"
            )
        else:
            possible_paths = [
                get_bin_path() / "translations",
                Path(__file__).parent.parent.parent / "resources" / "translations",
            ]
            try:
                pkg_dir = self._get_package_translations_dir()
                if pkg_dir.exists():
                    possible_paths.append(pkg_dir)
            except Exception as e:
                warn_tech(
                    code="translation.manager.package_dir_resolution_failed",
                    message="Could not resolve package translations dir",
                    error=e,
                )

            self.translations_dir = next(
                (p for p in possible_paths if p.exists()), None
            )
            if self.translations_dir is None:
                self.translations_dir = get_bin_path() / "translations"
                self.translations_dir.mkdir(parents=True, exist_ok=True)

    def _get_package_translations_dir(self) -> Path:
        try:
            import pkg_resources  # type: ignore[import-untyped]

            return Path(
                pkg_resources.resource_filename("ezqt_app", "resources/translations")
            )
        except Exception:
            return Path(__file__).parent.parent.parent / "resources" / "translations"

    # ------------------------------------------------------------------
    # .qm compilation helpers
    # ------------------------------------------------------------------

    def _find_lrelease(self) -> Path | None:
        """Locate the pyside6-lrelease executable.

        Searches PATH first (the ``pyside6-lrelease`` wrapper script), then
        falls back to the ``lrelease[.exe]`` binary inside the PySide6 package
        directory.  Returns ``None`` if the tool cannot be found.
        """
        import shutil

        which = shutil.which("pyside6-lrelease")
        if which:
            return Path(which)

        try:
            import PySide6

            pyside6_dir = Path(PySide6.__file__).parent
            for name in ("lrelease.exe", "lrelease"):
                candidate = pyside6_dir / name
                if candidate.exists():
                    return candidate
        except Exception as e:
            warn_tech(
                code="translation.manager.pyside6_lrelease_lookup_failed",
                message="Could not locate lrelease in PySide6 package directory",
                error=e,
            )

        return None

    def _ensure_qm_compiled(self, ts_path: Path, qm_path: Path) -> bool:
        """Compile *ts_path* → *qm_path* using ``pyside6-lrelease`` if needed.

        Skips recompilation when *qm_path* is already up-to-date (mtime ≥
        *ts_path* mtime).  Returns ``True`` if *qm_path* exists after the
        method completes (either freshly compiled or already current).
        """
        if qm_path.exists() and qm_path.stat().st_mtime >= ts_path.stat().st_mtime:
            return True

        lrelease = self._find_lrelease()
        if lrelease is None:
            warn_tech(
                code="translation.manager.lrelease_not_found",
                message=(
                    "pyside6-lrelease not found; .qm file will not be generated. "
                    "Install PySide6 tools or ensure pyside6-lrelease is on PATH."
                ),
            )
            return qm_path.exists()

        try:
            import subprocess

            result = subprocess.run(
                [str(lrelease), str(ts_path), "-qm", str(qm_path)],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode != 0:
                warn_tech(
                    code="translation.manager.lrelease_failed",
                    message=f"lrelease exited with code {result.returncode}: {result.stderr.strip()}",
                )
        except Exception as e:
            warn_tech(
                code="translation.manager.qm_compile_failed",
                message=f"Failed to compile {ts_path.name} to .qm",
                error=e,
            )

        return qm_path.exists()

    # ------------------------------------------------------------------

    def _load_ts_file(self, ts_file_path: Path) -> bool:
        try:
            import xml.etree.ElementTree as ET

            if not ts_file_path.exists():
                return False

            root = ET.parse(ts_file_path).getroot()  # noqa: S314
            translations: dict[str, str] = {}
            for message in root.findall(".//message"):
                source = message.find("source")
                translation = message.find("translation")
                if (
                    source is not None
                    and translation is not None
                    and source.text
                    and translation.text
                ):
                    translations[source.text] = translation.text

            self._ts_translations.update(translations)
            return True
        except Exception as e:
            warn_tech(
                code="translation.manager.load_ts_failed",
                message=f"Error loading .ts file {ts_file_path}",
                error=e,
            )
            return False

    def load_language(self, language_name: str) -> bool:
        name_to_code = {
            info["name"]: code for code, info in SUPPORTED_LANGUAGES.items()
        }
        if language_name in name_to_code:
            return self.load_language_by_code(name_to_code[language_name])
        return False

    def load_language_by_code(self, language_code: str) -> bool:
        if language_code not in SUPPORTED_LANGUAGES:
            warn_user(
                code="translation.manager.unsupported_language",
                user_message=f"Unsupported language: {language_code}",
            )
            return False

        self._ts_translations.clear()

        app = QCoreApplication.instance()
        if app is not None:
            try:
                QCoreApplication.removeTranslator(self.translator)
            except Exception as e:
                warn_tech(
                    code="translation.manager.remove_translator_failed",
                    message="Error removing translator",
                    error=e,
                )

        self.translator = QTranslator()
        language_info = SUPPORTED_LANGUAGES[language_code]
        self.current_language = language_code

        if self.translations_dir is None:
            warn_tech(
                code="translation.manager.translations_dir_unavailable",
                message=(
                    "Translations directory not resolved; .ts file load skipped "
                    f"for language '{language_code}'"
                ),
            )
            self.languageChanged.emit(language_code)
            return True

        ts_file_path = self.translations_dir / language_info["file"]

        if self._load_ts_file(ts_file_path):
            # Compile .ts → .qm (skipped when .qm is already up to date) and
            # load into the QTranslator so QCoreApplication.translate() works.
            qm_path = ts_file_path.with_suffix(".qm")
            if self._ensure_qm_compiled(
                ts_file_path, qm_path
            ) and not self.translator.load(str(qm_path)):
                warn_tech(
                    code="translation.manager.load_qm_failed",
                    message=f"QTranslator.load() failed for {qm_path.name}",
                )
            get_printer().debug_msg(
                f"[TranslationService] Language switched to {language_info['name']}"
            )
        elif language_code != DEFAULT_LANGUAGE:
            # No .ts file yet for this language. Warn but continue: installing an
            # empty translator still fires Qt's LanguageChange event, which causes
            # all widgets to call retranslate_ui() → QCoreApplication.translate()
            # → EzTranslator.translate() → auto-translation for every string.
            warn_user(
                code="translation.manager.load_language_failed",
                user_message=(
                    f"No translation file found for {language_info['name']} — "
                    "auto-translation will populate it progressively."
                ),
            )

        # Always install the translator (empty or .qm-backed) so Qt posts a
        # LanguageChange event.  Without this call, widgets never call
        # retranslate_ui() and EzTranslator is never invoked for the new language.
        if app is not None:
            try:
                QCoreApplication.installTranslator(self.translator)
            except Exception as e:
                warn_tech(
                    code="translation.manager.install_translator_failed",
                    message="Error installing translator",
                    error=e,
                )

        self.languageChanged.emit(language_code)
        return True

    def get_available_languages(self) -> list[str]:
        return list(SUPPORTED_LANGUAGES.keys())

    def get_current_language_name(self) -> str:
        if self.current_language in SUPPORTED_LANGUAGES:
            return SUPPORTED_LANGUAGES[self.current_language]["name"]
        return "Unknown"

    def get_current_language_code(self) -> str:
        return self.current_language

    @property
    def translation_count(self) -> int:
        """Return the number of cached translations."""
        return len(self._ts_translations)

    def translate(self, text: str) -> str:
        if text in self._ts_translations:
            return self._ts_translations[text]

        translated = self.translator.translate("", text)
        if translated and translated != text:
            return translated

        # Fire async auto-translation — widgets update via _on_auto_translation_ready
        # when the result arrives. Never call translate_sync() from the UI thread.
        if self.auto_translation_enabled and self.auto_translator.enabled:
            result = self.auto_translator.translate(text, "en", self.current_language)
            # Increment the pending counter only when a real async request was
            # dispatched (translate() returns None in that case).  A non-None
            # result means the cache was hit synchronously and no worker task
            # will emit translation_ready later.
            if result is None:
                self._increment_pending()

        return text

    # ------------------------------------------------------------------
    # Pending-count helpers
    # ------------------------------------------------------------------

    def _increment_pending(self) -> None:
        """Increment the pending auto-translation counter.

        Emits :attr:`translation_started` when the count transitions from 0
        to 1, signalling that at least one async translation is in flight.
        """
        self._pending_auto_translations += 1
        if self._pending_auto_translations == 1:
            self.translation_started.emit()

    def _decrement_pending(self) -> None:
        """Decrement the pending auto-translation counter (floor: 0).

        Emits :attr:`translation_finished` when the count reaches zero,
        signalling that all in-flight translations have been resolved.
        """
        self._pending_auto_translations = max(0, self._pending_auto_translations - 1)
        if self._pending_auto_translations == 0:
            self.translation_finished.emit()

    def _on_auto_translation_error(self, _original: str, _error: str) -> None:
        """Slot called when an async auto-translation fails.

        Decrements the pending counter so the UI indicator is hidden even on
        failure.  Error reporting is handled by :class:`AutoTranslator` itself.

        Args:
            _original: The source string that could not be translated (unused here).
            _error: The error message reported by the provider (unused here).
        """
        self._decrement_pending()

    def _on_auto_translation_ready(self, original: str, translated: str) -> None:
        """Slot called when an async auto-translation completes.

        Caches the result, optionally persists it to the .ts file (and
        recompiles the .qm), then triggers a ``QEvent::LanguageChange`` on all
        widgets by reinstalling ``_ez_translator``.  This causes every widget's
        ``changeEvent`` / ``retranslate_ui`` to run, at which point
        ``QCoreApplication.translate("EzQt_App", original)`` finds the new
        entry either in ``_ts_translations`` (via ``EzTranslator``) or in the
        freshly reloaded ``.qm`` file.

        Args:
            original: The source (English) string that was translated.
            translated: The translated string in the current language.
        """
        self._decrement_pending()
        self._ts_translations[original] = translated
        if self.auto_save_translations:
            # _save_auto_translation_to_ts reloads the .qm translator, which
            # already calls installTranslator() and thus posts LanguageChange.
            # No need to reinstall _ez_translator separately in that case.
            self._save_auto_translation_to_ts(original, translated)
        else:
            # Without .ts persistence the .qm is not reloaded.  Reinstall
            # _ez_translator to post LanguageChange so widgets call
            # retranslate_ui() and pick up the new entry from _ts_translations.
            app = QCoreApplication.instance()
            if app is not None:
                try:
                    QCoreApplication.installTranslator(self._ez_translator)
                except Exception as e:
                    warn_tech(
                        code="translation.manager.ez_translator_reinstall_failed",
                        message="Could not reinstall EzTranslator after auto-translation",
                        error=e,
                    )

    def _persist_translation(self, original: str, translated: str) -> None:
        """Persist an immediately-resolved translation to the current .ts file.

        Called by :class:`EzTranslator` when ``auto_translator.translate()``
        returns a result synchronously (identity translation or cache hit).
        Unlike :meth:`_save_auto_translation_to_ts` this method does **not**
        recompile the .qm or reinstall the translator — the text is already
        correct in the UI, so no ``LanguageChange`` event is needed.  The .qm
        will be recompiled on the next :meth:`load_language_by_code` call (the
        mtime check in :meth:`_ensure_qm_compiled` detects the stale .qm).

        Args:
            original: The source (English) string.
            translated: The translation to persist (may equal *original* for the
                source language — identity mapping).
        """
        if not self.auto_save_translations or self.translations_dir is None:
            return
        if self.current_language not in SUPPORTED_LANGUAGES:
            return
        language_info = SUPPORTED_LANGUAGES[self.current_language]
        ts_file_path = self.translations_dir / language_info["file"]
        self.auto_translator.save_translation_to_ts(
            original, translated, self.current_language, ts_file_path
        )

    def _save_auto_translation_to_ts(self, original: str, translated: str) -> None:
        """Persist *translated* to the active .ts file and reload the .qm translator.

        After writing the new entry to the .ts file the method recompiles it to
        a fresh .qm and reloads ``self.translator``.  Subsequent calls to
        ``QCoreApplication.translate("EzQt_App", original)`` will therefore
        find the string in the .qm-backed translator (in addition to
        ``EzTranslator``'s in-memory cache), making the translation durable
        across application restarts.

        Args:
            original: The source (English) string.
            translated: The translated string to persist.
        """
        try:
            if self.current_language not in SUPPORTED_LANGUAGES:
                return
            if self.translations_dir is None:
                return

            language_info = SUPPORTED_LANGUAGES[self.current_language]
            ts_file_path = self.translations_dir / language_info["file"]
            self.auto_translator.save_translation_to_ts(
                original, translated, self.current_language, ts_file_path
            )
            self._ts_translations[original] = translated

            # Recompile .ts → .qm so the entry is available via the native
            # QTranslator on the next language load (and on app restart).
            qm_path = ts_file_path.with_suffix(".qm")
            if self._ensure_qm_compiled(ts_file_path, qm_path):
                app = QCoreApplication.instance()
                if app is not None:
                    # Swap out the .qm translator atomically: remove the old
                    # one, load the updated binary, reinstall.
                    try:
                        QCoreApplication.removeTranslator(self.translator)
                        self.translator = QTranslator()
                        if not self.translator.load(str(qm_path)):
                            warn_tech(
                                code="translation.manager.reload_qm_failed",
                                message=(
                                    f"QTranslator.load() failed after auto-save "
                                    f"for {qm_path.name}"
                                ),
                            )
                        # Install first so it is consulted before EzTranslator
                        # (LIFO order: last installed = first consulted).
                        QCoreApplication.installTranslator(self.translator)
                    except Exception as e:
                        warn_tech(
                            code="translation.manager.reload_qm_install_failed",
                            message="Error reloading .qm translator after auto-save",
                            error=e,
                        )
        except Exception as e:
            warn_tech(
                code="translation.manager.auto_translation_save_failed",
                message="Error saving automatic translation",
                error=e,
            )

    def enable_auto_translation(self, enabled: bool = True) -> None:
        self.auto_translation_enabled = enabled
        if self.auto_translator:
            self.auto_translator.enabled = enabled
        get_printer().action(
            "[TranslationService] Automatic translation "
            f"{'enabled' if enabled else 'disabled'}"
        )

    def get_auto_translation_stats(self) -> dict[str, Any]:
        if self.auto_translator:
            return self.auto_translator.get_cache_stats()
        return {}

    def clear_auto_translation_cache(self) -> None:
        if self.auto_translator:
            self.auto_translator.clear_cache()


# ///////////////////////////////////////////////////////////////
# FUNCTIONS
# ///////////////////////////////////////////////////////////////
def get_translation_manager() -> TranslationManager:
    """Return the global TranslationManager singleton."""
    from .._registry import ServiceRegistry

    return ServiceRegistry.get(TranslationManager, TranslationManager)
