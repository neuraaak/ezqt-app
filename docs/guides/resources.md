# Qt resources pipeline

This guide explains the end-to-end Qt resource pipeline: what `init()` generates,
how to use `AppIcons` and `AppImages`, and how to customize the output directory.

## 🧭 Find all embedded assets

Use the dedicated API page to browse every built-in icon/image symbol and runtime
asset accessors:

- [Asset catalog](../api/assets.md)

Quick lookup import for built-in resources:

```python
from ezqt_app.shared.resources import Icons, Images

close_icon = Icons.icon_close
app_logo = Images.logo_placeholder
```

## ⚙️ What `init()` generates

When you call `init()`, the bootstrap sequence compiles Qt resources and writes
three Python modules into `bin/` (or your custom `bin_path`):

| File                  | Purpose                                                                                        |
| :-------------------- | :--------------------------------------------------------------------------------------------- |
| `bin/resources_rc.py` | Compiled Qt resource module — registers `:/icons/` and `:/images/` with the Qt resource system |
| `bin/app_icons.py`    | Auto-generated class `AppIcons` — one attribute per icon                                       |
| `bin/app_images.py`   | Auto-generated class `AppImages` — one attribute per image                                     |

These files are generated from the `.qrc` source bundled with the package and
from any custom assets you add to `bin/themes/`. They are created or overwritten
each time `init()` runs with the resource build step enabled (the default).

## 🔗 Resource path format

All Qt resource paths use a single prefix segment:

```qss
:/icons/<filename>.png
:/images/<filename>.jpg
```

!!! warning "Old double-prefix paths are invalid"
    Prior versions emitted paths like `:/icons/icons/cil-3d.png`. This was a
    bug. The correct format is `:/icons/cil-3d.png`. Update any hard-coded
    paths in your QSS files or Python code accordingly.

## 🖼️ Using AppIcons and AppImages

`AppIcons` and `AppImages` are module-level variables exported from
`ezqt_app.shared.resources`. They are `None` at import time and populated
by `init()` via `load_runtime_rc()`.

### Correct import pattern

Always call `init()` before accessing these symbols:

```python
from ezqt_app import init
from ezqt_app.shared.resources import AppIcons, AppImages

init()  # populates AppIcons and AppImages

icon_path = AppIcons.cil_home          # ":/icons/cil-home.png"
logo_path = AppImages.logo_placeholder # ":/images/logo-placeholder.jpg"
```

### When the import happens before `init()`

If you import `AppIcons` at the top of a module that is loaded before `init()`
runs, you capture the initial `None` value:

```python
# top_level_module.py — loaded before init() is called
from ezqt_app.shared.resources import AppIcons  # AppIcons is None here

init()  # too late — AppIcons in this module is still None
print(AppIcons.cil_home)  # AttributeError: 'NoneType' object has no attribute 'cil_home'
```

Use one of these safe patterns instead:

=== "Module-level attribute access (safest)"

    ```python
    from ezqt_app.shared import resources

    init()
    icon_path = resources.AppIcons.cil_home  # resolved at access time, always live
    ```

=== "Import after `init()`"

    ```python
    from ezqt_app import init

    init()

    from ezqt_app.shared.resources import AppIcons  # safe — init() already ran
    icon_path = AppIcons.cil_home
    ```

## 📁 What is no longer in the QRC

Starting from this version, `config/` and `translations/` are no longer
embedded in `resources_rc.py`. Those assets are read directly from the
filesystem at runtime.

This reduces the compiled resource size and avoids stale embedded copies
diverging from the user's project files.

## 📝 Custom `bin_path`

By default `init()` writes all generated assets to `<project_root>/bin/`.
Pass `bin_path` to choose a different directory:

```python
from ezqt_app import init

# Relative path — resolved against project_root (defaults to Path.cwd())
init(bin_path="binaries")

# Absolute path
from pathlib import Path
init(bin_path=Path("/opt/myapp/assets"))
```

The `bin_path` value is forwarded to `InitOptions.bin_path` and resolved in
`InitOptions.resolve()`. Relative values are made absolute by joining them
with `project_root`.

!!! note
    When using a custom `bin_path`, make sure your application code and
    `load_runtime_rc()` can locate the generated files. The path is stored
    in the runtime path registry and used automatically by the bootstrap
    sequence, but any hard-coded `bin/` references in your own code will
    need updating.

## ⚠️ ResourceCompilationError

If `pyside6-rcc` is not available on `PATH` when `init()` runs,
a `ResourceCompilationError` is raised immediately instead of silently
producing an empty or broken resource module:

```text
ezqt_app.domain.errors.ResourceCompilationError: pyside6-rcc not found
```

This is an explicit failure — it prevents the application from starting with
broken Qt resources. See the
[Troubleshooting section](../getting-started.md#pyside6-rcc-not-found) in
Getting Started for the fix.

## 🔍 How `load_runtime_rc()` works

The bootstrap sequence calls `load_runtime_rc()` after QRC compilation. This
function:

1. Reloads `bin/resources_rc.py` into `sys.modules`, registering all Qt
   resources with the Qt resource system.
2. Loads `bin/app_icons.py` and assigns its `AppIcons` class to
   `ezqt_app.shared.resources.AppIcons`.
3. Loads `bin/app_images.py` and assigns its `AppImages` class to
   `ezqt_app.shared.resources.AppImages`.

You do not need to call `load_runtime_rc()` manually — it is invoked
automatically as part of `init()`.

## ➡️ See also

- [Getting Started](../getting-started.md) — bootstrap and install
- [Asset catalog](../api/assets.md) — full embedded icons/images listing
- [API Reference — Application Layer](../api/reference/application.md) — `InitOptions`, `InitService`
- [Examples](../examples/index.md) — working code snippets
