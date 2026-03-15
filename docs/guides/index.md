# User Guides

In-depth guides and tutorials for **EzQt App**.

## Overview

This section provides practical guides for setup, contribution workflow, testing strategy, and styling conventions.

## Available Guides

| Guide                                                                        | Description                                 | Level        |
| ---------------------------------------------------------------------------- | ------------------------------------------- | ------------ |
| [Modular UI Guide](https://neuraaak.github.io/ezqt-app/guides/modular-ui/)   | Configure and disable UI components         | Beginner     |
| [QSS Style Guide](https://neuraaak.github.io/ezqt-app/guides/style-guide/)   | Visual customization with Qt stylesheets    | Beginner     |
| [Development Guide](https://neuraaak.github.io/ezqt-app/guides/development/) | Development workflow and contribution guide | Intermediate |
| [Testing Guide](https://neuraaak.github.io/ezqt-app/guides/testing/)         | Test suite execution and quality strategy   | Advanced     |

## Quick Links

### For Beginners

- [Getting Started](https://neuraaak.github.io/ezqt-app/getting-started/)
- [Examples](https://neuraaak.github.io/ezqt-app/examples/)
- [QSS Style Guide](https://neuraaak.github.io/ezqt-app/guides/style-guide/)

### For Developers

- [Development Guide](https://neuraaak.github.io/ezqt-app/guides/development/)
- [Testing Guide](https://neuraaak.github.io/ezqt-app/guides/testing/)
- [API Reference](https://neuraaak.github.io/ezqt-app/api/)

### For Advanced Users

- [API Reference](https://neuraaak.github.io/ezqt-app/api/)
- [CLI Reference](https://neuraaak.github.io/ezqt-app/cli/)
- [GitHub Repository](https://github.com/neuraaak/ezqt-app)

## Topics

### Core Concepts

- Architecture layers and migration constraints
- Bootstrap and initialization workflows
- Translation and auto-translation behavior
- Test scope selection and CI-quality checks

### Integration

- Application shell setup with `EzApplication` and `EzQt_App`
- Theme and config-driven runtime behavior
- Translation manager and string collection workflow

### Best Practices

- Keep domain/service boundaries explicit
- Prefer service APIs over direct legacy calls
- Maintain tests by scope (unit/integration/robustness)

## Development Workflow

### Setting Up

1. **Clone the repository**

   ```bash
   git clone https://github.com/neuraaak/ezqt-app.git
   cd ezqt_app
   ```

2. **Install in development mode**

   ```bash
   pip install -e ".[dev]"
   ```

3. **Install pre-commit hooks**

   ```bash
   pip install pre-commit
   pre-commit install
   ```

See the [Development Guide](https://neuraaak.github.io/ezqt-app/guides/development/) for detailed setup instructions.

### Testing

Run the test suite to ensure everything works:

```bash
# Run all tests
python tests/run_tests.py --type all

# Run by scope
python tests/run_tests.py --type unit
python tests/run_tests.py --type integration
python tests/run_tests.py --type robustness

# With coverage
python tests/run_tests.py --coverage

# Using pytest directly
pytest tests/unit/ -v
```

See the [Testing Guide](https://neuraaak.github.io/ezqt-app/guides/testing/) for more information.

### Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository** on GitHub
2. **Create a feature branch** (`git checkout -b feature/my-feature`)
3. **Make your changes** with tests
4. **Run tests and linting** (`pytest`, `ruff check`)
5. **Commit your changes** with conventional commits
6. **Push to your fork** (`git push origin feature/my-feature`)
7. **Open a Pull Request** on GitHub

See the [Development Guide](https://neuraaak.github.io/ezqt-app/guides/development/) for contribution guidelines.

## Code Style

EzQt App follows these coding standards:

- **PEP 8** – Python style guide
- **Type Hints** – Full type annotations for Python 3.10+
- **Docstrings** – Google-style docstrings for all public APIs
- **Ruff** – Formatting and linting
- **pyright / ty** – Static type checking

## Documentation

### Building Docs

Build the documentation locally:

```bash
# Install docs dependencies
pip install -e ".[docs]"

# Build documentation
mkdocs build

# Serve locally
mkdocs serve
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

### Using the CLI

```bash
ezqt docs --serve
ezqt docs --serve --port 8080
```

### Writing Docs

Documentation is written in Markdown and built with MkDocs Material:

- **Guides** – Located in `docs/guides/`
- **API Reference** – Auto-generated from docstrings with mkdocstrings
- **Examples** – Code examples in `docs/examples/`
- **CLI** – Command-line interface docs in `docs/cli/`

## See Also

- [Getting Started](https://neuraaak.github.io/ezqt-app/getting-started/)
- [API Reference](https://neuraaak.github.io/ezqt-app/api/)
- [Examples](https://neuraaak.github.io/ezqt-app/examples/)
- [CLI Reference](https://neuraaak.github.io/ezqt-app/cli/)

## Need Help?

- **Issues**: [GitHub Issues](https://github.com/neuraaak/ezqt-app/issues)
- **Repository**: [https://github.com/neuraaak/ezqt-app](https://github.com/neuraaak/ezqt-app)
- **Documentation**: [https://neuraaak.github.io/ezqt-app/](https://neuraaak.github.io/ezqt-app/)
