---
description: Process and execute a code simplification plan created by simplify:create-plan.md
argument-hint: [Plan file path] [Options: NOSUBCONF]
---

# Instructions

Execute the code simplification plan step by step according to the Plan Processing Protocol below.
$ARGUMENTS.

Also follow this repository's `AGENTS.md` for project-specific branch, testing, and safety rules.

<skip_subtask_confirmation>
If $ARGUMENTS contains NOSUBCONF then ignore step confirmation in plan execution below
</skip_subtask_confirmation>

<plan_file_tracking>
CRITICAL: Always track and update the plan file throughout execution:
- Extract plan file path from first argument
- Store plan file path as PLAN_FILE variable
- Update checkboxes using search_replace tool after each completed step
- Verify checkbox updates by reading back the plan file
- Never lose track of which plan file you're processing
</plan_file_tracking>

## Plan Processing Protocol

Guidelines for safely executing code simplification plans while preserving functionality and tracking progress.

### Critical Safety Requirements

**Functionality Preservation**
- Before any changes, run the primary test suite to establish a baseline.
- After each major step that alters code, rerun relevant tests and compare to the baseline.
- If any previously passing test fails, stop, surface details to the user, and wait for guidance before proceeding.

**Branch Management**
- Do not proceed unless you are on a git branch other than `main`.
- If needed, create a branch specifically for this simplification work (for example, `simplify/[area-name]-[date]`).

**Step-by-Step Execution**
- Execute steps in the plan in order, one at a time.
- Do not delegate execution to subagents; implement and validate changes directly.
- After each completed sub-step, immediately update its checkbox in the plan file from `[ ]` to `[x]` and verify the change.
- By default, stop after each major step and wait for the user’s go-ahead; if `NOSUBCONF` is present in `$ARGUMENTS`, you may proceed automatically between steps but must still pause on test failures and at phase boundaries.

### Checkbox Update Protocol

Before starting:
- Extract the plan file path from the first argument and store it as `PLAN_FILE`.
- Read the plan file once to understand current state and locate the next unchecked step.

For each completed step:
- Identify the specific `- [ ]` line for that step.
- Use a targeted search/replace update to change it to `- [x]`.
- Re-read the relevant section of `PLAN_FILE` to confirm the checkbox is now `[x]`.
- For nested items, update both sub-items and parent items when appropriate.

## Step Processing Workflow

For each step in the plan:

1. **Pre-Step Verification**
   - Confirm which step is next and understand its intent.
   - Ensure prerequisites are complete and the workspace is in a good state.

2. **Step Execution**
   - Execute the specific actions for the step (code changes, test creation, verification, etc.).
   - Immediately after completion, update the corresponding checkbox in `PLAN_FILE` from `[ ]` to `[x]` and verify the change.

3. **Post-Step Validation**
   - Run relevant tests when code has changed and compare to the baseline.
   - Update any “Relevant Files”, issues, or risk sections in the plan file as needed.

Do not proceed to the next step until the current step’s checkbox is confirmed `[x]` in the plan file and required tests for that step are passing or explicitly explained.

## Phase Completion Protocol

When all steps in a phase are marked `[x]`:

1. **Full Validation:**
   - Run complete test suite as defined in TESTING.md or CLAUDE.md
   - Verify all functionality preservation requirements
   - Check performance benchmarks
   - Validate integration points

2. **Git Management:**
   - Stage changes: `git add .`
   - Clean up temporary files and artifacts
   - Commit with descriptive message using conventional format:
     ```
     git commit -m "refactor: [phase description]" -m "- [key changes made]" -m "- [preservation verifications]" -m "Related to simplify-plan-[area-name]"
     ```

3. **Documentation:**
   - Update plan file with phase completion
   - Document any lessons learned or issues encountered
   - Update risk assessment if needed

4. **User Confirmation:**
   - Always stop and wait for user approval before next phase
   - Provide summary of phase accomplishments
   - Highlight any concerns or deviations from plan

## Progress Tracking

### Plan File Maintenance
1. **Real-time Updates:**
   - Mark steps `[x]` immediately upon completion using search_replace tool
   - Verify each checkbox update by reading the modified section back
   - Add newly discovered tasks as they emerge
   - Update risk assessments based on findings
   - NEVER skip checkbox updates - they are required for progress tracking

2. **Relevant Files Section:**
   - List every file created, modified, or deleted
   - Provide one-line description of changes made
   - Track test files separately from implementation files

3. **Issues and Risks Section:**
   - Document any unexpected challenges
   - Record deviations from original plan
   - Note any functionality concerns discovered

## Error Handling and Recovery

### Test Failure Response
1. **Immediate Actions:**
   - Stop all further execution
   - Document the exact test failure details
   - Identify what changed since last successful test run
   - Capture system state for debugging

2. **User Communication:**
   - Alert user with clear failure description
   - Provide specific error messages and logs
   - Suggest potential rollback options
   - Wait for explicit user decision on how to proceed

3. **Recovery Options:**
   - Rollback last change and retry
   - Debug and fix the issue before continuing
   - Skip problematic step and mark as deferred
   - Abort simplification plan entirely

### Git Safety Net
- Each phase should be a clean commit point
- Easy rollback to any previous stable state
- Clear commit messages for easy navigation
- Branch isolation from main codebase

## Success Criteria

A step is considered complete when:
- [ ] All step actions have been executed
- [ ] Step is marked `[x]` in plan file using search_replace tool
- [ ] Checkbox update verified by reading plan file back
- [ ] All tests pass (or degradation is explained and approved)
- [ ] No functionality regressions detected
- [ ] User has confirmed (unless NOSUBCONF specified)

A phase is considered complete when:
- [ ] All steps in phase are marked `[x]`
- [ ] Full test suite passes
- [ ] Git commit created with changes
- [ ] Documentation updated
- [ ] User approval received for next phase

The entire plan is complete when:
- [ ] All phases marked complete
- [ ] Final integration testing passed
- [ ] Performance benchmarks maintained
- [ ] All temporary artifacts cleaned up
- [ ] Completion documented in plan file

## Plan Processing Initialization

### REQUIRED: Start of Plan Processing Workflow

**Step 1: Plan File Setup**
```bash
# Extract plan file path from arguments
PLAN_FILE="$1"  # First argument should be plan file path
echo "Processing plan file: $PLAN_FILE"
```

**Step 2: Initial Plan File Analysis**
- Read the entire plan file to understand current state
- Identify which phases/steps are already completed `[x]`
- Identify the next uncompleted step to work on `[ ]`
- Verify file is writable and accessible

**Step 3: Establish Progress Tracking**
- Create a system for tracking which step you're currently working on
- Note the exact text of checkboxes that need updating
- Plan the search/replace strings for checkbox updates

**Step 4: Begin Step-by-Step Execution**
- Follow the Step Processing Workflow below
- Update checkboxes after each completed step
- Never proceed without updating progress in plan file

## AI Instructions for Plan Processing

When processing simplification plans, the AI must:

1. **Follow the safety protocol absolutely:**
   - Do not skip test validation or continue after test failures.
   - Do not delegate execution to subagents.

2. **Maintain progress tracking:**
   - Treat `PLAN_FILE` as the source of truth for progress.
   - After each step, mark the corresponding checkbox `[x]`, verify the change, and avoid batching updates.

3. **Execute steps directly:**
   - Implement code and tests yourself and run validations directly.

4. **Preserve functionality:**
   - Validate preservation after changes and stop immediately on any regression.

5. **Communicate clearly:**
   - Provide concise status updates, surface issues quickly, and ask for guidance when uncertain.

The goal is safe, systematic simplification with absolute functionality preservation; speed is secondary to safety and correctness.
