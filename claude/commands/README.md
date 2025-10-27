# Command Workflow Documentation

## Overview

This directory contains a comprehensive set of commands that support a complete development workflow from requirements to implementation and quality assurance:

### Core Build Commands
1. **`plan:create-prd.md`** - Creates Product Requirements Documents from scratch
2. **`plan:spec-to-tasks.md`** - Converts specifications directly to executable tasks (full fidelity)
3. **`plan:generate-tasks-from-spec.md`** - Converts source documents into execution plans  
4. **`plan:generate-tasks.md`** - Generates task lists from specifications
5. **`build:process-tasks.md`** - Processes and executes task lists
6. **`plan:review.md`** - Pre-PR quality reviews and validation
7. **`docs:update.md`** - Post-implementation documentation generation

### Simplification Commands
8. **`simplify:create-plan.md`** - Analyzes code for simplification opportunities
9. **`simplify:process-plan.md`** - Executes approved simplification plans

## Command Relationships

### Workflow 1: PRD-Based Development (Fidelity-Preserving)
```
plan:create-prd → plan:gen-tasks → build:process-tasks → plan:review → docs:update
```
- Create a PRD for a feature with exact scope preservation
- Generate task list using `plan:gen-tasks` with fidelity-preserving approach
- Process tasks using `build:process-tasks` with fidelity agents
- Review code quality before PR using `plan:review`
- Generate documentation after implementation using `docs:update`

### Workflow 1a: Full-Fidelity Specification Development
```
[Collaborative Spec] → plan:spec-to-tasks → build:process-tasks → plan:review → docs:update
```
- Start with detailed specification created through collaborative planning (Claude/Gemini/ChatGPT)
- Convert specification directly to executable tasks using `plan:spec-to-tasks` (preserves 100% fidelity)
- Process tasks using `build:process-tasks` with fidelity-preserving agents
- Review and document the completed implementation

### Workflow 2: Research-Driven Development
```
[Research Document] → plan:generate-tasks-from-spec → build:process-tasks → plan:review → docs:update
```
- Start with a comprehensive research document (strategy, architecture, technical analysis)
- Convert to rich execution plan using `plan:generate-tasks-from-spec`
- Process the execution plan using `build:process-tasks`
- Review and document the completed implementation

### Workflow 3: Code Simplification
```
simplify:create-plan → [Review/Approval] → simplify:process-plan
```
- Analyze codebase for simplification opportunities
- Get approval for changes from quality-reviewer or stakeholders
- Execute the approved simplification plan

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

### When to Use Each Command

**`plan:create-prd`**: 
- New feature development from scratch
- Clear, scoped requirements
- Junior developer implementation
- Need to ask clarifying questions about requirements

**`plan:spec-to-tasks`**:
- Detailed specifications from collaborative planning (Claude/Gemini/ChatGPT)
- Direct conversion to executable tasks (no PRD intermediate step)
- Absolute fidelity preservation - no scope changes or additions
- Uses fidelity-preserving agents (developer-fidelity, quality-reviewer-fidelity)

**`plan:generate-tasks-from-spec`**:
- Complex technical implementations
- Architecture-heavy projects
- Need for context preservation
- Multi-phase development

**`plan:gen-tasks`**:
- Converting PRDs to actionable development tasks with fidelity preservation
- Creating task lists that implement only specified requirements
- Using developer-fidelity and quality-reviewer-fidelity agents
- No scope expansion or assumptions beyond PRD content

**`build:process-tasks`**:
- Any task list execution with fidelity preservation
- Uses fidelity-preserving agents for implementation
- Requires git branch (not main)
- Supports `NOSUBCONF` for batch processing
- Implements only what's specified in source documents

**`plan:review`**:
- Pre-PR quality validation
- Security and performance checks
- Code quality assessment
- Production readiness verification

**`docs:update`**:
- Post-implementation documentation
- User guides and technical references
- API documentation generation
- After feature completion

**`simplify:create-plan`** & **`simplify:process-plan`**:
- Code complexity reduction
- Technical debt management
- Refactoring legacy systems
- Performance optimization through simplification

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