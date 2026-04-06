# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_SERVICES.TEST_RESOURCE_SERVICE - ResourceService tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for services/application/resource_service.py."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
from pathlib import Path
from unittest.mock import MagicMock, patch

from ezqt_app.services.application.resource_service import ResourceService


class TestResourceService:
    """Tests for font resource loading from package and app bins."""

    def test_should_load_package_and_app_ttf_fonts_when_app_is_false(
        self, tmp_path: Path
    ) -> None:
        package_fonts = tmp_path / "package_fonts"
        app_fonts = tmp_path / "bin" / "fonts"
        package_fonts.mkdir(parents=True)
        app_fonts.mkdir(parents=True)

        (package_fonts / "pkg.ttf").write_bytes(b"font")
        (package_fonts / "ignore.txt").write_text("n/a", encoding="utf-8")
        (app_fonts / "app.ttf").write_bytes(b"font")

        printer = MagicMock()

        with (
            patch(
                "ezqt_app.services.application.resource_service.get_package_resource",
                return_value=package_fonts,
            ),
            patch(
                "ezqt_app.services.application.resource_service.get_bin_path",
                return_value=tmp_path / "bin",
            ),
            patch(
                "ezqt_app.services.application.resource_service.get_printer",
                return_value=printer,
            ),
            patch(
                "ezqt_app.services.application.resource_service.QFontDatabase.addApplicationFont",
                side_effect=[1, 2],
            ) as add_font,
        ):
            ResourceService.load_fonts_resources(app=False)

        assert add_font.call_count == 2
        assert printer.action.call_count == 2

    def test_should_log_error_when_font_loading_fails(self, tmp_path: Path) -> None:
        fonts = tmp_path / "fonts"
        fonts.mkdir(parents=True)
        (fonts / "broken.ttf").write_bytes(b"font")

        printer = MagicMock()

        with (
            patch(
                "ezqt_app.services.application.resource_service.get_package_resource",
                return_value=fonts,
            ),
            patch(
                "ezqt_app.services.application.resource_service.get_printer",
                return_value=printer,
            ),
            patch(
                "ezqt_app.services.application.resource_service.QFontDatabase.addApplicationFont",
                return_value=-1,
            ),
            patch(
                "ezqt_app.services.application.resource_service.get_bin_path",
                return_value=tmp_path,
            ),
        ):
            ResourceService.load_fonts_resources(app=False)

        assert printer.error.call_count == 2

    def test_should_return_without_loading_when_fonts_dir_does_not_exist(
        self, tmp_path: Path
    ) -> None:
        with (
            patch(
                "ezqt_app.services.application.resource_service.get_package_resource",
                return_value=tmp_path / "missing",
            ),
            patch(
                "ezqt_app.services.application.resource_service.QFontDatabase.addApplicationFont"
            ) as add_font,
        ):
            ResourceService.load_fonts_resources(app=False)

        add_font.assert_not_called()
