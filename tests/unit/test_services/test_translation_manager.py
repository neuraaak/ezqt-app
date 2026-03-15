# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_SERVICES.TEST_TRANSLATION_MANAGER - Translation manager tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for the TranslationManager."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from unittest.mock import MagicMock, patch

# Local imports
from ezqt_app.services.translation.manager import TranslationManager

# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////


class TestTranslationManager:
    """Tests for the TranslationManager class."""

    def test_should_initialize_with_english_language_when_instantiated(self):
        """Test initialization with default language."""
        manager = TranslationManager()
        assert manager.current_language == "en"
        assert manager.translator is not None

    def test_should_return_list_of_available_languages_when_called(self):
        """Test retrieval of available languages."""
        manager = TranslationManager()
        languages = manager.get_available_languages()

        # Check that it's a list
        assert isinstance(languages, list)

        # v6 now returns language codes defined in SUPPORTED_LANGUAGES keys.
        expected_languages = ["en", "fr", "es", "de"]
        for lang in expected_languages:
            assert lang in languages

    def test_should_return_en_code_when_default_language_is_queried(self):
        """Test retrieval of current language code."""
        manager = TranslationManager()
        assert manager.get_current_language_code() == "en"

    def test_should_return_english_name_when_default_language_is_queried(self):
        """Test retrieval of current language name."""
        manager = TranslationManager()
        assert manager.get_current_language_name() == "English"

    def test_should_return_original_text_when_no_translation_file_is_loaded(self):
        """Test text translation without available translation."""
        manager = TranslationManager()
        text = "Hello World"
        translated = manager.translate(text)
        assert translated == text  # Returns original text if no translation

    @patch("ezqt_app.services.translation.manager.QTranslator")
    def test_should_load_language_when_translator_load_succeeds(self, mock_translator):
        """Test successful language loading."""
        manager = TranslationManager()

        # Mock successful loading
        mock_translator_instance = MagicMock()
        mock_translator_instance.load.return_value = True
        mock_translator.return_value = mock_translator_instance

        result = manager.load_language("English")
        assert result
        assert manager.get_current_language_code() == "en"

    @patch("ezqt_app.services.translation.manager.QTranslator")
    @patch("ezqt_app.services.translation.manager.QCoreApplication")
    @patch("pathlib.Path.exists")
    def test_should_fail_to_load_when_translation_file_does_not_exist(
        self, mock_exists, mock_qcore, mock_translator
    ):
        """Test failed language loading."""
        manager = TranslationManager()

        # Mock that no translation file exists
        mock_exists.return_value = False

        # Mock QCoreApplication
        mock_qcore.removeTranslator = MagicMock()
        mock_qcore.installTranslator = MagicMock()

        # Mock failed loading
        mock_translator_instance = MagicMock()
        mock_translator_instance.load.return_value = False
        mock_translator.return_value = mock_translator_instance

        # Test with valid language but no translation file
        result = manager.load_language("French")
        assert not result
        assert manager.get_current_language_code() == "en"  # Should remain default

    @patch("ezqt_app.services.translation.manager.QCoreApplication")
    def test_should_load_language_when_code_is_given(self, mock_qcore):
        """Test loading language by code."""
        manager = TranslationManager()

        # Mock QCoreApplication methods
        mock_qcore.removeTranslator = MagicMock()
        mock_qcore.installTranslator = MagicMock()

        # Test loading by code
        result = manager.load_language_by_code("fr")
        assert result
        assert manager.get_current_language_code() == "fr"

    def test_should_emit_language_changed_signal_when_language_is_loaded(
        self, qt_application
    ):
        """Test that the languageChanged signal is emitted."""
        manager = TranslationManager()
        signal_emitted = False

        def on_language_changed(lang):
            nonlocal signal_emitted
            signal_emitted = True
            assert lang == "fr"

        manager.languageChanged.connect(on_language_changed)
        manager.load_language("Français")
        assert signal_emitted


class TestTranslationManagerPendingCount:
    """Tests for the pending auto-translation counter and related signals."""

    def test_should_start_with_zero_pending_count_when_instantiated(self):
        """Pending counter must be zero before any requests are fired."""
        manager = TranslationManager()
        assert manager._pending_auto_translations == 0

    def test_should_increment_pending_when_increment_is_called(self):
        """_increment_pending raises counter from 0 to 1."""
        manager = TranslationManager()
        manager._increment_pending()
        assert manager._pending_auto_translations == 1

    def test_should_decrement_pending_when_decrement_is_called(self):
        """_decrement_pending lowers counter by one."""
        manager = TranslationManager()
        manager._increment_pending()
        manager._decrement_pending()
        assert manager._pending_auto_translations == 0

    def test_should_not_go_below_zero_when_decrement_is_called_on_empty_counter(self):
        """_decrement_pending is idempotent at zero — no underflow."""
        manager = TranslationManager()
        manager._decrement_pending()
        assert manager._pending_auto_translations == 0

    def test_should_emit_translation_started_when_count_transitions_from_zero(
        self, qt_application
    ):
        """translation_started is emitted exactly when pending goes 0 → 1."""
        manager = TranslationManager()
        started_count = 0

        def on_started():
            nonlocal started_count
            started_count += 1

        manager.translation_started.connect(on_started)
        manager._increment_pending()
        assert started_count == 1

        # Second increment must NOT re-emit translation_started.
        manager._increment_pending()
        assert started_count == 1

    def test_should_emit_translation_finished_when_count_reaches_zero(
        self, qt_application
    ):
        """translation_finished is emitted exactly when pending reaches 0."""
        manager = TranslationManager()
        finished_count = 0

        def on_finished():
            nonlocal finished_count
            finished_count += 1

        manager.translation_finished.connect(on_finished)
        manager._increment_pending()
        manager._decrement_pending()
        assert finished_count == 1

    def test_should_not_emit_translation_finished_while_requests_remain_pending(
        self, qt_application
    ):
        """translation_finished must not fire while counter is still above zero."""
        manager = TranslationManager()
        finished_count = 0

        def on_finished():
            nonlocal finished_count
            finished_count += 1

        manager.translation_finished.connect(on_finished)
        manager._increment_pending()
        manager._increment_pending()
        manager._decrement_pending()
        # One request still in flight — finished must not have been emitted.
        assert finished_count == 0

        manager._decrement_pending()
        # Now all resolved — finished must have fired exactly once.
        assert finished_count == 1

    def test_should_decrement_pending_when_auto_translation_error_is_received(self):
        """_on_auto_translation_error must decrement the pending counter."""
        manager = TranslationManager()
        manager._increment_pending()
        manager._on_auto_translation_error("Hello", "Network error")
        assert manager._pending_auto_translations == 0

    def test_should_decrement_pending_when_auto_translation_ready_is_received(self):
        """_on_auto_translation_ready must decrement the pending counter."""
        manager = TranslationManager()
        manager._increment_pending()
        manager._on_auto_translation_ready("Hello", "Bonjour")
        assert manager._pending_auto_translations == 0
