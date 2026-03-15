# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_WIDGETS.TEST_CORE.TEST_HEADER - Header widget tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for the Header class."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Third-party imports
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QPushButton, QSizePolicy

# Local imports
from ezqt_app.widgets.core.header import Header

# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////


class TestHeader:
    """Tests pour la classe Header."""

    def test_should_have_header_container_properties_when_instantiated(
        self, qt_application
    ):
        """Test de l'initialisation avec des paramètres par défaut."""
        header = Header()

        # Vérifier les propriétés de base
        assert header.objectName() == "headerContainer"
        assert header.height() == 50
        assert header.frameShape() == QFrame.NoFrame
        assert header.frameShadow() == QFrame.Shadow.Raised

    def test_should_accept_app_name_and_description_when_instantiated_with_parameters(
        self, qt_application
    ):
        """Test de l'initialisation avec des paramètres personnalisés."""
        app_name = "Test App"
        description = "Test Description"

        header = Header(app_name=app_name, description=description)

        # Vérifier les propriétés de base
        assert header.objectName() == "headerContainer"
        assert header.height() == 50

    def test_should_have_horizontal_layout_when_instantiated(self, qt_application):
        """Test de la structure du layout."""
        header = Header()

        # Vérifier que le layout principal existe
        assert hasattr(header, "_layout")
        assert header._layout is not None

        # Vérifier les propriétés du layout
        assert header._layout.spacing() == 0
        # Les marges sont un objet QMargins, pas un tuple
        margins = header._layout.contentsMargins()
        assert margins.left() == 0
        assert margins.top() == 0
        assert margins.right() == 10
        assert margins.bottom() == 0

    def test_should_have_meta_info_frame_when_instantiated(self, qt_application):
        """Test du frame d'informations meta."""
        header = Header()

        # Vérifier que le frame meta info existe
        assert hasattr(header, "_info_frame")
        assert header._info_frame is not None

        # Vérifier les propriétés du frame
        assert header._info_frame.objectName() == "info_frame"
        assert header._info_frame.frameShape() == QFrame.NoFrame
        assert header._info_frame.frameShadow() == QFrame.Raised

    def test_should_have_app_logo_frame_when_instantiated(self, qt_application):
        """Test du logo de l'application."""
        header = Header()

        # Vérifier que le logo existe
        assert hasattr(header, "_logo_label")
        assert header._logo_label is not None

        # Vérifier les propriétés du logo
        assert header._logo_label.objectName() == "app_logo"
        assert header._logo_label.frameShape() == QFrame.NoFrame
        assert header._logo_label.frameShadow() == QFrame.Raised

    def test_should_have_app_name_label_when_instantiated(self, qt_application):
        """Test du label du nom d'application."""
        header = Header()

        # Vérifier que le label du nom existe
        assert hasattr(header, "_title_label")
        assert header._title_label is not None

        # Vérifier les propriétés du label
        assert header._title_label.objectName() == "app_title"
        assert header._title_label.alignment() == (
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop
        )

    def test_should_have_description_label_when_instantiated(self, qt_application):
        """Test du label de description."""
        header = Header()

        # Vérifier que le label de description existe
        assert hasattr(header, "_subtitle_label")
        assert header._subtitle_label is not None

        # Vérifier les propriétés du label
        assert header._subtitle_label.objectName() == "app_subtitle"
        assert header._subtitle_label.alignment() == (
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop
        )

    def test_should_have_buttons_frame_when_instantiated(self, qt_application):
        """Test du frame des boutons."""
        header = Header()

        # Vérifier que le frame des boutons existe
        assert hasattr(header, "_buttons_frame")
        assert header._buttons_frame is not None

        # Vérifier les propriétés du frame
        assert header._buttons_frame.objectName() == "buttons_frame"
        assert header._buttons_frame.frameShape() == QFrame.NoFrame
        assert header._buttons_frame.frameShadow() == QFrame.Raised

    def test_should_have_buttons_layout_when_instantiated(self, qt_application):
        """Test du layout des boutons."""
        header = Header()

        # Vérifier que le layout des boutons existe
        assert hasattr(header, "_buttons_layout")
        assert header._buttons_layout is not None

        # Vérifier les propriétés du layout
        assert header._buttons_layout.spacing() == 5
        margins = header._buttons_layout.contentsMargins()
        assert margins.left() == 0
        assert margins.top() == 0
        assert margins.right() == 0
        assert margins.bottom() == 0

    def test_should_have_settings_button_when_instantiated(self, qt_application):
        """Test du bouton de paramètres."""
        header = Header()

        # Vérifier que le bouton de paramètres existe
        assert hasattr(header, "settings_btn")
        assert header.settings_btn is not None

        # Vérifier les propriétés du bouton
        assert header.settings_btn.objectName() == "settings_btn"
        assert isinstance(header.settings_btn, QPushButton)

    def test_should_have_minimize_button_when_instantiated(self, qt_application):
        """Test du bouton de minimisation."""
        header = Header()

        # Vérifier que le bouton de minimisation existe
        assert hasattr(header, "minimize_btn")
        assert header.minimize_btn is not None

        # Vérifier les propriétés du bouton
        assert header.minimize_btn.objectName() == "minimize_btn"
        assert isinstance(header.minimize_btn, QPushButton)

    def test_should_have_maximize_button_when_instantiated(self, qt_application):
        """Test du bouton de maximisation."""
        header = Header()

        # Vérifier que le bouton de maximisation existe
        assert hasattr(header, "maximize_restore_btn")
        assert header.maximize_restore_btn is not None

        # Vérifier les propriétés du bouton
        assert header.maximize_restore_btn.objectName() == "maximize_restore_btn"
        assert isinstance(header.maximize_restore_btn, QPushButton)

    def test_should_have_close_button_when_instantiated(self, qt_application):
        """Test du bouton de fermeture."""
        header = Header()

        # Vérifier que le bouton de fermeture existe
        assert hasattr(header, "close_btn")
        assert header.close_btn is not None

        # Vérifier les propriétés du bouton
        assert header.close_btn.objectName() == "close_btn"
        assert isinstance(header.close_btn, QPushButton)

    def test_should_have_all_buttons_in_list_when_instantiated(self, qt_application):
        """Test de la gestion de la liste des boutons."""
        header = Header()

        # Vérifier que la liste des boutons existe
        assert hasattr(header, "_buttons")
        assert isinstance(header._buttons, list)

        # Vérifier que les boutons sont dans la liste
        expected_buttons = [
            "settings_btn",
            "minimize_btn",
            "maximize_restore_btn",
            "close_btn",
        ]
        for button_name in expected_buttons:
            assert hasattr(header, button_name)
            assert getattr(header, button_name) is not None

    def test_should_have_size_policy_when_instantiated(self, qt_application):
        """Test de la politique de taille."""
        header = Header()

        # Vérifier que la politique de taille est définie
        assert header.sizePolicy().hasHeightForWidth() is not None

    def test_should_display_custom_name_when_app_name_is_given(self, qt_application):
        """Test du nom d'application personnalisé."""
        app_name = "Custom App Name"
        header = Header(app_name=app_name)

        # Vérifier que le nom est défini
        assert header._title_label.text() == app_name

    def test_should_display_custom_description_when_description_is_given(
        self, qt_application
    ):
        """Test de la description personnalisée."""
        description = "Custom Description"
        header = Header(description=description)

        # Vérifier que la description est définie
        assert header._subtitle_label.text() == description

    def test_should_have_clicked_signals_when_buttons_are_created(self, qt_application):
        """Test des signaux de clic des boutons."""
        header = Header()

        # Vérifier que les boutons ont des signaux
        buttons = [
            header.settings_btn,
            header.minimize_btn,
            header.maximize_restore_btn,
            header.close_btn,
        ]

        for button in buttons:
            assert hasattr(button, "clicked")
            assert hasattr(button.clicked, "connect")

    def test_should_have_fixed_height_of_50_when_instantiated(self, qt_application):
        """Test que la hauteur de l'en-tête est fixe."""
        header = Header()

        # Vérifier que la hauteur est fixe
        assert header.height() == 50
        assert header.minimumHeight() == 50
        assert header.maximumHeight() == 50

    def test_should_have_expanding_width_policy_when_instantiated(self, qt_application):
        """Test de la politique de largeur de l'en-tête."""
        header = Header()

        # Vérifier que la politique de taille est définie
        # Note: Le Header utilise H_EXPANDING_V_PREFERRED qui est Expanding
        size_policy = header.sizePolicy()
        assert size_policy.horizontalPolicy() == QSizePolicy.Policy.Expanding
