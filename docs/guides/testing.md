# Testing guide

Comprehensive documentation for the **ezqt_app** test suite.
The test suite ensures reliability and correctness of all services, widgets, and workflows
through three complementary scopes.

## 🏗️ Test structure

### Directory organization

```text
tests/
├── conftest.py                          # Shared fixtures and pytest configuration
├── pytest.ini                           # Markers, coverage, and runner settings
├── run_tests.py                         # Test runner script with CLI options
├── unit/                                # Fast, isolated unit tests
│   ├── test_services/
│   │   ├── test_app_functions.py        # ConfigService tests
│   │   ├── test_app_settings.py         # SettingsService tests
│   │   └── test_translation_manager.py  # TranslationManager tests
│   ├── test_utils/
│   │   └── test_cli.py                  # CLI initialization tests
│   └── test_widgets/
│       ├── test_core/
│       │   ├── test_ez_app.py           # EzApplication tests
│       │   ├── test_header.py           # Header widget tests
│       │   ├── test_menu.py             # Menu widget tests
│       │   ├── test_page_container.py   # PageContainer tests
│       │   └── test_settings_panel.py   # SettingsPanel tests
│       └── test_extended/
│           └── test_setting_widgets.py  # Extended setting widget tests
└── integration/                         # Cross-component integration tests
    ├── test_application/
    │   └── test_app_flow.py             # Full app initialization flow
    └── test_services/
        └── test_translations.py         # Translation workflow integration
```

### Test statistics

| Category         | Files  | Tests    |
| :--------------- | :----- | :------- |
| Services         | 3      | ~27      |
| Utils            | 1      | 3        |
| Core widgets     | 5      | ~86      |
| Extended widgets | 1      | ~33      |
| Integration      | 2      | ~27      |
| **Total**        | **12** | **~176** |

## 🧪 Running tests

=== "By scope"

    ```bash
    python tests/run_tests.py --type unit
    python tests/run_tests.py --type integration
    python tests/run_tests.py --type robustness
    python tests/run_tests.py --type all
    ```

=== "With coverage"

    ```bash
    python tests/run_tests.py --coverage
    ```

=== "Fast mode"

    ```bash
    # Excludes @pytest.mark.slow tests
    python tests/run_tests.py --fast
    ```

=== "Parallel mode"

    ```bash
    # Requires pytest-xdist
    python tests/run_tests.py --parallel
    ```

=== "pytest directly"

    ```bash
    pytest tests/unit/ -v
    pytest tests/integration/ -v
    pytest -m qt tests/unit/
    ```

## 📊 Coverage

Generate the HTML coverage report:

```bash
python tests/run_tests.py --coverage
```

View terminal details:

```bash
pytest --cov=ezqt_app --cov-report=term-missing tests/
```

Open the HTML report:

```text
htmlcov/index.html
```

## ⚙️ Test configuration

### `conftest.py` — shared fixtures

**Location:** `tests/conftest.py`

| Fixture                  | Scope    | Description                                         |
| :----------------------- | :------- | :-------------------------------------------------- |
| `qt_application`         | session  | `EzApplication` instance shared across all Qt tests |
| `qt_widget_cleanup`      | function | Calls `processEvents()` for cleanup after each test |
| `ez_application_cleanup` | function | Fresh `EzApplication` instance for singleton tests  |
| `wait_for_signal`        | function | Helper to wait for a Qt signal with timeout         |
| `mock_icon_path`         | function | Temp PNG file for icon-loading tests                |
| `mock_svg_path`          | function | Temp SVG file for icon-loading tests                |
| `mock_translation_files` | function | Temp `.ts` files (EN + FR) for translation tests    |
| `mock_yaml_config`       | function | Temp `app.config.yaml` for config service tests     |

### Test markers

Configured in `tests/pytest.ini`:

| Marker        | Description                               |
| :------------ | :---------------------------------------- |
| `unit`        | Unit tests (isolated modules/components)  |
| `integration` | Cross-component behavior tests            |
| `robustness`  | Edge case and failure path tests          |
| `slow`        | Slow tests (exclude with `-m "not slow"`) |
| `qt`          | Tests requiring a live `QApplication`     |

Usage examples:

```bash
# Run only unit tests
pytest -m unit

# Exclude slow tests
pytest -m "not slow"

# Run integration and robustness
pytest -m "integration or robustness"

# Run Qt-dependent tests only
pytest -m qt tests/unit/
```

## ✏️ Writing tests

### Test isolation

Each test should be self-contained and independent:

```python
def test_config_loads_defaults(mock_yaml_config):
    service = ConfigService(config_path=mock_yaml_config)
    assert service.get("app.name") == "Test Application"
```

### Fixture usage

Use shared fixtures from `conftest.py` rather than ad-hoc setup:

```python
def test_translation_switch(qt_application, mock_translation_files):
    manager = TranslationManager()
    manager.load_language_by_code("fr")
    assert manager.get_current_language_code() == "fr"
```

### Signal testing

Use `wait_for_signal` for async signal assertions:

```python
def test_language_changed_signal(qt_application, wait_for_signal):
    manager = TranslationManager()
    assert wait_for_signal(manager.languageChanged, timeout=1000)
```

### Best practices

- Keep tests deterministic and isolated.
- Use fixtures from `tests/conftest.py` instead of ad-hoc setup.
- Prefer integration tests on real flows when mocking is not required.
- Keep robustness tests explicit about expected failure behavior.

## Unit tests — services

### ConfigService

**File:** `unit/test_services/test_app_functions.py` — 5 tests (`TestConfigServiceV5`)

- Load config successfully from project root
- Load config when file is missing (returns empty dict)
- Get config value by key
- Save config writes `app.config.yaml`
- Get package resource returns existing path

### SettingsService

**File:** `unit/test_services/test_app_settings.py` — 8 tests (`TestSettings`)

- App settings shape and default values
- GUI settings shape and default values
- Settings mutability (read/write)
- `QSize` consistency across settings
- Boolean, integer, and string settings behavior
- Settings internal structure validation

### TranslationManager

**File:** `unit/test_services/test_translation_manager.py` — 14 tests (`TestTranslationManager`)

- Init with default language (`en`)
- Language mapping (code to locale name)
- Available languages list
- Get current language code and name
- Translate text when no translation is available (passthrough)
- Load language success and failure
- Register, unregister, and clear widgets
- Set translatable text on widget
- `languageChanged` signal emission

## Unit tests — core widgets

### EzApplication

14 tests covering: `QApplication` inheritance, singleton behavior, locale configuration,
environment variables, high DPI scaling, `themeChanged` signal.

### Header

20 tests covering: layout structure, all button types and signals, size policy, custom parameters.

### Menu

20 tests covering: layout structure, toggle button, menu expansion/collapse, size constraints.

### PageContainer

20 tests covering: `QStackedWidget` presence, page registration, layout margins, frame properties.

### SettingsPanel

12 tests covering: scroll area, content container, theme section, `settingChanged` signal, `set_width`.

## Unit tests — extended widgets

### Setting widgets

~33 tests across `TestBaseSettingWidget`, `TestSettingToggle`, `TestSettingSelect`,
`TestSettingSlider`, `TestSettingText`, `TestSettingCheckbox`.

Each class covers: initialization, UI components, `value` property, `get_value`/`set_value`, `valueChanged` signal.

## Integration tests

### App flow

**File:** `integration/test_application/test_app_flow.py` — 12 tests

- Application initialization (`EzApplication` + `EzQt_App`)
- Window properties, menu functionality, header signals
- Theme loading, window size, cleanup

### Translation workflows

**File:** `integration/test_services/test_translations.py` — 15 tests

- Manager integration, language change workflow, widget registration workflow
- Signal emission, `.ts` file loading, error handling, singleton behavior

## Known issues

!!! warning "Qt runtime errors"
    Tests requiring a `QApplication` must use `qt_application` or be marked `@pytest.mark.qt`:

    ```python
    @pytest.mark.qt
    def test_widget_renders(qt_application):
        panel = SettingsPanel()
        assert panel is not None
    ```

!!! note "Singleton behavior"
    `EzApplication` enforces a singleton pattern. Tests that must create a fresh instance
    should use the `ez_application_cleanup` fixture, which calls `create_for_testing()`.

| Issue                  | Solution                                            |
| :--------------------- | :-------------------------------------------------- |
| Qt runtime errors      | Verify PySide6 and use the `qt_application` fixture |
| Marker not recognized  | Check marker names in `tests/pytest.ini`            |
| Missing configs/assets | Re-run `ezqt init` in project root                  |
| Import errors          | Reinstall package: `pip install -e ".[dev]"`        |

## ➡️ Related

- [Coverage page](https://neuraaak.github.io/ezqt-app/coverage/)
- [Development guide](development.md)
