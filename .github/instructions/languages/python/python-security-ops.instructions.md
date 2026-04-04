# Python Security & Ops Standards (UIA)

Production hardening, secret management, and observability for AI-driven systems.

<rules>
- **SECRETS:** Never hardcode secrets; use environment variables or specialized vaults.
- **CRYPTOGRAPHY:** Always use `secrets` module, never `random` for cryptographic tasks.
- **DOCKER:** Use multi-stage builds to keep production images minimal and secure.
- **LOGGING:** Use structured JSON logging with correlation IDs (contextvars).
- **OBSERVABILITY:** Implement OpenTelemetry for tracing in distributed systems.
</rules>

## Security Foundations

- **`python-dotenv`:** Use for local development; use system env in production.
- **Hasing:** Use `bcrypt` or `argon2` for passwords; never direct `hashlib`.
- **Sanitization:** Sanitize all AI-generated or external inputs before further processing.

## Production Hardening

- **Gunicorn/Uvicorn:** Use proper production servers for ASGI/WSGI applications.
- **Health Checks:** Include endpoints that verify critical dependencies.
- **Graceful Shutdown:** Implement signal handlers for proper resource cleanup.

<examples>
# Secure secret loading
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY") or ""
</examples>

<success_criteria>

- No secrets in source code.
- Production images are multi-stage.
- Structured logging includes correlation IDs.

</success_criteria>
