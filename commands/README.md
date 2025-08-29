# Command Workflow Documentation

## Overview

This directory contains three interconnected commands that work together to support a complete development workflow from requirements to implementation:

1. **`user:create-prd.md`** - Creates Product Requirements Documents
2. **`user:research-to-execution.md`** - Converts source documents into execution plans  
3. **`user:process-tasks.md`** - Processes and executes task lists

## Command Relationships

### Workflow 1: PRD-Based Development
```
user:create-prd → user:process-tasks
```
- Create a PRD for a feature
- Process the PRD tasks directly using `user:process-tasks`

### Workflow 2: Research-Driven Development
```
[Research Document] → user:research-to-execution → user:process-tasks
```
- Start with a comprehensive research document (strategy, architecture, technical analysis)
- Convert to rich execution plan using `user:research-to-execution`
- Process the execution plan using `user:process-tasks`

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

**`user:create-prd`**: 
- New feature development
- Clear, scoped requirements
- Junior developer implementation

**`user:research-to-execution`**:
- Complex technical implementations
- Architecture-heavy projects
- Need for context preservation
- Multi-phase development

**`user:process-tasks`**:
- Any task list execution
- Both simple and complex plans
- Requires git branch (not main)
- Supports `NOSUBCONF` for batch processing

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