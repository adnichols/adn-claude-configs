---
description: Process tasks in a task list
argument-hint: [Files]
---

# Instructions

Your mission: Execute tasks from a structured tasklist through incremental delegation and rigorous quality assurance. CRITICAL: You NEVER implement fixes yourself - you coordinate and validate.

<tasklist_file>
$ARGUMENTS[0]
</tasklist_file>

<phase_filter>
$ARGUMENTS[1]
</phase_filter>

## RULE 0: MANDATORY EXECUTION PROTOCOL (+$500 reward for compliance)

Before ANY action, you MUST:

1. Read the specified tasklist file to understand all tasks and dependencies
2. If phase specified, filter to execute only that phase
3. Break tasks into 5-20 line increments if needed
4. Delegate ALL implementation to specialized agents
5. Validate each task before proceeding to the next task
6. Mark each subtask complete before proceeding to next task
7. Only mark parent task complete when all subtasks are complete AND test are passing fully
8. FORBIDDEN: Implementing fixes yourself (-$2000 penalty)

IMPORTANT: The tasks have been pre-analyzed. Your role is execution, not redesign.
CRITICAL: Task dependencies are defined - respect the execution order.

# EXECUTION PROTOCOL

# Task List Management

Guidelines for managing task lists in markdown files to track progress on completing a PRD

## Task Implementation

- Do not proceed with tasks unless you are on a git branch other than main
- If needed, create a branch for the phase of work you are implementing
  - Parent agent (you) are responsible for git branch creation, not subagents
- **One sub-task at a time:** Do **NOT** start the next sub‑task until you ask the user for permission and they say "yes" or "y"
- **Completion protocol:**
  1. When an agent finishes a **sub‑task**, immediately mark it as completed by changing `[ ]` to `[x]`.
  2. If **all** subtasks underneath a parent task are now `[x]`, follow this sequence:
    - **First**: Run the full test suite as defined in CLAUDE.md or TESTING.md
    - **Only if all tests pass**: Stage changes (`git add .`)
    - **Clean up**: Remove any temporary files and temporary code before committing
    - **Commit**: Use a descriptive commit message that:
      - Uses conventional commit format (`feat:`, `fix:`, `refactor:`, etc.)
      - Summarizes what was accomplished in the parent task
      - Lists key changes and additions
      - References the task number and PRD context
      - **Formats the message as a single-line command using `-m` flags**, e.g.:
        ```
        git commit -m "feat: add payment validation logic" -m "- Validates card type and expiry" -m "- Adds unit tests for edge cases" -m "Related to T123 in PRD"
        ```
  3. Once all the subtasks are marked completed and changes have been committed, mark the **parent task** as completed.

- Stop after each sub‑task and wait for the user's go‑ahead.

## Task List Maintenance

1. **Update the task list as you work:**
   - Mark tasks and subtasks as completed (`[x]`) per the protocol above.
   - Add new tasks as they emerge.

2. **Maintain the "Relevant Files" section:**
   - List every file created or modified.
   - Give each file a one‑line description of its purpose.

## AI Instructions

When working with task lists, the AI must:

1. Regularly update the task list file after finishing any significant work.
2. Follow the completion protocol:
   - Mark each finished **sub‑task** `[x]`.
   - Mark the **parent task** `[x]` once **all** its subtasks are `[x]`.
3. Add newly discovered tasks.
4. Keep "Relevant Files" accurate and up to date.
5. Before starting work, check which sub‑task is next.
6. After implementing a sub‑task, update the file and then pause for user approval.
