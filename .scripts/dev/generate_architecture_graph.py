#!/usr/bin/env python3
# ///////////////////////////////////////////////////////////////
# GENERATE_ARCHITECTURE_GRAPH - Import dependency graph for docs
# ///////////////////////////////////////////////////////////////

"""Generate architecture dependency graph for documentation.

Uses grimp to analyze the actual import graph of the project package
and produces a Mermaid flowchart + dependency table written to
docs/architecture.md (replacing any existing content).

The package name is read from pyproject.toml. Layers are auto-discovered
from the top-level subdirectories of src/<package>/. To control layer
order or add custom labels and role descriptions, edit the LAYER_ORDER
and LAYER_ROLES constants below.

Usage:
    PYTHONPATH=src python .scripts/dev/generate_architecture_graph.py
    # or in CI (package installed in editable mode):
    python .scripts/dev/generate_architecture_graph.py
"""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import io
import sys
import tomllib
import warnings
from pathlib import Path

# Third-party imports
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# ///////////////////////////////////////////////////////////////
# CONFIGURATION
# ///////////////////////////////////////////////////////////////

# Optional: set an explicit layer order to control graph node ordering.
# Set to None to auto-discover layers alphabetically from src/<package>/.
LAYER_ORDER: list[str] | None = None

# Optional: human-readable role descriptions shown in the responsibilities table.
# Keys are layer names; missing layers get an empty description.
LAYER_ROLES: dict[str, str] = {}

# Color palette for layer nodes — cycles automatically if there are more layers than colors.
_STYLE_PALETTE = [
    "fill:#4A90D9,color:#fff,stroke:#2C5F8A",
    "fill:#5BA85A,color:#fff,stroke:#3A6B39",
    "fill:#E8922A,color:#fff,stroke:#A3621B",
    "fill:#9B59B6,color:#fff,stroke:#6C3483",
    "fill:#E74C3C,color:#fff,stroke:#A93226",
    "fill:#7F8C8D,color:#fff,stroke:#566573",
    "fill:#1ABC9C,color:#fff,stroke:#148F77",
    "fill:#F39C12,color:#fff,stroke:#B7770D",
]

# ///////////////////////////////////////////////////////////////
# GLOBAL CONSOLE
# ///////////////////////////////////////////////////////////////

# Force UTF-8 encoding on Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
console = Console(legacy_windows=False)

# ///////////////////////////////////////////////////////////////
# PROJECT RESOLUTION
# ///////////////////////////////////////////////////////////////

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_FILE = PROJECT_ROOT / "docs" / "architecture.md"


def read_package_name() -> str:
    """Read the package name from pyproject.toml [project].name.

    Returns:
        str: The package name with hyphens replaced by underscores.
    """
    pyproject_path = PROJECT_ROOT / "pyproject.toml"
    with pyproject_path.open("rb") as f:
        data = tomllib.load(f)
    name: str = data["project"]["name"].replace("-", "_")
    console.print(f"[cyan]📖[/cyan] Package: [bold green]{name}[/bold green]")
    return name


def discover_layers(package: str) -> list[str]:
    """Discover top-level layers from src/<package>/ subdirectories.

    Falls back to LAYER_ORDER if set, otherwise returns discovered layers
    sorted alphabetically.

    Args:
        package: The package name (used to locate src/<package>/).

    Returns:
        list[str]: Ordered list of layer names.
    """
    if LAYER_ORDER is not None:
        return LAYER_ORDER

    src_root = PROJECT_ROOT / "src" / package
    if not src_root.exists():
        # Fallback: package installed without src layout
        src_root = PROJECT_ROOT / package

    layers = sorted(
        p.name
        for p in src_root.iterdir()
        if p.is_dir() and not p.name.startswith(("_", "."))
    )
    console.print(f"[cyan]🔍[/cyan] Discovered layers: [dim]{', '.join(layers)}[/dim]")
    return layers


def build_style_map(layers: list[str]) -> dict[str, str]:
    """Assign a color style to each layer, cycling through the palette.

    Args:
        layers: Ordered list of layer names.

    Returns:
        dict mapping layer name to a Mermaid style string.
    """
    return {
        layer: _STYLE_PALETTE[i % len(_STYLE_PALETTE)] for i, layer in enumerate(layers)
    }


# ///////////////////////////////////////////////////////////////
# GRAPH BUILDING
# ///////////////////////////////////////////////////////////////


def _layer_of(module: str, layers: list[str]) -> str | None:
    """Return the layer name for a module path, or None if not in a known layer.

    Args:
        module: Fully qualified module name (e.g. ``mypackage.services.compiler``).
        layers: Known layer names to match against.

    Returns:
        str | None: The layer name, or None if not recognized.
    """
    parts = module.split(".")
    if len(parts) >= 2:
        candidate = parts[1]
        return candidate if candidate in layers else None
    return None


def build_layer_edges(package: str, layers: list[str]) -> dict[str, set[str]]:
    """Build a layer-level dependency graph using grimp.

    Args:
        package: The top-level package name to analyze.
        layers: Known layers to group modules into.

    Returns:
        dict mapping each layer to the set of layers it directly imports.
    """
    try:
        import grimp  # noqa: PLC0415
    except ImportError:
        console.print(
            "[red]❌[/red] grimp is required. Install with: [cyan]uv add --dev grimp[/cyan]"
        )
        sys.exit(1)

    console.print(
        f"[cyan]⚙️[/cyan]  Building import graph for [bold]{package}[/bold]..."
    )
    graph = grimp.build_graph(package, include_external_packages=False)
    console.print(
        f"[cyan]📊[/cyan] Analyzed [bold]{len(graph.modules)}[/bold] modules."
    )

    # Group modules by layer
    layer_modules: dict[str, set[str]] = {layer: set() for layer in layers}
    for module in graph.modules:
        layer = _layer_of(module, layers)
        if layer:
            layer_modules[layer].add(module)

    # Collect direct inter-layer import edges
    edges: dict[str, set[str]] = {layer: set() for layer in layers}
    for src_layer, src_modules in layer_modules.items():
        for src_module in sorted(src_modules):
            try:
                imported = graph.find_modules_directly_imported_by(src_module)
            except Exception as e:  # noqa: BLE001
                warnings.warn(
                    f"Could not resolve imports for {src_module}: {e}", stacklevel=2
                )
                continue
            for imp in imported:
                dst_layer = _layer_of(imp, layers)
                if dst_layer and dst_layer != src_layer:
                    edges[src_layer].add(dst_layer)

    return edges


# ///////////////////////////////////////////////////////////////
# MERMAID GENERATION
# ///////////////////////////////////////////////////////////////


def _mermaid_diagram(
    edges: dict[str, set[str]], layers: list[str], styles: dict[str, str]
) -> str:
    """Generate a Mermaid flowchart from layer-level edges.

    Args:
        edges: Layer-level dependency graph.
        layers: Ordered list of layer names.
        styles: Mermaid style string per layer.

    Returns:
        str: Complete Mermaid diagram definition.
    """
    lines = ["graph TD"]

    for layer in layers:
        lines.append(f'    {layer}["{layer}/"]')

    lines.append("")

    has_edges = False
    for src_layer in layers:
        for dst_layer in sorted(edges.get(src_layer, set())):
            lines.append(f"    {src_layer} --> {dst_layer}")
            has_edges = True

    if not has_edges:
        lines.append("    %% No inter-layer imports detected")

    lines.append("")

    for layer in layers:
        if layer in styles:
            lines.append(f"    style {layer} {styles[layer]}")

    return "\n".join(lines)


def _dependency_table(edges: dict[str, set[str]], layers: list[str]) -> str:
    """Generate a markdown table of layer dependencies.

    Args:
        edges: Layer-level dependency graph.
        layers: Ordered list of layer names.

    Returns:
        str: Markdown table source.
    """
    rows = [
        "| Layer | Imports from |",
        "|-------|--------------|",
    ]
    for layer in layers:
        deps = sorted(edges.get(layer, set()))
        deps_str = ", ".join(f"`{d}`" for d in deps) if deps else "—"
        rows.append(f"| `{layer}` | {deps_str} |")
    return "\n".join(rows)


def _role_table(layers: list[str]) -> str:
    """Generate a markdown table of layer responsibilities.

    Descriptions are sourced from the LAYER_ROLES constant.
    Layers without an entry are shown with an empty description.

    Args:
        layers: Ordered list of layer names.

    Returns:
        str: Markdown table source, or empty string if LAYER_ROLES is empty.
    """
    if not LAYER_ROLES:
        return ""

    rows = [
        "| Layer | Responsibility |",
        "|-------|----------------|",
    ]
    for layer in layers:
        role = LAYER_ROLES.get(layer, "")
        rows.append(f"| `{layer}` | {role} |")
    return "\n".join(rows)


# ///////////////////////////////////////////////////////////////
# OUTPUT GENERATION
# ///////////////////////////////////////////////////////////////


def generate_page(
    package: str, edges: dict[str, set[str]], layers: list[str], styles: dict[str, str]
) -> str:
    """Render the full architecture.md content.

    Args:
        package: The package name shown in the page header.
        edges: Layer-level dependency graph.
        layers: Ordered list of layer names.
        styles: Mermaid style string per layer.

    Returns:
        str: Complete Markdown page content.
    """
    mermaid = _mermaid_diagram(edges, layers, styles)
    dep_table = _dependency_table(edges, layers)
    role_section = _role_table(layers)

    roles_block = (
        f"\n---\n\n## Layer Responsibilities\n\n{role_section}\n"
        if role_section
        else ""
    )

    return f"""\
# Architecture — Layer Dependency Graph

Import dependency graph generated by [grimp](https://github.com/seddonym/grimp)
from the live `{package}` source tree.

!!! info "Auto-generated"
    This page is regenerated at each documentation build from the actual source code.
    It reflects the **real** import graph, not a manually maintained diagram.

    To regenerate locally:

    ```bash
    PYTHONPATH=src python .scripts/dev/generate_architecture_graph.py
    ```

---

## Dependency Graph

```mermaid
{mermaid}
```

---

## Layer Import Matrix

{dep_table}
{roles_block}"""


# ///////////////////////////////////////////////////////////////
# MAIN
# ///////////////////////////////////////////////////////////////


def main() -> None:
    """Entry point — resolve package, build graph, write docs/architecture.md."""
    title = Text("🏗️  Architecture Graph Generation", style="bold cyan")
    console.print(Panel.fit(title, border_style="cyan"))
    console.print()

    try:
        package = read_package_name()
        layers = discover_layers(package)
        styles = build_style_map(layers)
        edges = build_layer_edges(package, layers)
        content = generate_page(package, edges, layers, styles)
        OUTPUT_FILE.write_text(content, encoding="utf-8")

        console.print()
        console.print(
            Panel.fit(
                f"[bold green]✓ Architecture graph generated![/bold green]\n"
                f"[dim]{OUTPUT_FILE.relative_to(PROJECT_ROOT)}[/dim]",
                border_style="green",
            )
        )
    except (FileNotFoundError, KeyError) as e:
        console.print()
        console.print(
            Panel.fit(
                f"[bold red]❌ Generation failed![/bold red]\n[red]{e}[/red]",
                border_style="red",
            )
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
