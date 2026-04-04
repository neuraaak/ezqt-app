# Core Security & Sanitization (UIA)

Standards for input validation, secret management, and threat mitigation in AI-driven systems.

<rules>
- **VALIDATION:** ALWAYS use strict schemas (Zod, Pydantic) at all system boundaries (I/O).
- **SANITIZATION:** Sanitize all AI-generated or external content before execution or storage.
- **SECRETS:** Never log, print, or commit sensitive data; use masked environment variables.
- **PRIVILEGE:** Apply the Principle of Least Privilege (PoLP) to all service and tool permissions.
</rules>

## Input/Output Hardening

- **Boundary Validation:** Treat every external input as untrusted. Fail fast with clear schema errors.
- **Injection Prevention:** Use parameterized queries (SQL) and safe templates (t-strings/templates) for all dynamic content.
- **Output Encoding:** Encode or escape all data rendered in UI or CLI to prevent XSS/Injection.

## Secret Lifecycle

- **Development:** Use `.env` (excluded from git) with `python-dotenv` or `dotenv`.
- **Production:** Use specialized vaults (AWS Secrets Manager, HashiCorp Vault).
- **Audit:** Regularly scan for secrets in history using `trufflehog` or `ggshield`.

<examples>
# Bad: Raw input processing
"data = request.json['payload']"

# Good: Strict Schema Validation (2026)

"payload = UserInputSchema.parse(request.json['payload'])"
</examples>

<success_criteria>

- All I/O is schema-validated.
- No secrets present in codebase or logs.
- Sanitization layers exist between LLM outputs and execution engines.

</success_criteria>
