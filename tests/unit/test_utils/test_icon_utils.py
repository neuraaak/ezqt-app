# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_UTILS.TEST_ICON_UTILS - Icon utils tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for utils/icon_utils.py."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
from pathlib import Path
from unittest.mock import MagicMock, patch

from PySide6.QtGui import QIcon, QPixmap

from ezqt_app.utils.icon_utils import (
    IconLoaderWorker,
    colorize_pixmap,
    load_icon_from_source,
    load_icon_from_url_async,
)


class TestColorizePixmap:
    """Tests for colorize_pixmap helper."""

    def test_should_return_pixmap_with_same_size(self, qt_application) -> None:
        src = QPixmap(16, 16)
        out = colorize_pixmap(src, "#FFFFFF", 0.5)
        assert out.size() == src.size()


class TestLoadIconFromSource:
    """Tests for local source icon loading."""

    def test_should_return_none_when_source_is_none(self) -> None:
        assert load_icon_from_source(None) is None

    def test_should_return_same_icon_when_source_is_qicon(self) -> None:
        icon = QIcon()
        assert load_icon_from_source(icon) is icon

    def test_should_return_none_for_http_source(self) -> None:
        assert load_icon_from_source("https://example.com/icon.png") is None

    def test_should_return_none_for_invalid_local_path(self) -> None:
        assert load_icon_from_source("missing-file.png") is None

    def test_should_load_svg_icon_from_local_file(self, mock_svg_path: str) -> None:
        icon = load_icon_from_source(mock_svg_path)
        assert isinstance(icon, QIcon)
        assert not icon.isNull()

    def test_should_load_png_icon_from_local_file(self, tmp_path: Path) -> None:
        # Build a valid PNG from QPixmap to avoid fixture binary corruption issues.
        pixmap = QPixmap(16, 16)
        valid_path = tmp_path / "valid-icon.png"
        pixmap.save(str(valid_path), "PNG")

        icon = load_icon_from_source(str(valid_path))
        assert isinstance(icon, QIcon)
        assert not icon.isNull()


class TestIconLoaderWorker:
    """Tests for IconLoaderWorker background fetch logic."""

    def test_should_emit_load_failed_when_content_type_is_not_image(self) -> None:
        worker = IconLoaderWorker("https://example.com/not-image.txt")
        mocked_response = MagicMock()
        mocked_response.headers = {"Content-Type": "text/plain"}
        mocked_response.content = b"hello"
        mocked_response.raise_for_status.return_value = None

        failed = {"called": False}

        def _on_failed() -> None:
            failed["called"] = True

        worker.load_failed.connect(_on_failed)

        with patch(
            "ezqt_app.utils.icon_utils.requests.get", return_value=mocked_response
        ):
            worker.run()

        assert failed["called"] is True

    def test_should_emit_icon_loaded_for_svg_payload(self) -> None:
        worker = IconLoaderWorker("https://example.com/icon.svg")
        svg = b"""<?xml version='1.0'?><svg xmlns='http://www.w3.org/2000/svg' width='16' height='16'><rect width='16' height='16' fill='red'/></svg>"""
        mocked_response = MagicMock()
        mocked_response.headers = {"Content-Type": "image/svg+xml"}
        mocked_response.content = svg
        mocked_response.raise_for_status.return_value = None

        loaded = {"called": False}

        def _on_loaded(_icon: QIcon) -> None:
            loaded["called"] = True

        worker.icon_loaded.connect(_on_loaded)

        with patch(
            "ezqt_app.utils.icon_utils.requests.get", return_value=mocked_response
        ):
            worker.run()

        assert loaded["called"] is True

    def test_should_emit_load_failed_when_request_raises(self) -> None:
        worker = IconLoaderWorker("https://example.com/icon.png")

        failed = {"called": False}

        def _on_failed() -> None:
            failed["called"] = True

        worker.load_failed.connect(_on_failed)

        with patch(
            "ezqt_app.utils.icon_utils.requests.get",
            side_effect=Exception("boom"),
        ):
            worker.run()

        assert failed["called"] is True


class TestLoadIconFromUrlAsync:
    """Tests for asynchronous worker factory."""

    def test_should_start_worker_and_return_it(self) -> None:
        with patch.object(IconLoaderWorker, "start") as mocked_start:
            worker = load_icon_from_url_async("https://example.com/icon.png")

        assert isinstance(worker, IconLoaderWorker)
        mocked_start.assert_called_once()
