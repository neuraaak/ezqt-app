# CLI -- Command-Line Interface

Documentation for the **ezqt** command-line interface.

---

## Installation

```bash
pip install -e ".[dev]"

# Verify installation
ezqt --version
```

---

## Commands

### `ezqt init` -- Initialize Project

Initialize project assets and configuration.

| Option      | Short | Description                       |
| ----------- | ----- | --------------------------------- |
| `--force`   | `-f`  | Force overwrite of existing files |
| `--verbose` | `-v`  | Verbose output                    |
| `--no-main` |       | Skip `main.py` generation         |

**Examples:**

```bash
ezqt init
ezqt init --verbose
ezqt init --force --no-main
```

### `ezqt create` -- Create Project Template

Create project template.

| Option       | Short | Description    |
| ------------ | ----- | -------------- |
| `--template` | `-t`  | Template type  |
| `--name`     | `-n`  | Project name   |
| `--verbose`  | `-v`  | Verbose output |

**Examples:**

```bash
ezqt create --template basic --name my_app
ezqt create --template advanced --name my_app --verbose
```

### `ezqt convert` / `ezqt mkqm` -- Convert Translation Files

Convert translation files to Qt binary format.

**Examples:**

```bash
ezqt convert
ezqt mkqm --verbose
```

### `ezqt test` -- Run Tests

Run tests from CLI wrappers.

| Option          | Short | Description         |
| --------------- | ----- | ------------------- |
| `--unit`        | `-u`  | Unit tests          |
| `--integration` | `-i`  | Integration tests   |
| `--coverage`    | `-c`  | Tests with coverage |
| `--verbose`     | `-v`  | Verbose output      |

**Examples:**

```bash
ezqt test --unit
ezqt test --integration
ezqt test --coverage --verbose
```

### `ezqt docs` -- Documentation Utilities

Serve docs locally.

| Option    | Short | Description          |
| --------- | ----- | -------------------- |
| `--serve` | `-s`  | Serve docs locally   |
| `--port`  | `-p`  | Port (default: 8000) |

### `ezqt info` -- Package Information

Display package/runtime information.

```bash
ezqt info
```

---

## Use Cases

### For Developers

```bash
ezqt init --verbose
ezqt test --unit --coverage
ezqt info
```

### For Maintainers

```bash
ezqt docs --serve --port 8000
ezqt convert
```

---

## Environment Variables

| Variable            | Description                                     |
| ------------------- | ----------------------------------------------- |
| `EZQT_VERBOSE`      | Enable verbose mode by default for all commands |
| `EZQT_PROJECT_ROOT` | Override the project root directory detection   |
| `EZQT_THEME_DIR`    | Custom path to the themes directory             |
| `EZQT_NO_COLOR`     | Disable colored CLI output                      |

---

## Troubleshooting

| Issue                      | Solution                                |
| -------------------------- | --------------------------------------- |
| `ezqt` not found           | Reinstall package in active environment |
| Init fails in wrong folder | Run command from project root           |
| Docs serve fails on port   | Use another `--port` value              |

---

## Implementation

CLI source: `src/ezqt_app/cli/main.py`

---

## Resources

- [API Reference](https://neuraaak.github.io/ezqt-app/api/) -- Widget documentation
- [Examples](https://neuraaak.github.io/ezqt-app/examples/) -- Example code
- [Testing Guide](https://neuraaak.github.io/ezqt-app/guides/testing/) -- Testing guidelines and best practices
- [QSS Style Guide](https://neuraaak.github.io/ezqt-app/guides/style-guide/) -- Visual customization
