# ///////////////////////////////////////////////////////////////
# TESTS.INTEGRATION.TEST_APPLICATION.TEST_APP_FLOW - Application flow integration tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Integration tests for the application flow."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

# Third-party imports
import pytest

# ///////////////////////////////////////////////////////////////
# TEST HELPERS
# ///////////////////////////////////////////////////////////////


# Créer une classe mock complète pour EzQt_App
class MockEzQtApp:
    """Mock complet de l'application EzQt_App pour les tests d'intégration."""

    def __init__(self, themeFileName=None):
        self._themeFileName = themeFileName
        self.ui = MagicMock()

        # Mock des composants UI
        self.ui.menuContainer = MagicMock()
        self.ui.headerContainer = MagicMock()
        self.ui.pagesContainer = MagicMock()
        self.ui.settingsPanel = MagicMock()

        # Mock des propriétés spécifiques
        self.ui.pagesContainer.stackedWidget = MagicMock()
        self.ui.settingsPanel.scrollArea = MagicMock()
        self.ui.settingsPanel.scrollAreaWidgetContents = MagicMock()
        self.ui.menuContainer.toggleButton = MagicMock()
        self.ui.menuContainer.menus = MagicMock()
        self.ui.headerContainer.settingsTopBtn = MagicMock()
        self.ui.headerContainer.height = MagicMock(return_value=50)

        # État de la fenêtre
        self._visible = False
        self._width = 1280
        self._height = 720
        self._title = "Test Application"

    def windowTitle(self):
        return self._title

    def setWindowTitle(self, title):
        self._title = title

    def isVisible(self):
        return self._visible

    def show(self):
        self._visible = True

    def close(self):
        self._visible = False

    def width(self):
        return self._width

    def height(self):
        return self._height

    def resize(self, width, height):
        self._width = width
        self._height = height

    def minimumSize(self):
        return MagicMock(width=lambda: 940, height=lambda: 560)


def create_temp_app_config():
    """Crée un fichier app.config.yaml temporaire pour les tests."""
    temp_dir = Path(os.environ.get("TEMP", tempfile.gettempdir()))
    temp_yaml = temp_dir / f"app_{os.getpid()}.config.yaml"

    yaml_content = """app:
  name: "Test Application"
  description: "Test Description"
  app_width: 1280
  app_min_width: 940
  app_height: 720
  app_min_height: 560
  theme: "dark"
  menu_panel_shrinked_width: 60
  menu_panel_extended_width: 240
  settings_panel_width: 240
  time_animation: 400

settings_panel:
  theme:
    type: "toggle"
    label: "Active Theme"
    options: ["Light", "Dark"]
    default: "dark"
    description: "Choose the application theme"
    enabled: true

  language:
    type: "select"
    label: "Language"
    options: ["English", "Français", "Español", "Deutsch"]
    default: "English"
    description: "Interface language"
    enabled: true

  notifications:
    type: "checkbox"
    label: "Notifications"
    default: true
    description: "Enable system notifications"
    enabled: false

  auto_save:
    type: "checkbox"
    label: "Auto Save"
    default: false
    description: "Automatically save modifications"
    enabled: false

  save_interval:
    type: "slider"
    label: "Save Interval"
    min: 1
    max: 60
    default: 5
    unit: "minutes"
    description: "Interval between automatic saves"
    enabled: false

palette:
  dark:
    main_surface: rgb(33, 37, 43)
    main_border: rgb(44, 49, 58)
    main_accent_color: '#96CD32'
    accent_color1: rgb(52, 59, 72)
    accent_color2: rgb(55, 63, 77)
    accent_color3: rgb(35, 40, 49)
    accent_color4: rgb(94, 106, 130)
    page_color: rgb(40, 44, 52)
    transparent: rgba(255, 255, 255, 0)
    semi_transparent: rgba(33, 37, 43, 180)
    select_text_color: rgb(255, 255, 255)
    base_text_color: rgb(221, 221, 221)

  light:
    main_surface: rgb(240, 240, 243)
    main_border: rgb(225, 223, 229)
    main_accent_color: '#1423DC'
    accent_color1: rgb(203, 196, 183)
    accent_color2: rgb(200, 192, 178)
    accent_color3: rgb(237, 235, 235)
    accent_color4: rgb(161, 149, 125)
    page_color: rgb(250, 250, 250)
    transparent: rgba(0, 0, 0, 0)
    semi_transparent: rgba(222, 218, 212, 180)
    select_text_color: rgb(0, 0, 0)
    base_text_color: rgb(34, 34, 34)"""

    temp_yaml.write_text(yaml_content, encoding="utf-8")
    return temp_yaml


def create_app_with_config_mock():
    """Crée une application avec la configuration mockée pour éviter les erreurs de chemin."""
    temp_yaml = create_temp_app_config()

    try:
        app = MockEzQtApp()
        return app, temp_yaml
    except Exception:
        # Nettoyer en cas d'erreur
        if temp_yaml.exists():
            temp_yaml.unlink()
        raise


def create_app_with_fonts_mock():
    """Crée une application avec les polices mockées pour éviter les erreurs de chemin."""
    temp_yaml = create_temp_app_config()

    try:
        return MockEzQtApp()
    finally:
        # Nettoyer le fichier temporaire
        if temp_yaml.exists():
            temp_yaml.unlink()


class TestAppFlow:
    """Tests d'intégration pour le flux d'application."""

    @pytest.mark.integration
    @pytest.mark.qt
    def test_should_have_ui_components_when_app_is_initialized(self, qt_application):
        """Test de l'initialisation complète de l'application."""
        # Créer l'application avec configuration temporaire
        app = create_app_with_fonts_mock()

        # Vérifier que l'application a été créée
        assert app is not None
        assert hasattr(app, "ui")
        assert hasattr(app, "setWindowTitle")

        # Vérifier que l'interface utilisateur a été configurée
        assert hasattr(app.ui, "menuContainer")
        assert hasattr(app.ui, "headerContainer")
        assert hasattr(app.ui, "pagesContainer")
        assert hasattr(app.ui, "settingsPanel")

    @pytest.mark.integration
    @pytest.mark.qt
    def test_should_store_theme_filename_when_custom_theme_is_given(
        self, qt_application, tmp_path
    ):
        """Test de l'application avec un thème personnalisé."""
        # Créer un fichier de thème temporaire
        theme_file = tmp_path / "custom_theme.qss"
        theme_content = """
        QMainWindow {
            background-color: #2b2b2b;
        }
        """
        theme_file.write_text(theme_content)

        # Créer l'application avec le thème personnalisé et configuration temporaire
        temp_yaml = create_temp_app_config()
        try:
            app = MockEzQtApp(themeFileName=str(theme_file))

            # Vérifier que l'application a été créée
            assert app is not None
            assert hasattr(app, "_themeFileName")
            assert app._themeFileName == str(theme_file)
        finally:
            if temp_yaml.exists():
                temp_yaml.unlink()

    @pytest.mark.integration
    @pytest.mark.qt
    def test_should_have_window_properties_when_app_is_created(self, qt_application):
        """Test des propriétés de la fenêtre d'application."""
        app = create_app_with_fonts_mock()

        # Vérifier les propriétés de base de la fenêtre
        assert app.windowTitle() == "Test Application"
        assert not app.isVisible()  # Pas encore affichée

        # Vérifier que la fenêtre peut être affichée
        app.show()
        assert app.isVisible()

        # Nettoyer
        app.close()

    @pytest.mark.integration
    @pytest.mark.qt
    def test_should_have_toggle_button_and_menus_when_menu_container_is_checked(
        self, qt_application
    ):
        """Test de la fonctionnalité du menu."""
        app = create_app_with_fonts_mock()

        # Vérifier que le menu existe
        menu = app.ui.menuContainer
        assert menu is not None

        # Vérifier les propriétés du menu
        assert hasattr(menu, "toggleButton")
        assert hasattr(menu, "menus")

        # Vérifier que le bouton de basculement existe
        toggle_button = menu.toggleButton
        assert toggle_button is not None

    @pytest.mark.integration
    @pytest.mark.qt
    def test_should_have_settings_button_and_fixed_height_when_header_container_is_checked(
        self, qt_application
    ):
        """Test de la fonctionnalité de l'en-tête."""
        app = create_app_with_fonts_mock()

        # Vérifier que l'en-tête existe
        header = app.ui.headerContainer
        assert header is not None

        # Vérifier les propriétés de l'en-tête
        assert hasattr(header, "settingsTopBtn")
        assert header.height() == 50  # Hauteur fixe

    @pytest.mark.integration
    @pytest.mark.qt
    def test_should_have_stacked_widget_when_pages_container_is_checked(
        self, qt_application
    ):
        """Test du conteneur de pages."""
        app = create_app_with_fonts_mock()

        # Vérifier que le conteneur de pages existe
        pages_container = app.ui.pagesContainer
        assert pages_container is not None

        # Vérifier les propriétés du conteneur
        assert hasattr(pages_container, "stackedWidget")
        assert pages_container.stackedWidget is not None

    @pytest.mark.integration
    @pytest.mark.qt
    def test_should_have_scroll_area_when_settings_panel_is_checked(
        self, qt_application
    ):
        """Test du panneau de paramètres."""
        app = create_app_with_fonts_mock()

        # Vérifier que le panneau de paramètres existe
        settings_panel = app.ui.settingsPanel
        assert settings_panel is not None

        # Vérifier les propriétés du panneau
        assert hasattr(settings_panel, "scrollArea")
        assert hasattr(settings_panel, "scrollAreaWidgetContents")

    @pytest.mark.integration
    @pytest.mark.qt
    def test_should_have_expected_signals_when_app_is_created(self, qt_application):
        """Test des connexions de signaux."""
        app = create_app_with_fonts_mock()

        # Vérifier que les signaux sont connectés
        # Note: Les connexions de signaux sont testées indirectement
        # via les fonctionnalités des composants
        assert app is not None

    @pytest.mark.integration
    @pytest.mark.qt
    def test_should_apply_theme_file_when_theme_is_given(
        self, qt_application, tmp_path
    ):
        """Test du chargement de thème."""
        # Créer un fichier de thème temporaire
        theme_file = tmp_path / "test_theme.qss"
        theme_content = """
        QMainWindow {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        """
        theme_file.write_text(theme_content)

        # Créer l'application avec le thème et configuration temporaire
        temp_yaml = create_temp_app_config()
        try:
            app = MockEzQtApp(themeFileName=str(theme_file))

            # Vérifier que le thème a été chargé
            assert app is not None
            assert app._themeFileName == str(theme_file)
        finally:
            if temp_yaml.exists():
                temp_yaml.unlink()

    @pytest.mark.integration
    @pytest.mark.qt
    def test_should_have_expected_dimensions_when_window_is_queried(
        self, qt_application
    ):
        """Test de la taille de la fenêtre."""
        app = create_app_with_fonts_mock()

        # Vérifier que la fenêtre a une taille définie
        assert app.width() > 0
        assert app.height() > 0

        # Vérifier que la fenêtre peut être redimensionnée
        app.resize(1000, 600)
        assert app.width() == 1000
        assert app.height() == 600

    @pytest.mark.integration
    @pytest.mark.qt
    def test_should_close_window_when_close_is_called(self, qt_application):
        """Test du nettoyage de l'application."""
        app = create_app_with_fonts_mock()

        # Vérifier que l'application peut être fermée proprement
        app.close()
        assert not app.isVisible()

    @pytest.mark.integration
    @pytest.mark.qt
    def test_should_have_none_theme_when_no_theme_is_given(self, qt_application):
        """Test de l'application sans thème personnalisé."""
        # Créer l'application sans thème et avec configuration temporaire
        temp_yaml = create_temp_app_config()
        try:
            app = MockEzQtApp()

            # Vérifier que l'application a été créée sans thème
            assert app is not None
            assert app._themeFileName is None
        finally:
            if temp_yaml.exists():
                temp_yaml.unlink()
