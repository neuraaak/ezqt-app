# CLI reference

`ezqt` is the command-line interface for **EzQt App**. It exposes project
initialization, test execution, documentation serving, and utility commands.

## 💻 Usage

```bash
ezqt [OPTIONS] COMMAND [ARGS]...
```

## ⚙️ Global options

| Option      | Short | Description                |
| :---------- | :---- | :------------------------- |
| `--version` | `-v`  | Show the version and exit  |
| `--help`    | `-h`  | Show help message and exit |

## 📋 Commands

| Command                               | Description                                               |
| :------------------------------------ | :-------------------------------------------------------- |
| [`init`](#ezqt-init)                  | Initialize project assets and configuration               |
| [`create`](#ezqt-create)              | Create a new project from a template                      |
| [`convert`](#ezqt-convert--ezqt-mkqm) | Convert translation `.ts` files to Qt binary `.qm` format |
| [`mkqm`](#ezqt-convert--ezqt-mkqm)    | Alias for `convert`                                       |
| [`test`](#ezqt-test)                  | Run the test suite                                        |
| [`docs`](#ezqt-docs)                  | Serve the documentation locally                           |
| [`info`](#ezqt-info)                  | Display package and runtime information                   |

<a id="ezqt-init"></a>

## 🔧 `ezqt init`

Initialize project assets and configuration.

```bash
ezqt init [OPTIONS]
```

| Option      | Short | Description                       |
| :---------- | :---- | :-------------------------------- |
| `--force`   | `-f`  | Force overwrite of existing files |
| `--verbose` | `-v`  | Verbose output                    |
| `--no-main` |       | Skip `main.py` generation         |

<a id="ezqt-create"></a>

## 🔧 `ezqt create`

Create a new project from a template.

```bash
ezqt create [OPTIONS]
```

| Option       | Short | Description    |
| :----------- | :---- | :------------- |
| `--template` | `-t`  | Template type  |
| `--name`     | `-n`  | Project name   |
| `--verbose`  | `-v`  | Verbose output |

<a id="ezqt-convert--ezqt-mkqm"></a>

## 🔧 `ezqt convert` / `ezqt mkqm`

Convert translation `.ts` files to Qt binary `.qm` format.

```bash
ezqt convert
ezqt mkqm
```

No options.

<a id="ezqt-test"></a>

## 🔧 `ezqt test`

Run the test suite.

```bash
ezqt test [OPTIONS]
```

| Option          | Short | Description                 |
| :-------------- | :---- | :-------------------------- |
| `--unit`        | `-u`  | Run unit tests              |
| `--integration` | `-i`  | Run integration tests       |
| `--coverage`    | `-c`  | Run with coverage reporting |
| `--verbose`     | `-v`  | Verbose output              |

<a id="ezqt-docs"></a>

## 🔧 `ezqt docs`

Serve the documentation locally.

```bash
ezqt docs [OPTIONS]
```

| Option    | Short | Description                   |
| :-------- | :---- | :---------------------------- |
| `--serve` | `-s`  | Start local dev server        |
| `--port`  | `-p`  | Port number (default: `8000`) |

<a id="ezqt-info"></a>

## 🔧 `ezqt info`

Display package and runtime information.

```bash
ezqt info
```

No options.

## ⚙️ Environment variables

| Variable            | Description                                     |
| :------------------ | :---------------------------------------------- |
| `EZQT_VERBOSE`      | Enable verbose mode by default for all commands |
| `EZQT_PROJECT_ROOT` | Override the project root directory detection   |
| `EZQT_THEME_DIR`    | Custom path to the themes directory             |
| `EZQT_NO_COLOR`     | Disable colored CLI output                      |

## 🧪 Examples

```bash
# Initialize a new project
ezqt init --verbose

# Bootstrap with force overwrite
ezqt init --force --no-main

# Create a project from the basic template
ezqt create --template basic --name my_app

# Run unit tests with coverage
ezqt test --unit --coverage

# Serve documentation on a custom port
ezqt docs --serve --port 8080

# Convert translation files
ezqt convert

# Display runtime info
ezqt info
```

## Troubleshooting

| Issue                      | Solution                                                           |
| :------------------------- | :----------------------------------------------------------------- |
| `ezqt` not found           | Reinstall package in active environment: `pip install -e ".[dev]"` |
| Init fails in wrong folder | Run command from project root                                      |
| Docs serve fails on port   | Use another `--port` value                                         |

??? note "CLI source"
    CLI implementation: `src/ezqt_app/cli/main.py`
