---
description: Generate a Product Requirements Document (PRD) based on user input with router-driven complexity determination
argument-hint: [Feature Description] [manual-complexity: minimum|basic|moderate|complex] (optional - router auto-detects)
---

# Rule: Generating a Product Requirements Document (PRD)

## Goal

To guide an AI assistant in creating a Product Requirements Document (PRD) in Markdown format with YAML front-matter, using the complexity inheritance router for automatic complexity determination. The document creation is the sole purpose of this command - implementation is handled by separate commands. Think harder.

## Router Integration

This command integrates with the central complexity router (`.claude/commands/_lib/complexity/get-complexity.sh`) to:

1. **Auto-detect complexity** based on feature characteristics
2. **Select appropriate agents** for downstream tasks
3. **Apply validation requirements** matching the complexity level
4. **Create audit trail** for complexity determination decisions

## Complexity Level Definitions (Router-Driven)

The PRD scope is determined automatically by the router's scoring algorithm:

### Minimum Level (Score: 0-2)

**Auto-detected when:** Simple feature, file-level impact, no sensitive data, basic requirements
**Include:** Basic problem statement, core functionality, simple success criteria
**Exclude:** User stories, testing details, technical considerations, edge cases

### Basic Level (Score: 3-4)

**Auto-detected when:** Standard feature, package-level impact, basic user requirements
**Include:** Problem statement, user stories, functional requirements, non-goals, basic success metrics
**Exclude:** Performance requirements, detailed technical specs, risk analysis, dependencies

### Moderate Level (Score: 5-7)

**Auto-detected when:** Production feature, service-level impact, performance/security concerns
**Include:** All basic elements plus technical/design considerations, edge cases, dependencies, detailed testing approach
**Exclude:** Enterprise compliance, migration planning, scalability analysis

### Complex Level (Score: 8+)

**Auto-detected when:** Enterprise feature, org-wide impact, regulated data, compliance requirements
**Include:** All sections including risk analysis, compliance requirements, scalability planning, migration strategies

## Input

The user will provide:

1. **Feature Description:** Brief description or request for new functionality
2. **Manual Complexity Override (Optional):** One of minimum|basic|moderate|complex (overrides router auto-detection)

## Process

1. **Gather Initial Requirements:** Ask clarifying questions to understand feature scope and characteristics
2. **Determine Complexity Using Router:**
   - Analyze feature characteristics to score complexity factors
   - Call `bash .claude/commands/_lib/complexity/get-complexity.sh` with initial assessment
   - Use router output to determine final complexity level and selected agents
   - Apply manual override if specified (with required justification)
3. **Ask Complexity-Appropriate Questions:** Based on router-determined complexity level, ask additional questions for that level
4. **Generate PRD with Front-Matter:** Create PRD with YAML front-matter containing routing metadata
5. **Save PRD:** Save as `prd-[feature-name].md` in `/tasks` directory with full complexity metadata
6. **End Command:** The command completes after saving the PRD. Implementation is a separate phase.

## Clarifying Questions by Complexity Level

Questions should scale with complexity level:

### Core Questions (All Levels)

**If problem is unclear:**
"What problem does this feature solve?
A) [Suggested interpretation 1]
B) [Suggested interpretation 2]
C) [Suggested interpretation 3]
D) Other (please describe)"

**If target user is ambiguous:**
"Who is the primary user of this feature?
A) End users (customers/clients)
B) Internal team members
C) Developers/technical users
D) System administrators"

### Basic Level Questions (Basic/Moderate/Complex)

**For user stories:**
"Which user stories best describe this feature? (Select all that apply)
A) As a [user type], I want to [action] so that [benefit]
B) As a [user type], I want to [action] so that [benefit]
C) As a [user type], I want to [action] so that [benefit]
D) Other (please describe)"

**For scope boundaries:**
"Are there specific things this feature should NOT do?
A) No restrictions - implement fully
B) Limit to basic functionality
C) Exclude certain capabilities (please specify)
D) Keep minimal for now"

### Moderate Level Questions (Moderate/Complex Only)

**For technical approach:**
"What technical constraints should we consider?
A) Must integrate with existing systems
B) Performance is critical
C) Security is a primary concern
D) All of the above"

**For edge cases:**
"Which edge cases are most important to handle?
A) Error conditions and failures
B) High load/scale scenarios
C) Data validation and boundaries
D) All edge cases must be covered"

### Complex Level Questions (Complex Only)

**For compliance:**
"Are there compliance or regulatory requirements?
A) Industry standards (specify which)
B) Security compliance (SOC2, etc.)
C) Data privacy (GDPR, CCPA)
D) None/Not applicable"

**For migration:**
"Is backward compatibility required?
A) Full compatibility required
B) Migration path needed
C) Breaking changes acceptable
D) Not applicable"

## PRD Structure by Complexity Level

### Minimum Level Template

```markdown
---
version: 1
complexity: minimum # or auto for router determination
agents:
  developer: auto
  reviewer: auto
risk:
  blast_radius: file
  external_api_change: false
  migration: false
nonfunctional:
  perf_budget_ms_p95: null
  data_sensitivity: none
  backward_compat_required: false
routing:
  allow_override: true
  override_reason: ""
  computed_score: [router-filled]
  selected_agents: [router-filled]
  audit_trail: [router-filled]
---

# [Feature Name] - Product Requirements Document

## Overview

[Brief description of the feature and the problem it solves]

## Goals

- [Primary objective]
- [Secondary objectives if any]

## Core Requirements

1. [Essential requirement 1]
2. [Essential requirement 2]
3. [Essential requirement 3]

## Success Criteria

- [How we know it works]
- [Key success indicator]

## Document Complete

[This PRD is ready for review and task generation]
```

### Basic Level Template (DEFAULT)

```markdown
---
version: 1
complexity: auto # router will determine
agents:
  developer: auto
  reviewer: auto
risk:
  blast_radius: package
  external_api_change: false
  migration: false
nonfunctional:
  perf_budget_ms_p95: null
  data_sensitivity: none
  backward_compat_required: false
routing:
  allow_override: true
  override_reason: ""
  computed_score: [router-filled]
  selected_agents: [router-filled]
  audit_trail: [router-filled]
---

# [Feature Name] - Product Requirements Document

## Introduction/Overview

[Briefly describe the feature and the problem it solves. State the goal.]

## Goals

- [Specific, measurable objective 1]
- [Specific, measurable objective 2]
- [Specific, measurable objective 3]

## User Stories

- As a [type of user], I want to [perform an action] so that [benefit]
- As a [type of user], I want to [perform an action] so that [benefit]
- As a [type of user], I want to [perform an action] so that [benefit]

## Functional Requirements

1. The system must [specific functionality]
2. The system must [specific functionality]
3. The system must [specific functionality]
4. The system must [specific functionality]

## Non-Goals (Out of Scope)

- [What this feature will NOT include]
- [What this feature will NOT include]

## Success Metrics

- [How success will be measured]
- [Key performance indicator]

## Open Questions

- [Remaining questions needing clarification]
- [Areas needing further discussion]

## Document Complete

[This PRD is ready for review and task generation]
```

### Moderate Level Template

```markdown
# [Feature Name] - Product Requirements Document (Complexity: Moderate)

## Introduction/Overview

[Comprehensive description of the feature, problem it solves, and strategic value]

## Goals

- [Primary strategic objective]
- [Measurable business outcome]
- [Technical objective]
- [User experience objective]

## User Stories

### Primary User Stories

- As a [type of user], I want to [perform an action] so that [benefit]
- As a [type of user], I want to [perform an action] so that [benefit]

### Secondary User Stories

- As a [type of user], I want to [perform an action] so that [benefit]
- As a [type of user], I want to [perform an action] so that [benefit]

## Functional Requirements

### Core Requirements

1. The system must [specific functionality with acceptance criteria]
2. The system must [specific functionality with acceptance criteria]

### Extended Requirements

3. The system should [additional functionality]
4. The system should [additional functionality]

## Non-Goals (Out of Scope)

- [Explicitly excluded functionality]
- [Features for future phases]

## Design Considerations

### User Interface

- [UI/UX requirements or mockup references]
- [Interaction patterns]

### User Experience

- [Key user flows]
- [Accessibility requirements]

## Technical Considerations

### Architecture

- [High-level technical approach]
- [Integration points]

### Security

- [Security requirements]
- [Data protection needs]

### Performance

- [Performance targets]
- [Scalability considerations]

## Edge Cases & Error Handling

- [Important edge case 1]
- [Important edge case 2]
- [Error handling approach]

## Dependencies

### Technical Dependencies

- [Required systems or services]
- [External APIs or libraries]

### Team Dependencies

- [Other teams involved]
- [External stakeholders]

## Success Metrics

### Quantitative Metrics

- [Measurable KPI with target]
- [Performance metric with threshold]

### Qualitative Metrics

- [User satisfaction indicator]
- [Quality measure]

## Testing Approach

- [Testing strategy]
- [Test coverage requirements]

## Open Questions

- [Technical questions needing resolution]
- [Business questions needing clarification]

## Document Complete

[This PRD is ready for review and task generation]
```

### Complex Level Template

```markdown
# [Feature Name] - Product Requirements Document (Complexity: Complex)

## Executive Summary

[Strategic overview including business impact, ROI, and alignment with company objectives]

## Problem Statement

### Current State

[Detailed analysis of current situation]

### Desired State

[Vision for future state]

### Gap Analysis

[What needs to change]

## Goals & Objectives

### Strategic Goals

- [Long-term strategic objective]
- [Business transformation goal]

### Tactical Objectives

- [Measurable objective with timeline]
- [Specific deliverable with success criteria]

## Stakeholders

### Primary Stakeholders

- [Stakeholder group]: [Their needs and concerns]
- [Stakeholder group]: [Their needs and concerns]

### Secondary Stakeholders

- [Stakeholder group]: [Impact on them]

## User Stories & Personas

### User Personas

#### Persona 1: [Name]

- Background: [Context]
- Needs: [What they need]
- Pain Points: [Current problems]

### Epic User Stories

- Epic: [High-level story]
  - Story 1: As a [user], I want [action] so that [benefit]
  - Story 2: As a [user], I want [action] so that [benefit]

## Functional Requirements

### Critical Requirements (P0)

1. The system MUST [requirement with detailed acceptance criteria]
2. The system MUST [requirement with detailed acceptance criteria]

### High Priority Requirements (P1)

3. The system SHOULD [requirement with acceptance criteria]
4. The system SHOULD [requirement with acceptance criteria]

### Medium Priority Requirements (P2)

5. The system COULD [nice-to-have requirement]

## Non-Functional Requirements

### Performance Requirements

- Response time: [Specific targets]
- Throughput: [Transactions per second]
- Availability: [Uptime requirements]

### Security Requirements

- Authentication: [Requirements]
- Authorization: [Access control needs]
- Data Protection: [Encryption, compliance]

### Scalability Requirements

- User Scale: [Expected growth]
- Data Scale: [Volume projections]
- Geographic Scale: [Regional considerations]

## Design Specifications

### User Interface Design

- [Detailed UI requirements]
- [Design system compliance]
- [Accessibility standards (WCAG)]

### System Architecture

- [Architectural decisions]
- [Technology stack]
- [Integration architecture]

## Technical Specifications

### Data Model

- [Key entities and relationships]
- [Data governance requirements]

### API Specifications

- [API contracts]
- [Versioning strategy]

### Infrastructure Requirements

- [Compute resources]
- [Storage requirements]
- [Network considerations]

## Compliance & Regulatory

### Regulatory Requirements

- [Specific regulations (GDPR, HIPAA, etc.)]
- [Compliance checkpoints]

### Industry Standards

- [Relevant standards to follow]
- [Certification requirements]

## Risk Analysis

### Technical Risks

| Risk     | Probability  | Impact       | Mitigation            |
| -------- | ------------ | ------------ | --------------------- |
| [Risk 1] | High/Med/Low | High/Med/Low | [Mitigation strategy] |

### Business Risks

| Risk     | Probability  | Impact       | Mitigation            |
| -------- | ------------ | ------------ | --------------------- |
| [Risk 1] | High/Med/Low | High/Med/Low | [Mitigation strategy] |

## Dependencies & Constraints

### Hard Dependencies

- [Blocking dependency with timeline]
- [Critical path items]

### Soft Dependencies

- [Preferred sequencing]
- [Optimization opportunities]

### Constraints

- Budget: [Financial constraints]
- Timeline: [Key deadlines]
- Resources: [Team/skill constraints]

## Migration & Rollout Strategy

### Migration Plan

- Phase 1: [Initial rollout]
- Phase 2: [Expansion]
- Phase 3: [Full deployment]

### Rollback Plan

- [Rollback triggers]
- [Rollback procedure]

## Success Metrics & KPIs

### Business Metrics

- [Revenue impact with target]
- [Cost savings with target]
- [User adoption with target]

### Technical Metrics

- [System performance with SLA]
- [Error rate thresholds]
- [Operational efficiency measures]

### Leading Indicators

- [Early success signals]
- [Progress tracking metrics]

## Testing & Quality Assurance

### Test Strategy

- Unit Testing: [Coverage requirements]
- Integration Testing: [Scope]
- Performance Testing: [Load profiles]
- Security Testing: [Penetration testing needs]
- UAT: [User acceptance criteria]

### Quality Gates

- [Release criteria]
- [Go/No-go decision points]

## Documentation Requirements

- [User documentation needs]
- [Technical documentation]
- [Training materials]

## Support & Maintenance

### Support Model

- [Support tier requirements]
- [SLA definitions]

### Maintenance Plan

- [Ongoing maintenance needs]
- [Update/patch strategy]

## Timeline & Milestones

### Key Milestones

| Milestone     | Date   | Deliverables   |
| ------------- | ------ | -------------- |
| [Milestone 1] | [Date] | [Deliverables] |

### Critical Path

[Gantt chart or timeline visualization reference]

## Budget & Resources

### Budget Allocation

- Development: [Amount/percentage]
- Infrastructure: [Amount/percentage]
- Operations: [Amount/percentage]

### Resource Requirements

- Engineering: [FTE needs]
- Design: [FTE needs]
- QA: [FTE needs]

## Open Questions & Decisions Needed

### Immediate Decisions Required

- [Decision 1 with options and recommendation]
- [Decision 2 with options and recommendation]

### Future Considerations

- [Long-term questions]
- [Strategic decisions for later phases]

## Appendices

### A. Glossary

[Key terms and definitions]

### B. References

[Related documents and resources]

### C. Revision History

| Version | Date   | Author   | Changes       |
| ------- | ------ | -------- | ------------- |
| 1.0     | [Date] | [Author] | Initial draft |

## Document Complete

[This PRD is ready for review and task generation]
```

## Target Audience by Complexity Level

**Minimum:** Junior developers needing basic direction for simple features
**Basic (Default):** Development teams implementing standard features
**Moderate:** Cross-functional teams building production features
**Complex:** Enterprise teams with multiple stakeholders and governance requirements

## Output

- **Format:** Markdown (`.md`)
- **Location:** `/tasks/`
- **Filename:** `prd-[complexity]-[feature-name].md`

## Router Integration Instructions

### Step-by-Step Router Usage

1. **Gather Requirements:** Ask initial clarifying questions to understand:

   - Feature scope and impact
   - Performance requirements
   - Data sensitivity level
   - Integration complexity
   - Security considerations

2. **Create Temporary Assessment File:** Create a temp file with initial metadata:

   ```yaml
   ---
   version: 1
   complexity: auto
   risk:
     blast_radius: [file|package|service|org]
     external_api_change: [true|false]
     migration: [true|false]
   nonfunctional:
     perf_budget_ms_p95: [number or null]
     data_sensitivity: [none|pii|regulated]
     backward_compat_required: [true|false]
   ---
   ```

3. **Call Router:** Execute `bash .claude/commands/_lib/complexity/get-complexity.sh temp_assessment.md`

4. **Use Router Output:** Parse the JSON response to get:

   - `computed_complexity.computed_level` (final complexity)
   - `selected_agents.developer` and `selected_agents.quality_reviewer`
   - `validation_requirements` (what validations to apply)

5. **Generate PRD:** Use the router-determined complexity level to create the appropriate PRD structure

6. **Include Router Metadata:** Add the router output to the YAML front-matter:
   ```yaml
   routing:
     computed_score: [router total score]
     selected_agents:
       developer: [router-selected agent]
       reviewer: [router-selected agent]
     audit_trail: [router audit information]
   ```

### Override Handling

If user specifies manual complexity override:

- Require justification in `override_reason` field
- Use `--strict` flag when calling router to validate override
- Document override rationale in the PRD

## Final Instructions

1. **Use Router First:** Always determine complexity using the router before generating content
2. **Respect Router Output:** Use the router-determined complexity level and agents
3. **Include Full Metadata:** Embed complete routing metadata in YAML front-matter
4. **Document Decisions:** Include audit trail showing how complexity was determined
5. **Validate Overrides:** Require justification for any manual complexity overrides

## Success Indicators

A well-crafted PRD should:

- **Router Integration:** Include complete YAML front-matter with router metadata
- **Appropriate Complexity:** Match the router-determined complexity level exactly
- **Agent Selection:** Reference the router-selected agents for next steps
- **Clear Audit Trail:** Show how complexity determination was made
- **Override Documentation:** If overridden, clearly document the reasoning
