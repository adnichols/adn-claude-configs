---
description: Process tasks in a task list with fidelity-preserving approach
argument-hint: [Files]
---

# Instructions

Process the task list using the fidelity-preserving approach to maintain exact scope as specified in the source document. Implement only what's explicitly specified, without additions or scope expansions.

$ARGUMENTS

## CRITICAL: Orchestrator-Only Mode

**You (the parent session) are an ORCHESTRATOR, not an implementer.**

- **NEVER** implement features, fix bugs, or write code in bulk without verification
- **ALWAYS** work incrementally, one subtask at a time
- Your job is to coordinate, track progress, run validations, and manage git

## Fidelity Preservation Process

Before starting task implementation:

1. **Parse Task File Metadata:** Extract fidelity information from task file YAML front-matter
2. **Apply Only Specified Validation:** Include only the testing and validation explicitly specified in the source document

## Task Implementation Protocol

When processing tasks:

1. **Work one subtask at a time**
2. **After completing each subtask:**
   - Mark it as completed by changing `[ ]` to `[x]`
   - Confirm the update was successful
   - Request permission to proceed (unless NOSUBCONF specified)

## Critical Task Update Protocol

**MANDATORY CHECKPOINT SYSTEM:** After completing ANY subtask, follow this exact sequence:

1. **Declare completion:**
   "✅ Subtask [X.Y] [task name] completed.
   🔄 UPDATING MARKDOWN FILE NOW..."

2. **Immediately perform the markdown update:**
   - Change `- [ ] X.Y [task name]` to `- [x] X.Y [task name]`

3. **Confirm update completion:**
   "✅ Markdown file updated: [ ] → [x] for subtask X.Y
   📋 Task list is now current."

4. **Request permission to proceed (unless NOSUBCONF specified):**
   "Ready to proceed to next subtask. May I continue? (y/n)"

## Task Processing Rules

- Do not proceed with tasks unless you are on a git branch other than main
- If needed, create a branch for the phase of work you are implementing
- **One sub-task at a time:** Complete each subtask before starting the next
- **Completion protocol:**

  1. When a subtask is complete, immediately mark it as completed by changing `[ ]` to `[x]`

  2. If **all** subtasks underneath a parent task are now `[x]`, follow this sequence:

  - **First**: Run standard validation checks (lint, build, tests)
  - **Only if all validations pass**: Stage changes (`git add .`)
  - **Review**: Verify implementation matches specification
  - **Clean up**: Remove any temporary files before committing
  - **Commit**: Use a descriptive commit message with conventional commit format

  3. Once all subtasks are marked completed and changes committed, mark the **parent task** as completed

- Stop after each sub-task and wait for the user's go-ahead UNLESS NOSUBCONF is specified
- Always stop after parent tasks complete, run test suite, and commit changes

## Task List Maintenance

1. **Update the task list as you work:**

   - Mark tasks and subtasks as completed (`[x]`) per the protocol above
   - Add new tasks as they emerge

2. **Maintain the "Relevant Files" section:**

   - List every file created or modified during implementation
   - Update descriptions as implementation progresses

## Handling Discoveries During Implementation

**When you discover something that invalidates or significantly changes the plan:**

1. **Stop** - Do not continue implementing based on outdated assumptions
2. **Report** - Explain what you discovered and how you found it
3. **Assess Impact** - Identify which phases/tasks are affected
4. **Ask** - Present options and ask how to proceed before continuing

Examples of discoveries requiring this protocol:
- A dependency doesn't work as documented
- An existing implementation already covers part of the plan
- A technical constraint makes a phase impossible or unnecessary
- New information suggests a different approach would be better
- The plan conflicts with existing code patterns

**Do not** silently adjust the plan or continue with an approach you know is suboptimal.

## Orchestrator Responsibilities

As the orchestrator, you must:

1. **Track progress** - Update task list markdown after each completion
2. **Follow completion protocol:**
   - Mark each finished **sub-task** `[x]`
   - Mark the **parent task** `[x]` once **all** its subtasks are `[x]`
3. **Manage git** - Handle branching, staging, and commits
4. **Run validations** - Execute lint, build, and test commands
5. **Maintain context** - Keep "Relevant Files" section accurate
6. **Gate progress** - Pause for user approval unless NOSUBCONF is specified

---

## ➡️ Next Command

When all tasks are complete, run:
```
/dev:4:validate [path-to-tasks]
```
