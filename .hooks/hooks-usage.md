# Git Hooks Usage

This directory contains Git hooks used by your project.

## Available Hooks

### `pre-commit`

- **Purpose**: Code quality and formatting before each commit
- **Behavior**:
  - Runs **Black**, **isort**, and **Ruff format** on the entire repository
  - Automatically stages reformatted files with `git add .`
  - Fails the commit if one of the tools fails

> Note: This is a **native Git hook** in `.hooks/`, independent from the Python `pre-commit` tool configured by `make setup-hooks`.

### `post-commit`

- **Purpose**: Automated tagging and local build after a successful commit
- **Behavior**:
  - Reads the version from `pyproject.toml` (or `setup.py` as fallback)
  - Creates or updates a lightweight tag `v<version>` on `HEAD`
  - Creates or updates a major “latest” tag `v<major>-latest`
  - Builds the local package with:

    ```bash
    python .scripts/build/build_package.py build
    ```

  - Pushes the tags to `origin` (forced update)

### Configuration

To activate these hooks at Git level, run:

```bash
git config core.hooksPath .hooks
```

This tells Git to use the `.hooks/` directory instead of `.git/hooks/`.

### Development

#### Adding a new hook

1. Create the file in `.hooks/` (e.g. `.hooks/pre-push`)
2. Make it executable: `chmod +x .hooks/pre-push`
3. Document the new hook in this file

#### Manual testing

You can test a hook manually from the project root:

```bash
# Test pre-commit
.hooks/pre-commit

# Test post-commit
.hooks/post-commit
```

### Future Extensions

- `pre-push`: Run tests or linters before pushing
- `commit-msg`: Validate commit messages (format, IDs, etc.)
- `post-merge`: Actions after merges (e.g. migrations, regeneration)
- `pre-rebase`: Checks before rebasing
