# Python Development Standards & Optimization Rules

Professional Python development practices focused on modern language features, type safety, and maintainable code patterns.

## Python Ecosystem Foundations

### Virtual Environment Management

Virtual environments are essential for isolating project dependencies and ensuring reproducible builds. Without them, you risk dependency conflicts and "works on my machine" issues that plague Python projects.

- **ALWAYS** use `.venv` virtual environment for all Python operations
- **ACTIVATE** `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Unix)
- **USE** `python -m pip` instead of `pip` when .venv is active to ensure correct interpreter
- **NEVER** install packages globally when .venv is available
- **MAINTAIN** clean dependency management with `pip-tools`, `poetry`, or `uv`

For dependency management, choose tools that provide lock files: `pip-tools` generates `requirements.txt` from `requirements.in`, `poetry` uses `pyproject.toml` with `poetry.lock`, and `uv` offers ultra-fast resolution. The key is maintaining deterministic builds across environments.

### Python Version Management

Modern Python versions provide significant improvements in syntax, performance, and error messages. Targeting Python 3.10+ unlocks union types, pattern matching, and better type hints, while 3.11+ offers measurable performance gains.

- **TARGET** Python 3.10+ for modern union syntax (`int | str`) and structural pattern matching
- **USE** Python 3.11+ for 10-25% performance improvements when possible
- **SPECIFY** Python version in `pyproject.toml` using `requires-python` or in `setup.py` with `python_requires`
- **TEST** against multiple Python versions with tox or GitHub Actions

Always specify version requirements explicitly rather than assuming a particular Python version is available. Test compatibility across versions in CI/CD to catch issues early.

## Modern Type System

### Native Type Annotations

Python 3.9+ introduced built-in generic types that replace the `typing` module equivalents. These native types are more readable, performant, and align with Python's evolution toward better type support.

- **PREFER** `list[str]` over `List[str]` (Python 3.9+)
- **USE** `dict[str, int]` over `Dict[str, int]` (Python 3.9+)
- **USE** `tuple[int, str]` over `Tuple[int, str]` (Python 3.9+)
- **IMPORT** from `collections.abc` instead of `typing` for `Sequence`, `Mapping`, `Iterable`, `Callable`

These built-in generics are more readable and performant. For collections from the standard library, import from `collections.abc` rather than `typing` when possible for better type checking and clearer intent.

### Advanced Type Features

Modern Python's type system supports sophisticated patterns that enable better code design without runtime overhead. Understanding when to use each feature is key to writing maintainable, type-safe code.

- **USE** `typing.Protocol` for structural typing when you need duck typing with type safety
- **USE** `typing.Literal` for string/numeric constants instead of enums when values are fixed at type-checking time
- **IMPLEMENT** `typing.TypedDict` for API response structures and structured dictionaries
- **USE** `typing.Annotated` for adding metadata to types, but keep validation logic separate
- **ALWAYS** use `from __future__ import annotations` at the top of files

`Protocol` allows defining interfaces without inheritance, making code more flexible. `TypedDict` provides type safety without runtime overhead. `Annotated` types are useful for metadata, but avoid mixing validation logic with type definitions.

## Code Quality Standards

### Formatting and Linting

Consistent code formatting and linting catch errors early and reduce cognitive load when reading code. Modern tools like `ruff` combine multiple tools into one fast, reliable solution.

- **USE** `ruff` as single tool for formatting AND linting (replaces Black + isort + flake8)
- **IMPLEMENT** `ruff format` for code formatting (88 character line length)
- **USE** `ruff check` with selective rule sets (`--select` specific categories, not `--select ALL`)
- **MAINTAIN** consistent line endings (LF for Unix, CRLF for Windows)
- **USE** `pre-commit` hooks with `ruff`, `mypy`, and `pytest`

Be selective with linting rules rather than enabling everything. The `--select ALL` option includes experimental rules that may cause noise. Configure your editor and Git to handle line endings automatically.

### Type Coverage and Documentation

Type hints improve code maintainability and enable better tooling support. However, aim for pragmatic coverage rather than 100% type coverage, which can create unnecessary friction for simple code.

- **IMPLEMENT** type hints for all public functions and methods
- **PRIORITIZE** critical paths and public APIs over internal helper functions
- **USE** `mypy` in strict mode or `pyright`/`basedpyright` for static type analysis
- **CONFIGURE** type checkers pragmatically to avoid blocking development on edge cases
- **WRITE** Google-style docstrings with type information in function signatures
- **INCLUDE** examples in docstrings when they clarify usage, but keep them simple

Write docstrings that complement type hints rather than duplicating them. Generate API documentation with `pdoc` for lightweight projects or `sphinx` for comprehensive documentation.

### Testing Practices

Test coverage is a means to an end, not an end in itself. Focus on testing critical business logic and edge cases rather than achieving arbitrary coverage percentages.

- **MAINTAIN** 80-90% test coverage with focus on critical business logic
- **USE** `pytest` as the testing framework with `pytest-cov` for coverage reporting
- **USE** `pytest.mark.parametrize` for data-driven tests to reduce duplication
- **IMPLEMENT** property-based testing with `hypothesis` for invariants and edge cases
- **USE** `pytest-asyncio` with proper fixture management for async code
- **USE** `pytest-benchmark` sparingly for performance regression testing

Avoid premature optimization and don't aim for 100% coverage of trivial code. Property-based testing is particularly valuable for finding edge cases that are difficult to enumerate manually.

## Performance Engineering

### Optimization Principles

Performance optimization should be data-driven, not speculative. Profile first to identify actual bottlenecks, then optimize only those code paths that matter.

- **PROFILE** before optimizing using `cProfile` and `pstats` for CPU, `tracemalloc` for memory
- **USE** `py-spy` for production debugging
- **OPTIMIZE** only code paths that are actually bottlenecks
- **USE** `__slots__` for data-intensive classes with many instances (40-50% memory reduction)
- **IMPLEMENT** `functools.lru_cache` with size limits for expensive computations
- **USE** `functools.singledispatch` for polymorphic performance

Premature optimization adds complexity without benefit. Use `__slots__` judiciously as it prevents dynamic attribute assignment. Be aware of memory implications and cache invalidation needs when using `lru_cache`.

### Concurrency Patterns

Choosing the right concurrency model depends on the problem characteristics. I/O-bound operations benefit from async/threading, while CPU-bound tasks require multiprocessing.

- **USE** `asyncio` for I/O-bound operations with high latency
- **USE** `threading.ThreadPoolExecutor` for I/O-bound operations with many files
- **USE** `multiprocessing.Pool` for CPU-bound independent tasks
- **USE** `multiprocessing` with `Manager` for CPU-bound tasks with shared state
- **COMBINE** approaches with `concurrent.futures` for mixed workloads
- **PREFER** `collections.deque` over `list` for FIFO operations (O(1) vs O(n))
- **USE** `bisect` module for maintaining sorted data efficiently
- **IMPLEMENT** lazy evaluation with `@property` and `functools.cached_property`

For mixed workloads, combine approaches appropriately. Use `deque` for queue operations where you need O(1) insertions/deletions at both ends. The `bisect` module provides efficient binary search for sorted sequences.

## Architectural Patterns

### Design Patterns

Python's dynamic nature and rich standard library provide elegant ways to implement common design patterns. Choose patterns that fit Python's philosophy rather than forcing patterns from other languages.

- **USE** `abc.ABC` with `@abstractmethod` for defining interfaces when you need runtime enforcement
- **PREFER** `typing.Protocol` for structural typing (more flexible, no inheritance required)
- **IMPLEMENT** factory patterns using `@classmethod` for alternative constructors
- **USE** `weakref.WeakSet` for observer patterns to prevent memory leaks
- **IMPLEMENT** proper cleanup in context managers using `contextlib.contextmanager` or `contextlib.asynccontextmanager`

Factory patterns with `@classmethod` provide clearer intent than complex `__init__` methods. Weak references prevent memory leaks when observers don't explicitly unsubscribe.

### Resource Management

Python's context manager protocol (`with` statements) is the standard way to manage resources. Always use context managers for anything that needs cleanup.

- **ALWAYS** use context managers for resources that need cleanup: file handles, database connections, network sockets, locks
- **PREFER** `with` statements over manual `try/finally` blocks
- **IMPLEMENT** `__enter__` and `__exit__` methods for custom resources
- **USE** `@contextmanager` decorator for simple context managers
- **USE** descriptors for advanced attribute access patterns (validation, lazy loading, computed properties)

Context managers provide exception safety and clarity. Keep descriptor logic simple and well-documented, as they can make code harder to understand for developers unfamiliar with the pattern.

## Data Processing

### Large Dataset Handling

Processing large datasets requires different strategies than small datasets. Memory efficiency and streaming become critical when data doesn't fit in RAM.

- **PROCESS** data in chunks rather than loading everything into memory
- **USE** generators and iterators to process data streams efficiently
- **USE** `pandas.read_csv(chunksize=...)` for CSV files larger than 1GB
- **CONSIDER** specialized tools like `polars` for better performance on large datasets
- **PREFER** NumPy with vectorization over Python loops for numerical computation
- **USE** `numpy.memmap` for out-of-core processing of arrays
- **CONSIDER** `h5py` or `zarr` formats for hierarchical data storage with efficient partial reads

For numerical computation, vectorization with NumPy provides orders of magnitude better performance than Python loops. Memory-mapped arrays allow processing datasets larger than available RAM.

## Security and Production Hardening

### Security Best Practices

Security is not optional in production code. Follow established practices for cryptographic operations, input validation, and secret management.

- **USE** `secrets` module for cryptographic operations, never `random`
- **USE** dedicated libraries like `bcrypt` or `argon2` for password hashing, not `hashlib` directly
- **VALIDATE** all user inputs with strict schemas
- **AVOID** complex regex patterns for email validation—use dedicated validation libraries
- **STORE** all secrets in environment variables, never hardcode them
- **USE** `python-dotenv` for local development
- **USE** proper secret management systems (AWS Secrets Manager, HashiCorp Vault) for production
- **IMPLEMENT** structured logging with correlation IDs for audit trails

Never use the `random` module for cryptographic purposes. For password hashing, use battle-tested libraries rather than implementing your own. Email validation with regex is notoriously fragile—use dedicated libraries or built-in validation.

### Error Handling

Proper error handling makes debugging easier and provides better user experience. Create meaningful exception hierarchies that reflect your domain model.

- **CREATE** custom exception hierarchies that inherit from appropriate base exceptions
- **USE** specific exception types rather than generic `Exception`
- **ALWAYS** use `raise ... from ...` to preserve exception chains
- **IMPLEMENT** retry logic with exponential backoff for external service calls
- **SET** reasonable retry limits to avoid cascading failures
- **USE** circuit breaker patterns for services that may be unavailable

Exception chains (`raise ... from ...`) preserve the original exception context, making debugging much easier. Circuit breakers prevent resource exhaustion during service outages.

## DevOps and Deployment

### Containerization

Docker containers provide consistent environments across development and production. Use best practices to minimize image size and ensure reliability.

- **USE** multi-stage Docker builds to minimize image size
- **SEPARATE** build dependencies from runtime dependencies
- **SPECIFY** exact Python version tags rather than using `latest`
- **INCLUDE** health checks in Dockerfiles for container orchestration systems
- **USE** `gunicorn` with `uvicorn` workers for ASGI applications in production
- **IMPLEMENT** graceful shutdown handling with signal handlers

Multi-stage builds significantly reduce image size by excluding build tools from the final image. Health checks enable container orchestration systems to detect and restart unhealthy containers.

### Observability

Observability is crucial for understanding system behavior in production. Structured logging and distributed tracing provide visibility into complex systems.

- **IMPLEMENT** structured logging with correlation IDs for request tracing
- **USE** `contextvars` to propagate request context through async code
- **INCLUDE** health check endpoints that verify critical dependencies
- **USE** OpenTelemetry for tracing in distributed systems

Correlation IDs enable tracing requests across service boundaries. `contextvars` provides thread-local-like behavior for async code without explicitly passing context. OpenTelemetry provides vendor-neutral observability standards.

## Code Generation Guidelines

### Modern Python Syntax

Modern Python syntax (3.10+) provides more readable and expressive code. Use these features when targeting supported Python versions.

- **USE** union operators (`int | str`) instead of `Union[int, str]` (Python 3.10+)
- **USE** structural pattern matching for complex conditionals (Python 3.10+)
- **USE** `pathlib.Path` exclusively for file operations instead of `os.path`
- **IMPLEMENT** async patterns for I/O-bound operations
- **AVOID** mixing async and sync code unnecessarily
- **USE** `asyncio` for concurrent I/O, not for CPU-bound tasks

`pathlib.Path` provides a more intuitive and cross-platform API than `os.path`. Structural pattern matching (`match/case`) is more readable than long `if/elif` chains for complex conditionals.

### Error Handling Patterns

Error handling should reflect your domain model and provide actionable information. Avoid generic exceptions that make debugging difficult.

- **CREATE** exception hierarchies that reflect your domain model
- **USE** specific exceptions for different error conditions
- **INCLUDE** context in error messages, but avoid exposing sensitive information
- **USE** environment variables with validation for configuration
- **PREFER** libraries that provide type-safe configuration with validation
- **VALIDATE** configuration at startup rather than discovering invalid values at runtime

Configuration validation at startup prevents runtime failures from invalid settings. Type-safe configuration libraries catch errors early and provide better developer experience.

## Continuous Integration

### Quality Gates

CI/CD pipelines should enforce quality standards without blocking development. Set reasonable thresholds that focus on critical issues rather than perfection.

- **CONFIGURE** CI/CD to run type checking, linting, and tests on every commit
- **USE** matrix builds to test against multiple Python versions
- **ENFORCE** 80-90% test coverage focused on critical paths
- **REQUIRE** all linting rules to pass
- **VALIDATE** type checking in strict mode with appropriate exemptions for edge cases
- **SCAN** dependencies for vulnerabilities using `pip-audit` or `safety`
- **CHECK** code complexity with `radon` (cyclomatic complexity of 10-15 is acceptable)
- **USE** `bandit` for security pattern detection, but review findings carefully

Reasonable quality gates prevent technical debt without creating friction. False positives from security scanners are common, so review findings rather than blindly enforcing all rules. Code complexity limits should be pragmatic—complexity of 10-15 is typically acceptable for business logic.
