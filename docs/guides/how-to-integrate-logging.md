# How to integrate logging with ezplog

Configure one logging policy for applications using ezqt_app.

## 🔧 Prerequisites

- Python 3.11+
- ezqt-app and ezplog installed
- A single application entrypoint where logging is configured once

## 📝 Steps

1. Keep library logging passive in ezqt_app.

   ezqt_app emits logs with `ezplog.lib_mode.get_logger(...)` and keeps its own internal printer.
   Do not instantiate `Ezpl()` inside library code.

2. Initialize Ezpl once in the host application (recommended).

   ```python
   from ezplog import Ezpl

   ezpl = Ezpl(
       log_file="app.log",
       log_level="INFO",
       hook_logger=True,
       hook_printer=False,
   )
   ```

   `hook_logger=True` captures logs emitted by ezqt_app loggers.
   `hook_printer=False` keeps ezqt_app printer behavior unchanged.

3. Optionally scope compatibility hooks to selected logger namespaces.

   ```python
   ezpl.set_compatibility_hooks(
       hook_logger=True,
       hook_printer=False,
       logger_names=["ezqt_app"],
   )
   ```

4. Run ezqt_app normally.

   ```python
   from ezqt_app import EzApplication, EzQt_App, init
   import sys

   app = EzApplication(sys.argv)
   init()
   window = EzQt_App().build()
   window.show()
   sys.exit(app.exec())
   ```

## ⚙️ Variations

### Use classic logging code with ezpl compatibility hook

If your application already uses `logging.getLogger(...)`, you can keep that code and still route records through ezpl.

```python
import logging
from ezplog import Ezpl, InterceptHandler

Ezpl(log_file="app.log", hook_logger=False, hook_printer=False)
logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO, force=True)

log = logging.getLogger("my_app")
log.info("Classic logging is now routed through ezpl")
```

### Keep ezqt_app internal debug printer disabled

`app.config.yaml` controls internal debug console output independently from logger hooks:

```yaml
app:
  debug_printer: false
```

With `debug_printer: false`, debug-level printer messages are not displayed.

## ✅ Result

- ezqt_app logs are captured by the host logging policy.
- Library code stays passive and side-effect free.
- Internal ezqt_app printer remains controlled by `app.debug_printer`.

## 🔗 References

- Official ezplog guide: [How to configure compatibility hooks](https://neuraaak.github.io/ezplog/latest/guides/configuration/)
- ezplog concept: [App mode vs lib mode](https://neuraaak.github.io/ezplog/latest/concepts/dual-mode/)
- ezqt_app CLI reference: [CLI reference](../cli/index.md)
