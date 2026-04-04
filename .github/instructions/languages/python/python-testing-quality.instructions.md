# Python Testing & Quality Standards (UIA)

Validation strategies, test architecture, and quality assurance patterns.

<rules>
- **FRAMEWORK:** Use `pytest` as the primary testing framework.
- **COVERAGE:** Target 80-90% coverage for business logic; don't chase 100% on trivialities.
- **PARAMETERIZE:** Use `pytest.mark.parametrize` to avoid duplicate test logic.
- **PROPERTY:** Use `hypothesis` for property-based testing of invariants.
- **FAIL-FAST:** Use `Pydantic` or `marshmallow` for immediate input validation.
</rules>

## Testing Structure

- **`conftest.py`:** Use for shared fixtures and custom hooks.
- **Markers:** Document custom markers (e.g., `@pytest.mark.slow`) in TOML.
- **Mocking:** Use `unittest.mock` or `pytest-mock` for external service isolation.

<examples>
# Parameterized test
import pytest

@pytest.mark.parametrize("val, expected", [(1, True), (0, False)])
def test_is_truthy(val, expected):
assert bool(val) == expected

# Property-based test

from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_sort_invariant(lst):
result = sorted(lst)
assert len(result) == len(lst)
</examples>

<success_criteria>

- Tests are modular and independent.
- High-level business invariants are verified.
- Input validation happens at boundaries.

</success_criteria>
