"""Unit tests for the SettingsPanel class."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QScrollArea, QSizePolicy, QWidget

from ezqt_app.widgets.core.settings_panel import SettingsPanel


class TestSettingsPanel:
    """Tests for the SettingsPanel class."""

    def test_init_default_parameters(self, qt_application):
        panel = SettingsPanel()
        assert panel.objectName() == "settingsPanel"
        assert panel.frameShape() == QFrame.NoFrame
        assert panel.frameShadow() == QFrame.Raised

    def test_init_with_custom_width(self, qt_application):
        panel = SettingsPanel(width=300)
        assert panel.get_width() == 300

    def test_init_with_parent(self, qt_application):
        parent = QWidget()
        panel = SettingsPanel(parent=parent)
        assert panel.parent() == parent

    def test_scroll_area(self, qt_application):
        panel = SettingsPanel()
        assert isinstance(panel.settingsScrollArea, QScrollArea)
        assert panel.settingsScrollArea.objectName() == "settingsScrollArea"
        assert panel.settingsScrollArea.widgetResizable() is True
        assert (
            panel.settingsScrollArea.horizontalScrollBarPolicy()
            == Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        assert (
            panel.settingsScrollArea.verticalScrollBarPolicy()
            == Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

    def test_content_container(self, qt_application):
        panel = SettingsPanel()
        assert hasattr(panel, "contentSettings")
        assert panel.contentSettings.objectName() == "contentSettings"
        assert panel.contentSettings.frameShape() == QFrame.NoFrame
        assert panel.VL_contentSettings.spacing() == 0

    def test_theme_container_and_label(self, qt_application):
        panel = SettingsPanel()
        assert panel.themeSettingsContainer.objectName() == "themeSettingsContainer"
        assert panel.themeLabel.objectName() == "themeLabel"
        assert isinstance(panel.themeLabel, QLabel)
        assert panel.themeLabel.text() == "Active Theme"

    def test_theme_layout_properties(self, qt_application):
        panel = SettingsPanel()
        assert panel.VL_themeSettingsContainer.spacing() == 8
        margins = panel.VL_themeSettingsContainer.contentsMargins()
        assert margins.left() == 10
        assert margins.top() == 10
        assert margins.right() == 10
        assert margins.bottom() == 10

    def test_signals_exist(self, qt_application):
        panel = SettingsPanel()
        assert hasattr(panel, "settingChanged")
        assert hasattr(panel, "languageChanged")

    def test_internal_collections(self, qt_application):
        panel = SettingsPanel(load_from_yaml=False)
        assert isinstance(panel._widgets, list)
        assert isinstance(panel._settings, dict)

    def test_size_constraints_and_policy(self, qt_application):
        panel = SettingsPanel()
        assert panel.minimumSize().width() == 0
        assert panel.maximumSize().width() == 0
        assert panel.sizePolicy().horizontalPolicy() == QSizePolicy.Policy.Preferred
        assert panel.sizePolicy().verticalPolicy() == QSizePolicy.Policy.Preferred

    def test_set_width(self, qt_application):
        panel = SettingsPanel()
        panel.set_width(350)
        assert panel.get_width() == 350

    def test_settings_panel_without_yaml_loading(self, qt_application):
        panel = SettingsPanel(load_from_yaml=False)
        assert panel._settings == {}

