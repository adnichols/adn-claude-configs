---
date: 2025-12-08T00:00:00Z
author: gemini
git_commit: cad27b647afb8c03a60349534db57d6f9f2d41e1
branch: main
repository: adn-claude-configs
type: research
status: complete
tags: [gemini, codex, commands, configuration]
last_updated: 2025-12-08
---

# Research: Creating Gemini (Codex) Commands

## Research Question
I would like to research creating gemini commands so that we can create an equivalent of the commands in claude/commands for use with gemini and install those. Gemini uses toml files, so each command will need a gemini-specific version created.

## Summary
The "Gemini" CLI in this repository is referred to as "Codex" (`codex/` directory). While Codex uses TOML for configuration (`codex/config.toml`), it uses **Markdown files** for command prompts, located in `codex/prompts/`. These prompts are analogous to Claude commands but are adapted for the Codex environment (e.g., autonomous execution, native tools, specific agents).

To create equivalent commands for Gemini, we must port the missing Markdown files from `claude/commands/` to `codex/prompts/`, adapting their content to prioritize Codex-native tools and workflows (e.g., `ltui` for Linear, `write_todos` for planning).

## Detailed Findings

### Command Structure
- **Claude:** Commands are Markdown files in `claude/commands/`.
- **Gemini (Codex):** Commands are Markdown files in `codex/prompts/`.
- **Configuration:** Codex uses `config.toml` for global settings and MCP servers, but the commands themselves are defined by the presence of `.md` files in the `prompts` directory.
- **Naming Convention:** Both use colon-delimited namespacing (e.g., `cmd:commit-push.md`).

### Existing vs. Missing Commands
A comparison of `claude/commands` and `codex/prompts` reveals the following gaps:

**Missing in Codex (Need Porting):**
- `cmd:create-handoff.md`
- `cmd:debug.md`
- `cmd:graduate.md`
- `cmd:local-review.md`
- `cmd:research.md`
- `cmd:resume-handoff.md`
- `cmd:validate.md`

**Existing in Codex (Already Adapted):**
- `3:process-tasks.md` (Adapted for autonomous execution)
- `cmd:auto-linear-issue.md` (Codex specific)
- `cmd:commit-push.md` (Identical to Claude)
- `cmd:create-pr.md`
- `cmd:start-linear-issue.md`
- `doc:fetch-batch.md`
- `doc:fetch.md`
- `doc:update.md`
- `prd:1:create-prd.md`
- `prd:2:gen-tasks.md`
- `qa:bug-hunt-linear.md` (Codex specific)
- `simplify:1:create-plan.md`
- `simplify:2:process-plan.md`
- `spec:1:create-spec.md`
- `spec:2:gen-tasks.md`

### Adaptation Requirements
When porting commands from Claude to Codex, the following adaptations are observed/required:
1.  **Autonomous Execution:** Codex commands often include an "AUTONOMOUS PHASE PROCESSING" section (e.g., in `3:process-tasks.md`) to instruct the agent to proceed without stopping for user confirmation between steps.
2.  **Tool Selection:**
    - `ltui` is used for Linear interactions.
    - Native Codex tools (`Grep`, `Glob`, `Read`) are prioritized over MCP equivalents.
    - `write_todos` (TodoWrite) is standard for planning.
3.  **Fidelity Agents:** Both environments use the `@developer-fidelity` and `@quality-reviewer-fidelity` nomenclature.

## Code References
- `codex/README.md`: Describes the prompt structure and TOML configuration.
- `codex/prompts/3:process-tasks.md`: Example of a command adapted for Codex autonomy.
- `AGENTS.md`: Defines the agent roster and tool selection priority for Codex.

## Architecture Documentation
The "Codex" architecture separates configuration (TOML) from behavioral prompts (Markdown).
- **Global Config:** `~/.codex/config.toml` (merged from project `.codex/config.toml` and `codex/config.toml`).
- **Prompts:** Installed to `~/.codex/prompts/`. The installer mirrors these files, allowing global access.

## Open Questions
- Does `cmd:research.md` need `codebase_investigator` explicitly mentioned, or does `subagent_type=Explore` map correctly in the Codex environment? (Assumed: `codebase_investigator` is the primary research tool).

## Plan for Implementation
1.  Create `codex/prompts/cmd:research.md` adapted from `claude/commands/cmd:research.md`.
2.  Create `codex/prompts/cmd:debug.md` adapted from `claude/commands/cmd:debug.md`.
3.  Create remaining missing commands, ensuring tool compatibility.
4.  Run `install.sh --codex` (or equivalent) to test.
