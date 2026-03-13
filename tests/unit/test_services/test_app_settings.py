# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_SERVICES.TEST_APP_SETTINGS - Application settings tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for application settings."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Local imports
from ezqt_app.services.settings import get_settings_service

# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////


class TestSettings:
    """Tests for the settings service state."""

    @staticmethod
    def _settings():
        return get_settings_service()

    def test_should_have_correct_app_settings_when_service_is_retrieved(self):
        """Test application settings."""
        settings = self._settings()
        # Check basic settings
        assert settings.app.NAME == "MyApplication"
        assert settings.app.DESCRIPTION == "MyDescription"
        assert settings.app.ENABLE_CUSTOM_TITLE_BAR is True

        # Check dimensions
        assert isinstance(settings.app.APP_MIN_SIZE, tuple)
        assert settings.app.APP_MIN_SIZE == (940, 560)
        assert settings.app.APP_WIDTH == 1280
        assert settings.app.APP_HEIGHT == 720

    def test_should_have_correct_gui_settings_when_service_is_retrieved(self):
        """Test GUI settings."""
        settings = self._settings()
        # Check default theme
        assert settings.gui.THEME == "dark"

        # Check menu settings
        assert settings.gui.MENU_PANEL_SHRINKED_WIDTH == 60
        assert settings.gui.MENU_PANEL_EXTENDED_WIDTH == 240

        # Check panel settings
        assert settings.gui.SETTINGS_PANEL_WIDTH == 240
        assert settings.gui.TIME_ANIMATION == 400

    def test_should_allow_settings_modification_when_values_are_changed(self):
        """Test that settings can be modified (expected behavior)."""
        settings = self._settings()
        # Save original values
        original_name = settings.app.NAME
        original_theme = settings.gui.THEME
        original_width = settings.gui.MENU_PANEL_SHRINKED_WIDTH

        # Modify settings (this is expected behavior)
        settings.app.NAME = "ModifiedName"
        settings.gui.THEME = "light"
        settings.gui.MENU_PANEL_SHRINKED_WIDTH = 100

        # Check that values were modified
        assert settings.app.NAME == "ModifiedName"
        assert settings.gui.THEME == "light"
        assert settings.gui.MENU_PANEL_SHRINKED_WIDTH == 100

        # Restore original values
        settings.app.NAME = original_name
        settings.gui.THEME = original_theme
        settings.gui.MENU_PANEL_SHRINKED_WIDTH = original_width

        # Check that values were restored
        assert original_name == settings.app.NAME
        assert original_theme == settings.gui.THEME
        assert original_width == settings.gui.MENU_PANEL_SHRINKED_WIDTH

    def test_should_have_consistent_min_size_when_app_min_size_is_queried(self):
        """Test minimum size tuple consistency."""
        min_size = self._settings().app.APP_MIN_SIZE
        assert min_size[0] == 940
        assert min_size[1] == 560

    def test_should_have_boolean_type_when_boolean_settings_are_checked(self):
        """Test boolean settings."""
        settings = self._settings()
        assert isinstance(settings.app.ENABLE_CUSTOM_TITLE_BAR, bool)
        assert settings.app.ENABLE_CUSTOM_TITLE_BAR is True

    def test_should_have_integer_type_when_integer_settings_are_checked(self):
        """Test integer settings."""
        settings = self._settings()
        assert isinstance(settings.app.APP_WIDTH, int)
        assert isinstance(settings.app.APP_HEIGHT, int)
        assert isinstance(settings.gui.MENU_PANEL_SHRINKED_WIDTH, int)
        assert isinstance(settings.gui.MENU_PANEL_EXTENDED_WIDTH, int)
        assert isinstance(settings.gui.SETTINGS_PANEL_WIDTH, int)
        assert isinstance(settings.gui.TIME_ANIMATION, int)

    def test_should_have_string_type_when_string_settings_are_checked(self):
        """Test string settings."""
        settings = self._settings()
        assert isinstance(settings.app.NAME, str)
        assert isinstance(settings.app.DESCRIPTION, str)
        assert isinstance(settings.gui.THEME, str)

    def test_should_have_app_and_gui_attributes_when_settings_service_is_queried(self):
        """Test general service structure."""
        settings = self._settings()
        assert hasattr(settings, "app")
        assert hasattr(settings, "gui")
