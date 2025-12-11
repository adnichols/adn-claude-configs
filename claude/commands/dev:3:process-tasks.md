---
description: Process tasks in a task list with fidelity-preserving agent selection
argument-hint: [Files]
---

# Instructions

Process the task list using the fidelity-preserving approach to maintain exact scope as specified in the source document. This command uses developer-fidelity and quality-reviewer-fidelity agents to implement only what's explicitly specified, without additions or scope expansions.
$ARGUMENTS. Think harder.

## Fidelity Preservation Process

Before starting task implementation:

1. **Parse Task File Metadata:** Extract fidelity information from task file YAML front-matter
2. **Use Fidelity Agents:** Always use fidelity-preserving agents for implementation:
   - Developer agent: `@developer-fidelity`
   - Quality reviewer: `@quality-reviewer-fidelity`
3. **Apply Only Specified Validation:** Include only the testing and validation explicitly specified in the source document:
   - Review source document for testing requirements
   - Implement only specified security measures
   - Do not add tests or validation beyond what's explicitly required

## Sub-Agent Delegation Protocol

When processing tasks, use the Task tool to spawn specialized sub-agents for implementation work. This preserves orchestrator context and ensures fidelity-focused execution.

### For Implementation Tasks

Delegate actual code implementation to the **developer-fidelity** agent using the Task tool:

**Task prompt template:**
```
Implement subtask [X.Y]: [subtask description]

Specification requirements:
- [Requirement 1 from source spec]
- [Requirement 2 from source spec]

Files: [relevant file paths]
Context: [relationship to other components]

IMPORTANT: Implement ONLY what's specified above. No additional features, tests, or security beyond requirements.
```

### For Quality Reviews

When all subtasks under a parent are complete, spawn a **quality-reviewer-fidelity** agent via Task tool:

**Task prompt template:**
```
Review Phase [N] implementation for specification fidelity.

Source specification: [path to spec/task file]
Modified files:
- [file1.ts]
- [file2.ts]

Verify: Implementation matches spec exactly, no scope creep, no unauthorized additions.
```

### Orchestrator Responsibilities (Do NOT Delegate)

The parent agent (you) handles coordination tasks directly:
- Git branch creation and management
- Task list updates (`[ ]` → `[x]`)
- User confirmation prompts
- Phase transitions and commits
- Validation command execution (lint, build, tests)


<skip_subtask_confirmation>
If $ARGUMENTS contains NOSUBCONF then ignore subtask confirmation in task implementation below
</skip_subtask_confirmation>

# Task List Management

Guidelines for managing task lists in markdown files to track progress on completing source document implementations

## Task Implementation

## Critical Task Update Protocol

**MANDATORY CHECKPOINT SYSTEM:** After completing ANY subtask, Claude MUST follow this exact sequence:

1. **Declare completion with mandatory update statement:**
   "✅ Subtask [X.Y] [task name] completed.
   🔄 UPDATING MARKDOWN FILE NOW..."

2. **Immediately perform the markdown update:**

- Use Edit tool to change `- [ ] X.Y [task name]` to `- [x] X.Y [task name]`
- Show the actual edit operation in the response

3. **Confirm update completion:**
   "✅ Markdown file updated: [ ] → [x] for subtask X.Y
   📋 Task list is now current."

4. **Request permission to proceed (unless NOSUBCONF specified):**
   "Ready to proceed to next subtask. May I continue? (y/n)"

**FAILURE TO FOLLOW THIS PROTOCOL IS A CRITICAL ERROR.** If Claude completes a subtask without immediately updating the markdown file, it MUST:

- Stop all work immediately
- State: "❌ CRITICAL ERROR: I failed to update the task list. Stopping work."
- Wait for user intervention before proceeding

**VERIFICATION REQUIREMENT:** After each edit, Claude must show the updated section of the markdown file to confirm the change was made correctly.

- Do not proceed with tasks unless you are on a git branch other than main
- If needed, create a branch for the phase of work you are implementing
  - Parent agent (you) are responsible for git branch creation, not subagents
- **One sub-task at a time:** Spawn a **developer-fidelity** sub-agent via Task tool for each subtask implementation. Do **NOT** start the next sub‑task until you ask the user for permission and they say "yes" or "y" UNLESS NOSUBCONF is specified by the user
- **Completion protocol:**

  1. When you finish a **sub‑task**, immediately mark it as completed by changing `[ ]` to `[x]`.

  - **MANDATORY TASK UPDATE:** Before doing anything else after subtask completion, immediately update the markdown file `[ ]` → `[x]` and confirm the update was successful

  2. If **all** subtasks underneath a parent task are now `[x]`, follow this sequence:

  - **First**: Run standard validation checks:
    - Always: lint, build, secrets scan, unit tests
  - **Only if all validations pass**: Stage changes (`git add .`)
  - **Quality Review**: Spawn a **quality-reviewer-fidelity** sub-agent via Task tool with the source specification and list of modified files for fidelity validation
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

## Handling Discoveries During Implementation

**When you discover something that invalidates or significantly changes the plan:**

1. **Stop** - Do not continue implementing based on outdated assumptions
2. **Report** - Explain what you discovered and how you found it
3. **Assess Impact** - Identify which phases/tasks are affected
4. **Ask** - Present options and ask me how to proceed before continuing

Examples of discoveries requiring this protocol:
- A dependency doesn't work as documented
- An existing implementation already covers part of the plan
- A technical constraint makes a phase impossible or unnecessary
- New information suggests a different approach would be better
- The plan conflicts with existing code patterns

**Do not** silently adjust the plan or continue with an approach you know is suboptimal. The plan is a guide, not a contract—but changes require explicit approval.

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
10. **CRITICAL CHECKPOINT:** After each subtask completion, Claude MUST immediately declare completion, update the markdown file, show the edit, confirm the update, and request permission to continue. Failure to do this is a critical error that requires stopping all work.
