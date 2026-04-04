# Core Agentic Collaboration (UIA)

Protocols for multi-agent handoffs, state persistence, and collaborative reasoning.

<rules>
- **HANDOFF:** Provide a structured "State Object" when passing tasks to other agents.
- **PERSISTENCE:** Use "Durable Checkpoints" to allow resumption after interruptions.
- **METADATA:** Include reasoning rationale in comments for future agent context.
- **CONFLICT:** If agents disagree, escalate to human or use a "Reviewer" agent for consensus.
</rules>

## Collaborative Workflow

- **Context Compression:** Summarize long execution histories before handoffs.
- **Atomic Tasks:** Break complex goals into independent, verifiable sub-tasks.
- **State Schema:** Maintain a JSON-based state for tracking goals, tool outputs, and errors.

## AI-to-AI Communication

When working in a multi-agent environment (e.g., Coder + Reviewer):

1. **Coder:** Implements logic and provides a "Testing Strategy" in the handoff.
2. **Reviewer:** Validates logic against `MANIFEST.md` and provides specific improvement points.
3. **Orchestrator:** Manages the overall state and ensures idempotency across turns.

<examples>
# Handoff Context (2026)
"<handoff_context>
Status: Part 1/3 complete.
State: Database connection established.
Next Step: Implement the 'Order' entity.
Rationale: Following Hexagonal isolation rules (core-hexagonal-architecture).
</handoff_context>"
</examples>

<success_criteria>

- Task progress is traceable via durable state.
- Handoffs are clear, structured, and goal-oriented.
- Reasoning is documented to prevent context loss.

</success_criteria>
