# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_MAIN_MODULE - main.py bridge tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for main.py — thin bridge to the bootstrap package."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
from pathlib import Path
from unittest.mock import patch

# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////


class TestInitBridge:
    """Tests for main.init() delegating to services.bootstrap.init."""

    # init is imported at module level as `init_app` → patch that binding
    _PATCH = "ezqt_app.main.init_app"

    def test_should_delegate_to_bootstrap_init_when_init_is_called(self) -> None:
        with patch(self._PATCH, return_value={}) as mock_init:
            from ezqt_app.main import init

            result = init(verbose=False)

        mock_init.assert_called_once()
        assert result == {}

    def test_should_convert_path_project_root_to_str_when_path_is_given(
        self, tmp_path: Path
    ) -> None:
        with patch(self._PATCH, return_value={}) as mock_init:
            from ezqt_app.main import init

            init(project_root=tmp_path, verbose=False)

        call_kwargs = mock_init.call_args.kwargs
        assert isinstance(call_kwargs.get("project_root"), str)

    def test_should_convert_path_bin_path_to_str_when_path_is_given(
        self, tmp_path: Path
    ) -> None:
        with patch(self._PATCH, return_value={}) as mock_init:
            from ezqt_app.main import init

            init(bin_path=tmp_path / "bin", verbose=False)

        call_kwargs = mock_init.call_args.kwargs
        assert isinstance(call_kwargs.get("bin_path"), str)

    def test_should_pass_none_when_project_root_is_none(self) -> None:
        with patch(self._PATCH, return_value={}) as mock_init:
            from ezqt_app.main import init

            init(project_root=None, verbose=False)

        call_kwargs = mock_init.call_args.kwargs
        assert call_kwargs.get("project_root") is None

    def test_should_forward_mk_theme_flag_when_init_is_called(self) -> None:
        with patch(self._PATCH, return_value={}) as mock_init:
            from ezqt_app.main import init

            init(mk_theme=False, verbose=False)

        call_kwargs = mock_init.call_args.kwargs
        assert call_kwargs.get("mk_theme") is False

    def test_should_resolve_default_overwrite_policy_when_policy_is_not_provided(
        self,
    ) -> None:
        with patch(self._PATCH, return_value={}) as mock_init:
            from ezqt_app.main import init

            init(verbose=False)

        call_kwargs = mock_init.call_args.kwargs
        # Default policy is OverwritePolicy.ASK
        assert call_kwargs.get("overwrite_policy") is not None


class TestSetupProjectBridge:
    """Tests for main.setup_project()."""

    def test_should_delegate_to_bootstrap_when_setup_project_is_called(self) -> None:
        with patch(
            "ezqt_app.services.bootstrap.setup_project", return_value=True
        ) as mock:
            from ezqt_app.main import setup_project

            result = setup_project()

        assert result is True
        mock.assert_called_once()

    def test_should_pass_base_path_when_base_path_is_given(
        self, tmp_path: Path
    ) -> None:
        with patch(
            "ezqt_app.services.bootstrap.setup_project", return_value=True
        ) as mock:
            from ezqt_app.main import setup_project

            setup_project(base_path=str(tmp_path))

        mock.assert_called_once_with(str(tmp_path))


class TestGenerateAssetsBridge:
    """Tests for main.generate_assets()."""

    def test_should_delegate_to_bootstrap_when_generate_assets_is_called(self) -> None:
        with patch(
            "ezqt_app.services.bootstrap.generate_assets", return_value=True
        ) as mock:
            from ezqt_app.main import generate_assets

            result = generate_assets()

        assert result is True
        mock.assert_called_once()


class TestConfigureStartupBridge:
    """Tests for main.configure_startup()."""

    def test_should_delegate_to_bootstrap_when_configure_startup_is_called(
        self,
    ) -> None:
        with patch("ezqt_app.services.bootstrap.configure_startup") as mock:
            from ezqt_app.main import configure_startup

            configure_startup()

        mock.assert_called_once()
