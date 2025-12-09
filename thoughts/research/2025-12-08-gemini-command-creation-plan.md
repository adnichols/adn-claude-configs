---
date: 2025-12-08T00:45:00Z
author: gemini
git_commit: cad27b647afb8c03a60349534db57d6f9f2d41e1
branch: main
repository: adn-claude-configs
type: research
status: complete
tags: [gemini, commands, toml, migration, hl]
last_updated: 2025-12-08
---

# Research: Creating Gemini CLI Commands (TOML)

## Research Question
Research creating Gemini commands so that we can create an equivalent of the commands in `claude/commands` for use with Gemini and install those. Gemini uses TOML files, so each command will need a Gemini-specific version created.

## Summary
The Gemini CLI uses **TOML files** for custom commands, distinctly different from the Markdown format used by Claude and Codex. To achieve parity, we must create a new `gemini/commands/` directory and convert each existing Markdown command into a corresponding TOML file.

## Findings

### Command Format: Markdown vs. TOML
*   **Claude/Codex:** Markdown files (`cmd:example.md`) with YAML front-matter. Arguments use `$ARGUMENTS`.
*   **Gemini:** TOML files (`cmd:example.toml`). Arguments use `{{args}}`.

#### Example Conversion

**Source (Claude Markdown):**
```markdown
---
description: Commit all changes
argument-hint: [Commit message]
---
# Commit Instructions
...
```

**Target (Gemini TOML):**
```toml
description = "Commit all changes"
prompt = """
# Commit Instructions
...
"""
```

### Directory Structure
A new directory structure `gemini/commands/` is required in the repository root to house these source files. The `install.sh` script will need to be updated to copy these files to `~/.gemini/commands/` or `.gemini/commands/`.

### Inventory of Commands to Port
The following 41 commands (19 core + 22 HL) need to be converted from `claude/commands/` to `gemini/commands/`.

**Core Commands:**
| Command Name | Source File | Notes |
| :--- | :--- | :--- |
| `3:process-tasks` | `3:process-tasks.md` | Adapts autonomous logic |
| `cmd:commit-push` | `cmd:commit-push.md` | |
| `cmd:create-handoff` | `cmd:create-handoff.md` | |
| `cmd:create-pr` | `cmd:create-pr.md` | |
| `cmd:debug` | `cmd:debug.md` | |
| `cmd:graduate` | `cmd:graduate.md` | |
| `cmd:local-review` | `cmd:local-review.md` | |
| `cmd:research` | `cmd:research.md` | |
| `cmd:resume-handoff` | `cmd:resume-handoff.md` | |
| `cmd:start-linear-issue` | `cmd:start-linear-issue.md` | |
| `cmd:validate` | `cmd:validate.md` | |
| `doc:fetch` | `doc:fetch.md` | |
| `doc:fetch-batch` | `doc:fetch-batch.md` | |
| `doc:update` | `doc:update.md` | |
| `prd:1:create-prd` | `prd:1:create-prd.md` | |
| `prd:2:gen-tasks` | `prd:2:gen-tasks.md` | |
| `simplify:1:create-plan` | `simplify:1:create-plan.md` | |
| `simplify:2:process-plan` | `simplify:2:process-plan.md` | |
| `spec:1:create-spec` | `spec:1:create-spec.md` | |
| `spec:2:gen-tasks` | `spec:2:gen-tasks.md` | |

**HL (HumanLayer) Commands:**
| Command Name | Source File | Target Name |
| :--- | :--- | :--- |
| `hl/ci_commit` | `hl/ci_commit.md` | `hl:ci_commit` |
| `hl/ci_describe_pr` | `hl/ci_describe_pr.md` | `hl:ci_describe_pr` |
| `hl/commit` | `hl/commit.md` | `hl:commit` |
| `hl/create_handoff` | `hl/create_handoff.md` | `hl:create_handoff` |
| `hl/create_plan` | `hl/create_plan.md` | `hl:create_plan` |
| `hl/create_plan_generic` | `hl/create_plan_generic.md` | `hl:create_plan_generic` |
| `hl/create_plan_nt` | `hl/create_plan_nt.md` | `hl:create_plan_nt` |
| `hl/create_worktree` | `hl/create_worktree.md` | `hl:create_worktree` |
| `hl/debug` | `hl/debug.md` | `hl:debug` |
| `hl/describe_pr` | `hl/describe_pr.md` | `hl:describe_pr` |
| `hl/describe_pr_nt` | `hl/describe_pr_nt.md` | `hl:describe_pr_nt` |
| `hl/founder_mode` | `hl/founder_mode.md` | `hl:founder_mode` |
| `hl/implement_plan` | `hl/implement_plan.md` | `hl:implement_plan` |
| `hl/iterate_plan` | `hl/iterate_plan.md` | `hl:iterate_plan` |
| `hl/iterate_plan_nt` | `hl/iterate_plan_nt.md` | `hl:iterate_plan_nt` |
| `hl/linear` | `hl/linear.md` | `hl:linear` |
| `hl/local_review` | `hl/local_review.md` | `hl:local_review` |
| `hl/research_codebase` | `hl/research_codebase.md` | `hl:research_codebase` |
| `hl/research_codebase_generic` | `hl/research_codebase_generic.md` | `hl:research_codebase_generic` |
| `hl/research_codebase_nt` | `hl/research_codebase_nt.md` | `hl:research_codebase_nt` |
| `hl/resume_handoff` | `hl/resume_handoff.md` | `hl:resume_handoff` |
| `hl/validate_plan` | `hl/validate_plan.md` | `hl:validate_plan` |

### Agent Strategy (Personas)
Gemini does not support native agent definition files like Claude. We will define the following agents as **Personas** within `gemini/GEMINI.template.md`, which will be installed as `GEMINI.md` in the target project.

**Personas to be included (from `claude/agents/*.md`):**
1.  **`@developer-fidelity`**: Implements specifications with absolute fidelity.
2.  **`@quality-reviewer-fidelity`**: Ensures code matches specs exactly without scope creep.
3.  **`@developer`**: Standard developer.
4.  **`@quality-reviewer`**: Standard quality reviewer.
5.  **`@technical-writer`**: For documentation updates.
6.  **`@simplify-planner`**: For code simplification.
7.  **`@debugger`**: For evidence-driven debugging.
8.  **`@codebase-analyzer`**: HL research agent.
9.  **`@codebase-locator`**: HL research agent.
10. **`@codebase-pattern-finder`**: HL research agent.
11. **`@thoughts-analyzer`**: HL research agent.
12. **`@thoughts-locator`**: HL research agent.
13. **`@web-search-researcher`**: HL research agent.
14. **`@worktree-creator`**: HL agent.
15. **`@fidelity-reviewer`**: HL agent.

These personas will be defined in a `## Available Personas` section in the template, copying the content from their respective files in `claude/agents/`.

### Installation Logic (`install.sh`)

The `install.sh` script will be updated to include a `install_gemini()` function and support the `--gemini` flag.

**Installation Steps:**
1.  **Flag Parsing:** Add `--gemini` to the argument parser.
2.  **Target Directory:** Determine installation target (`.gemini` in project root or `~/.gemini` if global is implied/requested).
3.  **Commands:**
    *   Create target directory: `mkdir -p <target>/commands`.
    *   Copy all `.toml` files from `gemini/commands/` to `<target>/commands/`.
4.  **Context File (`GEMINI.md`):**
    *   If installing to a project (not global):
        *   Check for `GEMINI.md` in project root.
        *   If missing, copy `gemini/GEMINI.template.md` to `GEMINI.md`.
        *   (Optional but recommended) If `GEMINI.md` exists, append missing sections (Personas, ltui guidance) similar to how `AGENTS.md` is handled for Codex.
5.  **Settings:**
    *   If `gemini/settings.json` exists, copy/merge it to `<target>/settings.json`.

## Open Questions
- **Shell Execution:** Gemini supports `!{command}`. We should verify if any Claude commands rely heavily on the `Bash` tool and if they can be optimized using Gemini's native shell syntax.

## Next Steps
Proceed with creating the `gemini/` directory and converting the commands.
