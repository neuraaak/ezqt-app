from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# GENERATE ASSETS CATALOG FOR DOCS
# ///////////////////////////////////////////////////////////////
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ICONS_FILE = ROOT / "src" / "ezqt_app" / "shared" / "resources" / "icons.py"
IMAGES_FILE = ROOT / "src" / "ezqt_app" / "shared" / "resources" / "images.py"
OUTPUT_FILE = ROOT / "docs" / "api" / "assets.generated.md"

# Public raw URL for image previews in docs.
# Override if your fork/repo path differs.
RAW_BASE_URL = (
    "https://raw.githubusercontent.com/neuraaak/ezqt-app/main/src/ezqt_app/resources"
)


def _extract_class_attrs(file_path: Path, class_name: str) -> list[tuple[str, str]]:
    source = file_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(file_path))

    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            rows: list[tuple[str, str]] = []
            for stmt in node.body:
                value: str | None = None
                attr: str | None = None

                if isinstance(stmt, ast.AnnAssign) and isinstance(
                    stmt.target, ast.Name
                ):
                    attr = stmt.target.id
                    if isinstance(stmt.value, ast.Constant) and isinstance(
                        stmt.value.value, str
                    ):
                        value = stmt.value.value

                if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1:
                    target = stmt.targets[0]
                    if isinstance(target, ast.Name):
                        attr = target.id
                        if isinstance(stmt.value, ast.Constant) and isinstance(
                            stmt.value.value, str
                        ):
                            value = stmt.value.value

                if attr and value and value.startswith(":/"):
                    rows.append((attr, value))

            return rows

    raise ValueError(f"Class {class_name} not found in {file_path}")


def _preview_cell(filename: str, kind: str) -> str:
    url = f"{RAW_BASE_URL}/{kind}/{filename}"
    if kind == "images":
        box_width = 56
        box_height = 40
        image_width = 50
    else:
        box_width = 30
        box_height = 30
        image_width = 20

    return (
        "<span "
        'style="display:inline-flex;align-items:center;justify-content:center;'
        f"width:{box_width}px;height:{box_height}px;background:#1f232b;border:1px solid #30363d;"
        'border-radius:6px;">'
        f'<img src="{url}" alt="{filename}" width="{image_width}" loading="lazy" />'
        "</span>"
    )


def _render_table(
    title: str, symbol: str, kind: str, rows: list[tuple[str, str]]
) -> list[str]:
    lines = [
        f"## {title}",
        "",
        "| File | Qt path | Accessor | Preview |",
        "| :--- | :------ | :------- | :------ |",
    ]

    for attr, qt_path in sorted(rows, key=lambda item: item[0]):
        filename = Path(qt_path).name
        accessor = f"{symbol}.{attr}"
        preview = _preview_cell(filename=filename, kind=kind)
        lines.append(f"| `{filename}` | `{qt_path}` | `{accessor}` | {preview} |")

    lines.append("")
    return lines


def generate_assets_catalog() -> Path:
    icons = _extract_class_attrs(ICONS_FILE, "Icons")
    images = _extract_class_attrs(IMAGES_FILE, "Images")

    content: list[str] = [
        "<!-- AUTO-GENERATED FILE. DO NOT EDIT MANUALLY. -->",
        "",
        "This table is generated from:",
        "",
        "- `src/ezqt_app/shared/resources/icons.py`",
        "- `src/ezqt_app/shared/resources/images.py`",
        "",
        "Preview images are loaded from the repository raw URL.",
        "",
    ]

    content.extend(_render_table("📦 Built-in icons", "Icons", "icons", icons))
    content.extend(_render_table("🖼️ Built-in images", "Images", "images", images))

    OUTPUT_FILE.write_text("\n".join(content), encoding="utf-8")
    return OUTPUT_FILE


if __name__ == "__main__":
    output = generate_assets_catalog()
    print(f"Generated: {output}")
