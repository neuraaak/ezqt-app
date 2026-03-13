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
        assert len(manager._translatable_widgets) == 0
        assert len(manager._translatable_texts) == 0

    def test_should_have_correct_language_mapping_when_instantiated(self):
        """Test language mapping."""
        manager = TranslationManager()
        expected_mapping = {
            "English": "en",
            "Français": "fr",
            "Español": "es",
            "Deutsch": "de",
        }
        assert manager.language_mapping == expected_mapping

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

    def test_should_add_widget_to_registry_when_register_widget_is_called(self):
        """Test widget registration."""
        manager = TranslationManager()
        mock_widget = MagicMock()

        manager.register_widget(mock_widget, "Hello")
        assert mock_widget in manager._translatable_widgets

    def test_should_remove_widget_from_registry_when_unregister_widget_is_called(self):
        """Test widget unregistration."""
        manager = TranslationManager()
        mock_widget = MagicMock()

        # Register then unregister
        manager.register_widget(mock_widget, "Hello")
        manager.unregister_widget(mock_widget)
        assert mock_widget not in manager._translatable_widgets

    def test_should_clear_all_widgets_when_clear_registered_widgets_is_called(self):
        """Test clearing all registered widgets."""
        manager = TranslationManager()
        mock_widget1 = MagicMock()
        mock_widget2 = MagicMock()

        # Register multiple widgets
        manager.register_widget(mock_widget1, "Hello")
        manager.register_widget(mock_widget2, "World")
        assert len(manager._translatable_widgets) == 2

        # Clear all
        manager.clear_registered_widgets()
        assert len(manager._translatable_widgets) == 0

    def test_should_store_text_mapping_when_set_translatable_text_is_called(self):
        """Test setting translatable text for a widget."""
        manager = TranslationManager()
        mock_widget = MagicMock()

        manager.set_translatable_text(mock_widget, "Hello")
        assert manager._translatable_texts[mock_widget] == "Hello"

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
