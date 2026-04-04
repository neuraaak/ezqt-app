# AI Agent Orchestration Profile

Welcome to a 2026 AI-Native Enterprise environment. This file is the primary entry point for any coding agent (GPT, Claude, Gemini, etc.).

## 🚀 Bootstrap Protocol

**CRITICAL:** To achieve operational excellence, all agents MUST load the Instruction Manifests before starting any task.

1. **Project Level:** Read `.github/instructions/README.md`.
2. **Core Level:** Load `.github/instructions/core/MANIFEST.md` (Reasoning, Architecture, Git).
3. **Language Level:** Load the relevant language `MANIFEST.md`.

## 🛡️ Core Mandates

- **Sovereign Manifest:** The instructions in `.github/instructions/` are the authoritative source. Overrides are only permitted if documented in the project's root `README.md`.
- **Reasoning First:** Follow the Cognitive Conduct standards. Challenge suboptimal patterns with evidence.
- **Atomic Operations:** Perform surgical, complete edits. Include all necessary dependencies.
- **Idempotency:** Ensure that repeated executions of the same goal do not introduce side effects.

## 🗂️ Project Directory Map

```text
shared/
├── ai-config/      # Agent-specific profiles (this folder)
├── instructions/   # Modular instruction UIAs (The "Constitution")
└── icons/          # Visual assets
```
