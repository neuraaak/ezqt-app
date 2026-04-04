# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_UTILS.TEST_CREATE_QM_FILES - .ts → .qm conversion tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for cli/create_qm_files.py — XML parsing and .qm binary writing."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
import struct
from pathlib import Path

import pytest

from ezqt_app.cli.commands._create_qm_files import (
    create_proper_qm_from_ts,
    create_qt_qm_file,
    extract_translations_from_ts,
)

# ///////////////////////////////////////////////////////////////
# FIXTURES
# ///////////////////////////////////////////////////////////////

MINIMAL_TS = """\
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="fr_FR">
  <context>
    <name>MainWindow</name>
    <message>
      <source>Hello</source>
      <translation>Bonjour</translation>
    </message>
    <message>
      <source>World</source>
      <translation>Monde</translation>
    </message>
  </context>
</TS>
"""

EMPTY_CONTEXT_TS = """\
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="fr_FR">
  <context>
    <name>X</name>
  </context>
</TS>
"""


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////


class TestExtractTranslationsFromTs:
    """Tests for extract_translations_from_ts()."""

    def test_should_return_translation_dict_when_ts_file_is_valid(
        self, tmp_path: Path
    ) -> None:
        ts_file = tmp_path / "test.ts"
        ts_file.write_text(MINIMAL_TS, encoding="utf-8")

        result = extract_translations_from_ts(ts_file)

        assert result == {"Hello": "Bonjour", "World": "Monde"}

    def test_should_raise_file_not_found_when_ts_file_is_missing(
        self, tmp_path: Path
    ) -> None:
        with pytest.raises(FileNotFoundError):
            extract_translations_from_ts(tmp_path / "does_not_exist.ts")

    def test_should_return_empty_dict_when_context_has_no_messages(
        self, tmp_path: Path
    ) -> None:
        ts_file = tmp_path / "empty.ts"
        ts_file.write_text(EMPTY_CONTEXT_TS, encoding="utf-8")

        result = extract_translations_from_ts(ts_file)

        assert result == {}

    def test_should_parse_all_messages_when_context_has_multiple_entries(
        self, tmp_path: Path
    ) -> None:
        ts = """\
<?xml version="1.0"?>
<TS><context><name>App</name>
  <message><source>A</source><translation>Alpha</translation></message>
  <message><source>B</source><translation>Beta</translation></message>
  <message><source>C</source><translation>Gamma</translation></message>
</context></TS>
"""
        ts_file = tmp_path / "multi.ts"
        ts_file.write_text(ts, encoding="utf-8")

        result = extract_translations_from_ts(ts_file)

        assert len(result) == 3
        assert result["A"] == "Alpha"
        assert result["C"] == "Gamma"


class TestCreateQtQmFile:
    """Tests for create_qt_qm_file()."""

    def test_should_create_output_file_when_qm_file_is_requested(
        self, tmp_path: Path
    ) -> None:
        qm_file = tmp_path / "out.qm"
        create_qt_qm_file(qm_file, {})
        assert qm_file.exists()

    def test_should_start_with_magic_bytes_when_qm_file_is_created(
        self, tmp_path: Path
    ) -> None:
        qm_file = tmp_path / "out.qm"
        create_qt_qm_file(qm_file, {"Hello": "Bonjour"})
        data = qm_file.read_bytes()
        assert data[:4] == b"qm\x00\x00"

    def test_should_encode_translation_count_when_qm_file_is_created(
        self, tmp_path: Path
    ) -> None:
        qm_file = tmp_path / "out.qm"
        translations = {"A": "B", "C": "D", "E": "F"}
        create_qt_qm_file(qm_file, translations)
        data = qm_file.read_bytes()
        # version at bytes 4-8, count at 8-12
        count = struct.unpack("<I", data[8:12])[0]
        assert count == 3

    def test_should_write_zero_count_when_translations_are_empty(
        self, tmp_path: Path
    ) -> None:
        qm_file = tmp_path / "out.qm"
        create_qt_qm_file(qm_file, {})
        data = qm_file.read_bytes()
        count = struct.unpack("<I", data[8:12])[0]
        assert count == 0

    def test_should_encode_utf8_strings_when_source_and_translation_contain_unicode(
        self, tmp_path: Path
    ) -> None:
        qm_file = tmp_path / "out.qm"
        create_qt_qm_file(qm_file, {"Héllo": "Wörld"})
        data = qm_file.read_bytes()
        assert "Héllo".encode() in data
        assert "Wörld".encode() in data


class TestCreateProperQmFromTs:
    """Tests for create_proper_qm_from_ts()."""

    def test_should_return_true_and_create_file_when_ts_file_is_valid(
        self, tmp_path: Path
    ) -> None:
        ts_file = tmp_path / "test.ts"
        ts_file.write_text(MINIMAL_TS, encoding="utf-8")
        qm_file = tmp_path / "out.qm"

        result = create_proper_qm_from_ts(ts_file, qm_file)

        assert result is True
        assert qm_file.exists()

    def test_should_return_false_when_ts_file_is_missing(self, tmp_path: Path) -> None:
        result = create_proper_qm_from_ts(tmp_path / "missing.ts", tmp_path / "out.qm")
        assert result is False

    def test_should_contain_translations_when_qm_file_is_created(
        self, tmp_path: Path
    ) -> None:
        ts_file = tmp_path / "test.ts"
        ts_file.write_text(MINIMAL_TS, encoding="utf-8")
        qm_file = tmp_path / "out.qm"

        create_proper_qm_from_ts(ts_file, qm_file)

        data = qm_file.read_bytes()
        assert b"Bonjour" in data
        assert b"Monde" in data
