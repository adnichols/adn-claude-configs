---
description: Convert detailed specification directly to executable task list with full fidelity preservation
argument-hint: [Specification File Path]
---

# Rule: Direct Specification to Task Conversion with Full Fidelity

## Goal

To guide an AI assistant in converting a detailed specification document directly into executable task lists while preserving 100% fidelity to the original specification. This command maintains exact scope boundaries and requirements as specified.

## Core Principle: Specification Fidelity

**The specification is the absolute authority.** This command:

- Adds ZERO requirements beyond the specification
- Makes NO scope expansions or "improvements"
- Preserves ALL original decisions and constraints
- Creates tasks that implement EXACTLY what's written

## Input

The user will provide:

1. **Specification File Path:** Path to the detailed specification document. This may be provided in $ARGUMENTS

## Process

1. **Read Specification Completely:** Parse the entire specification document to understand:

   - All functional requirements
   - All technical constraints and decisions
   - Stated testing requirements (if any)
   - Stated security requirements (if any)
   - Performance requirements and success criteria
   - Implementation timeline and phases
   - Resource constraints
   - Explicit scope boundaries (what's included/excluded)
   - **Dependency compatibility notes** (convert advisory notes to verification tasks)
   - **Infrastructure prerequisites** (client/server pairs, protocol dependencies)

2. **Extract Task Structure:** Identify natural implementation phases from the specification:

   - Use specification's own phase structure if provided
   - Create logical groupings based on specification content
   - Maintain specification's dependencies
   - Preserve specification's success criteria for each phase

3. **Create and Save Task List:** Generate and save tasks that implement:

   - ONLY what's explicitly stated in the specification
   - Testing ONLY as specified (not more, not less)
   - Security ONLY as specified (not more, not less)
   - Performance measures ONLY as specified
   - Documentation ONLY as specified
   - Save tasks to `thoughts/plans/tasks-fidelity-[spec-name].md`

## Converting Advisory Notes to Verification Tasks

**CRITICAL:** Specifications often contain advisory notes like "Ensure X", "Verify Y", or "Make sure Z matches". These are NOT documentation—they are **implicit requirements** that must become explicit, checkable tasks.

### Common Advisory Patterns to Convert

| Spec Note Pattern | Task Conversion |
|-------------------|-----------------|
| "Ensure versions are compatible" | "Verify @pkg/client and @pkg/server are same major version" |
| "Make sure X is configured" | "Configure X and validate configuration works" |
| "Use compatible versions" | "Check package.json versions match, run smoke test" |
| "Verify before proceeding" | Add blocking task before dependent work |

### Infrastructure Verification Rule

When a specification introduces **paired dependencies** (client/server libraries, protocol-based packages, WebSocket connections):

1. **Create explicit verification task** before any feature work
2. **Add smoke test task** to confirm basic connectivity
3. **Block feature tasks** until verification passes

**Why this exists:** A spec note saying "ensure compatibility" is guidance that gets skipped. A task saying "verify versions match" is a checkbox that blocks progress.

## Final Task File Format

The final task file at `thoughts/plans/tasks-fidelity-[spec-name].md`:

```markdown
# [Specification Title] - Fidelity Implementation Tasks

## 🎯 Implementation Authority

**Source Specification:** [path to spec file]
**Implementation Scope:** Exactly as specified, no additions or modifications

### Specification Summary

[Brief summary of what's being implemented - extracted from spec]

### Implementation Boundaries

**Included:** [What specification explicitly includes]
**Excluded:** [What specification explicitly excludes]
**Testing Level:** [As specified in original document]
**Security Level:** [As specified in original document]
**Documentation Level:** [As specified in original document]

## 🗂️ Implementation Files

[List of files that will need creation/modification based on specification analysis]

### Paired Dependencies (Version Alignment Required)

[List any client/server packages, protocol pairs, or infrastructure dependencies that MUST have matching versions]

| Package Pair | Required Alignment | Verification Method |
|--------------|-------------------|---------------------|
| @example/client ↔ @example/server | Same major version | Check package.json, run connectivity test |

### Development Notes

- Follow specification requirements exactly as written
- Do not add testing beyond what's specified
- Do not add security measures beyond what's specified
- Do not expand scope or "improve" requirements without user approval
- Question any ambiguity rather than assuming

### Approval & Clarification Protocol

**When implementing agents encounter any of the following, they MUST stop and ask for user approval:**

1. **Scope Adjustments** - Any addition, removal, or modification to specified requirements
2. **Ambiguity** - Specification is unclear about implementation details
3. **Contradictions** - Specification conflicts with existing code patterns or constraints
4. **Technical Blockers** - A specified approach is infeasible or would cause issues
5. **Missing Information** - Critical details needed to proceed are not in the specification
6. **Better Alternatives** - A clearly superior approach is discovered during implementation

## ⚙️ Implementation Phases

[Extract phases directly from specification structure]

### Phase 0: Infrastructure Verification (if paired dependencies exist)

**Objective:** Validate infrastructure prerequisites before feature implementation
**Blocking:** All subsequent phases are blocked until Phase 0 passes

**Tasks:**

- [ ] 0.1 Verify paired package versions match
- [ ] 0.2 Smoke test infrastructure connectivity
- [ ] 0.3 Document verified configuration

### Phase 1: [Phase Name from Specification]

**Objective:** [Exact objective from specification]

**Specification Requirements:**
[List requirements exactly as written in specification]

**Tasks:**

- [ ] 1.0 [High-level task matching specification]
  - [ ] 1.1 [Specific implementation task from spec]
  - [ ] 1.2 [Another specific task from spec]
  - [ ] 1.3 [Validation task as specified]

### Phase N: Final Phase

**Objective:** Complete implementation as specified

**Tasks:**

- [ ] N.0 Finalize Implementation
  - [ ] N.1 Complete all specified deliverables
  - [ ] N.2 Validate against specification success criteria
  - [ ] N.3 Document implementation (if specified in original spec)

## 🚨 Implementation Requirements

### Fidelity Requirements (MANDATORY)

- Implement ONLY what's explicitly specified
- Do not add features, tests, or security beyond specification
- Question ambiguities rather than making assumptions
- Preserve all specification constraints and limitations

### Success Criteria

[Extract success criteria exactly from specification]

## ✅ Validation Checklist

- [ ] Implementation matches specification exactly
- [ ] No scope additions or "improvements" made
- [ ] All specification constraints preserved
- [ ] Success criteria from specification met
- [ ] **Paired dependencies verified compatible** (versions match)
- [ ] **Infrastructure smoke tested** before feature implementation
```

## Key Principles

1. **Absolute Fidelity:** The specification is the complete and sole authority
2. **Zero Additions:** No requirements, tests, or features beyond specification
3. **Preserve Constraints:** Maintain all limitations and boundaries from specification
4. **Context Preservation:** Include necessary specification context in task file
5. **Notes → Tasks:** Advisory notes ("ensure X", "verify Y") become explicit verification tasks
6. **Infrastructure First:** Paired dependencies get Phase 0 verification before feature work

---

## ➡️ Next Command

When the task list is complete and approved, run:
```
/dev:3:process-tasks [path-to-tasks]
```
