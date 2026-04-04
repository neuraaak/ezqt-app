# Git Hooks

Pre-commit checks are managed by the **[pre-commit](https://pre-commit.com/)** library
via `.pre-commit-config.yaml` at the project root.

## Setup (run once per clone)

```bash
# 1. Disable the legacy .hooks/ mechanism if previously enabled
git config --unset core.hooksPath

# 2. Install the pre-commit library (already in dev deps)
uv sync                # ensures the project venv is up to date
uv run pre-commit install
```

`pre-commit install` writes `.git/hooks/pre-commit` and `.git/hooks/pre-push`
automatically — no manual `git config` required.

## What runs on each commit

Defined in `.pre-commit-config.yaml`, mirroring `.scripts/dev/lint.py`:

| Step         | Tool                | Action                                                      |
| ------------ | ------------------- | ----------------------------------------------------------- |
| File hygiene | pre-commit-hooks    | trailing whitespace, YAML/TOML validity, merge conflicts…   |
| 1            | `ruff-format`       | auto-format code                                            |
| 2            | `ruff check`        | lint with auto-fix (`--exit-non-zero-on-fix`)               |
| 3            | `ty check`          | type checking                                               |
| 4            | `lint-imports`      | layer dependency contracts                                  |
| 5            | `update_version.py` | sync `_version.py` ← `pyproject.toml` (on pyproject change) |

## Workflow when a hook modifies files

When ruff or `sync-version` modifies files, pre-commit **aborts the commit**
so you can review the changes:

```bash
# review what was auto-fixed
git diff

# re-stage and recommit
git add -u
git commit
```

## Run manually

```bash
# all files
pre-commit run --all-files

# specific hook
pre-commit run ruff --all-files
pre-commit run ty --all-files

# skip hooks for a one-off commit (use sparingly)
git commit --no-verify
```

## Update hook versions

```bash
pre-commit autoupdate
```
