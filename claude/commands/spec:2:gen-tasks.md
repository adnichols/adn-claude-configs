---
description: Convert detailed specification directly to executable task list with full fidelity preservation
argument-hint: [Specification File Path]
---

# Rule: Direct Specification to Task Conversion with Full Fidelity

## Goal

To guide an AI assistant in converting a detailed specification document (created through collaborative planning) directly into executable task lists while preserving 100% fidelity to the original specification. This command bypasses complexity systems and PRD conversion to maintain exact scope boundaries and requirements as specified. Think harder.

## Core Principle: Specification Fidelity

**The specification is the absolute authority.** This command:

- Adds ZERO requirements beyond the specification
- Makes NO scope expansions or "improvements"
- Preserves ALL original decisions and constraints
- Creates tasks that implement EXACTLY what's written
- Uses fidelity-preserving agents that cannot modify scope

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
   - Inform user of draft location for review

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

### Development Notes

- Follow specification requirements exactly as written
- Do not add testing beyond what's specified
- Do not add security measures beyond what's specified
- Do not expand scope or "improve" requirements
- Question any ambiguity rather than assuming

## ⚙️ Implementation Phases

[Extract phases directly from specification structure]

### Phase 1: [Phase Name from Specification]

**Objective:** [Exact objective from specification]
**Timeline:** [As specified in original document]

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

## 📋 Specification Context

### [Technical Section 1 from Spec]

[Preserve relevant technical details from specification]

### [Technical Section 2 from Spec]

[Preserve architectural decisions from specification]

## 🚨 Implementation Requirements

### Fidelity Requirements (MANDATORY)

- Implement ONLY what's explicitly specified
- Do not add features, tests, or security beyond specification
- Question ambiguities rather than making assumptions
- Preserve all specification constraints and limitations

### Success Criteria

[Extract success criteria exactly from specification]

### Testing Requirements

[Extract testing requirements exactly as specified - do not add more]

### Security Requirements

[Extract security requirements exactly as specified - do not add more]

## ✅ Validation Checklist

- [ ] Implementation matches specification exactly
- [ ] No scope additions or "improvements" made
- [ ] All specification constraints preserved
- [ ] Success criteria from specification met
- [ ] No testing beyond what specification requires
- [ ] No security measures beyond specification requirements

## 📊 Completion Criteria

[Extract completion criteria exactly from specification]
```

## Key Principles

1. **Absolute Fidelity:** The specification is the complete and sole authority
2. **Zero Additions:** No requirements, tests, or features beyond specification
3. **Preserve Constraints:** Maintain all limitations and boundaries from specification
4. **Context Preservation:** Include necessary specification context in task file

## Success Indicators

A well-converted task list should:

- **100% Specification Match:** Every task maps directly to specification requirements
- **Zero Scope Creep:** No additions, improvements, or expansions beyond spec
- **Complete Context:** Implementer has all necessary information from specification
- **Clear Boundaries:** Explicit documentation of what's included/excluded
- **Validation Criteria:** Clear success measures extracted from specification

## Target Audience

This command serves teams that have:

- Detailed specifications from collaborative planning
- Need exact scope preservation
- Want direct specification-to-implementation workflow
- Require fidelity guarantees throughout implementation
- Must avoid scope creep or complexity-based additions
