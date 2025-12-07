---
date: 2025-12-07T21:18:39Z
author: claude
git_commit: 585872a4dd971d2acb9b590569fb79eac186cfd6
branch: main
repository: adn-claude-configs
type: research
status: complete
tags: [subagents, context-preservation, humanlayer, claude-code, commands, agents]
last_updated: 2025-12-07
---

# Research: Sub-Agent Integration from humanlayer/.claude Configuration

## Research Question

How to integrate the sub-agents used in the `~/code/humanlayer/.claude` configuration into adn-claude-configs commands, specifically for research workflows. The goal is to utilize sub-agents within Claude Code where possible to preserve context in the main orchestration agent when researching, planning, and executing work.

## Summary

The humanlayer project has a sophisticated sub-agent system with 6 specialized agents designed for context preservation. These agents are purpose-built for specific tasks (locating files, analyzing code, finding patterns, searching thoughts, web research) and are invoked via Claude Code's `subagent_type` parameter in Task tool calls. The current adn-claude-configs uses a generic `subagent_type=Explore` approach, which could be enhanced with these specialized agents.

## Detailed Findings

### Humanlayer Sub-Agent Architecture

**Location:** `~/code/humanlayer/.claude/agents/`

The humanlayer project defines 6 specialized sub-agents:

| Agent | Purpose | Tools | Model |
|-------|---------|-------|-------|
| `codebase-locator` | Find WHERE files/components live | Grep, Glob, LS | sonnet |
| `codebase-analyzer` | Understand HOW specific code works | Read, Grep, Glob, LS | sonnet |
| `codebase-pattern-finder` | Find similar implementations/patterns | Grep, Glob, Read, LS | sonnet |
| `thoughts-locator` | Discover relevant documents in thoughts/ | Grep, Glob, LS | sonnet |
| `thoughts-analyzer` | Extract HIGH-VALUE insights from docs | Read, Grep, Glob, LS | sonnet |
| `web-search-researcher` | Research web sources | WebSearch, WebFetch, TodoWrite, Read, Grep, Glob, LS | sonnet |

**Note:** The humanlayer commands also reference `linear-issue-reader` and `linear-searcher` agents, but these agent definitions don't exist in the agents/ directory. They are conceptual agents referenced in commands that need to be created.

### Agent Definition Format

Each agent is defined in a markdown file with YAML front-matter:

**Example from `codebase-locator.md` (lines 1-6):**
```yaml
---
name: codebase-locator
description: Locates files, directories, and components relevant to a feature or task. Call `codebase-locator` with human language prompt describing what you're looking for. Basically a "Super Grep/Glob/LS tool" — Use it if you find yourself desiring to use one of these tools more than once.
tools: Grep, Glob, LS
model: sonnet
---
```

**Key attributes:**
- `name`: Identifier used for `subagent_type` parameter
- `description`: Purpose and usage guidance
- `tools`: Comma-separated list of tools the agent can use
- `model`: Model to use (sonnet, opus, etc.)

### How Commands Invoke Sub-Agents

**From `research_codebase.md` (lines 46-72):**

Commands instruct the orchestrator to spawn sub-agents using the Task tool:

```markdown
**For codebase research:**
- Use the **codebase-locator** agent to find WHERE files and components live
- Use the **codebase-analyzer** agent to understand HOW specific code works
- Use the **codebase-pattern-finder** agent to find examples of existing patterns

**For thoughts directory:**
- Use the **thoughts-locator** agent to discover what documents exist about the topic
- Use the **thoughts-analyzer** agent to extract key insights from specific documents

**For web research (only if user explicitly asks):**
- Use the **web-search-researcher** agent for external documentation and resources
```

### Sub-Agent Usage Pattern

**From `research_codebase.md` (lines 66-72):**

```markdown
The key is to use these agents intelligently:
- Start with locator agents to find what exists
- Then use analyzer agents on the most promising findings to document how they work
- Run multiple agents in parallel when they're searching for different things
- Each agent knows its job - just tell it what you're looking for
- Don't write detailed prompts about HOW to search - the agents already know
- Remind agents they are documenting, not evaluating or improving
```

### Current adn-claude-configs Approach

**From `cmd:research.md` (lines 39-57):**

Currently uses generic `subagent_type=Explore`:

```markdown
### 3. Spawn Parallel Research Tasks

Use the Task tool with `subagent_type=Explore` to research different aspects concurrently:

Task: Find WHERE components live
- Search for file patterns
- Locate key modules and entry points

Task: Understand HOW code works
- Read specific implementations
- Trace data flow

Task: Find PATTERNS
- Look for similar implementations
- Document conventions used
```

### Current adn-claude-configs Agent Inventory

**Location:** `claude/agents/`

The repository currently has these agents (focused on implementation, not research):

| Agent | Purpose |
|-------|---------|
| `developer` | Standard implementation with tests |
| `developer-fidelity` | Exact specification adherence |
| `quality-reviewer` | Production issue detection |
| `quality-reviewer-fidelity` | Specification compliance review |
| `fidelity-reviewer` | Comprehensive fidelity validation |
| `debugger` | Systematic bug analysis |
| `simplify-planner` | Code complexity reduction |
| `technical-writer` | Documentation creation |

**Gap identified:** No research-focused sub-agents exist. All current agents are implementation or review focused.

### Sub-Agent Invocation via Task Tool

Claude Code's Task tool accepts a `subagent_type` parameter that maps to agent definitions. When invoked:

1. Claude Code reads the agent's `.md` file
2. Applies the `tools` restriction (agent can only use listed tools)
3. Applies the `model` specification
4. Injects the agent's prompt/instructions as system context
5. Executes the sub-task with that configuration

### Benefits of Specialized Sub-Agents

**Context Preservation:**
- Main orchestrator keeps minimal context (synthesis role)
- Sub-agents handle deep dives with their own context windows
- Results flow back as structured findings with file:line references

**Efficiency:**
- Parallel execution of multiple sub-agents
- Each agent optimized for specific task type
- Tools restricted to what's needed (prevents scope creep)

**Consistency:**
- Standardized output formats per agent type
- Consistent documentation style (no evaluations, just facts)
- Reusable across multiple commands

## Code References

### Humanlayer Files

- `~/code/humanlayer/.claude/agents/codebase-locator.md` - File/component locator
- `~/code/humanlayer/.claude/agents/codebase-analyzer.md` - Implementation analyzer
- `~/code/humanlayer/.claude/agents/codebase-pattern-finder.md` - Pattern/example finder
- `~/code/humanlayer/.claude/agents/thoughts-locator.md` - Document locator for thoughts/
- `~/code/humanlayer/.claude/agents/thoughts-analyzer.md` - Document insight extractor
- `~/code/humanlayer/.claude/agents/web-search-researcher.md` - Web research specialist
- `~/code/humanlayer/.claude/commands/research_codebase.md` - Research command using sub-agents
- `~/code/humanlayer/.claude/commands/create_plan.md` - Planning command using sub-agents

### adn-claude-configs Files

- `claude/commands/cmd:research.md` - Current research command (uses generic Explore)
- `claude/agents/` - Current agent definitions (8 implementation-focused agents)

## Architecture Documentation

### Humanlayer Sub-Agent Categories

1. **Locator Agents** (find things, don't read deeply)
   - `codebase-locator` - Find files/directories by topic
   - `thoughts-locator` - Find documents in thoughts/

2. **Analyzer Agents** (read and explain, don't evaluate)
   - `codebase-analyzer` - Understand implementation details
   - `thoughts-analyzer` - Extract key insights from documents

3. **Pattern Agents** (find examples and templates)
   - `codebase-pattern-finder` - Find similar implementations

4. **External Research Agents**
   - `web-search-researcher` - Web documentation and resources

### Key Design Principles

1. **Separation of Concerns**: Each agent has ONE job
2. **Tool Restrictions**: Agents only get tools they need
3. **Documentation Focus**: All agents document, never evaluate
4. **Structured Output**: Each agent has standardized output format
5. **Parallel Execution**: Multiple agents spawn concurrently

## Related Documents

- `thoughts/research/2025-12-07-cross-agent-command-portability.md` - Related research on cross-platform commands

## Integration Opportunities

To integrate humanlayer's sub-agent approach into adn-claude-configs:

### New Agents to Add

```
claude/agents/
├── codebase-locator.md       # Find WHERE files/components live
├── codebase-analyzer.md      # Understand HOW code works
├── codebase-pattern-finder.md # Find similar implementations
├── thoughts-locator.md       # Find documents in thoughts/ (plans, specs, handoffs, etc.)
├── thoughts-analyzer.md      # Extract insights from documents
├── web-researcher.md         # Web research specialist
├── linear-issue-reader.md   # Read and understand Linear issue details via ltui
└── linear-searcher.md        # Search for related Linear issues via ltui
```

### Commands to Update

1. **`cmd:research.md`** - Replace `subagent_type=Explore` with specialized agents
2. **`spec:1:create-spec.md`** - Add sub-agent usage for research phase
3. **`prd:1:create-prd.md`** - Add sub-agent usage for research phase
4. **New command: `cmd:create-plan.md`** - Planning command with sub-agents

### Usage Pattern Changes

Current pattern:
```markdown
Use the Task tool with `subagent_type=Explore` to research...
```

New pattern:
```markdown
Use specialized sub-agents:
- `subagent_type=codebase-locator` to find WHERE files live
- `subagent_type=codebase-analyzer` to understand HOW code works
- `subagent_type=codebase-pattern-finder` to find similar implementations
```

## Decisions Made

1. **Naming**: Keep `thoughts-locator` name. The `thoughts/` directory contains more than research - it includes plans, specs, handoffs, debug reports, validation reports, and other context documentation.

2. **Model Selection**: Prioritize accuracy over speed. Use `sonnet` for all agents. See analysis below for potential haiku candidates if cost/speed becomes a concern.

3. **Linear Integration**: Yes - add `linear-issue-reader` and `linear-searcher` agents for ltui integration.

## Model Selection Analysis

While accuracy is prioritized (use sonnet), here are candidates where haiku could work if cost/speed optimization is needed later:

### Good Haiku Candidates (Simple Pattern Matching)

| Agent | Why Haiku Could Work |
|-------|---------------------|
| `codebase-locator` | Only uses Grep/Glob/LS - pattern matching, no deep analysis |
| `thoughts-locator` | Same - just finding files by keyword, no interpretation |

These agents find WHERE things are, not WHAT they mean. They return file paths, not insights.

### Keep on Sonnet (Requires Understanding)

| Agent | Why Sonnet Needed |
|-------|------------------|
| `codebase-analyzer` | Must understand code logic, trace data flow, explain implementation |
| `codebase-pattern-finder` | Must recognize patterns, extract meaningful examples |
| `thoughts-analyzer` | Must extract key insights, filter noise, assess relevance |
| `web-researcher` | Must synthesize information from multiple sources |
| `linear-issue-reader` | Must understand ticket context and extract actionable info |
| `linear-searcher` | Could potentially use haiku for simple keyword search |

### Recommendation - ACCEPTED

Start with sonnet for all agents. If context/cost becomes an issue:
1. First candidate: `codebase-locator` → haiku (pure file discovery)
2. Second candidate: `thoughts-locator` → haiku (pure document discovery)
3. Keep all analyzers on sonnet

## All Questions Resolved

1. **Tool Restrictions**: The `tools` field is advisory only - a hint for the orchestrator, not enforced by the system.
