# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_UTILS.TEST_APP_UTILS - App utility function tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for utils/app_utils.py — pure Path utility functions."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
from pathlib import Path

from ezqt_app.utils.app_utils import ensure_data_dir, get_app_data_dir, get_config_file

# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////


class TestGetAppDataDir:
    """Tests for get_app_data_dir()."""

    def test_should_return_path_instance_when_called(self) -> None:
        result = get_app_data_dir()
        assert isinstance(result, Path)

    def test_should_have_data_as_last_segment_when_called(self) -> None:
        result = get_app_data_dir()
        assert result.name == "data"

    def test_should_include_ezqt_app_in_path_when_called(self) -> None:
        result = get_app_data_dir()
        assert ".ezqt_app" in str(result)

    def test_should_be_under_home_directory_when_called(self) -> None:
        result = get_app_data_dir()
        assert Path.home() in result.parents


class TestEnsureDataDir:
    """Tests for ensure_data_dir()."""

    def test_should_return_path_when_ensure_data_dir_is_called(self) -> None:
        result = ensure_data_dir()
        assert isinstance(result, Path)

    def test_should_create_directory_when_ensure_data_dir_is_called(self) -> None:
        result = ensure_data_dir()
        assert result.exists()
        assert result.is_dir()

    def test_should_return_same_path_as_get_app_data_dir_when_called(self) -> None:
        assert ensure_data_dir() == get_app_data_dir()


class TestGetConfigFile:
    """Tests for get_config_file()."""

    def test_should_return_path_when_get_config_file_is_called(self) -> None:
        result = get_config_file()
        assert isinstance(result, Path)

    def test_should_have_yaml_extension_when_called(self) -> None:
        result = get_config_file()
        assert result.suffix == ".yaml"

    def test_should_be_named_config_yaml_when_called(self) -> None:
        result = get_config_file()
        assert result.name == "config.yaml"

    def test_should_reside_inside_data_directory_when_called(self) -> None:
        config = get_config_file()
        data_dir = get_app_data_dir()
        assert config.parent == data_dir
