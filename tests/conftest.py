# ///////////////////////////////////////////////////////////////
# CONFTEST - Pytest Configuration
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Pytest configuration for ezqt_app tests.

This module contains pytest fixtures and shared configuration.
"""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import shutil
import sys
import uuid
from pathlib import Path

# Third-party imports
import pytest
from PySide6.QtCore import QTimer, Signal
from PySide6.QtWidgets import QApplication


@pytest.fixture(scope="session")
def qt_application():
    """
    Fixture pour créer une instance QApplication pour tous les tests.
    Nécessaire pour tester les widgets Qt avec support des thèmes.
    """
    # ////// CRÉER L'APPLICATION QT
    # Utiliser EzApplication directement pour éviter les warnings High DPI
    from ezqt_app.widgets.core.ez_app import EzApplication

    app = QApplication.instance()
    if app is None:
        app = EzApplication(sys.argv)
    elif not isinstance(app, EzApplication):
        # Si une instance QApplication existe mais n'est pas EzApplication, la détruire
        app.quit()
        app.deleteLater()
        app = EzApplication(sys.argv)

    # ////// AJOUTER LE SIGNAL THEMECHANGED SI IL N'EXISTE PAS
    if not hasattr(app, "themeChanged"):
        # Créer un signal correctement configuré
        from PySide6.QtCore import QObject

        class SignalObject(QObject):
            themeChanged = Signal()

        signal_object = SignalObject()
        app.themeChanged = signal_object.themeChanged

    # ////// INITIALISER LES COMPOSANTS NÉCESSAIRES POUR LES TESTS
    try:
        from ezqt_app.services.ui import Fonts, SizePolicy

        Fonts.initFonts()
        SizePolicy.initSizePolicy()
    except ImportError:
        # Si les modules ne sont pas disponibles, continuer sans initialisation
        pass

    yield app

    # ////// NETTOYAGE APRÈS LES TESTS
    # Ne pas quitter l'application ici car elle peut être utilisée par d'autres tests
    # app.quit()


@pytest.fixture
def qt_widget_cleanup(qt_application):
    """
    Fixture pour nettoyer les widgets après chaque test.
    """
    yield qt_application

    # ////// FORCER LE NETTOYAGE DES WIDGETS
    qt_application.processEvents()


@pytest.fixture
def ez_application_cleanup():
    """
    Fixture pour créer une instance EzApplication propre pour les tests.
    Cette fixture contourne le problème de singleton en utilisant des mocks appropriés.
    """
    import time

    from PySide6.QtWidgets import QApplication

    from ezqt_app.widgets.core.ez_app import EzApplication

    # Détruire toute instance existante
    app = QApplication.instance()
    if app:
        app.quit()
        app.deleteLater()
        time.sleep(0.1)

        # Vérifier que l'instance a bien été détruite
        if QApplication.instance():
            QApplication.instance().quit()
            QApplication.instance().deleteLater()
            time.sleep(0.1)

    # Utiliser la méthode create_for_testing qui gère mieux les instances
    app = EzApplication.create_for_testing([])
    yield app

    # Nettoyer l'instance
    app.quit()
    app.deleteLater()
    time.sleep(0.1)


@pytest.fixture
def wait_for_signal(qt_application):
    """
    Fixture pour attendre qu'un signal soit émis.
    """

    def _wait_for_signal(signal, timeout=1000):
        """Attendre qu'un signal soit émis avec un timeout."""
        timer = QTimer()
        timer.setSingleShot(True)
        timer.start(timeout)

        # ////// CONNECTER LE SIGNAL À UN SLOT QUI ARRÊTE LE TIMER
        def stop_timer():
            timer.stop()

        signal.connect(stop_timer)

        # ////// ATTENDRE QUE LE TIMER S'ARRÊTE
        while timer.isActive():
            qt_application.processEvents()

        return not timer.isActive()

    return _wait_for_signal


@pytest.fixture
def mock_icon_path(tmp_path):
    """
    Fixture pour créer un chemin d'icône temporaire.
    """
    icon_file = tmp_path / "test_icon.png"
    # ////// CRÉER UN FICHIER D'ICÔNE TEMPORAIRE SIMPLE
    with open(icon_file, "wb") as f:
        # ////// EN-TÊTE PNG MINIMAL
        f.write(
            b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf5\xc7\xd3\xf7\x00\x00\x00\x00IEND\xaeB`\x82"
        )

    return str(icon_file)


@pytest.fixture
def mock_svg_path(tmp_path):
    """
    Fixture pour créer un fichier SVG temporaire.
    """
    svg_file = tmp_path / "test_icon.svg"
    # ////// CRÉER UN FICHIER SVG TEMPORAIRE SIMPLE
    svg_content = """<?xml version="1.0" encoding="UTF-8"?>
<svg width="16" height="16" xmlns="http://www.w3.org/2000/svg">
    <rect width="16" height="16" fill="red"/>
</svg>"""

    with open(svg_file, "w", encoding="utf-8") as f:
        f.write(svg_content)

    return str(svg_file)


@pytest.fixture
def mock_translation_files(tmp_path):
    """
    Fixture pour créer des fichiers de traduction temporaires.
    """
    translations_dir = tmp_path / "translations"
    translations_dir.mkdir()

    # Fichier de traduction anglais
    en_file = translations_dir / "ezqt_app_en.ts"
    en_content = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="en_US">
<context>
    <name>MainWindow</name>
    <message>
        <source>Hello</source>
        <translation>Hello</translation>
    </message>
    <message>
        <source>Settings</source>
        <translation>Settings</translation>
    </message>
</context>
</TS>"""

    with open(en_file, "w", encoding="utf-8") as f:
        f.write(en_content)

    # Fichier de traduction français
    fr_file = translations_dir / "ezqt_app_fr.ts"
    fr_content = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="fr_FR">
<context>
    <name>MainWindow</name>
    <message>
        <source>Hello</source>
        <translation>Bonjour</translation>
    </message>
    <message>
        <source>Settings</source>
        <translation>Paramètres</translation>
    </message>
</context>
</TS>"""

    with open(fr_file, "w", encoding="utf-8") as f:
        f.write(fr_content)

    return translations_dir


@pytest.fixture
def mock_yaml_config(tmp_path):
    """
    Fixture pour créer un fichier de configuration YAML temporaire.
    """
    config_file = tmp_path / "app.config.yaml"
    config_content = """app:
  name: "Test Application"
  description: "Test Description"

settings_panel:
  theme:
    default: "dark"
    enabled: true
  language:
    type: "select"
    label: "Language"
    description: "Select application language"
    options: ["English", "Français", "Español"]
    default: "English"
    enabled: true
  animation:
    type: "toggle"
    label: "Enable Animations"
    description: "Enable UI animations"
    default: true
    enabled: true"""

    with open(config_file, "w", encoding="utf-8") as f:
        f.write(config_content)

        return config_file


@pytest.fixture
def temp_project_root() -> Path:
    """Create an ephemeral project root under .tmp/ for config-writing tests."""
    project_root = Path.cwd() / ".tmp" / f"pytest-{uuid.uuid4().hex}"
    (project_root / "bin" / "config").mkdir(parents=True, exist_ok=True)
    try:
        yield project_root
    finally:
        shutil.rmtree(project_root, ignore_errors=True)


@pytest.fixture(autouse=True)
def isolate_config_service_root(temp_project_root: Path):
    """Route singleton config reads/writes to a per-test .tmp project root."""
    from ezqt_app.services._registry import ServiceRegistry
    from ezqt_app.services.config.config_service import ConfigService

    config = ConfigService()
    config.set_project_root(temp_project_root)
    ServiceRegistry.register(ConfigService, config)

    try:
        yield
    finally:
        ServiceRegistry.reset(ConfigService)
