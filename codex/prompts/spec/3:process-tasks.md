---
description: Process tasks in a task list with fidelity-preserving agent selection
argument-hint: [Files]
---

# Instructions

Process the task list end-to-end with fidelity-preserving agents, maintaining exact scope as specified in the source document. This automation uses `@developer-fidelity` for implementation and `@quality-reviewer-fidelity` for validation. Work continuously unless you need clarification or you cannot satisfy required quality gates after multiple recovery attempts.
$ARGUMENTS. Think harder.

## Autonomous Execution Flow

1. **Initialize context**
   - Parse task file metadata from YAML front matter.
   - Confirm you are on a non-main branch (create one if required).
   - Enumerate phases in order; assume responsibility for every phase unless the operator says otherwise.
2. **Phase loop**
   - Execute phases sequentially without pausing for approval between subtasks.
   - For each subtask: implement only what the spec authorizes, record relevant diffs, and update supporting context (docs, fixtures, configs).
   - Immediately update the task list entry (`[ ]` → `[x]`) once the subtask’s implementation is complete; show the edited snippet for confirmation.
3. **Continuous alignment**
   - Keep optional sections like “Relevant Files” and “Notes” accurate as you progress.
   - Raise clarifying questions only when requirements conflict or information is missing.

## Phase Quality Gates & Recovery

1. When all subtasks within a phase are `[x]`, run the validation stack defined by the source material:
   - Prioritize commands listed in the task file, TESTING.md, or AGENTS.md.
   - If nothing specific is provided, run the primary repository test suite; add lint, build, or secrets scans only when those commands exist and the scope requires them.
2. If a validation fails:
   - Summarize the failure, remediate the issue, and rerun the gate.
   - Repeat up to three remediation cycles per phase. After three failures, halt and ask the operator how to proceed.
3. Only proceed to the next phase when every required validation passes cleanly.
4. Stage files with `git add .` once validations succeed, run the fidelity quality review (`@quality-reviewer-fidelity`), perform cleanup, and craft a conventional commit message via multi-`-m` flags noting the phase scope.

## Task List Maintenance

- Update the markdown plan immediately after each subtask completion; never defer these updates.
- Reflect new discoveries by adding subtasks or notes in-place, preserving numbering and indentation.
- Once all subtasks under a parent task are complete and committed, mark the parent task `[x]` and document the validation commands executed.
- Provide concise progress logs after each phase summarizing work done, validations run, and outstanding risks (if any).

## Stop Conditions

- Continue through the entire task list without prompting the operator between phases.
- Stop only when:
  - You require clarification or additional input.
  - A phase fails quality gates three consecutive times and further autonomous recovery is unlikely.
  - The task list is fully complete, validated, and committed.

## Fidelity Guardrails

- Apply only the security, testing, and performance work explicitly authorized by the source material.
- Maintain exact traceability to requirements; cite the relevant section when making design or implementation choices.
- Escalate ambiguities instead of guessing; do not expand scope.
