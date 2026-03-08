# Python Formatting Standards

Code formatting and comment standards that enable easy navigation and clear structure identification in Python files. These standards prioritize readability and maintainability through consistent section markers and organized code layout.

## Overview

Consistent code formatting makes codebases easier to navigate, understand, and maintain. Well-structured files with clear section markers allow developers to quickly locate specific functionality and understand code organization at a glance.

The standards defined here focus on section markers, import organization, and documentation patterns that create visual landmarks in code files. This structure is particularly valuable in large codebases where quick navigation is essential.

## Section Markers

### Main Section Separators

Use forward slashes for main section separators to create clear visual boundaries between major code sections. This style provides excellent visibility and is easy to scan.

- **USE** `# ///////////////////////////////////////////////////////////////` for main section separators
- **PLACE** section title on the line immediately after the separator
- **USE** closing separator after section title for symmetry

```python
# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
```

The forward slash separator creates a strong visual boundary that's easy to spot when scrolling through code. The symmetry of opening and closing separators helps define clear section boundaries.

### Subsection Markers

Use dashes for subsections within classes or functions to create hierarchy without overwhelming visual noise.

- **USE** `# ------------------------------------------------` for subsections within classes or functions
- **PLACE** subsection title between dashes
- **USE** for grouping related methods or functionality

```python
# ------------------------------------------------
# ENHANCED METHODS
# ------------------------------------------------
```

Dash separators provide visual grouping without the weight of main section separators. They're ideal for organizing methods within a class or related functions within a module.

### Section Identification Patterns

Use clear section titles that immediately communicate the section's purpose. Combine section markers with descriptive titles for maximum clarity.

- **USE** uppercase section titles for main sections: `# IMPORTS`, `# CONSTANTS`, `# CLASSES`
- **USE** descriptive titles that match the section content
- **USE** `## ==> SECTION` pattern for special emphasis when needed

```python
## ==> CLASSES
# ///////////////////////////////////////////////////////////////
```

Clear section titles make it easy to jump to specific parts of a file using IDE navigation features. The `## ==>` pattern can be used for special emphasis on important sections.

## File Structure

### Standard File Layout

Organize files with a consistent structure that places related code together. This structure should be flexible enough to accommodate different file types while maintaining consistency.

- **START** with module docstring describing the file's purpose
- **FOLLOW** with imports section
- **ORGANIZE** code into logical sections (constants, classes, functions)
- **END** with public API exports if applicable

```python
# ///////////////////////////////////////////////////////////////
# MODULE_NAME - Brief Description
# Project: project_name
# ///////////////////////////////////////////////////////////////

"""
Module description.

Detailed explanation of the module's purpose and functionality.
"""

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import os
from pathlib import Path
from typing import Optional

# Third-party imports
from rich.console import Console

# Local imports
from .exceptions import CustomError

# ///////////////////////////////////////////////////////////////
# CONSTANTS
# ///////////////////////////////////////////////////////////////
# Configuration values and constants

# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
# Class definitions

# ///////////////////////////////////////////////////////////////
# FUNCTIONS
# ///////////////////////////////////////////////////////////////
# Function definitions

# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////
# Exported symbols

__all__ = ["Class1", "function1"]
```

This structure provides clear navigation points and makes it easy to understand file organization at a glance. The header comment with project name helps identify file context.

### Import Organization

Organize imports into logical groups with clear comments identifying each group. This makes dependencies obvious and helps identify import-related issues.

- **GROUP** imports into: standard library, third-party, local
- **SEPARATE** groups with blank lines
- **USE** comments to identify each group
- **SORT** imports alphabetically within each group

```python
# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from collections.abc import Generator
from contextlib import contextmanager
from typing import Any, Optional

# Third-party imports
from rich.console import Console
from rich.text import Text

# Local imports
from ..core.exceptions import ValidationError
from ..core.interfaces import LoggingHandler
from .utils import helper_function
```

Clear import organization makes dependencies obvious and helps identify potential circular import issues. Grouping also makes it easier to see which external libraries a module depends on.

## Class Structure

### Class Organization

Organize classes with clear section markers that identify different types of methods and properties. This makes it easy to navigate class implementations.

- **USE** `# ///////////////////////////////////////////////////////////////` for major class sections
- **USE** `# ------------------------------------------------` for method groups within classes
- **ORGANIZE** methods logically: `__init__`, getters, setters, public methods, private methods
- **GROUP** related methods together with subsection markers

```python
class ExampleClass:
    """Class description."""

    # ///////////////////////////////////////////////////////////////
    # INIT
    # ///////////////////////////////////////////////////////////////

    def __init__(self, param: str) -> None:
        """Initialize the class."""
        self._param = param

    # ///////////////////////////////////////////////////////////////
    # PUBLIC METHODS
    # ///////////////////////////////////////////////////////////////

    def public_method(self) -> None:
        """Public method description."""
        pass

    # ------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------

    def _private_method(self) -> None:
        """Private method description."""
        pass
```

Clear class organization makes it easy to find specific types of methods. The separation between public and private methods helps understand the class's API.

## Documentation Standards

### Module Docstrings

Module docstrings should provide clear context about the module's purpose and functionality. Keep them concise but informative.

- **INCLUDE** brief description of module purpose
- **EXPLAIN** key functionality and use cases
- **MENTION** important dependencies or requirements
- **KEEP** docstrings focused and readable

```python
"""
Module name - Brief description.

Detailed explanation of the module's purpose, key functionality,
and important usage patterns.
"""
```

Module docstrings serve as the first point of reference for understanding a file's purpose. They should be informative without being verbose.

### Class Docstrings

Class docstrings should explain the class's purpose, key functionality, and important usage patterns. Include examples when they clarify usage.

- **DESCRIBE** the class's purpose and responsibility
- **EXPLAIN** key functionality and behavior
- **INCLUDE** usage examples when helpful
- **MENTION** important design decisions or constraints

```python
class ExampleClass:
    """
    Class description.

    Detailed explanation of the class's functionality, behavior,
    and important design decisions.

    Example:
        >>> instance = ExampleClass(param="value")
        >>> instance.method()
    """
```

Class docstrings help developers understand when and how to use a class. Examples are particularly valuable for complex classes.

### Function and Method Docstrings

Function docstrings should follow a consistent format that includes description, parameters, return values, and exceptions. Use Google-style docstrings for consistency.

- **DESCRIBE** the function's purpose and behavior
- **DOCUMENT** all parameters with types and descriptions
- **DOCUMENT** return values with types and descriptions
- **LIST** exceptions that may be raised
- **INCLUDE** examples for complex functions

```python
def example_function(
    param1: str, param2: Optional[int] = None
) -> bool:
    """Brief description of the function.

    Detailed explanation of what the function does, how it works,
    and any important behavior or side effects.

    Args:
        param1: Description of the first parameter
        param2: Description of the optional second parameter

    Returns:
        bool: Description of the return value

    Raises:
        ValueError: When parameter validation fails
        CustomError: When operation cannot complete

    Example:
        >>> result = example_function("test", 42)
        >>> print(result)
        True
    """
```

Consistent docstring format makes code easier to understand and enables automatic documentation generation. The Google style is widely recognized and tool-friendly.

## Inline Comments

### Comment Language

Comments should be written in English by default to maintain consistency across the codebase and enable international collaboration. Only use other languages when explicitly requested in a prompt or when working with code that has established non-English conventions.

- **WRITE** comments in English by default
- **USE** other languages only when explicitly mentioned in a prompt
- **MAINTAIN** language consistency within a file
- **PREFER** clear English over complex technical jargon

English comments ensure code is accessible to international teams and align with most Python documentation standards. Consistency in comment language reduces cognitive load when reading code.

### Comment Guidelines

Inline comments should clarify non-obvious code behavior, not restate what the code does. Use comments to explain "why" rather than "what". Avoid comments that add no value or provide information that's already obvious from the code.

- **EXPLAIN** non-obvious behavior or design decisions
- **CLARIFY** complex logic or algorithms with high abstraction
- **DOCUMENT** workarounds, edge cases, or important gotchas
- **AVOID** comments that simply restate the code
- **AVOID** comments that add context-unrelated information
- **AVOID** comments that document obvious operations

```python
# Good: Explains why, not what
# Convert message to string safely - handles None and special objects
message = safe_str_convert(message)

# Good: Documents complex abstraction
# Map log levels to patterns for consistent output formatting
pattern_map = {
    "DEBUG": Pattern.DEBUG,
    "INFO": Pattern.INFO,
}

# Bad: Restates what the code does
# Setting variable to 64
x = 64

# Bad: Adds unnecessary context
# This method is no longer legacy (removed in refactoring)
def process_data(data: list) -> None:
    pass
```

Good comments explain the reasoning behind code, not just what it does. They're particularly valuable for complex logic, high abstraction levels, or non-obvious design decisions. Comments should add genuine value by explaining things that aren't immediately clear from reading the code.

### When to Comment

Comments should be used judiciously. Only add comments when they provide genuine value that cannot be inferred from the code itself.

- **COMMENT** complex sections with high abstraction or multiple layers of indirection
- **COMMENT** non-obvious behavior, edge cases, or gotchas that could surprise developers
- **COMMENT** workarounds, temporary solutions, or known limitations
- **COMMENT** business logic or domain-specific reasoning that isn't obvious from code
- **AVOID** commenting simple, self-explanatory code
- **AVOID** adding comments during refactoring that document the refactoring process itself
- **AVOID** comments that add meta-information about code changes or maintenance history

```python
# Good: Explains complex abstraction
# This decorator handles retry logic with exponential backoff, but
# skips retries for authentication errors to prevent account lockouts
@retry_with_backoff(skip_on=[AuthenticationError])
def fetch_user_data(user_id: int) -> User:
    pass

# Good: Documents important gotcha
# Note: This method modifies the input list in-place for performance.
# Call copy() if you need to preserve the original.
def process_items(items: list[Item]) -> None:
    pass

# Bad: Obvious operation doesn't need comment
# Initialize the counter
counter = 0

# Bad: Meta-information about code changes
# Removed legacy code here, now using new implementation
def new_method() -> None:
    pass
```

Comments are most valuable when they explain things that aren't obvious from the code: complex abstractions, non-obvious behavior, important edge cases, or domain-specific reasoning. Avoid comments that simply describe what the code does or add meta-information about code maintenance.

### Section Comments

Use section comments to group related code and provide context. These comments help organize code and make navigation easier.

- **USE** section comments to group related functionality
- **KEEP** section comments concise and descriptive
- **UPDATE** section comments when code structure changes

```python
# ------------------------------------------------
# ERROR HANDLING
# ------------------------------------------------

def handle_error(error: Exception) -> None:
    """Handle errors gracefully."""
    pass
```

Section comments create visual landmarks that make it easier to navigate code. They're especially useful in longer files.

## Best Practices

### Consistency

Consistency is more important than perfection. Choose a style and apply it consistently across the codebase.

- **MAINTAIN** consistent section marker style throughout the project
- **USE** the same import organization pattern in all files
- **FOLLOW** the same docstring format across modules
- **APPLY** formatting standards uniformly

Consistent formatting reduces cognitive load when reading code. Developers can focus on understanding logic rather than adapting to different formatting styles.

### Flexibility

These standards should be guidelines, not rigid rules. Adapt them to fit specific file needs while maintaining overall consistency.

- **ADAPT** structure to fit file-specific needs
- **OMIT** sections that don't apply to a particular file
- **ADD** sections when they improve organization
- **BALANCE** structure with readability

Over-structuring small files can reduce readability. Use structure where it adds value, not where it creates unnecessary overhead.

### Maintenance

Keep formatting standards up to date as the codebase evolves. Review and refine standards based on team feedback and changing needs.

- **REVIEW** formatting standards periodically
- **UPDATE** standards based on team feedback
- **DOCUMENT** any deviations or exceptions
- **ENFORCE** standards through code review and tooling

Formatting standards should evolve with the codebase. Regular review ensures they remain useful and don't become outdated.
