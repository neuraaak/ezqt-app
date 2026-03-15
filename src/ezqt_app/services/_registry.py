# ///////////////////////////////////////////////////////////////
# SERVICES._REGISTRY - Lightweight service registry
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Lightweight service registry supporting test-time instance overrides.

Usage — production (no change needed in calling code)::

    def get_config_service() -> ConfigService:
        return ServiceRegistry.get(ConfigService, ConfigService)

Usage — tests::

    ServiceRegistry.register(ConfigService, FakeConfigService())
    # … run test …
    ServiceRegistry.reset(ConfigService)

The registry acts as a lazy singleton cache in production and an override
mechanism in tests, removing the need to monkey-patch private module
variables or access ``_private`` attributes.
"""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from collections.abc import Callable
from typing import TypeVar

_T = TypeVar("_T")


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class ServiceRegistry:
    """Lightweight service registry supporting test-time instance overrides.

    In production, :meth:`get` acts as a lazy singleton: the factory is called
    once and the result is cached.  In tests, :meth:`register` injects a
    replacement instance for a specific type; :meth:`reset` removes it and
    clears the cached instance so the next :meth:`get` call rebuilds cleanly.
    """

    _instances: dict[type, object] = {}
    _overrides: dict[type, object] = {}

    @classmethod
    def get(cls, service_type: type[_T], factory: Callable[[], _T]) -> _T:
        """Return the registered override, or the lazily-cached instance.

        Parameters
        ----------
        service_type:
            The class used as the registry key.
        factory:
            Callable (usually the class itself) invoked once to create the
            instance when no cached value exists.
        """
        if service_type in cls._overrides:
            return cls._overrides[service_type]  # type: ignore[return-value]
        if service_type not in cls._instances:
            cls._instances[service_type] = factory()
        return cls._instances[service_type]  # type: ignore[return-value]

    @classmethod
    def register(cls, service_type: type[_T], instance: _T) -> None:
        """Register *instance* as the active implementation for *service_type*.

        Primarily intended for test fixtures.  The override takes precedence
        over any cached instance until :meth:`reset` is called.
        """
        cls._overrides[service_type] = instance

    @classmethod
    def reset(cls, service_type: type | None = None) -> None:
        """Remove override and cached instance.

        Parameters
        ----------
        service_type:
            Type to reset.  Pass ``None`` to clear the entire registry
            (useful in a global ``autouse`` teardown fixture).
        """
        if service_type is None:
            cls._overrides.clear()
            cls._instances.clear()
        else:
            cls._overrides.pop(service_type, None)
            cls._instances.pop(service_type, None)
