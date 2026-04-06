# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_WIDGETS.TEST_CORE.TEST_EZ_APP - EzApplication tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for the EzApplication class."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import contextlib
import locale
import os
from unittest.mock import MagicMock, patch

# Third-party imports
import pytest
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication

# Local imports
from ezqt_app.widgets.core.ez_app import EzApplication


# ///////////////////////////////////////////////////////////////
# FIXTURES
# ///////////////////////////////////////////////////////////////
@pytest.fixture(scope="session")
def ez_app():
    """Session-scoped EzApplication instance.

    Qt allows only one QApplication per process lifetime, so a single
    instance is created once and shared across all tests in the session.
    """
    app = EzApplication.create_for_testing([])
    yield app


# ///////////////////////////////////////////////////////////////
# TESTS
# ///////////////////////////////////////////////////////////////
class TestEzApplication:
    """Tests for the EzApplication class."""

    # ------------------------------------------------------------------
    # Class-level tests (no instance required)
    # ------------------------------------------------------------------

    def test_should_inherit_from_qapplication(self):
        """EzApplication must be a QApplication subclass."""
        assert issubclass(EzApplication, QApplication)

    def test_should_expose_theme_changed_signal_on_class(self):
        """themeChanged signal must be defined at class level."""
        assert hasattr(EzApplication, "themeChanged")
        assert isinstance(EzApplication.themeChanged, Signal)

    def test_should_have_required_qt_methods(self):
        """EzApplication must inherit core QApplication methods."""
        for method_name in ("setAttribute", "testAttribute", "applicationName"):
            assert hasattr(EzApplication, method_name), (
                f"EzApplication should have method '{method_name}'"
            )

    def test_should_accept_variadic_constructor(self):
        """Constructor must accept *args and **kwargs to forward to QApplication."""
        import inspect

        sig = inspect.signature(EzApplication.__init__)
        assert sig.parameters["args"].kind == inspect.Parameter.VAR_POSITIONAL
        assert sig.parameters["kwargs"].kind == inspect.Parameter.VAR_KEYWORD

    def test_should_have_class_docstring(self):
        """EzApplication and its __init__ must have docstrings."""
        assert EzApplication.__doc__ and EzApplication.__doc__.strip()
        assert EzApplication.__init__.__doc__ and EzApplication.__init__.__doc__.strip()

    def test_should_behave_as_qt_singleton(self):
        """EzApplication inherits QApplication's one-instance-per-process contract."""
        assert issubclass(EzApplication, QApplication)
        assert hasattr(EzApplication, "__init__")

    # ------------------------------------------------------------------
    # Instance-level tests (require the session-scoped ez_app fixture)
    # ------------------------------------------------------------------

    def test_should_set_python_io_encoding(self, ez_app):
        """PYTHONIOENCODING must be set to utf-8 during initialization."""
        assert os.environ.get("PYTHONIOENCODING") == "utf-8"

    def test_should_set_qt_font_dpi(self, ez_app):
        """QT_FONT_DPI must be set to 96 during initialization."""
        assert os.environ.get("QT_FONT_DPI") == "96"

    def test_should_configure_locale(self, ez_app):
        """locale.setlocale must be called with LC_ALL during initialization."""
        # After a successful init, getlocale() returns a valid (non-None) tuple.
        result = locale.getlocale()
        assert isinstance(result, tuple)

    def test_should_suppress_locale_error(self):
        """locale.Error raised during locale setup must not propagate."""
        raised = False
        try:
            with contextlib.suppress(locale.Error):
                raise locale.Error("Simulated locale unavailability")
        except locale.Error:
            raised = True
        assert not raised, "EzApplication must suppress locale.Error silently"

    def test_should_expose_application_interface(self, ez_app):
        """Instance must expose the standard QApplication interface."""
        assert hasattr(ez_app, "setAttribute")
        assert hasattr(ez_app, "testAttribute")
        assert hasattr(ez_app, "themeChanged")

    def test_should_expose_connectable_theme_changed_signal(self, ez_app):
        """themeChanged signal on an instance must support connect/disconnect/emit."""
        assert hasattr(ez_app.themeChanged, "connect")
        assert hasattr(ez_app.themeChanged, "disconnect")
        assert hasattr(ez_app.themeChanged, "emit")

    def test_should_be_qapplication_instance(self, ez_app):
        """create_for_testing must return a real QApplication subclass instance."""
        assert isinstance(ez_app, QApplication)
        assert isinstance(ez_app, EzApplication)

    def test_should_reuse_existing_instance(self, ez_app):
        """create_for_testing must return the same singleton on repeated calls."""
        second = EzApplication.create_for_testing([])
        assert second is ez_app

    def test_should_raise_runtime_error_when_non_ez_qapplication_exists(self):
        """Constructor must reject an existing non-Ez QApplication singleton."""

        class _ForeignApp:
            pass

        with (
            patch(
                "ezqt_app.widgets.core.ez_app.QApplication.instance",
                return_value=_ForeignApp(),
            ),
            pytest.raises(RuntimeError),
        ):
            EzApplication([])

    def test_should_set_runtime_environment_variables_in_create_for_testing(self):
        """create_for_testing should enforce expected runtime environment values."""
        app = EzApplication.create_for_testing([])
        assert app is not None
        assert os.environ.get("PYTHONIOENCODING") == "utf-8"
        assert os.environ.get("QT_FONT_DPI") == "96"

    def test_should_cleanup_existing_foreign_qapplication_in_create_for_testing(self):
        """create_for_testing should cleanup foreign QApplication instances."""

        class _DummyApp(EzApplication):
            def __init__(self, *args, **kwargs):  # noqa: ARG002
                self.created = True

        foreign = MagicMock()
        nested = MagicMock()

        with (
            patch(
                "ezqt_app.widgets.core.ez_app.QGuiApplication.instance",
                return_value=object(),
            ),
            patch(
                "ezqt_app.widgets.core.ez_app.QApplication.instance",
                side_effect=[foreign, nested, None],
            ),
            patch("ezqt_app.widgets.core.ez_app.time.sleep"),
            pytest.raises(
                RuntimeError,
            ),
        ):
            _DummyApp.create_for_testing([])

        foreign.quit.assert_called_once()
        foreign.deleteLater.assert_called_once()
        nested.quit.assert_called_once()
        nested.deleteLater.assert_called_once()
