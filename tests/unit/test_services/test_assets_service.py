# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_SERVICES.TEST_ASSETS_SERVICE - AssetsService tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for services/application/assets_service.py."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
from pathlib import Path
from unittest.mock import call, patch

from ezqt_app.services.application.assets_service import AssetsService


class TestAssetsService:
    """Tests for AssetsService orchestration methods."""

    def test_should_compile_rc_and_icons_when_qrc_generation_succeeds(self) -> None:
        with patch("ezqt_app.services.application.assets_service.FileService") as maker:
            maker.return_value.make_qrc.return_value = True

            AssetsService.check_assets_requirements()

        maker.return_value.make_assets_binaries.assert_called_once()
        maker.return_value.make_qrc.assert_called_once()
        maker.return_value.make_rc_py.assert_called_once()
        maker.return_value.make_app_icons_py.assert_called_once()
        maker.return_value.purge_rc_py.assert_not_called()

    def test_should_purge_rc_when_qrc_generation_fails(self) -> None:
        with patch("ezqt_app.services.application.assets_service.FileService") as maker:
            maker.return_value.make_qrc.return_value = False

            AssetsService.check_assets_requirements()

        maker.return_value.make_rc_py.assert_not_called()
        maker.return_value.make_app_icons_py.assert_not_called()
        maker.return_value.purge_rc_py.assert_called_once()

    def test_should_copy_all_required_files_when_flags_are_enabled(
        self, tmp_path: Path
    ) -> None:
        with (
            patch("ezqt_app.services.application.assets_service.FileService") as maker,
            patch(
                "ezqt_app.services.application.assets_service.get_package_resource"
            ) as get_resource,
        ):
            get_resource.side_effect = [
                Path("pkg/config/app.config.yaml"),
                Path("pkg/themes"),
                Path("pkg/translations"),
            ]

            AssetsService.make_required_files(base_path=tmp_path)

        get_resource.assert_has_calls(
            [
                call("resources/config/app.config.yaml"),
                call("resources/themes"),
                call("resources/translations"),
            ]
        )
        maker.return_value.make_yaml_from_package.assert_called_once()
        maker.return_value.make_qss_from_package.assert_called_once()
        maker.return_value.make_translations_from_package.assert_called_once()

    def test_should_skip_copy_steps_when_flags_are_disabled(
        self, tmp_path: Path
    ) -> None:
        with patch("ezqt_app.services.application.assets_service.FileService") as maker:
            AssetsService.make_required_files(
                mk_theme=False,
                mk_config=False,
                mk_translations=False,
                base_path=tmp_path,
            )

        maker.return_value.make_yaml_from_package.assert_not_called()
        maker.return_value.make_qss_from_package.assert_not_called()
        maker.return_value.make_translations_from_package.assert_not_called()
