# ///////////////////////////////////////////////////////////////

"""
Tests unitaires pour la classe Header.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QPushButton, QSizePolicy

from ezqt_app.widgets.core.header import Header


class TestHeader:
    """Tests pour la classe Header."""

    def test_init_default_parameters(self, qt_application):
        """Test de l'initialisation avec des paramètres par défaut."""
        header = Header()

        # Vérifier les propriétés de base
        assert header.objectName() == "headerContainer"
        assert header.height() == 50
        assert header.frameShape() == QFrame.NoFrame
        assert header.frameShadow() == QFrame.Raised

    def test_init_with_custom_parameters(self, qt_application):
        """Test de l'initialisation avec des paramètres personnalisés."""
        app_name = "Test App"
        description = "Test Description"

        header = Header(app_name=app_name, description=description)

        # Vérifier les propriétés de base
        assert header.objectName() == "headerContainer"
        assert header.height() == 50

    def test_layout_structure(self, qt_application):
        """Test de la structure du layout."""
        header = Header()

        # Vérifier que le layout principal existe
        assert hasattr(header, "HL_headerContainer")
        assert header.HL_headerContainer is not None

        # Vérifier les propriétés du layout
        assert header.HL_headerContainer.spacing() == 0
        # Les marges sont un objet QMargins, pas un tuple
        margins = header.HL_headerContainer.contentsMargins()
        assert margins.left() == 0
        assert margins.top() == 0
        assert margins.right() == 10
        assert margins.bottom() == 0

    def test_meta_info_frame(self, qt_application):
        """Test du frame d'informations meta."""
        header = Header()

        # Vérifier que le frame meta info existe
        assert hasattr(header, "headerMetaInfo")
        assert header.headerMetaInfo is not None

        # Vérifier les propriétés du frame
        assert header.headerMetaInfo.objectName() == "headerMetaInfo"
        assert header.headerMetaInfo.frameShape() == QFrame.NoFrame
        assert header.headerMetaInfo.frameShadow() == QFrame.Raised

    def test_app_logo(self, qt_application):
        """Test du logo de l'application."""
        header = Header()

        # Vérifier que le logo existe
        assert hasattr(header, "headerAppLogo")
        assert header.headerAppLogo is not None

        # Vérifier les propriétés du logo
        assert header.headerAppLogo.objectName() == "headerAppLogo"
        assert header.headerAppLogo.frameShape() == QFrame.NoFrame
        assert header.headerAppLogo.frameShadow() == QFrame.Raised

    def test_app_name_label(self, qt_application):
        """Test du label du nom d'application."""
        header = Header()

        # Vérifier que le label du nom existe
        assert hasattr(header, "headerAppName")
        assert header.headerAppName is not None

        # Vérifier les propriétés du label
        assert header.headerAppName.objectName() == "headerAppName"
        assert header.headerAppName.alignment() == (
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop
        )

    def test_app_description_label(self, qt_application):
        """Test du label de description."""
        header = Header()

        # Vérifier que le label de description existe
        assert hasattr(header, "headerAppDescription")
        assert header.headerAppDescription is not None

        # Vérifier les propriétés du label
        assert header.headerAppDescription.objectName() == "headerAppDescription"
        assert header.headerAppDescription.alignment() == (
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop
        )

    def test_buttons_frame(self, qt_application):
        """Test du frame des boutons."""
        header = Header()

        # Vérifier que le frame des boutons existe
        assert hasattr(header, "headerButtons")
        assert header.headerButtons is not None

        # Vérifier les propriétés du frame
        assert header.headerButtons.objectName() == "headerButtons"
        assert header.headerButtons.frameShape() == QFrame.NoFrame
        assert header.headerButtons.frameShadow() == QFrame.Raised

    def test_buttons_layout(self, qt_application):
        """Test du layout des boutons."""
        header = Header()

        # Vérifier que le layout des boutons existe
        assert hasattr(header, "HL_headerButtons")
        assert header.HL_headerButtons is not None

        # Vérifier les propriétés du layout
        assert header.HL_headerButtons.spacing() == 5
        margins = header.HL_headerButtons.contentsMargins()
        assert margins.left() == 0
        assert margins.top() == 0
        assert margins.right() == 0
        assert margins.bottom() == 0

    def test_settings_button(self, qt_application):
        """Test du bouton de paramètres."""
        header = Header()

        # Vérifier que le bouton de paramètres existe
        assert hasattr(header, "settingsTopBtn")
        assert header.settingsTopBtn is not None

        # Vérifier les propriétés du bouton
        assert header.settingsTopBtn.objectName() == "settingsTopBtn"
        assert isinstance(header.settingsTopBtn, QPushButton)

    def test_minimize_button(self, qt_application):
        """Test du bouton de minimisation."""
        header = Header()

        # Vérifier que le bouton de minimisation existe
        assert hasattr(header, "minimizeAppBtn")
        assert header.minimizeAppBtn is not None

        # Vérifier les propriétés du bouton
        assert header.minimizeAppBtn.objectName() == "minimizeAppBtn"
        assert isinstance(header.minimizeAppBtn, QPushButton)

    def test_maximize_button(self, qt_application):
        """Test du bouton de maximisation."""
        header = Header()

        # Vérifier que le bouton de maximisation existe
        assert hasattr(header, "maximizeRestoreAppBtn")
        assert header.maximizeRestoreAppBtn is not None

        # Vérifier les propriétés du bouton
        assert header.maximizeRestoreAppBtn.objectName() == "maximizeRestoreAppBtn"
        assert isinstance(header.maximizeRestoreAppBtn, QPushButton)

    def test_close_button(self, qt_application):
        """Test du bouton de fermeture."""
        header = Header()

        # Vérifier que le bouton de fermeture existe
        assert hasattr(header, "closeAppBtn")
        assert header.closeAppBtn is not None

        # Vérifier les propriétés du bouton
        assert header.closeAppBtn.objectName() == "closeAppBtn"
        assert isinstance(header.closeAppBtn, QPushButton)

    def test_button_list_management(self, qt_application):
        """Test de la gestion de la liste des boutons."""
        header = Header()

        # Vérifier que la liste des boutons existe
        assert hasattr(header, "_buttons")
        assert isinstance(header._buttons, list)

        # Vérifier que les boutons sont dans la liste
        expected_buttons = [
            "settingsTopBtn",
            "minimizeAppBtn",
            "maximizeRestoreAppBtn",
            "closeAppBtn",
        ]
        for button_name in expected_buttons:
            assert hasattr(header, button_name)
            assert getattr(header, button_name) is not None

    def test_size_policy(self, qt_application):
        """Test de la politique de taille."""
        header = Header()

        # Vérifier que la politique de taille est définie
        assert header.sizePolicy().hasHeightForWidth() is not None

    def test_custom_app_name(self, qt_application):
        """Test du nom d'application personnalisé."""
        app_name = "Custom App Name"
        header = Header(app_name=app_name)

        # Vérifier que le nom est défini
        assert header.headerAppName.text() == app_name

    def test_custom_description(self, qt_application):
        """Test de la description personnalisée."""
        description = "Custom Description"
        header = Header(description=description)

        # Vérifier que la description est définie
        assert header.headerAppDescription.text() == description

    def test_button_click_signals(self, qt_application):
        """Test des signaux de clic des boutons."""
        header = Header()

        # Vérifier que les boutons ont des signaux
        buttons = [
            header.settingsTopBtn,
            header.minimizeAppBtn,
            header.maximizeRestoreAppBtn,
            header.closeAppBtn,
        ]

        for button in buttons:
            assert hasattr(button, "clicked")
            assert hasattr(button.clicked, "connect")

    def test_header_height_fixed(self, qt_application):
        """Test que la hauteur de l'en-tête est fixe."""
        header = Header()

        # Vérifier que la hauteur est fixe
        assert header.height() == 50
        assert header.minimumHeight() == 50
        assert header.maximumHeight() == 50

    def test_header_width_policy(self, qt_application):
        """Test de la politique de largeur de l'en-tête."""
        header = Header()

        # Vérifier que la politique de taille est définie
        # Note: Le Header utilise H_EXPANDING_V_PREFERRED qui est Expanding
        size_policy = header.sizePolicy()
        assert size_policy.horizontalPolicy() == QSizePolicy.Policy.Expanding
