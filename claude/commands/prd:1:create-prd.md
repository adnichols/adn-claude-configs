---
description: Generate a Product Requirements Document (PRD) with strict scope preservation and fidelity focus
argument-hint: [Feature Description]
---

# Rule: Generating a Product Requirements Document (PRD) with Fidelity Preservation

## Goal

To guide an AI assistant in creating a Product Requirements Document (PRD) in Markdown format with YAML front-matter, using a fidelity-preserving approach that captures exact requirements without scope expansion. The document creation is the sole purpose of this command - implementation is handled by separate commands.

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

2. **Analyze Existing Codebase:** Systematically discover relevant context:
   - Use Glob to find similar features: `**/*[pattern]*`
   - Use Grep to locate related APIs, services, components
   - Identify existing patterns and conventions
   - Review testing infrastructure and standards
   - Document build and deployment patterns
   - **Use parallel tool calls** to read multiple files simultaneously for faster analysis
   - Compile findings into "Technical Considerations" section of PRD

3. **Define Clear Boundaries:** Explicitly capture what's included and what's excluded based on requirements and codebase analysis

4. **Generate PRD with Fidelity Metadata:** Create PRD with YAML front-matter containing fidelity settings

5. **Validate PRD Completeness:**
   - Verify all required sections are present and complete
   - Check that codebase analysis findings are incorporated (if applicable)
   - Confirm YAML front-matter is complete and correct
   - Validate that requirements address the user's original problem
   - Verify scope boundaries are clearly defined (explicitly included/excluded)
   - Mark PRD as validated in YAML front-matter

6. **Save PRD:** Save as `prd-[feature-name].md` in `/tasks` directory with fidelity preservation settings

7. **End Command:** The command completes after saving the PRD. Implementation is a separate phase.

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
  creation_date: [timestamp YYYY-MM-DD]
  fidelity_level: absolute
  scope_changes: none
codebase_analyzed: true
validated: true
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

[Include findings from codebase analysis:]

### Existing Patterns
- [Relevant existing implementations found via Glob/Grep]
- [Similar features that can be referenced or extended]

### Integration Points
- [Existing APIs, services, or components to integrate with]
- [Shared utilities or patterns to leverage]

### Testing Infrastructure
- [Existing test patterns and frameworks to follow]
- [Test coverage expectations based on project standards]

[If no specific technical aspects mentioned by user, include only codebase findings above]

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

✅ **PRD Complete and Validated:** This document has been validated and contains all necessary information:
- All required sections are present and complete
- Codebase analysis findings have been incorporated
- YAML front-matter is complete and accurate
- Requirements address the user's original problem
- Scope boundaries are clearly defined (explicitly included/excluded)
- Ready for handoff to task generation (prd/2:gen-tasks)
```

## Key Principles

1. **Absolute Fidelity:** User requirements are the complete and sole authority
2. **Zero Additions:** No requirements, features, or scope beyond user specifications
3. **Codebase-Driven:** Use systematic Glob/Grep analysis to discover existing patterns and integration points
4. **Parallel Efficiency:** Use parallel tool calls for faster codebase analysis
5. **Validated Output:** Verify PRD completeness before handoff to task generation
6. **Clear Boundaries:** Explicit documentation of what's included and excluded
7. **Fidelity Agents:** Always use developer-fidelity and quality-reviewer-fidelity for implementation
8. **Scope Preservation:** Maintain all limitations and boundaries from original requirements

## Output Format

- **Format:** Markdown (`.md`)
- **Location:** `/tasks/`
- **Filename:** `prd-[feature-name].md`
- **Metadata:** Fidelity-preserving YAML front-matter

## Success Indicators

A well-crafted PRD should:

- **Complete YAML:** Include all metadata fields (fidelity settings, codebase_analyzed, validated)
- **Codebase Integration:** Include findings from systematic codebase analysis (Glob/Grep results)
- **Validated Structure:** Pass all completeness checks before handoff to task generation
- **Clear Scope Boundaries:** Explicit documentation of included and excluded functionality
- **Agent Specification:** Reference fidelity-preserving agents for implementation
- **Zero Scope Creep:** No additions, improvements, or expansions beyond user requirements
- **Complete Context:** All necessary information captured without external dependencies
- **Ready for Handoff:** Marked as complete and validated, ready for prd/2:gen-tasks

## Target Audience

This command serves teams that need:

- Exact requirement preservation without scope creep
- Clear boundaries between what's included and excluded
- Fidelity guarantees throughout the development process
- Simple, predictable PRD creation without complexity overhead
