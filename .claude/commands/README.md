# Command Workflow Documentation

## Overview

This directory contains a comprehensive set of commands that support a complete development workflow from requirements to implementation and quality assurance:

### Core Build Commands
1. **`build:create-prd.md`** - Creates Product Requirements Documents
2. **`build:exec-spec.md`** - Converts source documents into execution plans  
3. **`build:generate-tasks.md`** - Generates task lists from specifications
4. **`build:process-tasks.md`** - Processes and executes task lists
5. **`build:review.md`** - Pre-PR quality reviews and validation
6. **`build:document.md`** - Post-implementation documentation generation

### Simplification Commands
7. **`simplify:create-plan.md`** - Analyzes code for simplification opportunities
8. **`simplify:process-plan.md`** - Executes approved simplification plans

## Command Relationships

### Workflow 1: PRD-Based Development
```
build:create-prd → build:process-tasks → build:review → build:document
```
- Create a PRD for a feature
- Process the PRD tasks directly using `build:process-tasks`
- Review code quality before PR using `build:review`
- Generate documentation after implementation using `build:document`

### Workflow 2: Research-Driven Development
```
[Research Document] → build:exec-spec → build:process-tasks → build:review → build:document
```
- Start with a comprehensive research document (strategy, architecture, technical analysis)
- Convert to rich execution plan using `build:exec-spec`
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

### Standardized Format
All commands use consistent:
- **Phase Structure**: `Phase N: [Name] (Timeframe)`
- **Task Format**: `N.0 [Parent]` → `N.1, N.2, N.3 [Sub-tasks]`
- **Commit Messages**: `git commit -m "feat: [summary]" -m "Related to Phase X.Y"`

### Context Handling
- **Simple Tasks**: Basic task lists from PRDs
- **Rich Context**: Full context preservation from research documents
- **Unified Processing**: Single `process-tasks` command handles both

### Enhanced Capabilities
- Git branch management
- Test suite integration
- Context-aware implementation
- Security and performance consideration
- Progress tracking and validation

## Usage Guidelines

### When to Use Each Command

**`build:create-prd`**: 
- New feature development
- Clear, scoped requirements
- Junior developer implementation

**`build:exec-spec`**:
- Complex technical implementations
- Architecture-heavy projects
- Need for context preservation
- Multi-phase development

**`build:generate-tasks`**:
- Breaking down large specifications
- Creating structured task lists from complex requirements
- Converting PRDs to actionable development tasks

**`build:process-tasks`**:
- Any task list execution
- Both simple and complex plans
- Requires git branch (not main)
- Supports `NOSUBCONF` for batch processing

**`build:review`**:
- Pre-PR quality validation
- Security and performance checks
- Code quality assessment
- Production readiness verification

**`build:document`**:
- Post-implementation documentation
- User guides and technical references
- API documentation generation
- After feature completion

**`simplify:create-plan`** & **`simplify:process-plan`**:
- Code complexity reduction
- Technical debt management
- Refactoring legacy systems
- Performance optimization through simplification

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