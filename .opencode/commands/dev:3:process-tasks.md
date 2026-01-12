---
description: Process tasks in a task list with fidelity-preserving agent selection
argument-hint: "[Files]"
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
2. **Check for Phase 0 (Infrastructure Verification):** If the task file contains a Phase 0:
   - **Phase 0 is BLOCKING** - no other phases can start until Phase 0 passes
   - Complete all Phase 0 subtasks (version checks, smoke tests, documentation)
   - Only proceed to Phase 1+ after Phase 0 is fully validated and committed
3. **Use Fidelity Agents:** Always use fidelity-preserving agents for implementation:
   - Developer agent: `@developer-fidelity`
   - Quality reviewer: `@quality-reviewer-fidelity`
4. **Apply Only Specified Validation:** Include only the testing and validation explicitly specified in the source document:
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
- **ONLY create a branch if currently on main**
- If already on a non-main branch (e.g., `feature/...`, `bugfix/...`), continue using it
- Parent agent (you) are responsible for git branch operations, not subagents
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
5. **Log the Deviation** - After user decision, append to the Deviations Log (see below)

Examples of discoveries requiring this protocol:
- A dependency doesn't work as documented
- An existing implementation already covers part of the plan
- A technical constraint makes a phase impossible or unnecessary
- New information suggests a different approach would be better
- The plan conflicts with existing code patterns
- **Phase 0 infrastructure verification fails** (version mismatch, connectivity issues)
- **Paired dependencies are incompatible** (client/server version conflict)

**Do not** silently adjust the plan or continue with an approach you know is suboptimal. The plan is a guide, not a contract—but changes require explicit approval.

### Proactive User Engagement for Discoveries

Use **AskUserQuestion** to engage the user when discoveries warrant input.

**Validation Question (confirm impact assessment):**
```
Question: "I discovered [X] during implementation. This affects [phases/tasks]. Is my assessment correct?"
Header: "Impact"
Options:
- Yes, your assessment is correct
- Impact is larger than you think
- Impact is smaller - proceed as planned
- Need more information before deciding
```

**Trade-off Question (present alternatives):**
```
Question: "I found an issue with the planned approach. Which direction should we take?"
Header: "Approach"
Options:
- Option A: [description with trade-offs]
- Option B: [description with trade-offs]
- Pause implementation while I investigate further
```

**Scope Question (adjust plan boundaries):**
```
Question: "This discovery means [feature] would require [significantly more work/different approach]. How should we adjust?"
Header: "Scope"
Options:
- Expand scope to handle this properly
- Defer this aspect to a follow-up task
- Simplify the approach (describe what changes)
- Let's discuss before deciding
```

### When to Surface vs Proceed Autonomously

**Always Surface (user engagement required):**
- Plan assumptions are invalidated (blocker discovered)
- Multiple viable paths with different trade-offs
- Scope would change (expand or contract)
- Risk level increases beyond original assessment
- Decisions affect future phases
- Implementation would diverge from spec intent

**Proceed Autonomously (log in Deviations, don't block):**
- Minor technical choices within spec boundaries
- Implementation details that don't affect behavior
- Choosing between equivalent approaches
- Obvious error corrections in the plan
- Well-established patterns in the codebase

**Threshold Guidance:** When in doubt, err toward engaging the user. The cost of a brief pause is lower than implementing the wrong thing.

### User Engagement During Sub-Agent Work

If a sub-agent reports an issue during implementation:

1. **Sub-agent reports issue** - Agent describes what they found
2. **You (orchestrator) evaluate** - Is this a blocker or solvable within scope?
3. **If blocker or scope question**: Use AskUserQuestion before spawning more agents
4. **If solvable within spec**: Guide the sub-agent, log decision if it deviates from plan

## Deviations Log Protocol

**MANDATORY:** When a discovery leads to a decision that differs from the original spec/plan, you MUST log it in the task file for downstream propagation to future phases.

### When to Log

Log a deviation when:
- The spec was ambiguous and you chose a specific implementation path
- A planned approach was changed due to discovered constraints
- Scope was adjusted (feature deferred, modified, or dropped)
- An API contract or pattern was established that future phases depend on
- A technical constraint was discovered that affects future work

### How to Log

After user approval for a deviation, append to the task file's `## Deviations Log` section (create if it doesn't exist):

```markdown
## Deviations Log

### D[N]: [Brief Decision Title] - [YYYY-MM-DD]
- **Category:** [Uncertainty Resolved | Scope Adjusted | Pattern Discovered | Constraint Identified | API Contract Defined]
- **Discovery:** [What was found that differed from spec/plan]
- **Spec/Plan Said:** [Quote or summary of original requirement]
- **Decision Made:** [What was actually implemented]
- **Rationale:** [Why this choice was made]
- **User Approved:** [Yes | No - autonomous decision]
- **Future Phases Affected:** [Phase 2, Phase 3, etc. | None | Unknown]
```

### Example Entry

```markdown
### D1: Use Partial Unique Index Instead of Trigger - 2025-12-27
- **Category:** Uncertainty Resolved
- **Discovery:** PostgreSQL partial unique indexes are more performant than triggers for conditional uniqueness
- **Spec/Plan Said:** "Ensure unique workspace slugs per user" (implementation unspecified)
- **Decision Made:** Used `CREATE UNIQUE INDEX ... WHERE deleted_at IS NULL` instead of trigger-based approach
- **Rationale:** Partial indexes are database-native, faster, and require less maintenance
- **User Approved:** Yes
- **Future Phases Affected:** Phase 3 (migration must preserve index), Phase 5 (cleanup can remove old trigger code)
```

### Logging Autonomous Decisions

For high-confidence decisions made without user input (e.g., obvious technical choices), still log them but mark as:
```
- **User Approved:** No - autonomous decision (high confidence)
```

This ensures `dev:5:phase-review` can still propagate these decisions to future phases.

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

---

## ➡️ Next Command

When all tasks are complete, run:
```
/dev:4:validate [path-to-tasks]
```
