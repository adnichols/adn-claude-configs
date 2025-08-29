---
description: Process tasks in a task list
argument-hint: [Files]
---

# Instructions

Take the tasks (either in a list or a file) below and process them according to the instructions in Task List Management. This command handles both simple task lists and complex execution plans with rich context from source documents (PRDs, research plans, etc.).
$ARGUMENTS. Think harder.

<skip_subtask_confirmation>
If $ARGUMENTS contains NOSUBCONF then ignore subtask confirmation in task implementation below
</skip_subtask_confirmation>

# Task List Management

Guidelines for managing task lists in markdown files to track progress on completing source document implementations

## Task Implementation

- Do not proceed with tasks unless you are on a git branch other than main
- If needed, create a branch for the phase of work you are implementing
  - Parent agent (you) are responsible for git branch creation, not subagents
- **One sub-task at a time:** Do **NOT** start the next sub‑task until you ask the user for permission and they say "yes" or "y" UNLESS NOSUBCONF is specified by the user
- **Completion protocol:**
  1. When you finish a **sub‑task**, immediately mark it as completed by changing `[ ]` to `[x]`.
  2. If **all** subtasks underneath a parent task are now `[x]`, follow this sequence:
  - **First**: Run the full test suite as defined in TESTING.md or CLAUDE.md
  - **Only if all tests pass**: Stage changes (`git add .`)
  - **Clean up**: Remove any temporary files and temporary code before committing
  - **Commit**: Use a descriptive commit message that:
    - Uses conventional commit format (`feat:`, `fix:`, `refactor:`, etc.)
    - Summarizes what was accomplished in the parent task
    - Lists key changes and additions
    - References the phase number and source context
    - **Formats the message as a single-line command using `-m` flags**, e.g.:

      ```
      git commit -m "feat: add payment validation logic" -m "- Validates card type and expiry" -m "- Adds unit tests for edge cases" -m "Related to Phase 2.1"
      ```
  3. Once all the subtasks are marked completed and changes have been committed, mark the **parent task** as completed.

- Stop after each sub‑task and wait for the user's go‑ahead UNLESS NOSUBCONF is specified by the user

- Always stop after parent tasks complete, run test suite, and commit changes

## Task List Maintenance

1. **Update the task list as you work:**
   - Mark tasks and subtasks as completed (`[x]`) per the protocol above.
   - Add new tasks as they emerge.

2. **Maintain the "Relevant Files" section:**
   - List every file created or modified during implementation.
   - Update descriptions as implementation progresses.
   - Add new files discovered during implementation.

3. **Context Validation (for rich execution plans):**
   - Ensure implementation stays true to source document's technical specifications.
   - Validate security requirements are being followed.
   - Confirm performance benchmarks are being met.

## AI Instructions

When working with task lists, the AI must:

1. Regularly update the task list file after finishing any significant work.
2. Follow the completion protocol:
   - Mark each finished **sub‑task** `[x]`.
   - Mark the **parent task** `[x]` once **all** its subtasks are `[x]`.
3. Add newly discovered tasks while maintaining phase structure.
4. Keep "Relevant Files" accurate and up to date.
5. Before starting work, check which sub‑task is next and review context sections if present.
6. After implementing a sub‑task, update the file and then pause for user approval.
7. For rich execution plans: Reference preserved context when making implementation decisions.
8. For rich execution plans: Ensure traceability between implementation and source document rationale.
9. For rich execution plans: Validate against success criteria throughout implementation.
