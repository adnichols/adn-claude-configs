---
description: Process tasks in a task list with fidelity-preserving agent selection
argument-hint: [Files]
---

# Instructions

Process the task list using the fidelity-preserving approach to maintain exact scope as specified in the source document. This command uses developer-fidelity and quality-reviewer-fidelity agents to implement only what's explicitly specified, without additions or scope expansions.
$ARGUMENTS. Think harder.

## CRITICAL: Orchestrator-Only Mode

**You (the parent session) are an ORCHESTRATOR, not an implementer.**

- **NEVER** use Edit, Write, or MultiEdit tools to modify code files
- **NEVER** implement features, fix bugs, or write code directly
- **ALWAYS** delegate ALL code changes to sub-agents via the Task tool

Your job is to coordinate, track progress, run validations, and manage git—NOT to write code.

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
- Task list updates (`[ ]` → `[x]`) in markdown files
- User confirmation prompts
- Phase transitions and commits
- Validation command execution (lint, build, tests)
- Reading files for context gathering
- Running Bash commands for git, npm, validation

### What You MUST Delegate (NEVER Do Directly)

**All code changes go to sub-agents.** This includes:
- Creating new files (use developer-fidelity agent)
- Editing existing code (use developer-fidelity agent)
- Writing tests (use developer-fidelity agent)
- Refactoring (use developer-fidelity agent)
- Code review (use quality-reviewer-fidelity agent)

If you find yourself about to use Edit/Write/MultiEdit on a code file, STOP and spawn a sub-agent instead.


<skip_subtask_confirmation>
If $ARGUMENTS contains NOSUBCONF then ignore subtask confirmation in task implementation below
</skip_subtask_confirmation>

# Task List Management

Guidelines for managing task lists in markdown files to track progress on completing source document implementations

## Task Implementation

## Critical Task Update Protocol

**MANDATORY CHECKPOINT SYSTEM:** After a sub-agent completes ANY subtask, you (the orchestrator) MUST follow this exact sequence:

1. **Declare completion with mandatory update statement:**
   "✅ Subtask [X.Y] [task name] completed by sub-agent.
   🔄 UPDATING MARKDOWN FILE NOW..."

2. **Immediately perform the markdown update:**

- Use Edit tool to change `- [ ] X.Y [task name]` to `- [x] X.Y [task name]`
- Show the actual edit operation in the response

3. **Confirm update completion:**
   "✅ Markdown file updated: [ ] → [x] for subtask X.Y
   📋 Task list is now current."

4. **Request permission to proceed (unless NOSUBCONF specified):**
   "Ready to proceed to next subtask. May I continue? (y/n)"

**FAILURE TO FOLLOW THIS PROTOCOL IS A CRITICAL ERROR.** If a subtask completes without you immediately updating the markdown file, you MUST:

- Stop all work immediately
- State: "❌ CRITICAL ERROR: I failed to update the task list. Stopping work."
- Wait for user intervention before proceeding

**VERIFICATION REQUIREMENT:** After each task list edit, show the updated section of the markdown file to confirm the change was made correctly.

- Do not proceed with tasks unless you are on a git branch other than main
- If needed, create a branch for the phase of work you are implementing
  - Parent agent (you) are responsible for git branch creation, not subagents
- **One sub-task at a time:** Spawn a **developer-fidelity** sub-agent via Task tool for each subtask. Do **NOT** start the next sub‑task until you ask the user for permission and they say "yes" or "y" UNLESS NOSUBCONF is specified by the user
- **Completion protocol:**

  1. When a **sub-agent completes** a subtask, immediately mark it as completed by changing `[ ]` to `[x]`.

  - **MANDATORY TASK UPDATE:** Before doing anything else after sub-agent completion, immediately update the markdown file `[ ]` → `[x]` and confirm the update was successful

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

As the orchestrator, you must:

1. **Delegate all code work** - Spawn sub-agents for every subtask that involves code changes
2. **Track progress** - Update task list markdown after each sub-agent completes
3. **Follow completion protocol:**
   - Mark each finished **sub‑task** `[x]` after sub-agent reports completion
   - Mark the **parent task** `[x]` once **all** its subtasks are `[x]`
4. **Manage git** - Handle branching, staging, and commits directly
5. **Run validations** - Execute lint, build, and test commands directly via Bash
6. **Coordinate quality reviews** - Spawn quality-reviewer-fidelity after phases complete
7. **Maintain context** - Keep "Relevant Files" section accurate based on sub-agent reports
8. **Gate progress** - Pause for user approval unless NOSUBCONF is specified
9. **CRITICAL CHECKPOINT:** After each subtask, immediately declare completion, update markdown, confirm the update, and request permission to continue

**Remember: You orchestrate, sub-agents implement. Never write code directly.**
