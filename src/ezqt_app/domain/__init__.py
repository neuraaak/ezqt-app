# ///////////////////////////////////////////////////////////////
# DOMAIN - Domain layer aggregator
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Domain layer — pure contracts and models, no infrastructure dependencies."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////
from .errors import (
    BootstrapError,
    DomainError,
    EzQtError,
    InitAlreadyInitializedError,
    InitStepError,
    InvalidOverwritePolicyError,
    MissingPackageResourceError,
    ResourceCompilationError,
    ResourceError,
)
from .models import (
    FONT_SPECS,
    SIZE_POLICY_SPECS,
    FontSpec,
    RuntimeStateModel,
    SizePolicySpec,
)
from .ports import (
    ConfigServiceProtocol,
    RuntimeStateServiceProtocol,
    SettingsServiceProtocol,
    TranslationServiceProtocol,
    UiComponentFactoryProtocol,
)
from .results import BaseResult, InitResult, InitStepResult, ResultError

# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////
__all__ = [
    # Models
    "RuntimeStateModel",
    "FontSpec",
    "SizePolicySpec",
    "FONT_SPECS",
    "SIZE_POLICY_SPECS",
    # Errors
    "EzQtError",
    "DomainError",
    "BootstrapError",
    "InitAlreadyInitializedError",
    "InitStepError",
    "ResourceError",
    "MissingPackageResourceError",
    "ResourceCompilationError",
    "InvalidOverwritePolicyError",
    # Ports
    "ConfigServiceProtocol",
    "RuntimeStateServiceProtocol",
    "SettingsServiceProtocol",
    "TranslationServiceProtocol",
    "UiComponentFactoryProtocol",
    # Results
    "BaseResult",
    "InitResult",
    "InitStepResult",
    "ResultError",
]
