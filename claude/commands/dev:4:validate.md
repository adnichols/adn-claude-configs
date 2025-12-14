---
description: Post-implementation verification against task list
argument-hint: [task file path]
---

# Validate Implementation

Verify that a task list was correctly executed. This provides independent verification after implementation.

Task file: $ARGUMENTS

## Process

### 1. Locate and Read Task List

If no argument provided, use the current active task list or search `thoughts/` for the most recent `task.md`.

Read the task file completely. Extract:
- All tasks and subtasks (items starting with `- [ ]` or `- [x]`)
- Any context or requirements blocks
- "Relevant Files" if listed

### 2. Gather Implementation Evidence

Run verification commands:

```bash
# Git history for changes
git log --oneline -20
git diff --stat HEAD~10

# Check for test results
# (Run project-specific test commands from CLAUDE.md)

# Check for build success
# (Run project-specific build commands from CLAUDE.md)
```

### 3. Verify Tasks

For each top-level task in the list:

1. **Check Completion Status**
   - Is the task marked as completed (`[x]`)?
   - Are all subtasks completed?

2. **Verify Deliverables**
   - If the task implies creating code, does that code exist?
   - If the task implies a fix, is there a regression test?

3. **Run Automated Verification**
   - Execute relevant tests
   - Verify build passes

4. **Assess Scope**
   - Did the implementation stay within the scope of the task?
   - Are there unrequested changes?

### Parallel Verification Strategy

Use the Task tool to spawn parallel verification subagents for efficient task-by-task validation.

#### Subagent Delegation

For each major task/phase, spawn a Task agent with `subagent_type=Explore`:

```
Task: Verify Phase [N] - [Phase Name]
- Check all subtasks marked complete
- Verify code changes exist for specified files
- Run relevant tests for this phase
- Confirm implementation matches spec requirements
- Report: status, evidence, issues found
```

#### Orchestrator Responsibilities

The parent agent (you) handles:
- Running global verification commands (build, lint)
- Coordinating per-phase verification subagents  
- Synthesizing individual reports into final validation
- Generating the validation report document

Wait for ALL verification subagents to complete before synthesizing the final report.

### 4. Generate Validation Report

Create document at: `thoughts/validation/YYYY-MM-DD-validation.md`

```markdown
---
date: [ISO timestamp]
author: [claude]
git_commit: [Commit hash]
type: validation
status: [pass|fail|partial]
task_file: [Path to validated task file]
---

# Validation Report

## Source Task List
`[Path to task file]`

## Validation Summary

| Task | Status | Notes |
|------|--------|-------|
| [Task Name] | [pass/fail] | [Brief note] |
| [Task Name] | [pass/fail] | [Brief note] |

**Overall Status**: [PASS / FAIL / PARTIAL]

## Detailed Findings

### [Task Name]

**Status:** [Completed/Incomplete]

**Verification:**
- [ ] Task marked complete
- [ ] Requirements met
- [ ] Tests pass

**Evidence:**
- [Cite file changes or logs]

### [Task Name]
...

## Deviations & Issues

### Unexpected Changes
- [Changes not in task list]

### Missing Items
- [Tasks marked complete but missing evidence]

## Manual Verification Required
- [ ] [Item 1]

## Recommendations
[Next steps]
```

### 5. Present Report

Present findings to user:
- Overall pass/fail status
- Key deviations found
- Manual tests needed
