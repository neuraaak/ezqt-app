# ///////////////////////////////////////////////////////////////
# TESTS.INTEGRATION.TEST_SERVICES.TEST_TRANSLATIONS - Translation integration tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Integration tests for the translation system."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from unittest.mock import MagicMock, patch

# Third-party imports
import pytest

# Local imports
from ezqt_app.services.translation import (
    TranslationManager,
    change_language,
    get_available_languages,
    get_current_language,
    get_translation_manager,
    register_tr,
    set_tr,
    tr,
    unregister_tr,
)

# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////


class TestTranslationSystem:
    """Tests d'intégration pour le système de traduction."""

    @pytest.mark.integration
    def test_translation_manager_integration(
        self, qt_application, mock_translation_files
    ):
        """Test d'intégration du gestionnaire de traduction."""
        # Créer le gestionnaire de traduction
        manager = TranslationManager()

        # Vérifier l'état initial
        assert manager.get_current_language_code() == "en"
        assert manager.get_current_language_name() == "English"

        # Vérifier les langues disponibles
        languages = manager.get_available_languages()
        expected_languages = ["en", "fr", "es", "de"]
        for lang in expected_languages:
            assert lang in languages

    @pytest.mark.integration
    def test_translation_helpers_integration(self, qt_application):
        """Test d'intégration des helpers de traduction."""
        # Vérifier que les fonctions helper existent
        assert callable(tr)
        assert callable(set_tr)
        assert callable(register_tr)
        assert callable(unregister_tr)
        assert callable(change_language)
        assert callable(get_available_languages)
        assert callable(get_current_language)

    @pytest.mark.integration
    def test_language_change_workflow(self, qt_application):
        """Test du workflow de changement de langue."""
        # Créer le gestionnaire de traduction
        manager = TranslationManager()

        # Vérifier l'état initial
        assert manager.get_current_language_code() == "en"

        # Changer la langue
        with patch("ezqt_app.services.translation.manager.QCoreApplication"):
            success = manager.load_language_by_code("fr")
            assert success
            assert manager.get_current_language_code() == "fr"

    @pytest.mark.integration
    def test_widget_registration_workflow(self, qt_application):
        """Test du workflow d'enregistrement de widgets."""
        # Créer le gestionnaire de traduction
        manager = TranslationManager()

        # Créer un widget mock
        mock_widget = MagicMock()
        original_text = "Hello World"

        # Enregistrer le widget
        manager.register_widget(mock_widget, original_text)

        # Vérifier que le widget est enregistré
        assert mock_widget in manager._translatable_widgets
        assert manager._translatable_texts[mock_widget] == original_text

        # Désenregistrer le widget
        manager.unregister_widget(mock_widget)

        # Vérifier que le widget est désenregistré
        assert mock_widget not in manager._translatable_widgets
        assert mock_widget not in manager._translatable_texts

    @pytest.mark.integration
    def test_translation_text_workflow(self, qt_application):
        """Test du workflow de traduction de texte."""
        # Créer le gestionnaire de traduction
        manager = TranslationManager()

        # Tester la traduction de texte
        text = "Hello World"
        translated = manager.translate(text)

        # Sans fichier de traduction, le texte original devrait être retourné
        assert translated == text

    @pytest.mark.integration
    def test_multiple_language_changes(self, qt_application):
        """Test de multiples changements de langue."""
        # Créer le gestionnaire de traduction
        manager = TranslationManager()

        # Changer vers plusieurs langues
        languages_to_test = ["en", "fr", "es", "de"]

        for lang_code in languages_to_test:
            with patch("ezqt_app.services.translation.manager.QCoreApplication"):
                success = manager.load_language_by_code(lang_code)
                assert success
                assert manager.get_current_language_code() == lang_code

    @pytest.mark.integration
    def test_widget_retranslation_workflow(self, qt_application):
        """Test du workflow de retraduction des widgets."""
        # Créer le gestionnaire de traduction
        manager = TranslationManager()

        # Créer plusieurs widgets mock
        widgets = []
        texts = ["Hello", "World", "Test"]

        for _i, text in enumerate(texts):
            mock_widget = MagicMock()
            manager.register_widget(mock_widget, text)
            widgets.append(mock_widget)

        # Vérifier que tous les widgets sont enregistrés
        assert len(manager._translatable_widgets) == 3

        # Nettoyer tous les widgets
        manager.clear_registered_widgets()

        # Vérifier que tous les widgets sont désenregistrés
        assert len(manager._translatable_widgets) == 0
        assert len(manager._translatable_texts) == 0

    @pytest.mark.integration
    def test_translation_signal_workflow(self, qt_application):
        """Test du workflow des signaux de traduction."""
        # Créer le gestionnaire de traduction
        manager = TranslationManager()

        # Variable pour capturer le signal
        signal_received = False
        received_language = None

        def on_language_changed(lang):
            nonlocal signal_received, received_language
            signal_received = True
            received_language = lang

        # Connecter le signal
        manager.languageChanged.connect(on_language_changed)

        # Changer la langue
        with patch("ezqt_app.services.translation.manager.QCoreApplication"):
            manager.load_language_by_code("fr")

        # Vérifier que le signal a été émis
        assert signal_received
        assert received_language == "fr"

    @pytest.mark.integration
    def test_translation_file_loading_workflow(
        self, qt_application, mock_translation_files
    ):
        """Test du workflow de chargement de fichiers de traduction."""
        # Créer le gestionnaire de traduction
        manager = TranslationManager()

        # Forcer le dossier de traductions vers le mock
        manager.translations_dir = mock_translation_files

        # Vérifier que le dossier de traductions est correct
        assert manager.translations_dir == mock_translation_files

        # Vérifier que les fichiers de traduction existent
        en_file = mock_translation_files / "ezqt_app_en.ts"
        fr_file = mock_translation_files / "ezqt_app_fr.ts"

        assert en_file.exists()
        assert fr_file.exists()

    @pytest.mark.integration
    def test_translation_mapping_workflow(self, qt_application):
        """Test du workflow de mapping des langues."""
        # Créer le gestionnaire de traduction
        manager = TranslationManager()

        # Vérifier le mapping des langues
        expected_mapping = {
            "English": "en",
            "Français": "fr",
            "Español": "es",
            "Deutsch": "de",
        }

        assert manager.language_mapping == expected_mapping

        # Tester la conversion de noms vers codes
        for name, code in expected_mapping.items():
            # Simuler le chargement d'une langue par nom
            with patch("ezqt_app.services.translation.manager.QCoreApplication"):
                success = manager.load_language(name)
                assert success
                assert manager.get_current_language_code() == code

    @pytest.mark.integration
    def test_translation_error_handling(self, qt_application):
        """Test de la gestion d'erreurs de traduction."""
        # Créer le gestionnaire de traduction
        manager = TranslationManager()

        # Tester avec une langue invalide en utilisant directement load_language_by_code
        with (
            patch("ezqt_app.services.translation.manager.QCoreApplication"),
            patch.object(manager, "translations_dir") as mock_dir,
        ):
            # Simuler que le dossier existe mais qu'aucun fichier de traduction n'est trouvé
            mock_dir.exists.return_value = True
            mock_dir.glob.return_value = []  # Aucun fichier trouvé

            # Tester avec un code de langue invalide directement
            success = manager.load_language_by_code("invalid_lang")
            # Devrait retourner False car aucun fichier de traduction n'est trouvé
            assert not success

    @pytest.mark.integration
    def test_translation_manager_singleton_behavior(self, qt_application):
        """Test du comportement singleton du gestionnaire de traduction."""
        # Utiliser la fonction singleton pour obtenir le gestionnaire

        # Obtenir plusieurs références au gestionnaire singleton
        manager1 = get_translation_manager()
        manager2 = get_translation_manager()

        # Vérifier que ce sont les mêmes instances (singleton)
        assert manager1 is manager2

        # Elles partagent les mêmes données de base
        assert manager1.language_mapping == manager2.language_mapping
        assert manager1.get_available_languages() == manager2.get_available_languages()

    @pytest.mark.integration
    def test_translation_text_setting_workflow(self, qt_application):
        """Test du workflow de définition de texte traduisible."""
        # Créer le gestionnaire de traduction
        manager = TranslationManager()

        # Créer un widget mock
        mock_widget = MagicMock()

        # Définir un texte traduisible
        text = "New Text"
        manager.set_translatable_text(mock_widget, text)

        # Vérifier que le widget est enregistré avec le nouveau texte
        assert mock_widget in manager._translatable_widgets
        assert manager._translatable_texts[mock_widget] == text

    @pytest.mark.integration
    def test_translation_manager_cleanup(self, qt_application):
        """Test du nettoyage du gestionnaire de traduction."""
        # Créer le gestionnaire de traduction
        manager = TranslationManager()

        # Ajouter des widgets
        widgets = []
        for i in range(5):
            mock_widget = MagicMock()
            manager.register_widget(mock_widget, f"Text {i}")
            widgets.append(mock_widget)

        # Vérifier que les widgets sont enregistrés
        assert len(manager._translatable_widgets) == 5

        # Nettoyer
        manager.clear_registered_widgets()

        # Vérifier que tout est nettoyé
        assert len(manager._translatable_widgets) == 0
        assert len(manager._translatable_texts) == 0

    @pytest.mark.integration
    def test_translation_manager_persistence(self, qt_application):
        """Test de la persistance des données de traduction."""
        # Utiliser la fonction singleton pour obtenir le gestionnaire

        # Créer le gestionnaire de traduction
        manager = get_translation_manager()

        # Changer la langue
        with patch("ezqt_app.services.translation.manager.QCoreApplication"):
            manager.load_language_by_code("fr")

        # Vérifier que la langue est persistante
        assert manager.get_current_language_code() == "fr"
        assert manager.get_current_language_name() == "Français"

        # Obtenir une nouvelle référence au même gestionnaire singleton
        manager2 = get_translation_manager()
        assert manager2.get_current_language_code() == "fr"
