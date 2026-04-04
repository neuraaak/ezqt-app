# Python Typing Standards (UIA)

Advanced static typing standards for type-safe, maintainable Python codebases.

<rules>
- **STRICTNESS:** Aim for pragmatic strictness; use `ty` as the principal type checker.
- **NATIVE:** Use built-in generic types (e.g., `list[str]`, `dict[str, int]`) (Python 3.9+).
- **IMMUTABILITY:** Use `frozendict` (3.14+) or `Mapping` for immutable configuration.
- **INTERFACE:** Prefer `typing.Protocol` over `abc.ABC` for flexible structural typing.
</rules>

## Modern Type Features

- **Structural Typing:** Use `Protocol` to define interfaces without inheritance.
- **Literal Types:** Use `Literal["a", "b"]` for fixed sets of values.
- **Typed Dictionaries:** Use `TypedDict` for structured data from external APIs (no runtime overhead).
- **Annotated:** Use `Annotated` for metadata, but keep validation logic in specialized libraries (Pydantic).

<examples>
# Protocol and TypedDict
from typing import Protocol, TypedDict

class UserData(TypedDict):
id: int
name: str

class Saver(Protocol):
def save(self, data: UserData) -> None: ...
</examples>

<success_criteria>

- No use of legacy `typing.List` or `typing.Dict`.
- Protocols used for duck-typing validation.
- `__future__` annotations included at file top.

</success_criteria>
