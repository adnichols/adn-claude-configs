---
description: Synthesize completed artifacts into permanent documentation
argument-hint: [feature name or spec/plan path]
---

# Graduate Feature

Synthesize completed feature artifacts into permanent documentation (SPECIFICATION.md, CHANGELOG.md, DECISIONS.md) and clean up working files. Git history preserves all original artifacts.

Feature or path: $ARGUMENTS

## Process

### 1. Locate Artifacts

Search for completed artifacts related to the feature:

```
thoughts/specs/spec-[feature].md       - Technical specification
thoughts/plans/prd-[feature].md        - PRD (if exists)
thoughts/plans/tasks-*-[feature].md    - Task list
thoughts/research/[date]-[feature].md  - Research documents
thoughts/handoffs/[feature]/           - Handoff documents
thoughts/validation/[date]-[feature].md - Validation reports
thoughts/debug/[date]-[feature].md     - Debug reports
```

Read all found artifacts completely.

### 2. Verify Completion

Before graduating, verify:
- [ ] All tasks in task list are checked
- [ ] Tests pass (if tests were specified)
- [ ] Build succeeds (if applicable)
- [ ] No open blockers

If incomplete, stop and report what's missing.

### 3. Synthesize to SPECIFICATION.md

Extract from specs and plans:
- Feature behaviors and constraints
- API contracts (if applicable)
- Configuration options
- User-facing functionality

Add new section to SPECIFICATION.md:

```markdown
## [Feature Name]

*Added: YYYY-MM-DD*

### Overview
[Brief description of feature]

### Behaviors
- [Behavior 1]
- [Behavior 2]

### Constraints
- [Constraint 1]
- [Constraint 2]

### Configuration
- `CONFIG_KEY`: [Description and default]

### Related
- [Links to other spec sections if related]
```

### 4. Synthesize to CHANGELOG.md

Extract from plans and task lists:
- What was built
- Key changes made
- Notable implementation details

Add entry to CHANGELOG.md (newest first):

```markdown
## [Feature Name] - YYYY-MM-DD

### Added
- [New functionality 1]
- [New functionality 2]

### Changed
- [Modification 1]

### Technical Notes
- [Implementation detail worth noting]
```

### 5. Synthesize to DECISIONS.md

Extract from research documents:
- Architectural decisions made
- Alternatives considered
- Rationale for choices

Add ADR entry to DECISIONS.md:

```markdown
## ADR-NNN: [Decision Title] - YYYY-MM-DD

### Context
[What prompted this decision]

### Decision
[What was decided]

### Alternatives Considered
- [Option 1]: [Why rejected]
- [Option 2]: [Why rejected]

### Consequences
- [Positive consequence]
- [Trade-off or risk]

### Related
- [Feature Name] in SPECIFICATION.md
```

### 6. Commit Permanent Docs

Commit all permanent documentation updates:

```bash
git add SPECIFICATION.md CHANGELOG.md DECISIONS.md
git commit -m "docs: graduate [feature-name] to permanent documentation

Synthesized from:
- thoughts/specs/spec-[feature].md
- thoughts/plans/tasks-*-[feature].md
- thoughts/research/*-[feature].md

This captures feature behaviors, changelog entry, and architectural decisions."
```

### 7. Delete Working Artifacts

Remove all `thoughts/` artifacts for this feature:

```bash
# Remove spec
rm thoughts/specs/spec-[feature].md

# Remove plans
rm thoughts/plans/prd-[feature].md
rm thoughts/plans/tasks-*-[feature].md

# Remove research
rm thoughts/research/*-[feature].md

# Remove handoffs
rm -rf thoughts/handoffs/[feature]/

# Remove validation/debug
rm thoughts/validation/*-[feature].md
rm thoughts/debug/*-[feature].md
```

### 8. Commit Artifact Removal

```bash
git add -A
git commit -m "chore: clean up [feature-name] working artifacts

Artifacts graduated to permanent documentation.
Original files preserved in git history."
```

### 9. Report Completion

```
Feature Graduated Successfully!
================================

Permanent Documentation Updated:
  ✓ SPECIFICATION.md - Feature behaviors and constraints
  ✓ CHANGELOG.md     - Implementation summary
  ✓ DECISIONS.md     - Architectural decisions

Artifacts Cleaned Up:
  - thoughts/specs/spec-[feature].md
  - thoughts/plans/tasks-*-[feature].md
  - thoughts/research/*-[feature].md
  - [other removed files]

Git History:
  All original artifacts preserved in git history.
  To recover: git show [commit]:[path]
```

## Guidelines

- **Verify completion first** - Don't graduate incomplete work
- **Synthesize, don't copy** - Permanent docs should be concise summaries
- **Preserve in git** - Original artifacts recoverable from history
- **Commit separately** - Docs update and cleanup are separate commits

## Dry Run

To preview what would be graduated without making changes:

```
/cmd:graduate [feature] --dry-run
```

This will show:
- Artifacts found
- What would be added to each permanent doc
- Files that would be deleted

## Output

- SPECIFICATION.md updated with feature behaviors
- CHANGELOG.md updated with implementation summary
- DECISIONS.md updated with architectural decisions (if applicable)
- All `thoughts/` artifacts for feature deleted
- Two commits: docs update + cleanup
