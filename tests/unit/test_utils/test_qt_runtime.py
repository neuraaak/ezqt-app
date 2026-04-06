# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_UTILS.TEST_QT_RUNTIME - Qt runtime tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for utils/qt_runtime.py."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
import builtins
import types

import pytest

from ezqt_app.utils import qt_runtime


class TestConfigureQtEnvironment:
    """Tests for environment-level Qt setup."""

    @pytest.mark.parametrize(
        "platform,expected",
        [
            ("win32", "windows:dpiawareness=0"),
            ("linux", "xcb"),
            ("darwin", "cocoa"),
        ],
    )
    def test_should_set_platform_qpa_default(
        self, monkeypatch, platform, expected
    ) -> None:
        monkeypatch.setattr(qt_runtime.sys, "platform", platform)
        monkeypatch.delenv("QT_QPA_PLATFORM", raising=False)

        qt_runtime.configure_qt_environment()

        assert qt_runtime.os.environ.get("QT_QPA_PLATFORM") == expected
        assert qt_runtime.os.environ.get("QT_FONT_DPI") == "96"


class TestConfigureQtHighDpi:
    """Tests for configure_qt_high_dpi behavior across runtime branches."""

    def test_should_return_false_when_pyside6_import_fails(self, monkeypatch) -> None:
        real_import = builtins.__import__

        def _fake_import(name, *args, **kwargs):
            if name.startswith("PySide6"):
                raise ImportError("missing pyside")
            return real_import(name, *args, **kwargs)

        monkeypatch.setattr(builtins, "__import__", _fake_import)

        assert qt_runtime.configure_qt_high_dpi() is False

    def test_should_return_true_when_no_qgui_instance_exists(self, monkeypatch) -> None:
        state = {"configured": False}

        class _FakePolicy:
            PassThrough = object()

        class _FakeQt:
            HighDpiScaleFactorRoundingPolicy = _FakePolicy

        class _FakeQGuiApplication:
            @staticmethod
            def instance():
                return None

            @staticmethod
            def setHighDpiScaleFactorRoundingPolicy(_policy):
                state["configured"] = True

        qtcore = types.ModuleType("PySide6.QtCore")
        qtcore.Qt = _FakeQt
        qtgui = types.ModuleType("PySide6.QtGui")
        qtgui.QGuiApplication = _FakeQGuiApplication

        monkeypatch.setitem(
            qt_runtime.sys.modules, "PySide6", types.ModuleType("PySide6")
        )
        monkeypatch.setitem(qt_runtime.sys.modules, "PySide6.QtCore", qtcore)
        monkeypatch.setitem(qt_runtime.sys.modules, "PySide6.QtGui", qtgui)

        assert qt_runtime.configure_qt_high_dpi() is True
        assert state["configured"] is True

    def test_should_return_false_when_qgui_instance_already_exists(
        self, monkeypatch
    ) -> None:
        class _FakePolicy:
            PassThrough = object()

        class _FakeQt:
            HighDpiScaleFactorRoundingPolicy = _FakePolicy

        class _FakeQGuiApplication:
            @staticmethod
            def instance():
                return object()

            @staticmethod
            def setHighDpiScaleFactorRoundingPolicy(_policy):
                raise AssertionError("must not be called")

        qtcore = types.ModuleType("PySide6.QtCore")
        qtcore.Qt = _FakeQt
        qtgui = types.ModuleType("PySide6.QtGui")
        qtgui.QGuiApplication = _FakeQGuiApplication

        monkeypatch.setitem(
            qt_runtime.sys.modules, "PySide6", types.ModuleType("PySide6")
        )
        monkeypatch.setitem(qt_runtime.sys.modules, "PySide6.QtCore", qtcore)
        monkeypatch.setitem(qt_runtime.sys.modules, "PySide6.QtGui", qtgui)

        assert qt_runtime.configure_qt_high_dpi() is False

    def test_should_return_false_when_runtime_error_mentions_qgui_instance(
        self, monkeypatch
    ) -> None:
        class _FakeQt:
            class HighDpiScaleFactorRoundingPolicy:
                PassThrough = object()

        class _FakeQGuiApplication:
            @staticmethod
            def instance():
                raise RuntimeError("QGuiApplication instance already exists")

            @staticmethod
            def setHighDpiScaleFactorRoundingPolicy(_policy):
                raise AssertionError("must not be called")

        qtcore = types.ModuleType("PySide6.QtCore")
        qtcore.Qt = _FakeQt
        qtgui = types.ModuleType("PySide6.QtGui")
        qtgui.QGuiApplication = _FakeQGuiApplication

        monkeypatch.setitem(
            qt_runtime.sys.modules, "PySide6", types.ModuleType("PySide6")
        )
        monkeypatch.setitem(qt_runtime.sys.modules, "PySide6.QtCore", qtcore)
        monkeypatch.setitem(qt_runtime.sys.modules, "PySide6.QtGui", qtgui)

        assert qt_runtime.configure_qt_high_dpi() is False

    def test_should_reraise_runtime_error_when_message_is_unrelated(
        self, monkeypatch
    ) -> None:
        class _FakeQt:
            class HighDpiScaleFactorRoundingPolicy:
                PassThrough = object()

        class _FakeQGuiApplication:
            @staticmethod
            def instance():
                raise RuntimeError("unexpected runtime")

            @staticmethod
            def setHighDpiScaleFactorRoundingPolicy(_policy):
                raise AssertionError("must not be called")

        qtcore = types.ModuleType("PySide6.QtCore")
        qtcore.Qt = _FakeQt
        qtgui = types.ModuleType("PySide6.QtGui")
        qtgui.QGuiApplication = _FakeQGuiApplication

        monkeypatch.setitem(
            qt_runtime.sys.modules, "PySide6", types.ModuleType("PySide6")
        )
        monkeypatch.setitem(qt_runtime.sys.modules, "PySide6.QtCore", qtcore)
        monkeypatch.setitem(qt_runtime.sys.modules, "PySide6.QtGui", qtgui)

        with pytest.raises(RuntimeError):
            qt_runtime.configure_qt_high_dpi()

    def test_should_return_false_when_unexpected_exception_occurs(
        self, monkeypatch
    ) -> None:
        class _FakeQt:
            class HighDpiScaleFactorRoundingPolicy:
                PassThrough = object()

        class _FakeQGuiApplication:
            @staticmethod
            def instance():
                return None

            @staticmethod
            def setHighDpiScaleFactorRoundingPolicy(_policy):
                raise ValueError("unexpected")

        qtcore = types.ModuleType("PySide6.QtCore")
        qtcore.Qt = _FakeQt
        qtgui = types.ModuleType("PySide6.QtGui")
        qtgui.QGuiApplication = _FakeQGuiApplication

        monkeypatch.setitem(
            qt_runtime.sys.modules, "PySide6", types.ModuleType("PySide6")
        )
        monkeypatch.setitem(qt_runtime.sys.modules, "PySide6.QtCore", qtcore)
        monkeypatch.setitem(qt_runtime.sys.modules, "PySide6.QtGui", qtgui)

        assert qt_runtime.configure_qt_high_dpi() is False

    def test_should_call_environment_and_high_dpi_when_early_setup_is_called(
        self, monkeypatch
    ) -> None:
        called = {"env": False, "dpi": False}

        def _env() -> None:
            called["env"] = True

        def _dpi() -> bool:
            called["dpi"] = True
            return True

        monkeypatch.setattr(qt_runtime, "configure_qt_environment", _env)
        monkeypatch.setattr(qt_runtime, "configure_qt_high_dpi", _dpi)

        assert qt_runtime.configure_qt_high_dpi_early() is True
        assert called == {"env": True, "dpi": True}
