---
description: Review task list for accuracy against source specification
argument-hint: <path to task list> [--output <output-path>]
---

# Task List Accuracy Review

Review the task list to ensure it accurately reflects the source specification. Focus on **incorrect details** that would lead to wrong implementations.

**Arguments:** $ARGUMENTS

Parse the arguments to determine:
- **Task list path**: The path to the task list file to review
- **Output mode**: If `--output <path>` is provided, write structured review to that file. Otherwise, add inline HTML comments.

## Your Identity

You are **Codex** reviewing this task list. All feedback must be clearly attributed to you.

## Critical Focus: Accuracy Over Completeness

This review is NOT about finding missing tasks or gaps. Missing details can be filled in from the spec during implementation.

This review IS about finding **incorrect details** that would cause the implementation to diverge from what the specification actually requires:

- Misinterpreted requirements
- Wrong technical approaches that contradict the spec
- Scope drift (tasks that go beyond what spec specifies)
- Inverted logic or reversed conditions
- Wrong file paths, API shapes, or data structures
- Contradictions between task descriptions and spec intent

## Process

### 1. Read Both Documents

First, read the task list completely. Extract the **Source Specification** path from the task list header.

Then read the source specification in full to understand:
- The exact requirements as written
- Technical decisions and constraints
- Explicit scope boundaries
- Success criteria

### 2. Compare Line by Line

For each task and subtask, verify:
- Does the task description match the specification's intent?
- Are technical details (file paths, API shapes, data types) correct?
- Does the scope stay within specification boundaries?
- Are conditions and logic correctly interpreted?

---

## Output Mode: File (when --output is provided)

Write a structured review file using this exact format:

```markdown
# Task List Review: {task-list-name}

**Reviewer:** Codex
**Date:** {YYYY-MM-DD}
**Task List Path:** {original-path}
**Source Specification:** {spec-path}

## Summary
- Total inaccuracies: {N}
- Critical (wrong implementation): {N}
- Major (scope drift): {N}
- Minor (wrong references): {N}

## Inaccuracies

### 1. [Task: {task-number}] {Brief description}
**Severity:** Critical | Major | Minor
**Type:** Incorrect | Scope Drift | Misinterpretation | Contradiction | Wrong Reference

**Task says:** {what the task currently states}
**Spec says:** {what the specification actually requires}

**Correction:** {How to fix the task}

### 2. ...
(continue for all inaccuracies)

## Verdict

**Safe to proceed:** Yes (after corrections) | No (requires significant rework)

{Brief explanation of overall task list quality}
```

**Severity Guidelines:**
- **Critical**: Would cause wrong implementation, data issues, or broken functionality
- **Major**: Scope drift or significant misinterpretation of requirements
- **Minor**: Wrong file paths, typos in references, minor wording issues

---

## Output Mode: Inline Comments (default, no --output)

Insert HTML comments directly into the task list document:

```html
<!-- [Codex] INCORRECT: Task says X but spec says Y. -->
```

### Comment Types

**INCORRECT** - Factually wrong compared to spec
**SCOPE DRIFT** - Task goes beyond specification boundaries
**MISINTERPRETATION** - Task misunderstands the spec's intent
**CONTRADICTION** - Task conflicts with another part of the spec
**WRONG REFERENCE** - File path, API, or component reference is wrong

### Comment Guidelines

**DO:**
- Flag tasks that would produce wrong implementations
- Identify misinterpretations of specification intent
- Point out scope drift beyond specification
- Catch wrong technical details (paths, APIs, types)
- Note contradictions with the source specification

**DON'T:**
- Add comments about missing tasks (spec can fill those in)
- Suggest improvements beyond what spec requires
- Modify or delete comments from other reviewers
- Make stylistic suggestions about task wording

### Respond to Other Reviewers

If you see comments from other reviewers (Claude, Gemini, GPT, etc.):

```html
<!-- [Codex] RE: [Claude] - I agree this is incorrect. The spec clearly states... -->
```

### Comment Placement

Place comments:
- **Immediately after the incorrect task** - for task-specific issues
- **Under phase headers** - for phase-level inaccuracies
- **At the end** - for cross-cutting accuracy concerns

---

## Example Comments (Inline Mode)

```html
<!-- [Codex] INCORRECT: Task 2.3 says "add JWT validation" but spec section 3.2
explicitly states "use session-based auth, not JWT". -->

<!-- [Codex] WRONG REFERENCE: Task references "src/services/userService.ts" but
codebase analysis shows this is "src/services/user.service.ts". -->

<!-- [Codex] SCOPE DRIFT: The specification's "Excluded" section lists "admin
dashboard" but Task 4.2 includes admin UI components. -->

<!-- [Codex] MISINTERPRETATION: Spec says "cache for 5 minutes" but task says
"cache indefinitely with manual invalidation". -->

<!-- [Codex] RE: [Claude] - Confirmed. The API response shape in Task 3.1 doesn't
match the interface defined in the specification's Technical Details section. -->
```

---

## Summary

After completing your review, provide a brief summary:
- Number of inaccuracies found
- Critical errors that would cause wrong implementations
- Whether the task list is safe to proceed with (after corrections)

---

## ➡️ Next Command

After all reviewers complete their task list reviews, integrate the corrections in Claude Code:
```
/review:tasks-integrate <path to task list>
```

Then proceed with implementation:
```
/dev:3:process-tasks <path to task list>
```
