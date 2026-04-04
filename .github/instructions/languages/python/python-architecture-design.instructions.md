# Python Architecture & Design Standards (UIA)

Design patterns, symbol visibility, and API surface design for scalable Python.

<rules>
- **VISIBILITY:** Use `_prefix` for internal details; `__all__` for public API surface.
- **CONTRACT:** Always define `__all__` in modules that export a public API.
- **DUNDERS:** Never use custom `__double_dunder__` names; only standard protocols.
- **PATTERN:** Use `@classmethod` for alternative constructors/factories.
- **ENUM:** Prefer `enum.Enum` or `Literal` over bare string/int constants.
</rules>

## Visibility & API Design

- **`_name`:** Protected — promises internal stability but not external.
- **`__name`:** Private — use only to avoid subclass name collisions.
- **`__all__`:** Explicit list of symbols that are part of the documented contract.

## Methods vs Functions Decision Rule

- **Method:** If it uses `self` or `cls`.
- **Module-level Function:** If it operates on plain data with no class dependency.
- **Staticmethod:** Avoid; use module-level functions instead for cleaner encapsulation.

<examples>
# Public API and Factory Pattern
from enum import Enum

class Status(Enum):
PENDING = "pending"

class Processor:
def **init**(self, name: str):
self.\_name = name

    @classmethod
    def from_config(cls, config: dict):
        return cls(config["name"])

**all** = ["Processor", "Status"]
</examples>

<success_criteria>

- `__all__` defines the explicit public surface.
- No "utility classes" with staticmethods.
- Protected members clearly use the underscore prefix.

</success_criteria>
