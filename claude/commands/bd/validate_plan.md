---
description: Validate implementation against plan with beads tracking
---

# Validate Plan (with Beads Integration)

You are tasked with validating that an implementation plan was correctly executed, verifying all success criteria and identifying any deviations or issues.

**This command uses `bd` (beads) for issue tracking instead of TodoWrite.**

## Initial Setup

When invoked:
1. **Determine context** - Are you in an existing conversation or starting fresh?
   - If existing: Review what was implemented in this session
   - If fresh: Need to discover what was done through git and codebase analysis

2. **Locate the plan**:
   - If plan path provided, use it
   - Otherwise, search recent commits for plan references or ask user

3. **Check beads for context**:
   ```bash
   bd list --status=open        # See any open issues
   bd list --status=in_progress # See what's being worked on
   bd list --status=closed      # See recently completed work
   ```

4. **Gather implementation evidence**:
   ```bash
   # Check recent commits
   git log --oneline -n 20
   git diff HEAD~N..HEAD  # Where N covers implementation commits

   # Run comprehensive checks
   cd $(git rev-parse --show-toplevel) && make check test
   ```

## Validation Process

### Step 1: Context Discovery

If starting fresh or need more context:

1. **Read the implementation plan** completely
2. **Identify what should have changed**:
   - List all files that should be modified
   - Note all success criteria (automated and manual)
   - Identify key functionality to verify

3. **Spawn parallel research tasks** to discover implementation:
   ```
   Task 1 - Verify database changes:
   Research if migration [N] was added and schema changes match plan.
   Check: migration files, schema version, table structure
   Return: What was implemented vs what plan specified

   Task 2 - Verify code changes:
   Find all modified files related to [feature].
   Compare actual changes to plan specifications.
   Return: File-by-file comparison of planned vs actual

   Task 3 - Verify test coverage:
   Check if tests were added/modified as specified.
   Run test commands and capture results.
   Return: Test status and any missing coverage
   ```

### Step 2: Systematic Validation

For each phase in the plan:

1. **Check completion status**:
   - Look for checkmarks in the plan (- [x])
   - Verify the actual code matches claimed completion
   - Cross-reference with beads issues:
     ```bash
     bd show <phase-issue-id>  # Check issue status and notes
     ```

2. **Run automated verification**:
   - Execute each command from "Automated Verification"
   - Document pass/fail status
   - If failures, investigate root cause

3. **Assess manual criteria**:
   - List what needs manual testing
   - Provide clear steps for user verification

4. **Think deeply about edge cases**:
   - Were error conditions handled?
   - Are there missing validations?
   - Could the implementation break existing functionality?

### Step 3: Generate Validation Report

Create comprehensive validation summary:

```markdown
## Validation Report: [Plan Name]

### Implementation Status
✓ Phase 1: [Name] - Fully implemented
✓ Phase 2: [Name] - Fully implemented
⚠️ Phase 3: [Name] - Partially implemented (see issues)

### Beads Issues Status
[Output from bd list showing relevant issues]

### Automated Verification Results
✓ Build passes: `make build`
✓ Tests pass: `make test`
✗ Linting issues: `make lint` (3 warnings)

### Code Review Findings

#### Matches Plan:
- Database migration correctly adds [table]
- API endpoints implement specified methods
- Error handling follows plan

#### Deviations from Plan:
- Used different variable names in [file:line]
- Added extra validation in [file:line] (improvement)

#### Potential Issues:
- Missing index on foreign key could impact performance
- No rollback handling in migration

### Manual Testing Required:
1. UI functionality:
   - [ ] Verify [feature] appears correctly
   - [ ] Test error states with invalid input

2. Integration:
   - [ ] Confirm works with existing [component]
   - [ ] Check performance with large datasets

### Recommendations:
- Address linting warnings before merge
- Consider adding integration test for [scenario]
- Document new API endpoints
```

### Step 4: Create Issues for Findings

If issues are discovered during validation:

```bash
# Create beads issues for any problems found
bd create "Fix: [linting issue description]" --type bug -p 2
bd create "Add: [missing test coverage]" --type task -p 3
bd create "Doc: [missing documentation]" --type task -p 4

# Link them to the original work if needed
bd dep add <new-issue-id> discovered-from:<original-issue-id>
```

## Working with Existing Context

If you were part of the implementation:
- Review the conversation history
- Check beads for what was completed:
  ```bash
  bd list --status=closed
  ```
- Focus validation on work done in this session
- Be honest about any shortcuts or incomplete items

## Important Guidelines

1. **Be thorough but practical** - Focus on what matters
2. **Run all automated checks** - Don't skip verification commands
3. **Document everything** - Both successes and issues
4. **Think critically** - Question if the implementation truly solves the problem
5. **Consider maintenance** - Will this be maintainable long-term?
6. **Use beads for tracking** - Create issues for any findings that need follow-up

## Validation Checklist

Always verify:
- [ ] All phases marked complete are actually done
- [ ] Beads issues align with plan completion
- [ ] Automated tests pass
- [ ] Code follows existing patterns
- [ ] No regressions introduced
- [ ] Error handling is robust
- [ ] Documentation updated if needed
- [ ] Manual test steps are clear

## Relationship to Other Commands

Recommended workflow:
1. `/bd:implement_plan` - Execute the implementation with beads tracking
2. `/hl:commit` - Create atomic commits for changes
3. `/bd:validate_plan` - Verify implementation correctness
4. `/hl:describe_pr` - Generate PR description

The validation works best after commits are made, as it can analyze the git history to understand what was implemented.

## Session Close

After validation is complete:
```bash
bd sync  # Ensure all beads changes are synced
```

Remember: Good validation catches issues before they reach production. Be constructive but thorough in identifying gaps or improvements.
