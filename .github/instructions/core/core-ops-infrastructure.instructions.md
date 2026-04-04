# Core Ops & Infrastructure (UIA)

Generic standards for containerization, observability, and deterministic runtimes.

<rules>
- **RUNTIME:** Target Node.js 24+ or Python 3.14+ for high-performance, stable runtimes.
- **DOCKER:** Use multi-stage builds and non-root users. Never use `latest` tags.
- **OBSERVABILITY:** Implement OpenTelemetry (OTel) for tracing, metrics, and logs.
- **DETERMINISM:** Use lockfiles (`pnpm-lock.yaml`, `uv.lock`) for reproducible builds.
</rules>

## Containerization Standards

- **Multi-Stage:** Separate build-time dependencies from the runtime image.
- **Small Footprint:** Prefer `alpine` or `distroless` images for production.
- **Health Checks:** Define `HEALTHCHECK` instructions for orchestration awareness.

## Observability & Logging

- **JSON Logging:** Emit structured logs for automated analysis.
- **Correlation IDs:** Propagate `trace_id` and `span_id` across service boundaries.
- **Proactive Monitoring:** Define thresholds for critical failure paths (circuit breakers).

<examples>
# Docker Multi-Stage Pattern (2026)
# Build stage
FROM python:3.14-slim AS builder
# ... install dependencies ...

# Runtime stage

FROM python:3.14-slim
RUN useradd -m appuser
USER appuser

# ... copy only necessary artifacts ...

</examples>

<success_criteria>

- Production images are minimal and secure (non-root).
- Observability stack follows OpenTelemetry standards.
- Build environments are deterministic via lockfiles.

</success_criteria>
