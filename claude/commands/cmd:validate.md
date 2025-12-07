---
description: Post-implementation verification against plan
argument-hint: [plan file path]
---

# Validate Implementation

Verify that an implementation plan was correctly executed. This provides independent verification after implementation.

Plan file: $ARGUMENTS

## Process

### 1. Locate and Read Plan

If no argument provided, search `thoughts/plans/` for recent task lists.

Read the plan file completely. Extract:
- All tasks and subtasks
- Success criteria (automated and manual)
- Files expected to be modified
- Expected behaviors

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

### 3. Verify Each Phase

For each phase in the plan:

1. **Check Completion Status**
   - Are all checkboxes marked?
   - Were any tasks skipped?

2. **Run Automated Verification**
   - Execute any test commands from success criteria
   - Run linting/type checking
   - Verify build passes

3. **Assess Code Changes**
   - Do the files mentioned exist?
   - Do changes match what was planned?
   - Are there unexpected changes?

4. **Evaluate Manual Criteria**
   - List manual verification items
   - Note which require user testing

### 4. Generate Validation Report

Create document at: `thoughts/validation/YYYY-MM-DD-description.md`

```markdown
---
date: [ISO timestamp]
author: [claude]
git_commit: [Commit hash]
branch: [Branch name]
type: validation
status: [pass|fail|partial]
plan_file: [Path to validated plan]
---

# Validation Report: [Plan Name]

## Plan Reference
`[Path to plan file]`

## Validation Summary

| Phase | Status | Notes |
|-------|--------|-------|
| 1.0 [Name] | [pass/fail] | [Brief note] |
| 2.0 [Name] | [pass/fail] | [Brief note] |

**Overall Status**: [PASS / FAIL / PARTIAL]

## Detailed Findings

### Phase 1: [Name]

**Planned:**
- Task 1.1: [Description]
- Task 1.2: [Description]

**Actual:**
- Task 1.1: [Completed/Not completed] - [Evidence]
- Task 1.2: [Completed/Not completed] - [Evidence]

**Automated Verification:**
- [ ] Tests pass: [output]
- [ ] Build succeeds: [output]
- [ ] Lint passes: [output]

### Phase 2: [Name]
...

## Deviations

### Matches (Plan vs Actual)
- [What matched expectations]

### Deviations
- [What differed from plan]
- [Reason if known]

### Unexpected Changes
- [Changes not in plan]

## Manual Verification Required

The following require manual testing:
- [ ] [Manual test item 1]
- [ ] [Manual test item 2]

## Potential Issues

[Edge cases or regressions to watch for]

## Recommendations

[Next steps based on findings]
```

### 5. Present Report

Present findings to user:
- Overall pass/fail status
- Key deviations found
- Manual tests needed
- Recommendations

## Think Harder

When validating:
- Consider edge cases the plan might have missed
- Look for regressions in related code
- Check for incomplete implementations
- Verify error handling exists
- Consider security implications

## Output

Report saved to: `thoughts/validation/YYYY-MM-DD-[plan-name].md`
