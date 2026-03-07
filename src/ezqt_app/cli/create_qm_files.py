# ///////////////////////////////////////////////////////////////
# CLI.CREATE_QM_FILES - Translation file converter (.ts -> .qm)
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Convert Qt translation source files (.ts) to binary format (.qm)."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import importlib.resources
import struct
import xml.etree.ElementTree as ET  # noqa: S314
from pathlib import Path

# Local imports
from ..utils.printer import get_printer


# ///////////////////////////////////////////////////////////////
# FUNCTIONS
# ///////////////////////////////////////////////////////////////
def extract_translations_from_ts(ts_file_path: Path) -> dict[str, str]:
    """Parse a Qt .ts XML file and return source→translation mapping.

    Args:
        ts_file_path: Path to the .ts file to parse.

    Returns:
        Dict mapping source strings to their translations.

    Raises:
        FileNotFoundError: If the .ts file does not exist.
        ET.ParseError: If the XML is malformed.
    """
    if not ts_file_path.exists():
        raise FileNotFoundError(f"Translation file not found: {ts_file_path}")

    root = ET.parse(ts_file_path).getroot()  # noqa: S314
    translations: dict[str, str] = {}

    for message in root.findall(".//message"):
        source = message.find("source")
        translation = message.find("translation")
        if (
            source is not None
            and translation is not None
            and source.text
            and translation.text
        ):
            translations[source.text] = translation.text

    return translations


def create_proper_qm_from_ts(ts_file_path: Path, qm_file_path: Path) -> bool:
    """Convert a .ts file to .qm binary format.

    Args:
        ts_file_path: Path to the source .ts file.
        qm_file_path: Path where the .qm file will be written.

    Returns:
        True on success, False on error.
    """
    printer = get_printer()
    printer.info(f"Converting {ts_file_path.name} to {qm_file_path.name}...")

    try:
        translations = extract_translations_from_ts(ts_file_path)
        create_qt_qm_file(qm_file_path, translations)
        printer.success(f"{len(translations)} translations converted")
        return True

    except Exception as e:
        printer.error(f"Error during conversion: {e}")
        return False


def create_qt_qm_file(qm_file_path: Path, translations: dict) -> None:
    """Write translations to a .qm file in Qt binary format.

    Args:
        qm_file_path: Output file path.
        translations: Dict mapping source strings to translated strings.
    """
    with open(qm_file_path, "wb") as f:
        # Qt .qm magic number
        f.write(b"qm\x00\x00")
        # Version (4 bytes little-endian)
        f.write(struct.pack("<I", 0x01))
        # Number of translations
        f.write(struct.pack("<I", len(translations)))

        for source, translation in translations.items():
            source_bytes = source.encode("utf-8")
            translation_bytes = translation.encode("utf-8")
            f.write(struct.pack("<I", len(source_bytes)))
            f.write(source_bytes)
            f.write(struct.pack("<I", len(translation_bytes)))
            f.write(translation_bytes)

        # Checksum (optional)
        f.write(struct.pack("<I", 0))


def _get_package_translations_dir() -> Path | None:
    """Locate the bundled translations directory via importlib.resources."""
    try:
        pkg = importlib.resources.files("ezqt_app")
        candidate = Path(str(pkg.joinpath("resources").joinpath("translations")))
        return candidate if candidate.exists() else None
    except Exception:
        fallback = Path(__file__).parent.parent / "resources" / "translations"
        return fallback if fallback.exists() else None


def main() -> None:
    """Entry point: convert all .ts files found in the translations directory."""
    printer = get_printer()
    printer.section("Creating .qm files in the correct Qt format")

    # Priority 1: user project translations directory
    current_project_translations = Path.cwd() / "bin" / "translations"
    # Priority 2: installed package translations
    package_translations = _get_package_translations_dir()

    if current_project_translations.exists():
        translations_dir = current_project_translations
        printer.info(f"Using project directory: {translations_dir}")
    elif package_translations is not None:
        translations_dir = package_translations
        printer.info(f"Using package directory (fallback): {translations_dir}")
    else:
        printer.error("No translations directory found")
        printer.verbose_msg(f"   Project: {current_project_translations}")
        printer.info("Make sure you are in an EzQt_App project or run 'ezqt init'")
        return

    ts_files = list(translations_dir.glob("*.ts"))

    if not ts_files:
        printer.error("No .ts files found")
        return

    printer.info(f".ts files found: {len(ts_files)}")

    for ts_file in ts_files:
        qm_file = ts_file.with_suffix(".qm")
        if create_proper_qm_from_ts(ts_file, qm_file):
            printer.success(f"{qm_file.name} created")
        else:
            printer.error(f"Failed to create {qm_file.name}")

    printer.success("Process completed!")
    printer.info("Next steps:")
    printer.verbose_msg("   1. Test the new .qm files")
    printer.verbose_msg("   2. If it still doesn't work, use the .ts files")


# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////
__all__ = [
    "extract_translations_from_ts",
    "create_proper_qm_from_ts",
    "create_qt_qm_file",
    "main",
]

if __name__ == "__main__":
    main()
