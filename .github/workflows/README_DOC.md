# 📚 GitHub Actions Workflow - Deploy Documentation

## Overview

The `docs.yml` workflow automatically builds and deploys **ezqt-widgets** documentation to GitHub Pages using **MkDocs Material**. The documentation is served at `https://neuraaak.github.io/ezqt-widgets/`.

## 🎯 Triggers

The workflow is triggered automatically in the following cases:

### 1. Push to main (with documentation changes)

```bash
git checkout main
git add docs/ mkdocs.yml ezqt_widgets/
git commit -m "docs: update API documentation"
git push origin main
```

- Triggers when files are modified in:
  - `docs/**` - Documentation markdown files
  - `mkdocs.yml` - MkDocs configuration
  - `ezqt_widgets/**` - Source code (for auto-generated API docs)
- Only deploys when pushing to the `main` branch
- Automatically builds and deploys to GitHub Pages

### 2. Manual trigger (Workflow Dispatch)

- From GitHub interface: Actions → Deploy Documentation → Run workflow
- Allows manual deployment at any time
- Useful for testing or forcing a rebuild

## 🔄 Workflow Architecture

The workflow consists of **one job** with the following steps:

### Job `deploy` - Build and Deploy Documentation

1. **Checkout code** - Retrieves source code with full history
2. **Set up Python** - Installs Python 3.11 with pip cache
3. **Install extra system dependencies** - Optional system dependencies (empty by default)
4. **Install package with docs dependencies** - Installs package with `[docs]` extras
5. **Build and deploy documentation** - Builds and deploys to GitHub Pages using `mkdocs gh-deploy`

## 📦 Documentation Stack

### MkDocs Configuration

The documentation uses the following stack:

| Component                | Version  | Purpose                                |
| ------------------------ | -------- | -------------------------------------- |
| **mkdocs**               | >=1.6.0  | Static site generator                  |
| **mkdocs-material**      | >=9.5.0  | Material theme                         |
| **mkdocstrings[python]** | >=0.27.0 | Auto-generate API docs from docstrings |
| **mkdocs-section-index** | >=0.3.0  | Section index pages                    |

### Documentation Structure

```text
docs/
├── index.md                          # Home page
├── getting-started.md                # Installation & quick start
├── api/
│   ├── index.md                      # API overview
│   ├── button.md                     # ::: ezqt_widgets.button
│   ├── input.md                      # ::: ezqt_widgets.input
│   ├── label.md                      # ::: ezqt_widgets.label
│   └── misc.md                       # ::: ezqt_widgets.misc
├── cli/
│   └── index.md                      # CLI reference
├── examples/
│   └── index.md                      # Practical examples
├── guides/
│   ├── index.md                      # Guides overview
│   ├── style-guide.md                # QSS style guide
│   ├── development.md                # Development guide
│   └── testing.md                    # Testing guide
└── stylesheets/
    └── extra.css                     # Custom styles
```

## 🚀 Features

### MkDocs Material Theme

The documentation includes:

- ✅ **Dark/Light mode** - User-selectable theme
- ✅ **Navigation tabs** - Sticky tabs for main sections
- ✅ **Search** - Full-text search with suggestions
- ✅ **Code highlighting** - Syntax highlighting for all languages
- ✅ **Copy button** - One-click code copying
- ✅ **Mobile responsive** - Optimized for all screen sizes
- ✅ **Social links** - GitHub & PyPI links
- ✅ **TOC** - Table of contents on the right
- ✅ **Edit on GitHub** - Direct links to edit pages

### Auto-Generated API Documentation

Using **mkdocstrings**, the documentation automatically generates API reference from source code docstrings:

```markdown
::: ezqt_widgets.button.date_button.DateButton
options:
  show_source: true
  docstring_style: google
  show_signature_annotations: true
```

**Benefits:**

- Documentation always up-to-date with code
- Automatic method signatures and type hints
- Cross-references between modules
- Source code links

### Markdown Extensions

Enabled extensions:

- **admonition** - Warning, note, tip boxes
- **pymdownx.details** - Collapsible sections
- **pymdownx.superfences** - Code blocks with mermaid diagrams
- **pymdownx.highlight** - Advanced syntax highlighting
- **pymdownx.tabbed** - Tabbed content
- **pymdownx.emoji** - Emoji support 🚀
- **tables** - Markdown tables
- **toc** - Table of contents with permalinks

## 📋 Usage

### Automatic deployment

The easiest way is to let the workflow handle deployment automatically:

```bash
# 1. Modify documentation
vim docs/getting-started.md

# 2. Commit and push to main
git add docs/
git commit -m "docs: update getting started guide"
git push origin main
```

→ ✅ Documentation automatically deployed to GitHub Pages

### Manual deployment

If you need to force a rebuild:

#### Method 1: GitHub interface

1. Go to Actions
2. Select "Deploy Documentation"
3. Click "Run workflow"
4. Select the `main` branch
5. Click "Run workflow"

#### Method 2: gh CLI

```bash
gh workflow run docs.yml
```

### Local preview

Before pushing, preview documentation locally:

```bash
# Install docs dependencies
pip install -e ".[docs]"

# Serve locally
mkdocs serve

# Open http://127.0.0.1:8000
```

## 🔐 Required Permissions

The workflow requires **write permissions** to deploy to GitHub Pages:

```yaml
permissions:
  contents: write
```

This is automatically configured in the workflow file.

### GitHub Pages Configuration

Ensure GitHub Pages is configured correctly:

1. Go to **Repository Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: **gh-pages** / **root**
4. Click **Save**

The `mkdocs gh-deploy` command automatically:

- Creates/updates the `gh-pages` branch
- Builds the documentation
- Pushes to `gh-pages`
- GitHub Pages serves from `gh-pages`

## ✅ Validation

The workflow performs the following validations:

### 1. Build Validation

- ✅ MkDocs builds without errors
- ✅ All internal links are valid
- ✅ All markdown files are valid
- ✅ mkdocstrings can import all modules

### 2. Package Installation

- ✅ Package can be installed in editable mode
- ✅ All dependencies are available
- ✅ Source code is importable for API docs

### 3. Deployment Validation

- ✅ `gh-pages` branch is updated
- ✅ Documentation is pushed successfully
- ✅ GitHub Pages deployment triggers

## ✅ Post-Deployment Verification

After deployment, verify:

1. **Visit documentation**: <https://neuraaak.github.io/ezqt-widgets/>
2. **Check all pages** load correctly
3. **Test navigation** between sections
4. **Verify search** functionality
5. **Check auto-generated API docs** display correctly
6. **Test mobile view** if needed

## 🧪 Testing Documentation Changes

### Local testing workflow

```bash
# 1. Create feature branch
git checkout -b docs/update-api-reference

# 2. Make changes
vim docs/api/index.md

# 3. Preview locally
mkdocs serve

# 4. Check build
mkdocs build --strict

# 5. Commit and push
git add docs/
git commit -m "docs: update API reference"
git push origin docs/update-api-reference

# 6. Create PR for review
gh pr create --title "docs: update API reference"

# 7. After PR merge, docs deploy automatically
```

### Build validation

Test that the documentation builds without errors:

```bash
# Strict mode (fails on warnings)
mkdocs build --strict

# Check specific page
mkdocs serve
# Navigate to http://127.0.0.1:8000/api/button/
```

## 🚨 Troubleshooting

### Workflow fails with "Module not found"

**Cause**: mkdocstrings cannot import a module for API documentation.

**Solution**:

1. Check that the module path in `docs/api/*.md` is correct:

   ```markdown
   ::: ezqt_widgets.button.date_button.DateButton # Must match actual module path
   ```

2. Verify the package installs correctly:

   ```bash
   pip install -e .
   python -c "from ezqt_widgets.button import DateButton"
   ```

3. Check for missing dependencies in `pyproject.toml`

### Workflow fails with "Page not found"

**Cause**: A link in documentation points to a non-existent page.

**Solution**:

1. Check internal links in markdown files
2. Use mkdocs strict mode to find broken links:

   ```bash
   mkdocs build --strict
   ```

3. Fix or remove broken links

### Documentation not updating

**Cause**: GitHub Pages cache or deployment delay.

**Solution**:

1. Check workflow completed successfully in Actions tab
2. Wait 1-2 minutes for GitHub Pages to update
3. Hard refresh the page (Ctrl+F5)
4. Check `gh-pages` branch was updated:

   ```bash
   git fetch origin
   git log origin/gh-pages --oneline -5
   ```

### mkdocstrings docstring not rendering

**Cause**: Docstring format doesn't match configured style.

**Solution**:

1. Verify docstrings use Google style:

   ```python
   def example(param: str) -> bool:
       """Brief description.

       Args:
           param: Description

       Returns:
           bool: Description
       """
   ```

2. Check mkdocstrings configuration in `mkdocs.yml`:

   ```yaml
   plugins:
     - mkdocstrings:
         handlers:
           python:
             options:
               docstring_style: google
   ```

### Deployment fails with "Permission denied"

**Cause**: Missing write permissions for `gh-pages` branch.

**Solution**:

1. Check workflow permissions:

   ```yaml
   permissions:
     contents: write
   ```

2. Verify GitHub Actions has write access in repository settings
3. Check if branch protection rules block `gh-pages` updates

## 📝 Important Notes

- **Automatic deployment**: Only `main` branch changes trigger deployment
- **Build time**: Documentation build takes ~30-60 seconds
- **Cache**: GitHub Pages may cache content for a few minutes
- **API docs**: Auto-generated from source code docstrings (always up-to-date)
- **Preview URL**: <https://neuraaak.github.io/ezqt-widgets/>
- **Custom domain**: Can be configured in repository settings
- **gh-pages branch**: Created/managed automatically by `mkdocs gh-deploy`

## 🔧 Configuration Files

### mkdocs.yml

Main configuration file:

```yaml
site_name: EzQt Widgets Documentation
site_url: https://neuraaak.github.io/ezqt-widgets/
theme:
  name: material
  features:
    - navigation.tabs
    - search.suggest
    - content.code.copy
plugins:
  - search
  - section-index
  - mkdocstrings:
      handlers:
        python:
          options:
            docstring_style: google
```

### pyproject.toml

Documentation dependencies:

```toml
[project.optional-dependencies]
docs = [
    "mkdocs>=1.6.0",
    "mkdocs-material>=9.5.0",
    "mkdocstrings[python]>=0.27.0",
    "mkdocs-section-index>=0.3.0",
]
```

## 🔗 Useful Links

### Documentation

- **Live documentation**: <https://neuraaak.github.io/ezqt-widgets/>
- **MkDocs**: <https://www.mkdocs.org/>
- **Material for MkDocs**: <https://squidfunk.github.io/mkdocs-material/>
- **mkdocstrings**: <https://mkdocstrings.github.io/>

### Repository

- **GitHub Pages settings**: Repository → Settings → Pages
- **Actions workflows**: Repository → Actions
- **gh-pages branch**: Repository → Branches

## 🚀 Best Practices

### Documentation Updates

1. **Always preview locally** before pushing
2. **Use descriptive commit messages**: `docs: update API reference`
3. **Check all links** work correctly
4. **Test code examples** are runnable
5. **Update navigation** in `mkdocs.yml` when adding pages

### API Documentation

1. **Write Google-style docstrings** in source code
2. **Include examples** in docstrings
3. **Document all parameters** and return types
4. **Add type hints** for better documentation
5. **Keep docstrings up-to-date** with code changes

### Markdown Style

1. **Use consistent heading levels** (h1 → h2 → h3)
2. **Add admonitions** for important notes:

   ```markdown
   !!! warning "Important"
   This is a warning message
   ```

3. **Use code blocks** with language specifiers:

   ````markdown
   ```python
   from ezqt_widgets.button import DateButton
   ```
   ````

4. **Add table of contents** for long pages
5. **Use relative links** for internal navigation

## 📞 Support

For issues with documentation:

1. **Build errors**: Check workflow logs in Actions tab
2. **Content issues**: Open an issue on GitHub
3. **MkDocs questions**: Consult MkDocs documentation
4. **Theme customization**: See Material for MkDocs docs
