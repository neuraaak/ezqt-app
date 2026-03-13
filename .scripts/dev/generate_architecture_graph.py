#!/usr/bin/env python3
# ///////////////////////////////////////////////////////////////
# GENERATE_ARCHITECTURE_GRAPH - Import dependency graph for docs
# ///////////////////////////////////////////////////////////////

"""
Generate architecture dependency graph for EzQt-App documentation.

Uses grimp to analyze the actual import graph of the ezqt_app package
and produces a Mermaid flowchart + dependency table written to
docs/architecture.md (replacing the skeleton).

Usage:
    PYTHONPATH=src python .scripts/dev/generate_architecture_graph.py
    # or in CI (package installed in editable mode):
    python .scripts/dev/generate_architecture_graph.py
"""

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import sys
import warnings
from pathlib import Path

# ///////////////////////////////////////////////////////////////
# CONSTANTS
# ///////////////////////////////////////////////////////////////

PACKAGE = "ezqt_app"
OUTPUT_FILE = Path(__file__).resolve().parents[2] / "docs" / "architecture.md"

# Ordered layers — defines graph node order and which layers to include
LAYERS = ["cli", "services", "widgets", "domain", "shared", "utils"]

LAYER_LABELS = {
    "cli": "cli/<br/>(CLI Entry Point)",
    "services": "services/<br/>(Business Logic)",
    "widgets": "widgets/<br/>(Qt Widget Implementations)",
    "domain": "domain/<br/>(Models + Ports + Results)",
    "shared": "shared/<br/>(Shared Resources)",
    "utils": "utils/<br/>(Utilities)",
}

LAYER_STYLES = {
    "cli": "fill:#4A90D9,color:#fff,stroke:#2C5F8A",
    "services": "fill:#5BA85A,color:#fff,stroke:#3A6B39",
    "widgets": "fill:#E8922A,color:#fff,stroke:#A3621B",
    "domain": "fill:#9B59B6,color:#fff,stroke:#6C3483",
    "shared": "fill:#E74C3C,color:#fff,stroke:#A93226",
    "utils": "fill:#7F8C8D,color:#fff,stroke:#566573",
}

LAYER_ROLES = {
    "cli": "Public entry point — Click CLI (`ezqt` command)",
    "services": "Business logic and orchestration (`ApplicationService`, `ConfigService`, `TranslationManager`, …)",
    "widgets": "Concrete Qt widget implementations (`MainWindow`, `SplashScreen`, extended widgets, …)",
    "domain": "Pure domain — models, ports (interfaces), result types, errors (no Qt dependency)",
    "shared": "Cross-layer shared resources and constants",
    "utils": "Pure utility functions and helpers",
}

# ///////////////////////////////////////////////////////////////
# GRAPH BUILDING
# ///////////////////////////////////////////////////////////////


def _layer_of(module: str) -> str | None:
    """Return the layer name for a module path, or None if not in a known layer."""
    parts = module.split(".")
    if len(parts) >= 2:
        candidate = parts[1]
        return candidate if candidate in LAYERS else None
    return None


def build_layer_edges() -> dict[str, set[str]]:
    """
    Build a layer-level dependency graph using grimp.

    Returns:
        dict mapping each layer to the set of layers it directly imports.
    """
    try:
        import grimp  # noqa: PLC0415
    except ImportError:
        print("ERROR: grimp is required. Install with: pip install grimp")
        print("       (or via: pip install import-linter)")
        sys.exit(1)

    print(f"  Building import graph for '{PACKAGE}'...")
    graph = grimp.build_graph(PACKAGE, include_external_packages=False)
    print(f"  Analyzed {len(graph.modules)} modules.")

    # Group modules by layer
    layer_modules: dict[str, set[str]] = {layer: set() for layer in LAYERS}
    for module in graph.modules:
        layer = _layer_of(module)
        if layer:
            layer_modules[layer].add(module)

    # Collect direct inter-layer import edges
    edges: dict[str, set[str]] = {layer: set() for layer in LAYERS}
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
                dst_layer = _layer_of(imp)
                if dst_layer and dst_layer != src_layer:
                    edges[src_layer].add(dst_layer)

    return edges


# ///////////////////////////////////////////////////////////////
# MERMAID GENERATION
# ///////////////////////////////////////////////////////////////


def _mermaid_diagram(edges: dict[str, set[str]]) -> str:
    """Generate a Mermaid flowchart from layer-level edges."""
    lines = ["graph TD"]

    # Node definitions
    for layer in LAYERS:
        label = LAYER_LABELS.get(layer, layer)
        lines.append(f'    {layer}["{label}"]')

    lines.append("")

    # Edges
    has_edges = False
    for src_layer in LAYERS:
        for dst_layer in sorted(edges.get(src_layer, set())):
            lines.append(f"    {src_layer} --> {dst_layer}")
            has_edges = True

    if not has_edges:
        lines.append("    %% No inter-layer imports detected")

    lines.append("")

    # Node styles
    for layer, style in LAYER_STYLES.items():
        lines.append(f"    style {layer} {style}")

    return "\n".join(lines)


def _dependency_table(edges: dict[str, set[str]]) -> str:
    """Generate a markdown table of layer dependencies."""
    rows = [
        "| Layer | Imports from |",
        "|-------|--------------|",
    ]
    for layer in LAYERS:
        deps = sorted(edges.get(layer, set()))
        deps_str = ", ".join(f"`{d}`" for d in deps) if deps else "—"
        rows.append(f"| `{layer}` | {deps_str} |")
    return "\n".join(rows)


def _role_table() -> str:
    """Generate a markdown table of layer responsibilities."""
    rows = [
        "| Layer | Responsibility |",
        "|-------|----------------|",
    ]
    for layer in LAYERS:
        role = LAYER_ROLES.get(layer, "")
        rows.append(f"| `{layer}` | {role} |")
    return "\n".join(rows)


# ///////////////////////////////////////////////////////////////
# OUTPUT GENERATION
# ///////////////////////////////////////////////////////////////


def generate_page(edges: dict[str, set[str]]) -> str:
    """Render the full architecture.md content."""
    mermaid = _mermaid_diagram(edges)
    dep_table = _dependency_table(edges)
    role_table = _role_table()

    return f"""\
# Architecture — Layer Dependency Graph

Import dependency graph generated by [grimp](https://github.com/seddonym/grimp)
from the live `{PACKAGE}` source tree.

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

---

## Layer Responsibilities

{role_table}
"""


# ///////////////////////////////////////////////////////////////
# MAIN
# ///////////////////////////////////////////////////////////////


def main() -> None:
    """Entry point — build graph, generate page, write to docs/."""
    print("Generating architecture dependency graph...")
    edges = build_layer_edges()
    content = generate_page(edges)
    OUTPUT_FILE.write_text(content, encoding="utf-8")
    print(
        f"Architecture graph written to: {OUTPUT_FILE.relative_to(OUTPUT_FILE.parents[2])}"
    )


if __name__ == "__main__":
    main()
