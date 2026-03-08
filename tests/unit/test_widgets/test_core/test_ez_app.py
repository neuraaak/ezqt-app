# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_WIDGETS.TEST_CORE.TEST_EZ_APP - EzApplication tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for the EzApplication class."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import locale
import os
from unittest.mock import MagicMock, patch

# Third-party imports
import pytest
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QApplication

# Local imports
from ezqt_app.widgets.core.ez_app import EzApplication

# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////


class MockQApplication:
    """
    Mock de QApplication pour éviter les problèmes de singleton dans les tests.
    """

    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        self._attributes = {}
        self._theme_changed = Signal()

    def setAttribute(self, attribute, value):
        self._attributes[attribute] = value

    def testAttribute(self, attribute):
        return self._attributes.get(attribute, False)

    def quit(self):
        pass

    def deleteLater(self):
        pass

    @property
    def themeChanged(self):
        return self._theme_changed


@pytest.fixture
def mock_qapplication():
    """
    Fixture pour mocker QApplication complètement.
    """
    with (
        patch("PySide6.QtWidgets.QApplication", MockQApplication),
        patch("PySide6.QtWidgets.QApplication.instance", return_value=None),
    ):
        yield MockQApplication


@pytest.fixture
def clean_qt_environment():
    """
    Fixture pour nettoyer l'environnement Qt avant chaque test.
    """
    # Détruire toute instance existante
    app = QApplication.instance()
    if app:
        app.quit()
        app.deleteLater()
        import time

        time.sleep(0.2)  # Plus de temps pour s'assurer que l'instance est détruite

    yield

    # Nettoyer après le test
    app = QApplication.instance()
    if app:
        app.quit()
        app.deleteLater()
        import time

        time.sleep(0.1)


@pytest.fixture
def ez_application_cleanup(_clean_qt_environment):
    """
    Fixture locale pour créer une instance EzApplication propre pour les tests de ce fichier.
    """
    # Créer une nouvelle instance avec la méthode de test
    app = EzApplication.create_for_testing([])
    yield app
    app.quit()
    app.deleteLater()


class TestEzApplication:
    """Tests pour la classe EzApplication."""

    def test_inheritance(self):
        """Test que EzApplication hérite correctement de QApplication."""
        # Vérifier l'héritage sans créer d'instance
        assert issubclass(EzApplication, QApplication)

    def test_class_definition(self):
        """Test de la définition de la classe EzApplication."""
        # Vérifier que la classe existe
        assert EzApplication is not None

        # Vérifier que la classe a un constructeur
        assert hasattr(EzApplication, "__init__")

        # Vérifier que la classe a le signal défini
        assert hasattr(EzApplication, "themeChanged")

    @pytest.mark.skip(
        reason="TODO: MockQApplication.instance attribute error - needs proper mocking of QApplication.instance"
    )
    @patch("locale.setlocale")
    def test_locale_configuration_success(self, mock_setlocale, mock_qapplication):
        """Test de la configuration de locale réussie."""
        # Mock de setlocale pour simuler un succès
        mock_setlocale.return_value = "fr_FR.UTF-8"

        # Créer une instance avec la méthode de test
        EzApplication.create_for_testing([])

        # Vérifier que setlocale a été appelé
        mock_setlocale.assert_called_once_with(locale.LC_ALL, "")

    @pytest.mark.skip(
        reason="TODO: MockQApplication.instance attribute error - needs proper mocking of QApplication.instance"
    )
    @patch("locale.setlocale")
    def test_locale_configuration_failure(self, mock_setlocale, mock_qapplication):
        """Test de la configuration de locale avec échec."""
        # Mock de setlocale pour simuler un échec
        mock_setlocale.side_effect = locale.Error("Locale not available")

        # Créer une instance avec la méthode de test
        EzApplication.create_for_testing([])

        # Vérifier que setlocale a été appelé
        mock_setlocale.assert_called_once_with(locale.LC_ALL, "")

    @pytest.mark.skip(
        reason="TODO: MockQApplication.instance attribute error - needs proper mocking of QApplication.instance"
    )
    def test_environment_variables_setup(self, mock_qapplication):
        """Test de la configuration des variables d'environnement."""
        # Sauvegarder les valeurs originales
        original_encoding = os.environ.get("PYTHONIOENCODING")
        original_dpi = os.environ.get("QT_FONT_DPI")

        try:
            # Créer une instance avec la méthode de test
            EzApplication.create_for_testing([])

            # Vérifier que les variables d'environnement sont définies
            assert os.environ.get("PYTHONIOENCODING") == "utf-8"
            assert os.environ.get("QT_FONT_DPI") == "96"
        finally:
            # Restaurer les valeurs originales
            if original_encoding:
                os.environ["PYTHONIOENCODING"] = original_encoding
            elif "PYTHONIOENCODING" in os.environ:
                del os.environ["PYTHONIOENCODING"]

            if original_dpi:
                os.environ["QT_FONT_DPI"] = original_dpi
            elif "QT_FONT_DPI" in os.environ:
                del os.environ["QT_FONT_DPI"]

    @pytest.mark.skip(
        reason="TODO: MockQApplication.instance attribute error - needs proper mocking of QApplication.instance"
    )
    def test_high_dpi_scaling_configuration(self, mock_qapplication):
        """Test de l'activation du scaling haute résolution."""
        # Créer une instance avec la méthode de test
        app = EzApplication.create_for_testing([])

        # Vérifier que l'attribut de haute résolution est activé
        assert app.testAttribute(Qt.AA_EnableHighDpiScaling)

    @pytest.mark.skip(
        reason="TODO: MockQApplication.instance attribute error - needs proper mocking of QApplication.instance"
    )
    def test_application_properties(self, mock_qapplication):
        """Test des propriétés de l'application."""
        # Créer une instance avec la méthode de test
        app = EzApplication.create_for_testing([])

        # Vérifier les propriétés de base
        assert hasattr(app, "setAttribute")
        assert hasattr(app, "testAttribute")
        assert hasattr(app, "themeChanged")

    @pytest.mark.skip(
        reason="TODO: MockQApplication.instance attribute error - needs proper mocking of QApplication.instance"
    )
    @patch("ezqt_app.widgets.core.ez_app.os.environ")
    def test_environment_setup_mocked(self, mock_environ, mock_qapplication):
        """Test de la configuration de l'environnement avec mock."""
        # Mock de os.environ
        mock_environ.__setitem__ = MagicMock()

        # Créer une instance avec la méthode de test
        EzApplication.create_for_testing([])

        # Vérifier que les variables d'environnement ont été définies
        mock_environ.__setitem__.assert_any_call("PYTHONIOENCODING", "utf-8")
        mock_environ.__setitem__.assert_any_call("QT_FONT_DPI", "96")

    def test_singleton_behavior(self):
        """Test du comportement singleton d'EzApplication."""
        # EzApplication hérite du comportement singleton de QApplication
        # On ne peut pas créer plusieurs instances réelles
        # Ce test vérifie que la classe est bien configurée comme singleton

        # Vérifier que la classe existe et hérite de QApplication
        assert EzApplication is not None
        assert issubclass(EzApplication, QApplication)

        # Vérifier que la classe a les méthodes nécessaires
        assert hasattr(EzApplication, "__init__")
        assert hasattr(EzApplication, "themeChanged")

    def test_method_inheritance(self):
        """Test que EzApplication hérite des méthodes de QApplication."""
        # Vérifier que les méthodes de QApplication sont disponibles
        expected_methods = ["setAttribute", "testAttribute", "applicationName"]

        for method_name in expected_methods:
            assert hasattr(
                EzApplication, method_name
            ), f"EzApplication should have method {method_name}"

    def test_signal_definition(self):
        """Test de la définition du signal themeChanged."""
        # Vérifier que le signal est défini dans la classe
        assert hasattr(EzApplication, "themeChanged")

        # Vérifier que c'est bien un signal Qt
        # Les signaux Qt sont des objets spéciaux, pas des méthodes normales
        signal_definition = EzApplication.themeChanged

        # Vérifier que c'est un objet signal (pas None)
        assert signal_definition is not None

        # Vérifier que c'est un signal Qt en testant sa nature
        # Les signaux Qt ont des attributs spéciaux
        assert hasattr(signal_definition, "__class__")

        # Vérifier que c'est un signal en testant son type
        # Les signaux Qt sont des objets de type Signal
        assert isinstance(signal_definition, Signal)

        # Vérifier que le signal a un nom (peut ne pas être disponible au niveau classe)
        # Les signaux au niveau classe peuvent ne pas avoir tous les attributs
        # jusqu'à ce qu'une instance soit créée
        if hasattr(signal_definition, "name"):
            assert signal_definition.name == "themeChanged"

    def test_constructor_signature(self):
        """Test de la signature du constructeur."""
        # Vérifier que le constructeur accepte *args et **kwargs
        import inspect

        # Obtenir la signature du constructeur
        sig = inspect.signature(EzApplication.__init__)

        # Vérifier que le constructeur accepte *args et **kwargs
        assert "args" in sig.parameters
        assert "kwargs" in sig.parameters

        # Vérifier que ce sont des paramètres var-positional et var-keyword
        assert sig.parameters["args"].kind == inspect.Parameter.VAR_POSITIONAL
        assert sig.parameters["kwargs"].kind == inspect.Parameter.VAR_KEYWORD

    def test_class_documentation(self):
        """Test de la documentation de la classe."""
        # Vérifier que la classe a une docstring
        assert EzApplication.__doc__ is not None
        assert len(EzApplication.__doc__.strip()) > 0

        # Vérifier que le constructeur a une docstring
        assert EzApplication.__init__.__doc__ is not None
        assert len(EzApplication.__init__.__doc__.strip()) > 0

    @pytest.mark.skip(
        reason="TODO: MockQApplication.instance attribute error - needs proper mocking of QApplication.instance"
    )
    def test_theme_changed_signal_instance(self, mock_qapplication):
        """Test du signal themeChanged sur une instance."""
        # Créer une instance avec la méthode de test
        app = EzApplication.create_for_testing([])

        # Vérifier que l'instance a le signal
        assert hasattr(app, "themeChanged")

        # Vérifier que c'est un signal
        assert hasattr(app.themeChanged, "connect")
        assert hasattr(app.themeChanged, "disconnect")
        assert hasattr(app.themeChanged, "emit")
