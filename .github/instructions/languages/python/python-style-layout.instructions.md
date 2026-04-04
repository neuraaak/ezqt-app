# Python Style & Layout Standards (UIA)

Visual structure, import organization, and documentation standards for Python source files.

<rules>
- **SECTIONING:** Use `# ///////////////////////////////////////////////////////////////` for main sections.
- **DOCSTRINGS:** Use Google-style docstrings exclusively.
- **IMPORTS:** Group by: 1. stdlib, 2. 3rd-party, 3. local. Sort alphabetically.
- **LANGUAGE:** Always use English for comments and docstrings.
- **COMMENTS:** Explain "why", not "what". Avoid noise.
</rules>

## Main Section Separators

Use the forward slash separator to create clear visual boundaries.

```python
# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
```

## Subsection Markers

Use dashes for internal organization within classes or functions.

```python
# ------------------------------------------------
# PRIVATE METHODS
# ------------------------------------------------
```

## Import Organization Pattern

```python
# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library
import os
from pathlib import Path

# Third-party
from rich.console import Console

# Local
from .exceptions import CustomError
```

<examples>
# Google-style docstring example
def calculate_metrics(data: list[float]) -> dict[str, float]:
    """Calculates statistical metrics for a dataset.

    Args:
        data: A list of numeric measurements.

    Returns:
        dict: A mapping of metric names to values.
    """

</examples>

<success_criteria>

- Section markers used for navigation.
- Imports correctly grouped and sorted.
- Google docstrings present for all public symbols.

</success_criteria>
