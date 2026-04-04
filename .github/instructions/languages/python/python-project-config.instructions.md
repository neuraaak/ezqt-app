# Python Project Configuration Standards (UIA)

Centralized configuration standards for `pyproject.toml` and development tools.

<rules>
- **CENTRAL:** All tool configuration MUST live in `pyproject.toml`.
- **BACKEND:** ALWAYS use `hatchling` as the build backend.
- **EMOJI:** Use standard emojis for section titles to aid visual navigation.
- **STACK:** Standardize on `uv` (package), `ruff` (lint/format), `ty` (typing), `mkdocs` (doc), and `pre-commit`.
</rules>

## Section Order & Markers

| Section       | Emoji | Tool Key                                        |
| :------------ | :---- | :---------------------------------------------- |
| Build System  | 🔨    | `[build-system]` (Hatchling)                    |
| Metadata      | 📦    | `[project]`                                     |
| Documentation | 📖    | `[tool.mkdocs]`                                 |
| Code Quality  | 🎨    | `[tool.ruff]`, `[tool.ty]`, `[tool.pre-commit]` |

## Hatchling Build Configuration

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

## Ruff Configuration Pattern

Always document rule selections and ignores with inline comments.

```toml
[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "F",   # pyflakes
    "I",   # isort
    "S",   # bandit (security)
]
```

<success_criteria>

- `pyproject.toml` is the single source of truth for tools.
- Line length (88) is consistent across tools.
- Ruff rules are documented within the TOML file.

</success_criteria>
