# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_SERVICES.TEST_STARTUP_CONFIG - StartupConfig tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for services/bootstrap/startup_config.py."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
import os
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from ezqt_app.services.bootstrap.startup_config import StartupConfig

# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////


class TestStartupConfig:
    """Tests for StartupConfig.configure() and env-var setup methods."""

    def _make_config(self) -> StartupConfig:
        return StartupConfig()

    # ------------------------------------------------------------------
    # configure() — environment variables
    # ------------------------------------------------------------------

    def test_should_set_python_io_encoding_when_configure_is_called(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv("PYTHONIOENCODING", raising=False)
        with patch.object(StartupConfig, "_configure_project_root"):
            self._make_config().configure()
        assert os.environ.get("PYTHONIOENCODING") == "utf-8"

    def test_should_set_qt_font_dpi_when_configure_is_called(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv("QT_FONT_DPI", raising=False)
        with patch.object(StartupConfig, "_configure_project_root"):
            self._make_config().configure()
        assert os.environ.get("QT_FONT_DPI") == "96"

    def test_should_set_qt_auto_screen_scale_factor_when_configure_is_called(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv("QT_AUTO_SCREEN_SCALE_FACTOR", raising=False)
        with patch.object(StartupConfig, "_configure_project_root"):
            self._make_config().configure()
        assert os.environ.get("QT_AUTO_SCREEN_SCALE_FACTOR") == "1"

    def test_should_set_qt_scale_factor_rounding_policy_when_configure_is_called(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv("QT_SCALE_FACTOR_ROUNDING_POLICY", raising=False)
        with patch.object(StartupConfig, "_configure_project_root"):
            self._make_config().configure()
        assert os.environ.get("QT_SCALE_FACTOR_ROUNDING_POLICY") == "PassThrough"

    # ------------------------------------------------------------------
    # configure() — idempotency
    # ------------------------------------------------------------------

    def test_should_be_idempotent_when_configure_is_called_twice(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Second call to configure() must be a no-op."""
        with patch.object(StartupConfig, "_configure_project_root"):
            config = self._make_config()
            config.configure()
            monkeypatch.setenv("QT_FONT_DPI", "OVERRIDDEN")
            config.configure()  # Must not reset env
        # OVERRIDDEN survives because the second call is ignored
        assert os.environ.get("QT_FONT_DPI") == "OVERRIDDEN"

    # ------------------------------------------------------------------
    # Platform-specific env vars
    # ------------------------------------------------------------------

    def test_should_set_windows_qt_platform_when_configure_windows_is_called(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv("QT_QPA_PLATFORM", raising=False)
        self._make_config()._configure_windows()
        assert os.environ.get("QT_QPA_PLATFORM") == "windows:dpiawareness=0"

    def test_should_set_linux_qt_platform_when_configure_linux_is_called(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv("QT_QPA_PLATFORM", raising=False)
        self._make_config()._configure_linux()
        assert os.environ.get("QT_QPA_PLATFORM") == "xcb"

    def test_should_set_macos_qt_platform_when_configure_macos_is_called(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv("QT_QPA_PLATFORM", raising=False)
        self._make_config()._configure_macos()
        assert os.environ.get("QT_QPA_PLATFORM") == "cocoa"

    # ------------------------------------------------------------------
    # Encoding / locale accessors
    # ------------------------------------------------------------------

    def test_should_return_non_empty_string_when_get_encoding_is_called(self) -> None:
        result = self._make_config().get_encoding()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_should_return_string_or_none_when_get_locale_is_called(self) -> None:
        with patch.object(StartupConfig, "_configure_project_root"):
            config = self._make_config()
            config.configure()
        result = config.get_locale()
        assert result is None or isinstance(result, str)

    # ------------------------------------------------------------------
    # Project root detection
    # ------------------------------------------------------------------

    def test_should_call_app_service_when_explicit_project_root_is_given(
        self, tmp_path: Path
    ) -> None:
        """_configure_project_root must accept an explicit path without raising."""
        (tmp_path / "main.py").touch()
        # AppService is lazily imported inside _configure_project_root
        with patch(
            "ezqt_app.services.application.app_service.AppService.set_project_root"
        ) as mock_set:
            self._make_config()._configure_project_root(tmp_path)
        mock_set.assert_called_once()

    # ------------------------------------------------------------------
    # Encoding internal method
    # ------------------------------------------------------------------

    def test_should_not_raise_when_configure_encoding_is_called(self) -> None:
        """_configure_encoding must not raise even on restricted stdout."""
        # Should complete without error
        self._make_config()._configure_encoding()
        assert hasattr(sys.stdout, "encoding")
