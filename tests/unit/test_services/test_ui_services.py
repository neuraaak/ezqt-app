# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_SERVICES.TEST_UI_SERVICES - UI service tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for services/ui/window_service.py, panel_service.py,
and definitions_service.py."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
from unittest.mock import MagicMock, patch

from ezqt_app.services.ui.panel_service import PanelService
from ezqt_app.services.ui.window_service import WindowService

# ///////////////////////////////////////////////////////////////
# HELPERS
# ///////////////////////////////////////////////////////////////

_RUNTIME_PATH = "ezqt_app.services.ui.window_service.get_runtime_state_service"
_SETTINGS_PATH = "ezqt_app.services.ui.panel_service.get_settings_service"


def _mock_window(**ui_attrs: object) -> MagicMock:
    window = MagicMock()
    for attr, value in ui_attrs.items():
        setattr(window.ui, attr, value)
    return window


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////


class TestWindowServiceGetSetStatus:
    """Tests for WindowService.get_status() and set_status()."""

    def test_should_return_false_when_window_is_not_maximized(self) -> None:
        mock_runtime = MagicMock()
        mock_runtime.get_global_state.return_value = False
        with patch(_RUNTIME_PATH, return_value=mock_runtime):
            result = WindowService.get_status()
        assert result is False

    def test_should_return_true_when_window_is_maximized(self) -> None:
        mock_runtime = MagicMock()
        mock_runtime.get_global_state.return_value = True
        with patch(_RUNTIME_PATH, return_value=mock_runtime):
            result = WindowService.get_status()
        assert result is True

    def test_should_delegate_to_runtime_service_when_set_status_is_called_with_true(
        self,
    ) -> None:
        mock_runtime = MagicMock()
        with patch(_RUNTIME_PATH, return_value=mock_runtime):
            WindowService.set_status(True)
        mock_runtime.set_global_state.assert_called_once_with(True)

    def test_should_delegate_to_runtime_service_when_set_status_is_called_with_false(
        self,
    ) -> None:
        mock_runtime = MagicMock()
        with patch(_RUNTIME_PATH, return_value=mock_runtime):
            WindowService.set_status(False)
        mock_runtime.set_global_state.assert_called_once_with(False)


class TestWindowServiceMaximizeRestore:
    """Tests for WindowService.maximize_restore()."""

    def test_should_maximize_window_when_current_state_is_not_maximized(self) -> None:
        mock_runtime = MagicMock()
        mock_runtime.get_global_state.return_value = False
        window = _mock_window()

        with patch(_RUNTIME_PATH, return_value=mock_runtime):
            WindowService.maximize_restore(window)

        window.showMaximized.assert_called_once()
        mock_runtime.set_global_state.assert_called_once_with(True)

    def test_should_restore_window_when_current_state_is_maximized(self) -> None:
        mock_runtime = MagicMock()
        mock_runtime.get_global_state.return_value = True
        window = _mock_window()
        window.width.return_value = 1280
        window.height.return_value = 720

        with patch(_RUNTIME_PATH, return_value=mock_runtime):
            WindowService.maximize_restore(window)

        window.showNormal.assert_called_once()
        mock_runtime.set_global_state.assert_called_once_with(False)

    def test_should_hide_all_grips_when_window_is_maximized(self) -> None:
        mock_runtime = MagicMock()
        mock_runtime.get_global_state.return_value = False
        window = _mock_window()

        with patch(_RUNTIME_PATH, return_value=mock_runtime):
            WindowService.maximize_restore(window)

        window.left_grip.hide.assert_called_once()
        window.right_grip.hide.assert_called_once()
        window.top_grip.hide.assert_called_once()
        window.bottom_grip.hide.assert_called_once()

    def test_should_show_all_grips_when_window_is_restored(self) -> None:
        mock_runtime = MagicMock()
        mock_runtime.get_global_state.return_value = True
        window = _mock_window()
        window.width.return_value = 800
        window.height.return_value = 600

        with patch(_RUNTIME_PATH, return_value=mock_runtime):
            WindowService.maximize_restore(window)

        window.left_grip.show.assert_called_once()
        window.right_grip.show.assert_called_once()


class TestPanelServiceToggleMenu:
    """Tests for PanelService.toggle_menu_panel()."""

    def test_should_return_early_when_menu_toggle_is_disabled(self) -> None:
        window = _mock_window()
        PanelService.toggle_menu_panel(window, enable=False)
        window.ui.menuContainer.width.assert_not_called()

    def test_should_start_animation_when_menu_is_in_shrunk_state(self) -> None:
        mock_settings = MagicMock()
        mock_settings.gui.TIME_ANIMATION = 200
        window = _mock_window()
        window.ui.menuContainer.width.return_value = 60
        window.ui.menuContainer.get_extended_width.return_value = 200
        window.ui.menuContainer.get_shrink_width.return_value = 60

        with (
            patch(_SETTINGS_PATH, return_value=mock_settings),
            patch("ezqt_app.services.ui.panel_service.QPropertyAnimation"),
        ):
            PanelService.toggle_menu_panel(window, enable=True)

        # Animation must have been assigned to window
        assert hasattr(window, "menu_animation")

    def test_should_start_animation_when_menu_is_in_extended_state(self) -> None:
        mock_settings = MagicMock()
        mock_settings.gui.TIME_ANIMATION = 200
        window = _mock_window()
        window.ui.menuContainer.width.return_value = 200
        window.ui.menuContainer.get_extended_width.return_value = 200
        window.ui.menuContainer.get_shrink_width.return_value = 60

        with (
            patch(_SETTINGS_PATH, return_value=mock_settings),
            patch("ezqt_app.services.ui.panel_service.QPropertyAnimation"),
        ):
            PanelService.toggle_menu_panel(window, enable=True)

        assert hasattr(window, "menu_animation")


class TestPanelServiceToggleSettings:
    """Tests for PanelService.toggle_settings_panel()."""

    def test_should_return_early_when_settings_toggle_is_disabled(self) -> None:
        window = _mock_window()
        PanelService.toggle_settings_panel(window, enable=False)
        window.ui.settingsPanel.width.assert_not_called()

    def test_should_start_animation_when_settings_panel_toggle_is_enabled(self) -> None:
        mock_settings = MagicMock()
        mock_settings.gui.TIME_ANIMATION = 300
        mock_settings.gui.SETTINGS_PANEL_WIDTH = 240
        mock_settings.gui.THEME = "dark"
        window = _mock_window()
        window.ui.settingsPanel.width.return_value = 0  # currently closed

        with (
            patch(_SETTINGS_PATH, return_value=mock_settings),
            patch("ezqt_app.services.ui.panel_service.QPropertyAnimation"),
        ):
            PanelService.toggle_settings_panel(window, enable=True)

        assert hasattr(window, "settings_animation")
