# Agent Catalog

Current roster of bespoke Claude and Codex agents defined in this repository. All briefs live under `agents/`, and templates for new roles live in `agents/templates/`.

## Implementation & Architecture
- `developer` (sonnet; `agents/developer.md`) — Implements specs with tests and enforces zero linting violations.
- `developer-fidelity` (sonnet; `agents/developer-fidelity.md`) — Implements specifications with absolute fidelity—no extra tests, features, or safeguards.
- `architect` (opus; `agents/plan-architect.md`) — Senior architecture partner who analyses codebases and produces designs/ADRs without writing implementation code.
- `simplify-planner` (opus; `agents/simplify-planner.md`) — Refactor planning specialist who produces cleanup plans that preserve existing behaviour.

## Tool Selection Priority (Codex Environment)

When agents run within Codex, they MUST prioritize native Codex tools over MCP server tools:

**DO:**
- Use native `Grep` tool (not `claude.Grep`)
- Use native `Glob` tool (not `claude.Glob`)
- Use native `Read` tool (not `claude.Read`)
- Use direct bash commands (`rg`, `find`, etc.) when appropriate

**DO NOT:**
- Call MCP-prefixed tools for basic filesystem operations
- Route through Claude Code MCP server for searches or file reads
- Use `claude.*` tool variants when native equivalents exist

**Rationale:** MCP tool wrapping introduces unnecessary latency and may produce inconsistent results. Native Codex tools are optimized for the local filesystem and provide superior performance.

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

## Fidelity & Execution House Rules (Template for Project Repos)

Many of the Codex prompts in this repo assume that application repositories define their own fidelity and execution rules in a project-level `AGENTS.md`. The following block can be copied and adapted into those repos.

### Fidelity

- Treat the source document (user requirements, PRD, specification, or task file) as the single source of truth.
- Do not add requirements, tests, or security work beyond what is explicitly specified.
- Do not broaden scope; when something is ambiguous or missing, ask for clarification instead of guessing.
- Preserve stated constraints and limitations unless the project’s AGENTS.md explicitly allows widening them.

### Execution

- Always do implementation work on a non-`main` branch; create a branch if needed and follow the project’s naming conventions.
- Run the repository’s primary test command(s) before committing any change that touches behavior, plus any additional checks (lint, build, etc.) defined in the project’s AGENTS.md or TESTING.md.
- When working from task lists or simplification plans:
  - After completing a listed sub-task or step, immediately change its checkbox from `[ ]` to `[x]` in the same file.
  - Verify that the change is reflected in the file (do not batch updates at the end).
  - Keep any “Relevant Files” or similar sections accurate as files are created or modified.
- Prefer repository-specific guidance for tools, security, and performance; this central file is only a baseline.

Projects should copy this section into their own `AGENTS.md` and adjust details (branch naming, test commands, security expectations) to match local norms.
