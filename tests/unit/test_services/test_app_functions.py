# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_SERVICES.TEST_APP_FUNCTIONS - Config service tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for v5 configuration and resource services."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from pathlib import Path

# Third-party imports
import yaml

# Local imports
from ezqt_app.services.config.config_service import ConfigService, get_package_resource

# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////


class TestConfigServiceV5:
    """Tests aligned with v5 service architecture."""

    def setup_method(self) -> None:
        self.service = ConfigService()

    def test_load_config_success_from_project_root(self, tmp_path: Path) -> None:
        config_dir = tmp_path / "bin" / "config"
        config_dir.mkdir(parents=True, exist_ok=True)

        config_file = config_dir / "app.config.yaml"
        config_data = {
            "app": {
                "name": "Test App",
                "description": "Test Description",
                "theme": "dark",
            }
        }
        with open(config_file, "w", encoding="utf-8") as file:
            yaml.safe_dump(config_data, file)

        self.service.set_project_root(tmp_path)
        loaded = self.service.load_config("app")

        assert loaded["app"]["name"] == "Test App"
        assert loaded["app"]["theme"] == "dark"

    def test_load_config_missing_returns_empty_dict(self, tmp_path: Path) -> None:
        self.service.set_project_root(tmp_path)
        assert self.service.load_config("missing") == {}

    def test_get_config_value(self, tmp_path: Path) -> None:
        config_dir = tmp_path / "bin" / "config"
        config_dir.mkdir(parents=True, exist_ok=True)

        config_file = config_dir / "theme.config.yaml"
        with open(config_file, "w", encoding="utf-8") as file:
            yaml.safe_dump(
                {"palette": {"dark": {"$_main_surface": "rgb(0, 0, 0)"}}}, file
            )

        self.service.set_project_root(tmp_path)
        value = self.service.get_config_value(
            "theme", "palette.dark.$_main_surface", "fallback"
        )
        assert value == "rgb(0, 0, 0)"

    def test_save_config_writes_config_yaml(self, tmp_path: Path) -> None:
        self.service.set_project_root(tmp_path)

        data = {"app": {"name": "Updated App", "theme": "light"}}
        result = self.service.save_config("app", data)

        assert result is True
        saved_file = tmp_path / "bin" / "config" / "app.config.yaml"
        assert saved_file.exists()
        loaded = yaml.safe_load(saved_file.read_text(encoding="utf-8"))
        assert loaded["app"]["theme"] == "light"

    def test_get_package_resource_returns_existing_path(self) -> None:
        resource = get_package_resource("resources/config/app.config.yaml")
        assert isinstance(resource, Path)
        assert resource.exists()
        assert resource.name == "app.config.yaml"
