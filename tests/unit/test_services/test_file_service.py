# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_SERVICES.TEST_FILE_SERVICE - FileService tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for services/application/file_service.py."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from ezqt_app.domain.errors import (
    InvalidOverwritePolicyError,
    MissingPackageResourceError,
    ResourceCompilationError,
)
from ezqt_app.services.application.file_service import FileService


@pytest.fixture
def mocked_printer() -> MagicMock:
    """Return a mocked printer used by FileService."""
    with patch("ezqt_app.services.application.file_service.get_printer") as factory:
        printer = MagicMock()
        factory.return_value = printer
        yield printer


class TestFileServiceBasics:
    """Tests for constructor, policies and basic helpers."""

    def test_should_raise_error_for_invalid_overwrite_policy(self) -> None:
        with pytest.raises(InvalidOverwritePolicyError):
            FileService(overwrite_policy="invalid")

    def test_should_generate_fallback_error_code_for_unknown_key(
        self, mocked_printer
    ) -> None:
        service = FileService(base_path=Path("."), overwrite_policy="skip")
        assert service._error_code("My Custom Key") == "resources.my_custom_key"

    def test_should_skip_existing_file_when_policy_is_skip(
        self, tmp_path: Path, mocked_printer
    ) -> None:
        target = tmp_path / "already.txt"
        target.write_text("x", encoding="utf-8")

        service = FileService(base_path=tmp_path, overwrite_policy="skip")
        assert service._should_write(target) is False
        mocked_printer.verbose_msg.assert_called()

    def test_should_write_existing_file_when_policy_is_force(
        self, tmp_path: Path, mocked_printer
    ) -> None:
        target = tmp_path / "already.txt"
        target.write_text("x", encoding="utf-8")

        service = FileService(base_path=tmp_path, overwrite_policy="force")
        assert service._should_write(target) is True

    def test_should_skip_existing_file_when_policy_is_ask_and_no_context(
        self, tmp_path: Path, mocked_printer
    ) -> None:
        target = tmp_path / "already.txt"
        target.write_text("x", encoding="utf-8")

        service = FileService(base_path=tmp_path, overwrite_policy="ask")
        assert service._should_write(target) is False


class TestFileServiceCopies:
    """Tests for YAML/QSS/TS copy workflows."""

    def test_should_copy_yaml_from_package(
        self, tmp_path: Path, mocked_printer
    ) -> None:
        src = tmp_path / "src.yaml"
        src.write_text("app: {}", encoding="utf-8")

        service = FileService(base_path=tmp_path, bin_path=tmp_path / "bin")
        target = service.make_yaml_from_package(src)

        assert target is not None
        assert target.exists()
        mocked_printer.action.assert_called()

    def test_should_raise_error_when_yaml_source_is_missing(
        self, tmp_path: Path, mocked_printer
    ) -> None:
        service = FileService(base_path=tmp_path, bin_path=tmp_path / "bin")

        with pytest.raises(MissingPackageResourceError):
            service.make_yaml_from_package(tmp_path / "missing.yaml")

    def test_should_skip_qtstrap_file_when_qss_source_is_single_file(
        self, tmp_path: Path, mocked_printer
    ) -> None:
        src = tmp_path / "qtstrap.qss"
        src.write_text("/* skip */", encoding="utf-8")

        service = FileService(base_path=tmp_path, bin_path=tmp_path / "bin")
        assert service.make_qss_from_package(src) is False

    def test_should_copy_qss_files_from_directory(
        self, tmp_path: Path, mocked_printer
    ) -> None:
        themes = tmp_path / "themes"
        themes.mkdir()
        (themes / "dark.qss").write_text("QWidget {}", encoding="utf-8")
        (themes / "qtstrap.qss").write_text("skip", encoding="utf-8")

        service = FileService(base_path=tmp_path, bin_path=tmp_path / "bin")
        assert service.make_qss_from_package(themes) is True
        assert (tmp_path / "bin" / "themes" / "dark.qss").exists()

    def test_should_copy_translation_files_from_directory(
        self, tmp_path: Path, mocked_printer
    ) -> None:
        translations = tmp_path / "translations"
        translations.mkdir()
        (translations / "ezqt_app_fr.ts").write_text("<TS/>", encoding="utf-8")

        service = FileService(base_path=tmp_path, bin_path=tmp_path / "bin")
        assert service.make_translations_from_package(translations) is True
        assert (tmp_path / "bin" / "translations" / "ezqt_app_fr.ts").exists()


class TestFileServiceResources:
    """Tests for QRC/RC and generated python accessors."""

    def test_should_generate_qrc_from_bin_content(
        self, tmp_path: Path, mocked_printer
    ) -> None:
        for folder in ("fonts", "images", "icons", "themes"):
            path = tmp_path / "bin" / folder
            path.mkdir(parents=True, exist_ok=True)
            (path / f"{folder}.txt").write_text("x", encoding="utf-8")

        service = FileService(base_path=tmp_path, bin_path=tmp_path / "bin")
        assert service.make_qrc() is True

        qrc = tmp_path / "bin" / "resources.qrc"
        assert qrc.exists()
        content = qrc.read_text(encoding="utf-8")
        assert "fonts/fonts.txt" in content

    def test_should_warn_when_make_rc_py_called_without_qrc(
        self, tmp_path: Path, mocked_printer
    ) -> None:
        service = FileService(base_path=tmp_path, bin_path=tmp_path / "bin")

        service.make_rc_py()

        mocked_printer.warning.assert_called_once()

    def test_should_raise_resource_error_when_rcc_returns_called_process_error(
        self, tmp_path: Path, mocked_printer
    ) -> None:
        service = FileService(base_path=tmp_path, bin_path=tmp_path / "bin")
        service._qrc_file = str(tmp_path / "bin" / "resources.qrc")

        import subprocess

        with (
            patch(
                "ezqt_app.services.application.file_service.subprocess.run",
                side_effect=subprocess.CalledProcessError(
                    1,
                    ["pyside6-rcc"],
                    output=b"stdout",
                    stderr=b"stderr",
                ),
            ),
            pytest.raises(ResourceCompilationError) as exc_info,
        ):
            service.make_rc_py()

        assert exc_info.value.code == "resources.qrc_compilation_failed"

    def test_should_raise_resource_error_when_rcc_tool_is_missing(
        self, tmp_path: Path, mocked_printer
    ) -> None:
        service = FileService(base_path=tmp_path, bin_path=tmp_path / "bin")
        service._qrc_file = str(tmp_path / "bin" / "resources.qrc")

        with (
            patch(
                "ezqt_app.services.application.file_service.subprocess.run",
                side_effect=FileNotFoundError(),
            ),
            pytest.raises(ResourceCompilationError),
        ):
            service.make_rc_py()

    def test_should_call_qrc_result_on_successful_compilation(
        self, tmp_path: Path, mocked_printer
    ) -> None:
        service = FileService(base_path=tmp_path, bin_path=tmp_path / "bin")
        service._qrc_file = str(tmp_path / "bin" / "resources.qrc")

        with patch("ezqt_app.services.application.file_service.subprocess.run"):
            service.make_rc_py()

        mocked_printer.qrc_compilation_result.assert_called_once_with(True)

    def test_should_purge_generated_rc_file(
        self, tmp_path: Path, mocked_printer
    ) -> None:
        rc = tmp_path / "bin" / "resources_rc.py"
        rc.parent.mkdir(parents=True, exist_ok=True)
        rc.write_text("# generated", encoding="utf-8")

        service = FileService(base_path=tmp_path, bin_path=tmp_path / "bin")
        service.purge_rc_py()

        assert not rc.exists()

    def test_should_generate_app_icons_and_images_python_modules(
        self, tmp_path: Path, mocked_printer
    ) -> None:
        icons = tmp_path / "bin" / "icons" / "status"
        images = tmp_path / "bin" / "images"
        icons.mkdir(parents=True, exist_ok=True)
        images.mkdir(parents=True, exist_ok=True)

        (icons / "ok-icon.png").write_bytes(b"img")
        (images / "hero photo.jpg").write_bytes(b"img")

        service = FileService(base_path=tmp_path, bin_path=tmp_path / "bin")
        service.make_app_icons_py()

        app_icons = (tmp_path / "bin" / "app_icons.py").read_text(encoding="utf-8")
        app_images = (tmp_path / "bin" / "app_images.py").read_text(encoding="utf-8")

        assert "status_ok_icon" in app_icons
        assert "hero_photo" in app_images

    def test_should_generate_main_file_from_template(
        self, tmp_path: Path, mocked_printer
    ) -> None:
        template = tmp_path / "main.py.template"
        template.write_text("print('hello')", encoding="utf-8")

        service = FileService(base_path=tmp_path, bin_path=tmp_path / "bin")
        service.make_main_from_template(template)

        assert (tmp_path / "main.py").exists()

    def test_should_expose_accessor_values(
        self, tmp_path: Path, mocked_printer
    ) -> None:
        service = FileService(base_path=tmp_path, bin_path=tmp_path / "bin")
        service._qrc_file = "abc.qrc"

        assert service.get_bin_path() == tmp_path / "bin"
        assert service.get_qrc_file() == "abc.qrc"
        assert service.get_resources_module_file() == ""
