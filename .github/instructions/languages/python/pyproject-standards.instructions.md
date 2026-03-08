# Pyproject.toml Standards

Configuration file formatting and organization standards that enable easy navigation and clear structure identification in Python project configuration. These standards prioritize readability and maintainability through consistent section markers and organized layout.

## Overview

The `pyproject.toml` file is the central configuration hub for modern Python projects. A well-organized configuration file makes it easy to find settings, understand project structure, and maintain consistency across tools. Clear section markers and logical grouping reduce cognitive load when navigating complex configurations.

## Section Markers

### Section Separator Format

Use forward slashes with emojis for main section separators to create clear visual boundaries. This style provides excellent visibility and quick section identification.

- **USE** `# ///////////////////////////////////////////////////////////////` for section separators
- **INCLUDE** emoji at the start of section title for quick visual identification
- **ADD** descriptive subtitle explaining section purpose
- **CLOSE** with matching separator for symmetry

```toml
# ///////////////////////////////////////////////////////////////
# 🔨 BUILD SYSTEM
# Defines the build backend and requirements
# ///////////////////////////////////////////////////////////////

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
```

The emoji prefix enables instant section recognition when scrolling. The descriptive subtitle provides context without needing to read configuration values.

### Recommended Section Emojis

Use consistent emojis that visually represent each section's purpose:

| Section                   | Emoji | Rationale             |
| ------------------------- | ----- | --------------------- |
| Build System              | 🔨    | Construction/building |
| Project Metadata          | 📦    | Package/box           |
| Dependencies              | 📚    | Library/books         |
| Optional Dependencies     | 🛠️    | Tools                 |
| Project URLs              | 🔗    | Links                 |
| Setuptools Config         | 📦    | Package configuration |
| Code Formatting & Linting | 🎨    | Art/style             |
| Type Checking             | ✅    | Validation/check      |
| Testing & Coverage        | 🧪    | Lab/testing           |
| Security Tools            | 🔒    | Lock/security         |

Consistent emoji usage creates a visual language that developers can quickly learn and recognize.

### Tool-Specific Comments

For individual tools within a section, use single-line comments that identify the tool and its purpose:

```toml
# Black: Code formatter (88 char line length, Python 3.10+)
[tool.black]
line-length = 88

# isort: Import sorting (black-compatible profile)
[tool.isort]
profile = "black"
```

These comments help identify which tool each configuration block belongs to, especially when tools have similar settings.

## File Structure

### Standard Section Order

Organize sections in a logical order that follows the natural flow of project configuration:

1. **Build System** - How the package is built
2. **Project Metadata** - Package identity and information
3. **Dependencies** - Runtime requirements
4. **Optional Dependencies** - Development and test requirements
5. **Project URLs** - Links to resources
6. **Setuptools Configuration** - Package discovery settings
7. **Code Formatting & Linting Tools** - Black, isort, Ruff
8. **Type Checking Tools** - ty, pyright, mypy
9. **Testing & Coverage** - pytest, coverage
10. **Security Tools** - bandit

```toml
# ///////////////////////////////////////////////////////////////
# 🔨 BUILD SYSTEM
# ///////////////////////////////////////////////////////////////

# ///////////////////////////////////////////////////////////////
# 📦 PROJECT METADATA
# ///////////////////////////////////////////////////////////////

# ///////////////////////////////////////////////////////////////
# 📚 DEPENDENCIES
# ///////////////////////////////////////////////////////////////

# ///////////////////////////////////////////////////////////////
# 🛠️ OPTIONAL DEPENDENCIES
# ///////////////////////////////////////////////////////////////

# ... continue with remaining sections
```

This order places foundational configuration first, then runtime concerns, then development tooling. It mirrors the typical workflow of understanding a project.

### Dependency Organization

Organize optional dependencies with inline comments grouping related packages:

```toml
[project.optional-dependencies]
dev = [
    # Development tools
    "black>=23.0.0",
    "isort>=5.12.0",
    "ruff>=0.1.0",
    "ty>=0.0.13",
    "pyright>=1.1.0",
    "pre-commit>=3.0.0",

    # Security
    "bandit>=1.7.0",

    # Tests
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "pytest-mock>=3.10.0",
    "pytest-xdist>=3.0.0",

    # Build and distribution
    "build>=1.0.0",
    "twine>=4.0.0",
]
```

Grouping dependencies by purpose makes it easy to understand why each package is included and simplifies maintenance.

## Tool Configuration Patterns

### Consistent Exclude Patterns

Maintain consistent exclude patterns across tools to avoid unexpected behavior:

```toml
# Common exclude patterns - use consistently across tools
exclude = [
    "**/__pycache__",
    ".venv",
    "venv",
    "build",
    "dist",
    "tests",
    "docs",
    "examples",
]
```

Inconsistent exclusions can lead to tools processing unexpected files. Define a standard set and apply it uniformly.

### Version Targeting

Specify Python version consistently across all tools:

```toml
# Black
target-version = ['py310', 'py311', 'py312']

# Ruff
target-version = "py310"

# Pyright
pythonVersion = "3.10"

# ty
python-version = "3.10"
```

All tools should target the same minimum Python version to ensure consistent behavior.

### Line Length Consistency

Use consistent line length across formatting tools:

```toml
# Black
line-length = 88

# isort
line_length = 88

# Ruff
line-length = 88
```

The value 88 is Black's default and provides a good balance between readability and space efficiency.

## Ruff Configuration (within Code Formatting & Linting)

Ruff is configured within the same section as Black and isort since it handles both linting and formatting.

### Rule Selection with Comments

Document rule categories with inline comments for clarity:

```toml
[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
    "S",   # bandit security
    "T20", # flake8-print
    "ARG", # flake8-unused-arguments
    "PIE", # flake8-pie
    "SIM", # flake8-simplify
]
```

Comments explain what each rule code represents, making configuration self-documenting.

### Ignore Rules with Explanations

Document why rules are ignored:

```toml
ignore = [
    "E501", # line too long, handled by black
    "B008", # do not perform function calls in argument defaults
    "S101", # assert_used (for tests)
    "S106", # hardcoded_password_funcarg
    "T201", # print statements (for init.py and scripts)
    "S603", # subprocess.run without check=True
]
```

Explaining ignored rules helps future maintainers understand the reasoning and avoid accidentally re-enabling them.

### Per-File Ignores

Use per-file ignores for context-specific exceptions:

```toml
[tool.ruff.lint.per-file-ignores]
"tests/**/*" = ["S101", "S311", "E501", "ARG002", "S105", "S602", "S603"]
"examples/**/*" = ["T201", "E501"]
"ezqt_app/cli/**/*" = ["T201", "E501", "S603"]
```

This approach allows stricter rules in production code while permitting necessary exceptions in tests and examples.

## Pytest Configuration

### Marker Documentation

Document test markers with clear descriptions:

```toml
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests (default)",
    "cli: marks tests related to CLI",
]
```

Clear marker descriptions help developers understand when to use each marker and how to filter tests.

### Coverage Thresholds

Set meaningful coverage thresholds:

```toml
addopts = [
    "--cov-fail-under=60",
]
```

The threshold should be realistic for the project. Start lower and increase as coverage improves.

## Best Practices

### Synchronization

Keep related files synchronized:

- **SYNC** `pyproject.toml` dependencies with `requirements*.in` files
- **SYNC** Python version across all tool configurations
- **SYNC** exclude patterns across all tools
- **UPDATE** all locations when making changes

### Validation

Validate configuration after changes:

- **TEST** that all tools can parse the configuration
- **VERIFY** exclude patterns work as expected
- **CHECK** that version constraints are compatible

### Documentation

Keep configuration self-documenting:

- **USE** section comments to explain organization
- **ADD** inline comments for non-obvious settings
- **DOCUMENT** ignored rules and exceptions
- **EXPLAIN** custom configurations

## Example Template

Complete example showing all standards:

```toml
# ///////////////////////////////////////////////////////////////
# 🔨 BUILD SYSTEM
# Defines the build backend and requirements
# ///////////////////////////////////////////////////////////////

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

# ///////////////////////////////////////////////////////////////
# 📦 PROJECT METADATA
# Package information, version, authors, and classifiers
# ///////////////////////////////////////////////////////////////

[project]
name = "package-name"
version = "1.0.0"
description = "Package description"
readme = "README.md"
requires-python = ">=3.10"
license = { text = "MIT" }
authors = [{ name = "Author Name" }]

# ///////////////////////////////////////////////////////////////
# 📚 DEPENDENCIES
# Core production dependencies for runtime
# ///////////////////////////////////////////////////////////////

dependencies = [
    "dependency>=1.0.0",
]

# ///////////////////////////////////////////////////////////////
# 🛠️ OPTIONAL DEPENDENCIES
# Development tools, testing, and build dependencies
# ///////////////////////////////////////////////////////////////

[project.optional-dependencies]
dev = [
    # Development tools
    "black>=23.0.0",
    "ruff>=0.1.0",

    # Tests
    "pytest>=7.0.0",
]

# ///////////////////////////////////////////////////////////////
# 🎨 CODE FORMATTING & LINTING TOOLS
# Auto-formatting, import sorting, and style checking
# ///////////////////////////////////////////////////////////////

# Black: Code formatter
[tool.black]
line-length = 88
target-version = ['py310', 'py311', 'py312']

# isort: Import sorting (black-compatible profile)
[tool.isort]
profile = "black"
line_length = 88

# Ruff: All-in-one linter with comprehensive rule sets
[tool.ruff]
target-version = "py310"
line-length = 88

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "F",   # pyflakes
    "I",   # isort
]

# ///////////////////////////////////////////////////////////////
# 🧪 TESTING & COVERAGE TOOLS
# Test execution, coverage analysis, and test configuration
# ///////////////////////////////////////////////////////////////

# Pytest: Test runner
[tool.pytest.ini_options]
testpaths = ["tests"]
```

This template demonstrates all formatting standards while remaining practical and adaptable to different projects.
