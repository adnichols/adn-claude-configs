# Codex Prompts Documentation

## Overview

This directory contains a comprehensive set of prompts organized by workflow category. The structure mirrors the Claude Code commands layout for consistency across tools.

## Naming & Layout

```
codex/prompts/
├── README.md                    # This file
├── _lib/                        # Internal library scripts shared by prompts
│   └── scripts/
│       ├── docs-fetch.py
│       ├── docs-fetch-batch.py
│       ├── markdown-converter.py
│       └── site-patterns.json
├── cmd:commit-push.md           # Git helper (cmd namespace)
├── cmd:create-pr.md             # Git helper (cmd namespace)
├── doc:fetch.md                 # Documentation fetch command
├── doc:update.md                # Documentation update command
├── prd:1:create-prd.md          # PRD workflow (step 1)
├── prd:2:gen-tasks.md           # PRD workflow (step 2)
├── prd:3:process-tasks.md       # PRD workflow (step 3)
├── spec:1:create-spec.md        # Specification workflow (step 1)
├── spec:2:gen-tasks.md          # Specification workflow (step 2)
├── spec:3:process-tasks.md      # Specification workflow (step 3)
├── simplify:1:create-plan.md    # Simplification workflow (step 1)
└── simplify:2:process-plan.md   # Simplification workflow (step 2)
```

> 📌 Codex only indexes prompt files that live directly under `~/.codex/prompts` (or a project-level `.codex/prompts`).
> To preserve category structure without folders we encode namespaces, phases, and steps directly in the filename using colon-delimited segments.

## Available Prompts by Category

### Command Operations (`cmd:*`)
- **`cmd:commit-push`** - Commit and push changes to repository
- **`cmd:create-pr`** - Create pull request with changelog
- **`cmd:start-linear-issue`** - Bootstrap a worktree/branch with local config for a Linear issue
- **`cmd:auto-linear-issue`** - Setup worktree and autonomously implement, test, and ship the Linear issue

### Documentation (`doc:*`)
- **`doc:fetch`** - Fetch documentation for a single library/framework
- **`doc:fetch-batch`** - Batch fetch documentation from markdown lists
- **`doc:update`** - Update documentation after feature completion

### PRD Workflow (`prd:*`)
1. **`prd:1:create-prd`** - Create Product Requirements Documents from scratch
2. **`prd:2:gen-tasks`** - Convert PRDs to executable task lists
3. **`prd:3:process-tasks`** - Process and execute PRD-based tasks

### Specification Workflow (`spec:*`)
1. **`spec:1:create-spec`** - Research and generate technical specifications
2. **`spec:2:gen-tasks`** - Convert specs to executable task lists
3. **`spec:3:process-tasks`** - Process and execute spec-based tasks

### Code Simplification (`simplify:*`)
1. **`simplify:1:create-plan`** - Analyze code for simplification opportunities
2. **`simplify:2:process-plan`** - Execute approved simplification plans

### Quality Assurance (`qa:*`)
- **`qa:bug-hunt-linear`** - Identify top-priority visual/UX bugs from recent changes and log them directly to Linear

## Command Relationships

### Workflow 1: PRD-Based Development (Fidelity-Preserving)
```
prd:1:create-prd → prd:2:gen-tasks → prd:3:process-tasks → doc:update
```
- Create a PRD for a feature with exact scope preservation
- Generate task list using `prd:2:gen-tasks` with fidelity-preserving approach
- Process tasks using `prd:3:process-tasks` with fidelity agents
- Generate documentation after implementation using `doc:update`

### Workflow 2: Specification-Driven Development
```
spec:1:create-spec → spec:2:gen-tasks → spec:3:process-tasks → doc:update
```
- Start with research and generate technical specification
- Convert specification to executable tasks (preserves 100% fidelity)
- Process tasks using `spec:3:process-tasks` with fidelity-preserving agents
- Document the completed implementation

### Workflow 3: Code Simplification
```
simplify:1:create-plan → [Review/Approval] → simplify:2:process-plan
```
- Analyze codebase for simplification opportunities using `simplify:1:create-plan`
- Get approval for changes from quality-reviewer or stakeholders
- Execute the approved simplification plan using `simplify:2:process-plan`

### Workflow 4: Documentation Management
```
doc:fetch → [Development] → doc:update
```
- Fetch documentation for libraries/frameworks using `doc:fetch` or `doc:fetch-batch`
- Complete feature development
- Update project documentation using `doc:update`

## Key Features

### Fidelity-Preserving Approach
All commands now follow strict fidelity preservation:
- **Exact Scope Implementation**: Build only what's specified in source documents
- **No Scope Creep**: Zero additions beyond explicit requirements
- **Fidelity Agents**: Always use developer-fidelity and quality-reviewer-fidelity
- **Question Ambiguity**: Ask for clarification rather than making assumptions

### Standardized Format
All commands use consistent:
- **Phase Structure**: `Phase N: [Name] (Timeframe)`
- **Task Format**: `N.0 [Parent]` → `N.1, N.2, N.3 [Sub-tasks]`
- **Commit Messages**: `git commit -m "feat: [summary]" -m "Related to Phase X.Y"`

### Enhanced Capabilities
- Git branch management
- Test suite integration (only as specified)
- Context-aware implementation
- Scope boundary enforcement
- Progress tracking and validation

## Usage Guidelines

### When to Use Each Prompt

**`prd:1:create-prd`**:
- New feature development from scratch
- Clear, scoped requirements
- Need to ask clarifying questions about requirements
- Want exact scope preservation

**`prd:2:gen-tasks`**:
- Converting PRDs to actionable development tasks with fidelity preservation
- Creating task lists that implement only specified requirements
- Using fidelity-preserving agents
- No scope expansion or assumptions beyond PRD content

**`prd:3:process-tasks`**:
- Execute PRD-based task lists
- Uses fidelity-preserving agents for implementation
- Requires git branch (not main)
- Implements only what's specified in PRD

**`spec:1:create-spec`**:
- Complex technical implementations
- Architecture-heavy projects
- Need for research and context gathering
- Generating detailed specifications

**`spec:2:gen-tasks`**:
- Convert specifications to executable tasks
- Absolute fidelity preservation - no scope changes or additions
- Direct conversion from spec to tasks
- Uses fidelity-preserving agents

**`spec:3:process-tasks`**:
- Execute specification-based task lists
- Uses fidelity-preserving agents for implementation
- Requires git branch (not main)
- Supports `NOSUBCONF` for batch processing

**`doc:fetch`**:
- Fetch documentation for a single library/framework
- AI-friendly markdown format
- Stored in project docs directory

**`doc:fetch-batch`**:
- Batch fetch documentation from markdown lists
- Process multiple libraries at once
- Supports parallel processing

**`doc:update`**:
- Post-implementation documentation
- User guides and technical references
- API documentation generation
- After feature completion

**`simplify:1:create-plan`** & **`simplify:2:process-plan`**:
- Code complexity reduction
- Technical debt management
- Refactoring legacy systems
- Performance optimization through simplification

**`cmd:commit-push`**:
- Commit all changes and push to remote
- Simple git workflow automation

**`cmd:create-pr`**:
- Create pull request with changelog
- Automated PR creation

## Fidelity-Preserving Agents

### developer-fidelity
- Implements EXACTLY what's specified in source documents
- Adds NO tests, security, or features beyond specification requirements
- Questions ambiguity rather than making assumptions
- Used by `plan:spec-to-tasks` workflow

### quality-reviewer-fidelity  
- Reviews implementation against specification requirements ONLY
- Does NOT require additional security, testing, or compliance beyond specification
- Validates fidelity preservation and prevents scope creep
- Used by `plan:spec-to-tasks` workflow

### Best Practices

1. **Always work on feature branches** (not main)
2. **One sub-task at a time** unless `NOSUBCONF` specified
3. **Test before commit** - all commands enforce test passing
4. **Context preservation** - rich execution plans maintain full context
5. **Progress tracking** - regular task list updates required

## File Outputs

- **PRDs**: `/tasks/prd-[feature-name].md`
- **Execution Plans**: `/tasks/tasks-execution-[source-name].md`
- **Task Processing**: Updates existing task files in place

## Integration Notes

All commands integrate with:
- Git workflow and branching
- Test commands from `TESTING.md` or `CLAUDE.md`
- Conventional commit formatting
- Security and performance validation (where applicable)
