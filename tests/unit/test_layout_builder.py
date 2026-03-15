# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_LAYOUT_BUILDER - Tests for modular layout system
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for the modular layout (Builder Pattern + Null Objects)."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from unittest.mock import MagicMock, patch

# Local imports
from ezqt_app.app import EzQt_App
from ezqt_app.widgets.core.menu import Menu
from ezqt_app.widgets.core.null_widgets import NullMenuContainer, NullSettingsPanel
from ezqt_app.widgets.core.settings_panel import SettingsPanel

# ///////////////////////////////////////////////////////////////
# HELPERS
# ///////////////////////////////////////////////////////////////


def _mock_settings() -> MagicMock:
    """Create a mock settings service with standard GUI dimensions."""
    mock = MagicMock()
    mock.gui.MENU_PANEL_SHRINKED_WIDTH = 50
    mock.gui.MENU_PANEL_EXTENDED_WIDTH = 200
    mock.gui.SETTINGS_PANEL_WIDTH = 240
    mock.app.NAME = "Test App"
    mock.gui.THEME = "dark"
    return mock


def _mock_config() -> MagicMock:
    """Create a mock config service with default app/translation settings."""
    mock = MagicMock()
    mock.load_config.return_value = {
        "app": {"theme": "dark", "language": "en"},
        "translation": {"collect_strings": False},
    }
    return mock


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////


class TestLayoutBuilder:
    """
    Tests for the EzQt_App layout builder functionality.

    Verifies the Fluent API (no_menu, no_settings_panel) and the
    injection of Null Objects.
    """

    # ///////////////////////////////////////////////////////////////
    # TESTS
    # ///////////////////////////////////////////////////////////////

    @patch("ezqt_app.app.get_settings_service", return_value=_mock_settings())
    @patch("ezqt_app.app.get_config_service", return_value=_mock_config())
    @patch("ezqt_app.app.AppService")
    @patch("ezqt_app.app.ThemeService")
    @patch("ezqt_app.app.Fonts")
    @patch("ezqt_app.app.SizePolicy")
    def test_should_have_full_layout_by_default(
        self,
        mock_size,
        mock_fonts,
        mock_theme,
        mock_app_svc,
        mock_cfg,
        mock_settings,
        qt_application,
    ) -> None:
        """Verify that a standard EzQt_App still has menu and settings by default."""
        app = EzQt_App()
        app.build()

        # Check types of containers
        assert isinstance(app.ui.menu_container, Menu)
        assert isinstance(app.ui.settings_panel, SettingsPanel)
        assert not app.ui.header_container.settings_btn.isHidden()

    @patch("ezqt_app.app.get_settings_service", return_value=_mock_settings())
    @patch("ezqt_app.app.get_config_service", return_value=_mock_config())
    @patch("ezqt_app.app.AppService")
    @patch("ezqt_app.app.ThemeService")
    @patch("ezqt_app.app.Fonts")
    @patch("ezqt_app.app.SizePolicy")
    def test_should_disable_menu_when_no_menu_is_called(
        self,
        mock_size,
        mock_fonts,
        mock_theme,
        mock_app_svc,
        mock_cfg,
        mock_settings,
        qt_application,
    ) -> None:
        """Verify that no_menu() injects NullMenuContainer."""
        app = EzQt_App()
        app.no_menu().build()

        assert isinstance(app.ui.menu_container, NullMenuContainer)
        assert isinstance(app.ui.settings_panel, SettingsPanel)

    @patch("ezqt_app.app.get_settings_service", return_value=_mock_settings())
    @patch("ezqt_app.app.get_config_service", return_value=_mock_config())
    @patch("ezqt_app.app.AppService")
    @patch("ezqt_app.app.ThemeService")
    @patch("ezqt_app.app.Fonts")
    @patch("ezqt_app.app.SizePolicy")
    def test_should_disable_settings_panel_when_no_settings_panel_is_called(
        self,
        mock_size,
        mock_fonts,
        mock_theme,
        mock_app_svc,
        mock_cfg,
        mock_settings,
        qt_application,
    ) -> None:
        """Verify that no_settings_panel() injects NullSettingsPanel and hides btn."""
        app = EzQt_App()
        app.no_settings_panel().build()

        assert isinstance(app.ui.settings_panel, NullSettingsPanel)
        assert isinstance(app.ui.menu_container, Menu)
        # Button in header should be hidden
        assert app.ui.header_container.settings_btn.isHidden()

    @patch("ezqt_app.app.get_settings_service", return_value=_mock_settings())
    @patch("ezqt_app.app.get_config_service", return_value=_mock_config())
    @patch("ezqt_app.app.AppService")
    @patch("ezqt_app.app.ThemeService")
    @patch("ezqt_app.app.Fonts")
    @patch("ezqt_app.app.SizePolicy")
    def test_should_disable_both_when_chained(
        self,
        mock_size,
        mock_fonts,
        mock_theme,
        mock_app_svc,
        mock_cfg,
        mock_settings,
        qt_application,
    ) -> None:
        """Verify that chaining no_menu() and no_settings_panel() works."""
        app = EzQt_App()
        app.no_menu().no_settings_panel().build()

        assert isinstance(app.ui.menu_container, NullMenuContainer)
        assert isinstance(app.ui.settings_panel, NullSettingsPanel)
        # Check through signal indirectly or isHidden
        assert app.ui.header_container.settings_btn.isHidden()

    @patch("ezqt_app.app.get_settings_service", return_value=_mock_settings())
    @patch("ezqt_app.app.get_config_service", return_value=_mock_config())
    @patch("ezqt_app.app.AppService")
    @patch("ezqt_app.app.ThemeService")
    @patch("ezqt_app.app.Fonts")
    @patch("ezqt_app.app.SizePolicy")
    def test_should_auto_build_on_show(
        self,
        mock_size,
        mock_fonts,
        mock_theme,
        mock_app_svc,
        mock_cfg,
        mock_settings,
        qt_application,
    ) -> None:
        """Verify that build() is called automatically when show() is called."""
        app = EzQt_App()
        # Should not have UI attribute yet as we decoupled init and setup
        assert not hasattr(app, "ui")

        app.show()

        assert hasattr(app, "ui")
        assert app._ui_initialized is True
        app.close()
