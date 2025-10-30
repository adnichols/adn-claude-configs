# Agent Catalog

Current roster of bespoke Claude and Codex agents defined in this repository. All briefs live under `agents/`, and templates for new roles live in `agents/templates/`.

## Implementation & Architecture
- `developer` (sonnet; `agents/developer.md`) — Implements specs with tests and enforces zero linting violations.
- `developer-fidelity` (sonnet; `agents/developer-fidelity.md`) — Implements specifications with absolute fidelity—no extra tests, features, or safeguards.
- `architect` (opus; `agents/plan-architect.md`) — Senior architecture partner who analyses codebases and produces designs/ADRs without writing implementation code.
- `simplify-planner` (opus; `agents/simplify-planner.md`) — Refactor planning specialist who produces cleanup plans that preserve existing behaviour.

## Review & Fidelity Safeguards
- `quality-reviewer` (inherits workspace default model; `agents/quality-reviewer.md`) — Production safety review covering security, data loss, regressions, and performance.
- `quality-reviewer-opus` (opus; `agents/quality-reviewer-opus.md`) — High-rigor variant of the quality reviewer for complex or high-risk diffs.
- `quality-reviewer-fidelity` (sonnet; `agents/quality-reviewer-fidelity.md`) — Ensures code matches specification requirements exactly with no scope expansion.
- `fidelity-reviewer` (opus; `agents/fidelity-reviewer.md`) — Compares generated task lists against source specifications and researches discrepancies.

## Debugging Support
- `debugger` (sonnet; `agents/debugger.md`) — Evidence-driven debugger who gathers logs, forms hypotheses, and recommends fixes without modifying production code.
- `debugger` (opus; `agents/debugger-hard.md`) — Manual “hard mode” debugger reserved for stubborn issues; enforces TodoWrite tracking and strict cleanup before reporting.

## Documentation
- `technical-writer` (sonnet; `agents/technical-writer.md`) — Produces concise post-implementation documentation with tight token limits.

---

When adding new agents, create the brief in `agents/` (using templates when possible) and update this catalog so downstream installations discover the new capability.
