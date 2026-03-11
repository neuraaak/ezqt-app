# Hexagonal Architecture Standards for Python

Practical guidelines for implementing Hexagonal Architecture (Ports & Adapters) in Python projects, focusing on domain isolation, testability, and pragmatic application of clean architecture principles.

## Core Principles

### The Dependency Rule

The dependency rule is the foundation of hexagonal architecture: dependencies always point inward, from infrastructure toward the domain. The domain layer has zero knowledge of the outside world — it defines contracts (ports) that the infrastructure implements (adapters). This inversion of control ensures the business logic remains testable and independent of frameworks, databases, or external services.

- **ENFORCE** the dependency rule: `infrastructure` → `application` → `domain`, never the reverse
- **NEVER** import infrastructure modules from domain or application layers
- **DEFINE** all external interaction contracts as ports in the application layer
- **IMPLEMENT** ports through adapters in the infrastructure layer
- **USE** `import-linter` to enforce dependency boundaries in CI/CD

The dependency rule is non-negotiable. If you find domain code importing from infrastructure, refactor immediately. Use `import-linter` with a `layers` contract to catch violations automatically.

```ini
# .importlinter configuration in pyproject.toml
[tool.importlinter]
root_packages = ["{{my_project}}"]

[[tool.importlinter.contracts]]
name = "Hexagonal layers"
type = "layers"
layers = [
    "{{my_project}}.infrastructure",
    "{{my_project}}.application",
    "{{my_project}}.domain",
]
```

### When to Use Hexagonal Architecture

Hexagonal architecture introduces structural overhead that pays off in medium-to-large projects with complex business logic. For simple CRUD applications or scripts, it adds unnecessary complexity.

- **APPLY** hexagonal architecture when the project has non-trivial business rules or domain logic
- **APPLY** when the project needs to support multiple entry points (CLI, API, queue consumers)
- **APPLY** when infrastructure components may change (database swap, API provider migration)
- **AVOID** for simple CRUD applications, small scripts, or prototypes
- **START** simple and refactor toward hexagonal when complexity warrants it

A good rule of thumb: if your application mostly shuttles data between a database and an API without meaningful transformation or business rules, hexagonal architecture is overkill. When in doubt, start with a simpler layered structure and introduce ports/adapters as the domain logic grows.

### Architecture Decision Watchguard

Before applying hexagonal architecture to a project, evaluate it against the following criteria. If fewer than **3 criteria are met**, prefer a simpler layered approach.

- [ ] The project has non-trivial business rules or domain logic that must be protected from framework concerns
- [ ] Multiple entry points are needed or planned (e.g., API + CLI + queue consumer)
- [ ] Infrastructure components are likely to change (database swap, external API migration)
- [ ] The codebase is expected to grow significantly and be maintained long-term
- [ ] Testability of the domain in isolation is a hard requirement

**If hexagonal architecture is not justified → use a simple layered structure instead:**

```text
my_project/
├── models.py        # Data models (dataclasses, Pydantic)
├── services.py      # Business logic
├── repositories.py  # Data access
└── api.py / cli.py  # Entry points
```

Start simple. Introduce ports and adapters only when a concrete need emerges (e.g., needing to swap a dependency, add a second entry point, or isolate domain tests from infrastructure). Premature application of hexagonal architecture adds structural overhead without benefit.

> **Watchguard rule**: If you are unsure whether hexagonal architecture is warranted for the current project, default to the simple layered structure. Document the decision in `.github/instructions/README.md` so the choice is explicit and revisable.

## Project Structure

### Standard Layout

A well-organized project structure makes the architecture visible and discoverable. The three-layer split (domain, application, infrastructure) should be immediately apparent from the directory structure.

- **ORGANIZE** code into three top-level layers: `domain/`, `application/`, `infrastructure/`
- **PLACE** domain models, value objects, and domain services in `domain/`
- **PLACE** ports (interfaces) and use cases in `application/`
- **PLACE** adapters, framework integration, and configuration in `infrastructure/`
- **KEEP** the composition root (dependency wiring) in a dedicated module at the infrastructure level

```text
{{my_project}}/
├── domain/
│   ├── __init__.py
│   ├── models.py              # Entities, aggregates
│   ├── value_objects.py        # Immutable value types
│   ├── exceptions.py           # Domain-specific exceptions
│   └── services.py             # Domain services (stateless logic)
│
├── application/
│   ├── __init__.py
│   ├── ports/
│   │   ├── __init__.py
│   │   ├── repositories.py     # Data persistence ports
│   │   ├── services.py         # External service ports
│   │   └── notifications.py    # Notification ports
│   └── use_cases/
│       ├── __init__.py
│       ├── create_order.py     # One use case per file
│       └── cancel_order.py
│
├── infrastructure/
│   ├── __init__.py
│   ├── adapters/
│   │   ├── __init__.py
│   │   ├── sqlalchemy_order_repository.py
│   │   ├── redis_cache_service.py
│   │   └── smtp_notification_service.py
│   ├── api/                    # FastAPI/Flask routes (driving adapters)
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── cli/                    # CLI entry points (driving adapters)
│   │   └── __init__.py
│   └── container.py            # Composition root / DI wiring
│
└── main.py                     # Application entry point
```

### Scaling with Bounded Contexts

For larger projects with distinct business domains, organize by bounded context first, then by hexagonal layers within each context. This prevents a single monolithic domain layer from growing unwieldy.

- **SPLIT** large projects into bounded contexts when distinct business domains emerge
- **MAINTAIN** the hexagonal structure within each bounded context
- **SHARE** common types and utilities through a `shared/` module
- **AVOID** direct imports between bounded contexts — use application-level ports instead

```text
{{my_project}}/
├── orders/
│   ├── domain/
│   ├── application/
│   └── infrastructure/
├── payments/
│   ├── domain/
│   ├── application/
│   └── infrastructure/
└── shared/
    ├── domain/               # Shared value objects, base classes
    └── infrastructure/       # Shared adapters (logging, config)
```

## Domain Layer

### Domain Models

Domain models are the heart of the application. They encapsulate business rules and invariants, and should be pure Python objects with no dependencies on frameworks, ORMs, or external libraries.

- **USE** `dataclasses` with `frozen=True` for value objects (immutable by design)
- **USE** `dataclasses` for entities (mutable, identity-based equality)
- **KEEP** domain models as pure Python — no Pydantic, no SQLAlchemy, no framework dependencies
- **IMPLEMENT** business rules as methods on entities or domain services
- **VALIDATE** invariants in `__post_init__` for dataclasses
- **OVERRIDE** `__eq__` and `__hash__` on entities to use identity (ID-based), not structural equality

Domain models should never know how they are stored, serialized, or transported. Use Pydantic only at boundaries (API schemas, configuration) — never in the domain layer, as it introduces a framework dependency.

```python
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from {{my_project}}.domain.exceptions import InvalidOrderError


# Value Object — immutable, equality by value
@dataclass(frozen=True)
class Money:
    amount: int  # cents to avoid floating point
    currency: str = "EUR"

    def __post_init__(self) -> None:
        if self.amount < 0:
            msg = "Amount cannot be negative"
            raise ValueError(msg)

    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            msg = "Cannot add different currencies"
            raise ValueError(msg)
        return Money(amount=self.amount + other.amount, currency=self.currency)


# Entity — mutable, equality by identity
@dataclass
class Order:
    id: UUID = field(default_factory=uuid4)
    customer_id: UUID = field(default_factory=uuid4)
    items: list["OrderItem"] = field(default_factory=list)
    status: str = "draft"
    created_at: datetime = field(default_factory=datetime.now)

    def add_item(self, item: "OrderItem") -> None:
        if self.status != "draft":
            raise InvalidOrderError("Cannot modify a confirmed order")
        self.items.append(item)

    @property
    def total(self) -> Money:
        if not self.items:
            return Money(amount=0)
        result = self.items[0].subtotal
        for item in self.items[1:]:
            result = result.add(item.subtotal)
        return result

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Order):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
```

### Domain Exceptions

Domain exceptions express business rule violations in domain language. They should form a clear hierarchy rooted in a project-specific base exception.

- **CREATE** a base exception class for the entire project
- **DERIVE** domain exceptions from the base class, not from generic `Exception`
- **NAME** exceptions after the business rule they represent, not after technical details
- **INCLUDE** relevant context in exception messages

```python
class DomainError(Exception):
    """Base exception for all domain errors."""


class InvalidOrderError(DomainError):
    """Raised when an order violates business rules."""


class InsufficientStockError(DomainError):
    """Raised when stock is insufficient for the requested quantity."""
```

## Application Layer

### Ports (Interfaces)

Ports define the contracts between the application and the outside world. In Python, use `typing.Protocol` for structural typing — it provides duck typing with type safety, without requiring adapters to inherit from the port.

- **USE** `typing.Protocol` for all port definitions (preferred over `abc.ABC`)
- **DEFINE** ports in the `application/ports/` directory
- **KEEP** port methods focused — each port should represent a single responsibility
- **USE** domain types in port signatures, never infrastructure types
- **NAME** ports after what they do, not how they do it (e.g., `OrderRepository`, not `SQLAlchemyOrderRepository`)

`Protocol` is preferred over `abc.ABC` because it enables structural subtyping (duck typing with type checking). Adapters don't need to explicitly inherit from the port — they just need to implement the right methods. This reduces coupling and makes testing easier.

```python
from typing import Protocol
from uuid import UUID

from {{my_project}}.domain.models import Order


class OrderRepository(Protocol):
    def save(self, order: Order) -> None: ...

    def find_by_id(self, order_id: UUID) -> Order | None: ...

    def find_by_customer(self, customer_id: UUID) -> list[Order]: ...


class NotificationService(Protocol):
    def send_order_confirmation(self, order: Order) -> None: ...
```

When `abc.ABC` is preferable: use `abc.ABC` with `@abstractmethod` when you need runtime enforcement (e.g., frameworks that instantiate classes dynamically) or when you want to provide shared default implementations. For pure domain contracts, `Protocol` is the better choice.

### Use Cases

Use cases orchestrate the application's business operations. Each use case represents a single action the system can perform, coordinating domain objects and ports.

- **CREATE** one use case per file for clarity and single responsibility
- **INJECT** ports through the constructor (constructor injection)
- **KEEP** use cases thin — delegate business logic to domain models, not use cases
- **RETURN** domain types or simple result types, never infrastructure types
- **NAME** use cases with action verbs: `CreateOrder`, `CancelOrder`, `GetOrderDetails`

Use cases should read like a recipe: get data, apply business rules (via domain objects), persist results. If a use case grows beyond 20-30 lines, it likely contains logic that belongs in the domain layer.

```python
from dataclasses import dataclass
from uuid import UUID

from {{my_project}}.application.ports.repositories import OrderRepository
from {{my_project}}.application.ports.services import NotificationService
from {{my_project}}.domain.exceptions import InvalidOrderError
from {{my_project}}.domain.models import Order


@dataclass
class CreateOrderUseCase:
    order_repository: OrderRepository
    notification_service: NotificationService

    def execute(self, customer_id: UUID, items: list[dict]) -> Order:
        order = Order(customer_id=customer_id)

        for item_data in items:
            order.add_item(
                OrderItem(
                    product_id=item_data["product_id"],
                    quantity=item_data["quantity"],
                    unit_price=Money(amount=item_data["price_cents"]),
                )
            )

        self.order_repository.save(order)
        self.notification_service.send_order_confirmation(order)
        return order
```

### CQRS-Lite Pattern

For read-heavy applications, separate read and write operations without full event sourcing. This allows optimized read paths while maintaining clean domain models for writes.

- **SEPARATE** command use cases (mutations) from query use cases (reads) when performance requires it
- **ALLOW** query use cases to bypass the domain layer and read directly from optimized views
- **KEEP** write operations through the standard domain model path
- **AVOID** full CQRS with event sourcing unless the project genuinely requires event replay

CQRS-lite gives you the performance benefits of optimized reads without the complexity of event sourcing. Only introduce full CQRS when you need event replay, audit trails, or temporal queries.

## Infrastructure Layer

### Adapters (Implementations)

Adapters implement ports and handle all interaction with external systems: databases, APIs, file systems, message queues. They translate between domain types and infrastructure-specific types.

- **IMPLEMENT** one adapter per port per technology (e.g., `SQLAlchemyOrderRepository`, `InMemoryOrderRepository`)
- **HANDLE** all data mapping between domain models and infrastructure formats within the adapter
- **NEVER** leak infrastructure types (ORM models, API response objects) outside the adapter
- **NAME** adapters with the technology prefix: `SQLAlchemy...`, `Redis...`, `SMTP...`
- **KEEP** adapters focused on translation — no business logic in adapters

```python
from uuid import UUID

from sqlalchemy.orm import Session

from {{my_project}}.application.ports.repositories import OrderRepository
from {{my_project}}.domain.models import Money, Order, OrderItem


class SQLAlchemyOrderRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, order: Order) -> None:
        db_order = self._to_db_model(order)
        self._session.merge(db_order)
        self._session.flush()

    def find_by_id(self, order_id: UUID) -> Order | None:
        db_order = self._session.get(OrderDBModel, str(order_id))
        if db_order is None:
            return None
        return self._to_domain(db_order)

    def find_by_customer(self, customer_id: UUID) -> list[Order]:
        db_orders = (
            self._session.query(OrderDBModel)
            .filter_by(customer_id=str(customer_id))
            .all()
        )
        return [self._to_domain(o) for o in db_orders]

    @staticmethod
    def _to_domain(db_order: "OrderDBModel") -> Order:
        """Map database model to domain entity."""
        return Order(
            id=UUID(db_order.id),
            customer_id=UUID(db_order.customer_id),
            status=db_order.status,
            items=[
                OrderItem(
                    product_id=UUID(item.product_id),
                    quantity=item.quantity,
                    unit_price=Money(amount=item.price_cents),
                )
                for item in db_order.items
            ],
        )

    @staticmethod
    def _to_db_model(order: Order) -> "OrderDBModel":
        """Map domain entity to database model."""
        # Implementation depends on ORM specifics
        ...
```

### Composition Root and Dependency Injection

The composition root is where all dependencies are wired together. It lives in the infrastructure layer and is the only place that knows about all concrete implementations.

- **PREFER** manual dependency injection through constructor parameters for small-to-medium projects
- **CONSIDER** DI frameworks (`dependency-injector`, `lagom`, `dishka`) for large projects with many dependencies
- **WIRE** all dependencies in a single composition root module
- **USE** factory functions or a container class to create fully-configured use cases
- **NEVER** use service locator pattern — always inject dependencies explicitly

Manual DI is simpler, more transparent, and easier to debug. DI frameworks add value when the dependency graph becomes large (20+ dependencies) and tedious to manage manually. The composition root should be the only module that imports from all layers.

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from {{my_project}}.application.use_cases.create_order import CreateOrderUseCase
from {{my_project}}.infrastructure.adapters.sqlalchemy_order_repository import (
    SQLAlchemyOrderRepository,
)
from {{my_project}}.infrastructure.adapters.smtp_notification_service import (
    SMTPNotificationService,
)


class Container:
    """Composition root — wires all dependencies."""

    def __init__(self, database_url: str, smtp_host: str) -> None:
        self._engine = create_engine(database_url)
        self._session_factory = sessionmaker(bind=self._engine)
        self._smtp_host = smtp_host

    def create_order_use_case(self) -> CreateOrderUseCase:
        session = self._session_factory()
        return CreateOrderUseCase(
            order_repository=SQLAlchemyOrderRepository(session),
            notification_service=SMTPNotificationService(self._smtp_host),
        )
```

### Driving Adapters (API, CLI)

Driving adapters are entry points that invoke use cases. They handle request parsing, response formatting, and framework-specific concerns — but delegate all business logic to use cases.

- **KEEP** route handlers thin — parse request, call use case, format response
- **USE** Pydantic models for API request/response schemas (boundary validation only)
- **MAP** between API schemas and domain types in the driving adapter, not in use cases
- **HANDLE** domain exceptions and translate them to appropriate HTTP status codes

```python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from {{my_project}}.domain.exceptions import InvalidOrderError
from {{my_project}}.infrastructure.container import Container


router = APIRouter()


class CreateOrderRequest(BaseModel):
    customer_id: str
    items: list[dict]


class OrderResponse(BaseModel):
    id: str
    status: str
    total_cents: int


@router.post("/orders", response_model=OrderResponse)
def create_order(
    request: CreateOrderRequest,
    container: Container = Depends(get_container),
) -> OrderResponse:
    use_case = container.create_order_use_case()
    try:
        order = use_case.execute(
            customer_id=UUID(request.customer_id),
            items=request.items,
        )
    except InvalidOrderError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e

    return OrderResponse(
        id=str(order.id),
        status=order.status,
        total_cents=order.total.amount,
    )
```

## Testing Strategy

### Testing Diamond

Hexagonal architecture enables a testing strategy weighted toward fast, isolated tests. The "testing diamond" prioritizes domain unit tests and use case tests with fakes over slow integration tests.

- **WRITE** the most tests for domain logic (pure unit tests, no mocks needed)
- **TEST** use cases with in-memory fakes (fast, deterministic)
- **WRITE** fewer integration tests for adapters (database, API calls)
- **WRITE** minimal end-to-end tests for critical user journeys only
- **PREFER** fakes (in-memory implementations) over `unittest.mock.Mock` for port testing

```text
         /  E2E  \           ← Few: critical user journeys
        / Integration \      ← Some: adapter tests with real DB/API
       /  Use Cases     \    ← Many: use cases with fakes
      /  Domain Units     \  ← Most: pure domain logic tests
```

### In-Memory Fakes

Fakes are lightweight implementations of ports that store data in memory. They are faster, more readable, and more maintainable than mock objects because they implement real behavior.

- **CREATE** an in-memory fake for each repository port
- **PLACE** fakes in `tests/fakes/` or alongside the port definitions
- **IMPLEMENT** realistic behavior (store, retrieve, filter) — not just return values
- **REUSE** the same fakes across all tests that need that port

```python
from uuid import UUID

from {{my_project}}.domain.models import Order


class InMemoryOrderRepository:
    def __init__(self) -> None:
        self._orders: dict[UUID, Order] = {}

    def save(self, order: Order) -> None:
        self._orders[order.id] = order

    def find_by_id(self, order_id: UUID) -> Order | None:
        return self._orders.get(order_id)

    def find_by_customer(self, customer_id: UUID) -> list[Order]:
        return [o for o in self._orders.values() if o.customer_id == customer_id]
```

### Contract Tests

Contract tests verify that both the fake and the real adapter behave identically. Write the test suite once and run it against both implementations to ensure your fakes stay in sync with reality.

- **WRITE** a shared test suite that validates the port's contract
- **RUN** the same tests against both the fake and the real adapter
- **USE** pytest fixtures with parametrization to switch implementations
- **MARK** real adapter tests with `@pytest.mark.integration` for selective execution

```python
import pytest
from uuid import uuid4

from {{my_project}}.domain.models import Order
from tests.fakes.repositories import InMemoryOrderRepository


class OrderRepositoryContractTests:
    """Shared tests for any OrderRepository implementation."""

    @pytest.fixture
    def repository(self):
        raise NotImplementedError

    def test_save_and_find_by_id(self, repository):
        order = Order(customer_id=uuid4())
        repository.save(order)
        found = repository.find_by_id(order.id)
        assert found is not None
        assert found.id == order.id

    def test_find_by_id_returns_none_for_unknown(self, repository):
        assert repository.find_by_id(uuid4()) is None


class TestInMemoryOrderRepository(OrderRepositoryContractTests):
    @pytest.fixture
    def repository(self):
        return InMemoryOrderRepository()


@pytest.mark.integration
class TestSQLAlchemyOrderRepository(OrderRepositoryContractTests):
    @pytest.fixture
    def repository(self, db_session):
        return SQLAlchemyOrderRepository(db_session)
```

## Common Anti-Patterns

### Violations to Avoid

These anti-patterns undermine the benefits of hexagonal architecture. Recognizing them helps maintain clean boundaries and testability.

- **AVOID** "Anemic Domain" — entities that are just data holders with all logic in use cases or services. Push business rules into domain models.
- **AVOID** "Leaky Abstractions" — ports that expose infrastructure types (e.g., `SQLAlchemy.Query`, `requests.Response`). Use domain types exclusively.
- **AVOID** "God Use Case" — a single use case that handles multiple operations. Split into focused, single-responsibility use cases.
- **AVOID** "Premature Abstraction" — creating ports for internal domain logic that will never have multiple implementations. Only abstract at system boundaries.
- **AVOID** "Mock Overuse" — using `unittest.mock.Mock` for ports in tests. Use in-memory fakes that implement real behavior.
- **AVOID** "Framework Coupling" — importing FastAPI, Django, or SQLAlchemy in domain or application layers.
- **AVOID** "Shared Mutable State" — global variables or singletons that bypass dependency injection.
- **AVOID** "Pass-Through Layers" — creating port/adapter pairs for trivial operations that add no value. Apply hexagonal patterns selectively.

The most common mistake is abstracting too early or too much. Create ports only for true system boundaries where you need substitutability (testing, technology swaps). Internal domain collaborations don't need port abstractions.
