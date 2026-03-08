# Commit Standards & Version Control Discipline

Professional commit framework optimized for clean project history, meaningful traceability, and team collaboration. This model guides the assistant to produce commits that tell a coherent story of the project's evolution and facilitate efficient code review.

## Core Commit Principles

### Atomic Commit Philosophy

Each commit should represent a single, coherent unit of change. Mixing unrelated modifications in a single commit obscures intent, complicates reviews, and makes selective reverts nearly impossible.

- **ONE PURPOSE** per commit - never mix features, fixes, and refactoring
- **SELF-CONTAINED** changes that compile and pass tests independently
- **COMPLETE** implementations - avoid partial work in committed state
- **REVERSIBLE** without side effects on unrelated functionality
- **MINIMAL** scope - include only what is necessary for the stated purpose

Atomic commits enable precise git bisect, clean cherry-picks, and meaningful blame output. A commit that does one thing well is infinitely more valuable than one that does three things partially.

### Commit Message Structure

Well-structured commit messages are documentation that lives inside the repository. They explain not just what changed, but why it changed, which is information that code alone cannot convey.

**Format:**

```
<type>: <concise imperative description>

<optional body explaining WHY, not WHAT>

<optional footer with references>
```

**Type prefixes:**

- **feat**: New functionality or capability
- **fix**: Bug correction or error resolution
- **refactor**: Code restructuring without behavior change
- **docs**: Documentation updates only
- **style**: Formatting, whitespace, or cosmetic changes
- **test**: Adding or modifying tests exclusively
- **build**: Build system, dependencies, or CI configuration
- **perf**: Performance optimization without functional change
- **chore**: Maintenance tasks, tooling, or configuration

The type prefix enables automated changelog generation, semantic versioning, and rapid scanning of project history. Consistent usage transforms git log into a navigable project timeline.

### Message Quality Standards

A commit message is read far more often than it is written. Investing time in a clear message pays dividends every time someone investigates that area of code.

- **IMPERATIVE MOOD** in subject line - "Add feature" not "Added feature"
- **50 CHARACTERS** maximum for subject line when possible
- **NO PERIOD** at the end of the subject line
- **BLANK LINE** separating subject from body
- **72 CHARACTERS** wrap for body text
- **EXPLAIN WHY** the change was made, not what was changed
- **REFERENCE** issues, tickets, or discussions when relevant

The imperative mood matches git's own conventions (e.g., "Merge branch..."). Character limits ensure readability in git log --oneline and GitHub interfaces. Explaining "why" provides context that the diff already shows for "what".

## Staging Discipline

### Intentional Staging

Staging is not a formality - it is the deliberate act of curating what enters the project history. Careless staging introduces noise, secrets, and unintended changes into the permanent record.

- **REVIEW** every staged file before committing
- **STAGE BY NAME** - prefer explicit file paths over blanket `git add .`
- **EXCLUDE** generated files, build artifacts, and environment-specific configs
- **NEVER COMMIT** secrets, credentials, API keys, or sensitive data
- **VERIFY** .gitignore coverage before first commit in new projects
- **INSPECT** diffs to catch debug code, console.log, and TODO leftovers

Blanket staging commands bypass the critical review step that catches accidental inclusions. Secrets committed even once persist in git history and require history rewriting to fully remove - prevention is orders of magnitude cheaper than remediation.

### Pre-Commit Validation

Commits that break the build or fail tests waste everyone's time. Validating before committing prevents broken states from entering the shared history.

- **RUN** relevant tests before committing
- **VERIFY** the build succeeds with staged changes
- **RESPECT** pre-commit hooks - never bypass with --no-verify
- **CHECK** for linting violations and formatting inconsistencies
- **CONFIRM** no unintended files are included in the staging area

Pre-commit hooks exist to enforce project standards automatically. Bypassing them introduces the exact problems they were designed to prevent. If a hook fails, fix the underlying issue rather than circumventing the safety mechanism.

## Branch & History Hygiene

### Branch Strategy

Branches isolate work streams and enable parallel development. Clear naming conventions and disciplined lifecycle management prevent the confusion that comes from stale or ambiguous branches.

- **DESCRIPTIVE NAMES** using `type/short-description` format (e.g., `feat/user-auth`, `fix/login-redirect`)
- **SHORT-LIVED** feature branches - merge or close promptly
- **UP TO DATE** with base branch before creating pull requests
- **CLEAN** history through meaningful commits, not fixup noise

Branch names serve as documentation visible in merge commits, PR lists, and CI pipelines. Short-lived branches minimize merge conflicts and reduce cognitive overhead from context switching.

### History Integrity

Git history is a shared asset. Destructive operations on shared branches undermine trust and can cause data loss for the entire team.

- **NEVER** force-push to shared branches (main, develop, release/\*)
- **PREFER** new commits over amending published history
- **USE** interactive rebase only on local, unpublished branches
- **PRESERVE** merge context through meaningful merge commit messages

Force-pushing rewrites history that others may have already based work on. Amending published commits creates divergent histories. Interactive rebase is a powerful tool for cleaning up local work before sharing, but becomes destructive once changes are published.

## Pull Request Alignment

### PR-Ready Commits

Commits should be structured with code review in mind. Each commit in a PR should build on the previous one logically, making the reviewer's job as efficient as possible.

- **LOGICAL ORDERING** - each commit builds on the previous coherently
- **REVIEWABLE SIZE** - prefer multiple small PRs over one massive changeset
- **DESCRIPTIVE** commit messages that guide the reviewer through the changes
- **TESTED** at each commit boundary - no commit should break the build
- **LINKED** to issues or tickets for traceability

Small, focused PRs get reviewed faster and more thoroughly. Large PRs invite rubber-stamping because reviewers experience cognitive fatigue. Logical commit ordering transforms code review from "spot the difference" into "follow the story".

## Commit Anti-Patterns

### Patterns to Actively Avoid

These anti-patterns degrade project history quality and signal undisciplined version control practices. Recognizing and avoiding them maintains a professional, navigable repository.

- **"WIP" COMMITS** on shared branches - use local branches or stash instead
- **"Fix typo" CHAINS** - squash trivial fixes into the relevant commit locally
- **MEGA-COMMITS** that bundle unrelated changes - split into atomic units
- **EMPTY MESSAGES** or meaningless descriptions like "update" or "changes"
- **COMMENTED-OUT CODE** committed "just in case" - trust version control
- **GENERATED FILE** commits that bloat history with reproducible artifacts

WIP commits on shared branches create noise in the project timeline. Fix-typo chains indicate insufficient review before the original commit. Mega-commits make reviews, reverts, and blame analysis nearly impossible. Commented-out code reveals distrust of the very tool designed to preserve history.
