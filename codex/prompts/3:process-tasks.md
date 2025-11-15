---
description: Process tasks in a task list with fidelity-preserving agent selection
argument-hint: [Files]
---

# Instructions

Process the task list using the fidelity-preserving approach to maintain exact scope as specified in the source document. Implement only what's explicitly specified, without additions or scope expansions.
$ARGUMENTS.

Also follow this repository's `AGENTS.md` for project-specific branch, testing, and security rules.

## AUTONOMOUS PHASE PROCESSING

**EXECUTION MODE**: This command processes an ENTIRE PHASE autonomously.

- Process ALL subtasks in the current phase WITHOUT stopping for confirmation between subtasks
- Update markdown after each subtask completion
- Follow all fidelity safeguards
- Only stop after completing the ENTIRE PHASE (all parent task subtasks done)
- After phase completion: run tests, commit changes, and report completion

## Fidelity Preservation Process

Before starting task implementation:

1. **Parse Task File Metadata:** Extract fidelity information from task file YAML front-matter
2. **Apply Only Specified Validation:** Include only the testing and validation explicitly specified in the source document:
   - Review source document for testing requirements
   - Implement only specified security measures
   - Do not add tests or validation beyond what's explicitly required

## Task Implementation

**GIT BRANCH REQUIREMENTS:**
- Do not proceed with tasks unless you are on a git branch other than main
- If needed, create a branch for the phase of work you are implementing

## Critical Task Update Protocol

After completing any subtask:

1. Immediately update the corresponding line in the task list file, changing `- [ ] X.Y [task name]` to `- [x] X.Y [task name]`.
2. Show the edit operation in the response and display the updated section of the markdown file to confirm the change.
3. Continue directly to the next subtask without waiting for additional confirmation.

If a subtask is completed but the markdown file was not updated promptly:
- Stop further work.
- Clearly state that the task list is out of sync and await operator guidance before resuming.

## Completion Protocol

When you finish a **sub‑task**, immediately mark it as completed by changing `[ ]` to `[x]`.

If **all** subtasks underneath a parent task are now `[x]`, follow this sequence:

1. **First**: Run validation checks defined by the plan and repository guidance:
   - Prioritize commands listed in the task file, TESTING.md, or AGENTS.md
   - If nothing specific is provided, run the primary repository test suite and add lint, build, or secrets scans only when those commands exist and the scope requires them

2. **If validation fails:**
   - Summarize the failure, remediate the issue, and rerun validation
   - Repeat up to three remediation cycles per phase
   - After three failures, halt and ask the operator how to proceed

3. **Only if all validations pass**: Stage changes (`git add .`)

4. **Quality Review**: Perform quality review for final approval

5. **Clean up**: Remove any temporary files and temporary code before committing

6. **Commit**: Use a descriptive commit message that:
   - Uses conventional commit format (`feat:`, `fix:`, `refactor:`, etc.)
   - Summarizes what was accomplished in the parent task
   - Lists key changes and additions
   - References the phase number and source context
   - **Formats the message as a single-line command using `-m` flags**, e.g.:
     ```
     git commit -m "feat: add payment validation logic" -m "- Validates card type and expiry" -m "- Adds unit tests for edge cases" -m "Related to Phase 2.1"
     ```

7. Once all the subtasks are marked completed and changes have been committed, mark the **parent task** as completed.

**PHASE COMPLETION:** When all parent tasks in the current phase are complete and validated, ensure tests and commits are up to date, then stop and report completion.

## Task List Maintenance

1. **Update the task list as you work:**
   - Mark tasks and subtasks as completed (`[x]`) per the protocol above
   - Add follow-up tasks only when they directly trace back to requirements or clarifications in the source document

2. **Maintain the "Relevant Files" section:**
   - List every file created or modified during implementation
   - Update descriptions as implementation progresses
   - Add new files discovered during implementation

3. **Context Validation (for rich execution plans):**
   - Ensure implementation stays true to source document's technical specifications
   - Validate security requirements are being followed
   - Confirm performance benchmarks are being met

## AI Instructions

When working with task lists, the AI must:

1. Process the entire phase autonomously without stopping for confirmation between subtasks.
2. Regularly update the task list file after finishing any significant work.
3. Follow the completion protocol:
   - Mark each finished **sub‑task** `[x]`.
   - Mark the **parent task** `[x]` once **all** its subtasks are `[x]`.
4. Add newly discovered tasks while maintaining phase structure.
5. Keep "Relevant Files" accurate and up to date.
6. Before starting work, check which sub‑task is next and review context sections if present.
7. After implementing a sub‑task:
   - Update the markdown file immediately
   - State you're proceeding and continue immediately to next subtask
8. For rich execution plans: Reference preserved context when making implementation decisions.
9. For rich execution plans: Ensure traceability between implementation and source document rationale.
10. For rich execution plans: Validate against success criteria throughout implementation.
11. **CRITICAL CHECKPOINT:** After each subtask completion, the Codex agent MUST immediately declare completion, update the markdown file, show the edit, confirm the update, and then continue to the next subtask without pausing. Failure to do this is a critical error that requires stopping all work.

## Stop Conditions

Continue through the entire phase without prompting between subtasks. Stop only when:
- You require clarification or additional input
- A phase fails quality gates three consecutive times and further autonomous recovery is unlikely
- The entire phase is complete, validated, and committed

## Fidelity Guardrails

- Apply only the security, testing, and performance work explicitly authorized by the source material
- Maintain exact traceability to requirements; cite the relevant section when making design or implementation choices
- Escalate ambiguities instead of guessing; do not expand scope
