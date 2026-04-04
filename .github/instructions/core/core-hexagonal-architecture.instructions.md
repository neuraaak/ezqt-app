# Core Hexagonal Architecture (UIA)

Framework for implementing Ports & Adapters to ensure domain isolation and testability.

<rules>
- **DEPENDENCY:** Always inward: Infrastructure -> Application -> Domain.
- **ISOLATION:** Domain must have zero knowledge of external frameworks or libraries.
- **PORTS:** Use `typing.Protocol` (Python) or `interface` (JS/TS) for contracts.
- **ADAPTERS:** Translate between infrastructure types and domain models.
- **DRIVING:** Entry points (API, CLI) must only invoke Use Cases.
</rules>

## Layered Structure

| Layer              | Responsibility                                          |
| :----------------- | :------------------------------------------------------ |
| **Domain**         | Entities, Value Objects, Domain Services (Stateless).   |
| **Application**    | Use Cases (Interactors) and Ports (Contracts).          |
| **Infrastructure** | Adapters (Repositories, Services) and Composition Root. |

## Why Hexagonal?

- **Testability:** Domain logic can be tested in pure isolation without mocks.
- **Flexibility:** Swapping a database or an AI model only affects one adapter.
- **Focus:** Prevents business logic from being scattered in API routes or ORM models.

<examples>
# Bad: Domain calling database
"Domain logic imports SQLAlchemy models directly."

# Good: Domain using a Port

"Application defines an OrderRepository Port; Infrastructure implements it via SQLAlchemyAdapter."
</examples>

<success_criteria>

- No infrastructure imports in Domain/Application.
- Fakes used for testing Ports instead of complex mocks.
- Logic resides in Domain Entities, not just Use Cases (Anemic Domain).

</success_criteria>
