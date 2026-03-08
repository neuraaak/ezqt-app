# Testing Guide

Comprehensive documentation for the **ezqt_app** test suite.
The test suite ensures reliability and correctness of all services, widgets, and workflows through three complementary scopes.

---

## Test Structure

### Directory Organization

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

### Test Statistics

| Category         | Files  | Tests    |
| ---------------- | ------ | -------- |
| Services         | 3      | ~27      |
| Utils            | 1      | 3        |
| Core Widgets     | 5      | ~86      |
| Extended Widgets | 1      | ~33      |
| Integration      | 2      | ~27      |
| **Total**        | **12** | **~176** |

---

## Unit Tests – Services

### ConfigService

**File:** `unit/test_services/test_app_functions.py` – 5 tests (`TestConfigServiceV5`)

- Load config successfully from project root
- Load config when file is missing (returns empty dict)
- Get config value by key
- Save config writes `app.config.yaml`
- Get package resource returns existing path

### SettingsService

**File:** `unit/test_services/test_app_settings.py` – 8 tests (`TestSettings`)

- App settings shape and default values
- GUI settings shape and default values
- Settings mutability (read/write)
- `QSize` consistency across settings
- Boolean settings behavior
- Integer settings behavior
- String settings behavior
- Settings internal structure validation

### TranslationManager

**File:** `unit/test_services/test_translation_manager.py` – 14 tests (`TestTranslationManager`)

- Init with default language (`en`)
- Language mapping (code → locale name)
- Available languages list
- Get current language code
- Get current language name
- Translate text when no translation is available (passthrough)
- Load language success (with mock translator)
- Load language failure (with mock file system and QCore)
- Register a widget for translation
- Unregister a widget from translation
- Clear all registered widgets
- Set translatable text on widget
- Load language by code helper
- `languageChanged` signal emission

---

## Unit Tests – Utils

### CLI

**File:** `unit/test_utils/test_cli.py` – 3 tests

- CLI group initialization (Click app object exists)
- CLI lists expected commands (`init`, `test`, `docs`, `info`, etc.)
- CLI `--help` runs successfully and exits cleanly

---

## Unit Tests – Core Widgets

### EzApplication

**File:** `unit/test_widgets/test_core/test_ez_app.py` – 14 tests

- Inheritance from `QApplication`
- Class definition and module location
- Locale configuration success path
- Locale configuration failure path
- Environment variables setup (`QT_*` flags)
- High DPI scaling configuration
- Application properties (name, version)
- Environment setup with mocked `os.environ`
- Singleton behavior (single instance pattern)
- Method inheritance from QApplication
- `themeChanged` signal definition
- Constructor signature validation
- Class-level documentation presence
- `themeChanged` signal on live instance

### Header

**File:** `unit/test_widgets/test_core/test_header.py` – 20 tests

- Default parameter initialization
- Custom parameter initialization
- Layout structure (QHBoxLayout)
- Meta info frame presence and properties
- App logo label
- App name label
- App description label
- Buttons frame presence
- Buttons layout (QHBoxLayout)
- Settings button presence and type
- Minimize button presence and type
- Maximize button presence and type
- Close button presence and type
- Button list management
- Size policy (Expanding horizontal)
- Custom app name applied
- Custom description applied
- Button click signals (minimize, maximize, close, settings)
- Header fixed height constraint
- Header width size policy

### Menu

**File:** `unit/test_widgets/test_core/test_menu.py` – 20 tests

- Default parameter initialization
- Custom widths (`expanded_width`, `collapsed_width`)
- Layout structure (QVBoxLayout)
- Main menu frame properties
- Main menu layout properties
- Toggle container presence
- Toggle layout properties
- Toggle button type and properties
- Menu dictionary initialization
- Button list management
- Icon list management
- Size constraints (min/max width)
- Toggle button visual properties
- Toggle button signal (`toggled`)
- Menu expansion capability
- Menu initial state (collapsed)
- Menu behavior with different widths
- Menu frame QSS properties
- Menu layout margins and spacing
- Menu object names

### PageContainer

**File:** `unit/test_widgets/test_core/test_page_container.py` – 20 tests

- Default parameter initialization
- Initialization with parent widget
- Layout structure (QVBoxLayout)
- QStackedWidget presence
- Pages dictionary initialization
- Add page (name, type, registration)
- Add multiple pages
- Page object names
- Initial state (no pages)
- With pre-existing pages
- Add page with special characters in name
- Add page with empty name
- Add page with numeric name
- Layout margins validation
- Layout spacing validation
- QStackedWidget style sheet presence
- Frame properties (shape, shadow)
- Frame object name
- QFrame inheritance
- Size policy (Expanding)

### SettingsPanel

**File:** `unit/test_widgets/test_core/test_settings_panel.py` – 12 tests

- Default parameter initialization
- Custom width parameter
- Initialization with parent widget
- Scroll area presence and properties
- Content container presence
- Theme container and label
- Theme layout properties
- Signals existence (`settingChanged`)
- Internal collections (settings dict, widgets list)
- Size constraints and size policy
- `set_width` method behavior
- Panel without YAML config loading (graceful fallback)

---

## Unit Tests – Extended Widgets

### Setting Widgets

**File:** `unit/test_widgets/test_extended/test_setting_widgets.py` – ~33 tests

#### `TestBaseSettingWidget` – 2 tests

- Widget init and base properties
- `set_key` method updates key

#### `TestSettingToggle` – 6 tests

- Default initialization
- Initialization with description
- UI components (label, toggle control)
- Toggle value behavior
- `set_value` method
- `valueChanged` signal

#### `TestSettingSelect` – 6 tests

- Default initialization
- Initialization with default value
- UI components (label, combo box)
- `value` property
- `get_value` / `set_value` methods
- `valueChanged` signal

#### `TestSettingSlider` – 7 tests

- Default initialization
- Initialization with custom range
- UI components (label, slider)
- Slider min/max properties
- `value` property
- `get_value` / `set_value` methods
- `valueChanged` signal

#### `TestSettingText` – 6 tests

- Default initialization
- Initialization with default value
- UI components (label, line edit)
- `value` property
- `get_value` / `set_value` methods
- `valueChanged` signal

#### `TestSettingCheckbox` – 6 tests

- Default initialization
- Initialization with default value
- UI components (label, checkbox)
- `value` property
- `get_value` / `set_value` methods
- `valueChanged` signal

---

## Integration Tests

### App Flow

**File:** `integration/test_application/test_app_flow.py` – 12 tests

- Application initialization (`EzApplication` + `EzQt_App`)
- App with custom theme file
- Window properties (title, geometry, flags)
- Menu functionality (addMenu, page switching)
- Header functionality (signals, buttons)
- Pages container behavior
- Settings panel presence and behavior
- Signal connections (header → app, menu → app)
- Theme loading from file path
- Window size on launch
- App cleanup (widget destruction)
- App without theme file (graceful fallback)

### Translation Workflows

**File:** `integration/test_services/test_translations.py` – 15 tests

- TranslationManager integration (init → load → query)
- Translation helpers integration (module-level functions)
- Language change workflow (code → locale → UI update)
- Widget registration workflow (register → change language → retranslate)
- Translation text workflow (set text → change language → verify)
- Multiple successive language changes
- Widget retranslation workflow (register → change → verify text)
- `languageChanged` signal workflow (signal → slot triggered)
- Translation file loading workflow (`.ts` file → load → verify)
- Translation mapping workflow (source → target language)
- Translation error handling (invalid language code)
- TranslationManager singleton behavior
- Translation text setting workflow
- TranslationManager cleanup
- TranslationManager state persistence across language changes

---

## Run Tests

```bash
python tests/run_tests.py --type unit
python tests/run_tests.py --type integration
python tests/run_tests.py --type robustness
python tests/run_tests.py --type all
```

With coverage:

```bash
python tests/run_tests.py --coverage
```

Fast mode (excludes `@pytest.mark.slow`):

```bash
python tests/run_tests.py --fast
```

Parallel mode (requires `pytest-xdist`):

```bash
python tests/run_tests.py --parallel
```

Using pytest directly:

```bash
pytest tests/unit/ -v
pytest tests/integration/ -v
pytest -m qt tests/unit/
```

---

## Coverage

Generate report:

```bash
python tests/run_tests.py --coverage
```

Terminal coverage details:

```bash
pytest --cov=ezqt_app --cov-report=term-missing tests/
```

Open the HTML report:

```text
htmlcov/index.html
```

---

## Test Configuration

### `conftest.py` – Shared Fixtures

**Location:** `tests/conftest.py`

| Fixture                  | Scope    | Description                                         |
| ------------------------ | -------- | --------------------------------------------------- |
| `qt_application`         | session  | `EzApplication` instance shared across all Qt tests |
| `qt_widget_cleanup`      | function | Calls `processEvents()` for cleanup after each test |
| `ez_application_cleanup` | function | Fresh `EzApplication` instance for singleton tests  |
| `wait_for_signal`        | function | Helper to wait for a Qt signal with timeout         |
| `mock_icon_path`         | function | Temp PNG file for icon-loading tests                |
| `mock_svg_path`          | function | Temp SVG file for icon-loading tests                |
| `mock_translation_files` | function | Temp `.ts` files (EN + FR) for translation tests    |
| `mock_yaml_config`       | function | Temp `app.config.yaml` for config service tests     |

### Test Markers

Configured in `tests/pytest.ini`:

| Marker        | Description                               |
| ------------- | ----------------------------------------- |
| `unit`        | Unit tests (isolated modules/components)  |
| `integration` | Cross-component behavior tests            |
| `robustness`  | Edge case and failure path tests          |
| `slow`        | Slow tests (exclude with `-m "not slow"`) |
| `qt`          | Tests requiring a live `QApplication`     |

**Usage:**

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

---

## Best Practices

- Keep tests deterministic and isolated.
- Use fixtures from `tests/conftest.py` instead of ad-hoc setup.
- Prefer integration tests on real flows when mocking is not required.
- Keep robustness tests explicit about expected failure behavior.

### Test Isolation

Each test should be self-contained and independent:

```python
def test_config_loads_defaults(mock_yaml_config):
    service = ConfigService(config_path=mock_yaml_config)
    assert service.get("app.name") == "Test Application"
```

### Fixture Usage

Use shared fixtures from `conftest.py` rather than ad-hoc setup:

```python
def test_translation_switch(qt_application, mock_translation_files):
    manager = TranslationManager()
    manager.load_language_by_code("fr")
    assert manager.get_current_language_code() == "fr"
```

### Signal Testing

Use `wait_for_signal` for async signal assertions:

```python
def test_language_changed_signal(qt_application, wait_for_signal):
    manager = TranslationManager()
    assert wait_for_signal(manager.languageChanged, timeout=1000)
```

---

## Known Issues

### Qt Runtime Errors

Tests requiring a QApplication must use `qt_application` or be marked `@pytest.mark.qt`:

```python
@pytest.mark.qt
def test_widget_renders(qt_application):
    panel = SettingsPanel()
    assert panel is not None
```

### Singleton Behavior

`EzApplication` enforces a singleton pattern. Tests that must create a fresh instance should use the `ez_application_cleanup` fixture, which calls `create_for_testing()`.

### Common Issues

| Issue                  | Solution                                     |
| ---------------------- | -------------------------------------------- |
| Qt runtime errors      | Verify PySide6 and `qt_application` fixture  |
| Marker not recognized  | Check marker names in `tests/pytest.ini`     |
| Missing configs/assets | Re-run `ezqt init` in project root           |
| Import errors          | Reinstall package: `pip install -e ".[dev]"` |

---

## Notes

- Test runner streams output in real time (no buffering).
- Some tests still rely on heavy mocks; prefer real integration paths when extending coverage.
- The `robustness/` directory is reserved for future edge case suites.

---

## Related

- [Coverage Page](https://neuraaak.github.io/ezqt-app/coverage/)
- [Development Guide](https://neuraaak.github.io/ezqt-app/guides/development/)
