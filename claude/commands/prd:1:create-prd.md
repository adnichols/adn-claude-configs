---
description: Generate a Product Requirements Document (PRD) with strict scope preservation and fidelity focus
argument-hint: [Feature Description]
---

# Rule: Generating a Product Requirements Document (PRD) with Fidelity Preservation

## Goal

To guide an AI assistant in creating a Product Requirements Document (PRD) in Markdown format with YAML front-matter, using a fidelity-preserving approach that captures exact requirements without scope expansion. The document creation is the sole purpose of this command - implementation is handled by separate commands. Think harder.

## Core Principle: Specification Fidelity

**The user's requirements are the absolute authority.** This command:

- Adds ZERO requirements beyond user specifications
- Makes NO scope expansions or "improvements"
- Preserves ALL original decisions and constraints
- Creates PRDs that document EXACTLY what's requested
- Uses fidelity-preserving agents that cannot modify scope

## Input

Some input may be provided via $ARGUMENTS

The user will provide:

1. **Feature Description:** Brief description or request for new functionality

## Process

1. **Gather Precise Requirements:** Ask focused questions to understand exact scope and boundaries
2. **Define Clear Boundaries:** Explicitly capture what's included and what's excluded
3. **Generate PRD with Fidelity Metadata:** Create PRD with YAML front-matter containing fidelity settings
4. **Save PRD:** Save as `prd-[feature-name].md` in `thoughts/plans/` directory with fidelity preservation settings
5. **End Command:** The command completes after saving the PRD. Implementation is a separate phase.

## Clarifying Questions for Scope Definition

Ask targeted questions to define precise boundaries:

### Core Scope Questions

**For problem clarity:**
"What specific problem does this feature solve?
A) [Suggested interpretation 1]
B) [Suggested interpretation 2]
C) [Suggested interpretation 3]
D) Other (please describe)"

**For user identification:**
"Who is the primary user of this feature?
A) End users (customers/clients)
B) Internal team members
C) Developers/technical users  
D) System administrators"

### Boundary Definition Questions

**For explicit inclusions:**
"What specific functionality should this feature include?
A) [Core functionality option 1]
B) [Core functionality option 2]
C) [Core functionality option 3]
D) Other (please specify)"

**For explicit exclusions:**
"Are there specific things this feature should NOT do?
A) No restrictions - implement all related functionality
B) Keep minimal - exclude complex features
C) Exclude certain capabilities (please specify which)
D) Exclude integration with other systems"

**For testing scope:**
"What level of testing is expected?
A) Basic functionality validation only
B) Comprehensive testing including edge cases
C) No specific testing requirements mentioned
D) Testing scope to be determined later"

**For security scope:**
"Are there specific security requirements?
A) Standard security practices
B) Enhanced security measures needed
C) No specific security requirements mentioned  
D) Security scope to be determined later"

## PRD Template Structure

### Unified Fidelity-Preserving Template

```markdown
---
version: 1
fidelity_mode: strict
agents:
  developer: developer-fidelity
  reviewer: quality-reviewer-fidelity
scope_preservation: true
additions_allowed: none
document_metadata:
  source_type: user_requirements
  creation_date: [timestamp]
  fidelity_level: absolute
  scope_changes: none
---

# [Feature Name] - Product Requirements Document

## Problem Statement

[Clear description of the specific problem being solved - exactly as understood from user input]

## Explicit Requirements

### Core Functionality

1. [Requirement 1 - exactly as specified by user]
2. [Requirement 2 - exactly as specified by user]
3. [Requirement 3 - exactly as specified by user]

### User Stories (if provided)

- As a [user type], I want to [action] so that [benefit]
- As a [user type], I want to [action] so that [benefit]

## Scope Boundaries

### Explicitly Included

- [Functionality that is clearly part of this PRD]
- [Features mentioned by user or clarified as included]

### Explicitly Excluded

- [Functionality that is clearly NOT part of this PRD]
- [Features explicitly ruled out during clarification]
- [Future considerations not in current scope]

### Assumptions & Clarifications

- [Any assumptions made during requirement gathering]
- [Areas where user provided specific clarification]

## Success Criteria

- [Measurable criteria tied directly to explicit requirements]
- [Success indicators that match specified functionality only]

## Testing Requirements

[Include only if user explicitly mentioned testing needs, otherwise use:]
Testing scope: To be determined during implementation phase

## Security Requirements

[Include only if user explicitly mentioned security needs, otherwise use:]
Security scope: To be determined during implementation phase

## Technical Considerations

[Include only technical aspects explicitly mentioned by user, otherwise use:]
Technical approach: To be determined during implementation phase

## Implementation Notes

### Fidelity Requirements (MANDATORY)

- Implement ONLY what's explicitly specified in this PRD
- Do not add features, tests, or security beyond requirements
- Question ambiguities rather than making assumptions
- Preserve all requirement constraints and limitations

### Next Steps

- Use developer-fidelity agent for implementation planning
- Use quality-reviewer-fidelity agent for validation
- Follow strict scope preservation throughout implementation

## Open Questions

- [Any remaining questions needing clarification before implementation]
- [Areas where user input was ambiguous and needs resolution]

## Document Status

✅ **PRD Complete:** This document captures the exact requirements as specified. Ready for fidelity-preserving implementation.
```

## Key Principles

1. **Absolute Fidelity:** User requirements are the complete and sole authority
2. **Zero Additions:** No requirements, features, or scope beyond user specifications
3. **Clear Boundaries:** Explicit documentation of what's included and excluded
4. **Fidelity Agents:** Always use developer-fidelity and quality-reviewer-fidelity for implementation
5. **Scope Preservation:** Maintain all limitations and boundaries from original requirements

## Output Format

- **Format:** Markdown (`.md`)
- **Location:** `thoughts/plans/`
- **Filename:** `prd-[feature-name].md`
- **Metadata:** Fidelity-preserving YAML front-matter

## Success Indicators

A well-crafted PRD should:

- **Fidelity Metadata:** Include complete YAML front-matter with fidelity settings
- **Clear Scope Boundaries:** Explicit documentation of included and excluded functionality
- **Agent Specification:** Reference fidelity-preserving agents for implementation
- **Zero Scope Creep:** No additions, improvements, or expansions beyond user requirements
- **Complete Context:** All necessary information captured without external dependencies

## Target Audience

This command serves teams that need:

- Exact requirement preservation without scope creep
- Clear boundaries between what's included and excluded
- Fidelity guarantees throughout the development process
- Simple, predictable PRD creation without complexity overhead
