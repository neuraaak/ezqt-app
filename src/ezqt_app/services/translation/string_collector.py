# ///////////////////////////////////////////////////////////////
# SERVICES.TRANSLATION.STRING_COLLECTOR - UI string collector
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Collects translatable strings from Qt widgets for translation workflows."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

# Local imports
from ...utils.diagnostics import warn_tech, warn_user
from ...utils.printer import get_printer


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class StringCollector:
    """String collector with language detection and task generation."""

    def __init__(self, user_dir: Path | None = None):
        if user_dir is None:
            user_dir = Path.home() / ".ezqt"

        self.user_dir = user_dir
        self.user_dir.mkdir(parents=True, exist_ok=True)

        self.translations_dir = self.user_dir / "translations"
        self.cache_dir = self.user_dir / "cache"
        self.logs_dir = self.user_dir / "logs"

        self.translations_dir.mkdir(exist_ok=True)
        self.cache_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)

        self.pending_file = self.translations_dir / "pending_strings.txt"
        self.processed_file = self.translations_dir / "processed_strings.txt"
        self.language_detected_file = self.translations_dir / "language_detected.txt"
        self.translation_tasks_file = self.translations_dir / "translation_tasks.json"

        self._collected_strings: set[str] = set()
        self._new_strings: set[str] = set()
        self._language_detected_strings: list[tuple[str, str]] = []

    def collect_strings_from_widget(
        self, widget: Any, recursive: bool = True
    ) -> set[str]:
        collected: set[str] = set()

        def collect_recursive(w: Any) -> None:
            try:
                if hasattr(w, "text") and callable(getattr(w, "text", None)):
                    try:
                        text = w.text().strip()
                        if self._is_valid_string(text):
                            collected.add(text)
                    except Exception as e:
                        warn_tech(
                            code="translation.collector.read_text_failed",
                            message="Could not read widget text",
                            error=e,
                        )

                if hasattr(w, "toolTip") and callable(getattr(w, "toolTip", None)):
                    try:
                        tooltip = w.toolTip().strip()
                        if self._is_valid_string(tooltip):
                            collected.add(tooltip)
                    except Exception as e:
                        warn_tech(
                            code="translation.collector.read_tooltip_failed",
                            message="Could not read widget toolTip",
                            error=e,
                        )

                if hasattr(w, "placeholderText") and callable(
                    getattr(w, "placeholderText", None)
                ):
                    try:
                        placeholder = w.placeholderText().strip()
                        if self._is_valid_string(placeholder):
                            collected.add(placeholder)
                    except Exception as e:
                        warn_tech(
                            code="translation.collector.read_placeholder_failed",
                            message="Could not read widget placeholderText",
                            error=e,
                        )

                if hasattr(w, "windowTitle") and callable(
                    getattr(w, "windowTitle", None)
                ):
                    try:
                        title = w.windowTitle().strip()
                        if self._is_valid_string(title):
                            collected.add(title)
                    except Exception as e:
                        warn_tech(
                            code="translation.collector.read_window_title_failed",
                            message="Could not read widget windowTitle",
                            error=e,
                        )

                if recursive:
                    try:
                        for child in w.findChildren(type(w)):
                            collect_recursive(child)
                    except Exception as e:
                        warn_tech(
                            code="translation.collector.iter_children_failed",
                            message="Could not iterate widget children",
                            error=e,
                        )

            except Exception as e:
                warn_tech(
                    code="translation.collector.scan_widget_failed",
                    message=f"Error scanning widget {type(w)}",
                    error=e,
                )

        collect_recursive(widget)
        return collected

    def _is_valid_string(self, text: str) -> bool:
        if not text or len(text) < 2:
            return False
        if (
            text.startswith(("_", "menu_", "btn_", "setting"))
            or text.isdigit()
            or text in ("", " ", "\n", "\t")
        ):
            return False
        technical_patterns = [
            r"^[A-Z_]+$",
            r"^[a-z_]+$",
            r"^[a-z]+[A-Z][a-z]+$",
            r"^[A-Z][a-z]+[A-Z][a-z]+$",
        ]
        return not any(re.match(p, text) for p in technical_patterns)

    def _detect_language(self, text: str) -> str:
        try:
            from langdetect import (
                DetectorFactory,
                detect,
            )

            DetectorFactory.seed = 0
            return detect(text)
        except ImportError:
            return self._simple_language_detection(text)
        except Exception as e:
            warn_tech(
                code="translation.collector.language_detection_failed",
                message="Language detection error",
                error=e,
            )
            return "en"

    def _simple_language_detection(self, text: str) -> str:
        french_chars = "àáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞŸ"
        german_chars = "äöüßÄÖÜ"
        spanish_chars = "ñáéíóúüÑÁÉÍÓÚÜ"
        if any(c in french_chars for c in text):
            return "fr"
        if any(c in german_chars for c in text):
            return "de"
        if any(c in spanish_chars for c in text):
            return "es"
        return "en"

    def save_pending_strings(self, strings: set[str]) -> None:
        try:
            sorted_strings = sorted(strings)
            with open(self.pending_file, "w", encoding="utf-8") as f:
                f.write(f"# Pending strings - {datetime.now().isoformat()}\n")
                f.write(f"# Total: {len(sorted_strings)} strings\n\n")
                for s in sorted_strings:
                    f.write(f"{s}\n")
            get_printer().info(f"✅ {len(strings)} pending strings saved")
        except Exception as e:
            warn_tech(
                code="translation.collector.save_pending_failed",
                message="Error saving strings",
                error=e,
            )

    def detect_languages_and_save(self, strings: set[str]) -> list[tuple[str, str]]:
        language_detected: list[tuple[str, str]] = []
        for text in strings:
            try:
                lang = self._detect_language(text)
                language_detected.append((lang, text))
            except Exception as e:
                warn_tech(
                    code="translation.collector.detect_languages_failed",
                    message="Language detection error",
                    error=e,
                )
                language_detected.append(("en", text))

        try:
            sorted_results = sorted(language_detected, key=lambda x: x[0])
            with open(self.language_detected_file, "w", encoding="utf-8") as f:
                f.write(
                    f"# Strings with detected language - {datetime.now().isoformat()}\n"
                )
                f.write("# Format: language_code|text\n\n")
                for lang, text in sorted_results:
                    f.write(f"{lang}|{text}\n")
            self._language_detected_strings = language_detected
        except Exception as e:
            warn_tech(
                code="translation.collector.save_language_results_failed",
                message="Error saving language detection results",
                error=e,
            )

        return language_detected

    def load_processed_strings(self) -> set[str]:
        processed: set[str] = set()
        try:
            if self.processed_file.exists():
                with open(self.processed_file, encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            processed.add(line)
                get_printer().info(f"✅ {len(processed)} processed strings loaded")
            else:
                get_printer().info("📝 No processed strings file found")
        except Exception as e:
            warn_tech(
                code="translation.collector.load_processed_failed",
                message="Error loading processed strings",
                error=e,
            )
        return processed

    def get_supported_languages(self) -> list[str]:
        return ["en", "fr", "de", "es", "it", "pt", "ru", "ja", "ko", "zh"]

    def generate_translation_tasks(
        self, language_detected: list[tuple[str, str]]
    ) -> dict[str, Any]:
        tasks: dict[str, Any] = {}
        supported = self.get_supported_languages()
        for source_lang, text in language_detected:
            tasks.setdefault(source_lang, {})
            for target_lang in (lang for lang in supported if lang != source_lang):
                tasks[source_lang].setdefault(target_lang, []).append(text)
        try:
            with open(self.translation_tasks_file, "w", encoding="utf-8") as f:
                json.dump(tasks, f, indent=2, ensure_ascii=False)
            get_printer().info(f"✅ {len(tasks)} translation tasks generated")
        except Exception as e:
            warn_tech(
                code="translation.collector.save_tasks_failed",
                message="Error saving tasks",
                error=e,
            )
        return tasks

    def get_new_strings(self) -> set[str]:
        return self._new_strings.copy()

    def collect_and_compare(
        self, widget: Any, recursive: bool = True
    ) -> dict[str, Any]:
        collected = self.collect_strings_from_widget(widget, recursive)
        self.save_pending_strings(collected)
        language_detected = self.detect_languages_and_save(collected)
        tasks = self.generate_translation_tasks(language_detected)
        processed = self.load_processed_strings()
        self._new_strings = collected - processed

        stats: dict[str, Any] = {
            "total_collected": len(collected),
            "total_processed": len(processed),
            "new_strings": len(self._new_strings),
            "languages_detected": len({lang for lang, _ in language_detected}),
            "translation_tasks": len(tasks),
        }
        get_printer().info("📊 Collection summary:")
        for key, val in stats.items():
            get_printer().info(f"  - {key}: {val}")
        return stats

    def mark_strings_as_processed(self, strings: set[str] | None = None) -> None:
        if strings is None:
            strings = self._new_strings
        if not strings:
            warn_user(
                code="translation.collector.mark_processed_empty",
                user_message="No strings to mark as processed",
            )
            return
        try:
            processed = self.load_processed_strings()
            processed.update(strings)
            sorted_strings = sorted(processed)
            with open(self.processed_file, "w", encoding="utf-8") as f:
                f.write(f"# Processed strings - {datetime.now().isoformat()}\n")
                f.write(f"# Total: {len(sorted_strings)} strings\n\n")
                for s in sorted_strings:
                    f.write(f"{s}\n")
            get_printer().info(f"✅ {len(strings)} strings marked as processed")
        except Exception as e:
            warn_user(
                code="translation.collector.mark_processed_failed",
                user_message="Error marking strings",
                log_message="Error marking strings",
                error=e,
            )

    def get_stats(self) -> dict[str, Any]:
        return {
            "collected_strings": len(self._collected_strings),
            "new_strings": len(self._new_strings),
            "language_detected": len(self._language_detected_strings),
            "pending_file": str(self.pending_file),
            "processed_file": str(self.processed_file),
            "language_detected_file": str(self.language_detected_file),
            "translation_tasks_file": str(self.translation_tasks_file),
        }

    def clear_cache(self) -> None:
        self._collected_strings.clear()
        self._new_strings.clear()
        self._language_detected_strings.clear()
        get_printer().info("Collector cache cleared")


# ///////////////////////////////////////////////////////////////
# SINGLETON
# ///////////////////////////////////////////////////////////////
_string_collector_instance: StringCollector | None = None


def get_string_collector(user_dir: Path | None = None) -> StringCollector:
    """Return the global StringCollector singleton."""
    global _string_collector_instance
    if _string_collector_instance is None:
        _string_collector_instance = StringCollector(user_dir)
    return _string_collector_instance
