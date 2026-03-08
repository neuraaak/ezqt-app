# ///////////////////////////////////////////////////////////////

"""
Unit tests for the TranslationManager.
"""

from unittest.mock import MagicMock, patch

from ezqt_app.services.translation.manager import TranslationManager


class TestTranslationManager:
    """Tests for the TranslationManager class."""

    def test_init_default_language(self):
        """Test initialization with default language."""
        manager = TranslationManager()
        assert manager.current_language == "en"
        assert manager.translator is not None
        assert len(manager._translatable_widgets) == 0
        assert len(manager._translatable_texts) == 0

    def test_language_mapping(self):
        """Test language mapping."""
        manager = TranslationManager()
        expected_mapping = {
            "English": "en",
            "Français": "fr",
            "Español": "es",
            "Deutsch": "de",
        }
        assert manager.language_mapping == expected_mapping

    def test_get_available_languages(self):
        """Test retrieval of available languages."""
        manager = TranslationManager()
        languages = manager.get_available_languages()

        # Check that it's a list
        assert isinstance(languages, list)

        # v6 now returns language codes defined in SUPPORTED_LANGUAGES keys.
        expected_languages = ["en", "fr", "es", "de"]
        for lang in expected_languages:
            assert lang in languages

    def test_get_current_language_code(self):
        """Test retrieval of current language code."""
        manager = TranslationManager()
        assert manager.get_current_language_code() == "en"

    def test_get_current_language_name(self):
        """Test retrieval of current language name."""
        manager = TranslationManager()
        assert manager.get_current_language_name() == "English"

    def test_translate_text_no_translation(self):
        """Test text translation without available translation."""
        manager = TranslationManager()
        text = "Hello World"
        translated = manager.translate(text)
        assert translated == text  # Returns original text if no translation

    @patch("ezqt_app.services.translation.manager.QTranslator")
    def test_load_language_success(self, mock_translator):
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
    def test_load_language_failure(self, mock_exists, mock_qcore, mock_translator):
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

    def test_register_widget(self):
        """Test widget registration."""
        manager = TranslationManager()
        mock_widget = MagicMock()

        manager.register_widget(mock_widget, "Hello")
        assert mock_widget in manager._translatable_widgets

    def test_unregister_widget(self):
        """Test widget unregistration."""
        manager = TranslationManager()
        mock_widget = MagicMock()

        # Register then unregister
        manager.register_widget(mock_widget, "Hello")
        manager.unregister_widget(mock_widget)
        assert mock_widget not in manager._translatable_widgets

    def test_clear_registered_widgets(self):
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

    def test_set_translatable_text(self):
        """Test setting translatable text for a widget."""
        manager = TranslationManager()
        mock_widget = MagicMock()

        manager.set_translatable_text(mock_widget, "Hello")
        assert manager._translatable_texts[mock_widget] == "Hello"

    @patch("ezqt_app.services.translation.manager.QCoreApplication")
    def test_load_language_by_code(self, mock_qcore):
        """Test loading language by code."""
        manager = TranslationManager()

        # Mock QCoreApplication methods
        mock_qcore.removeTranslator = MagicMock()
        mock_qcore.installTranslator = MagicMock()

        # Test loading by code
        result = manager.load_language_by_code("fr")
        assert result
        assert manager.get_current_language_code() == "fr"

    def test_language_changed_signal(self, qt_application):
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
