---
description: Research an idea and produce a specification document
argument-hint: [Idea/Feature Description]
---

# Rule: Research and Generate Specification Document

## Goal

To guide an AI assistant in researching a user's idea and creating a focused, practical specification document in Markdown format with YAML front-matter. This document will serve as input to downstream task generation commands.

Also follow this repository's `AGENTS.md` for project-specific technical constraints, testing expectations, and security requirements.

## Research Approach

This command uses a standard research depth approach to create comprehensive specification documents that include:

1. Core functionality analysis based on research findings and feature characteristics.
2. Appropriate technical depth matching the requirements.
3. Integration considerations for existing codebase patterns.
4. Quality requirements appropriate for production-ready features where warranted.
  
**Operational note:** this workflow assumes web search and filesystem access are available so the agent can perform end-to-end research. If those capabilities are restricted, state the limitation clearly and proceed with the best specification you can produce from available context.

## Input

Consider any input from $ARGUMENTS

The user will provide:

1. **Idea/Feature Description:** Initial concept or problem statement that needs research

## Instructions

The AI will need to:

1. Analyze the user's idea for completeness and scope
2. Conduct comprehensive research on the feature
3. Ask clarifying questions if critical information is missing
4. Generate a complete specification document

## Process

1. **Initial Research:** Conduct preliminary research to understand the idea's scope and characteristics
2. **Requirements Analysis:** Based on research findings:
   - Analyze impact scope and integration needs
   - Identify functional requirements
   - Assess technical constraints and decisions
   - Evaluate integration complexity
3. **Deep Research Phase:** Conduct comprehensive research covering:
   - Core functionality and integration patterns
   - Testing approaches and security considerations
   - Performance considerations and reliability features
   - Implementation planning and dependencies
4. **Generate Specification:** Create complete document with all necessary sections
5. **Save Specification:** Save as `research-spec-[idea-name].md` in `/tasks/` directory
6. **End Command:** The command completes after saving the specification. Task generation and implementation are separate phases.

## Research Areas

The research should cover at least:

- Existing implementations, design patterns, and recommended frameworks/libraries (prefer those already used in the codebase).
- Integration with existing systems, APIs, and shared components.
- Data modeling and configuration requirements.
- Security considerations (input validation, authn/authz) and error handling patterns.
- Testing approaches (unit, integration, e2e) and quality gates.
- Performance, reliability, monitoring/observability, deployment, and backward compatibility (when applicable).

## Clarifying Questions (Only When Needed)

Ask clarifying questions only when needed to resolve important gaps. Prefer short letter/number option lists for quick selection, focusing on:

- Problem scope (simple addition, enhancement, standalone app, developer tool, etc.).
- Target users (end users, internal teams, developers, administrators).
- Backward compatibility expectations (no compatibility, must remain compatible, partial, or not applicable).

## Specification Template

The specification document uses this comprehensive structure:

```markdown
# [Idea Name] - Research Specification

## Executive Summary

[Comprehensive problem, solution, value, and success criteria]

## Core Research Findings

### Technical Approach

[Implementation patterns and architecture decisions from codebase research]

### Integration Points

[System integration considerations and existing code patterns]

### Performance Considerations

[Performance requirements, scalability needs, and optimization approach]

## 📊 Problem & Solution

### Core Problem

[Detailed problem analysis with context and background]

### Target Users

[User personas and detailed use cases]

### Success Criteria

[Measurable success indicators and acceptance criteria]

## 🏗️ Technical Design

### Implementation Strategy

[Comprehensive technical architecture and approach]

### Data Requirements

[Detailed data modeling, storage, and management considerations]

### Security & Reliability

[Security best practices, reliability features, and compliance requirements]

## User Interface

### User Flow

[Detailed user journeys and interaction patterns]

### Interface Needs

[Comprehensive UI/UX requirements and design considerations]

## Testing Approach

### Test Strategy

[Comprehensive testing including unit, integration, e2e, and performance tests]

### Quality Assurance

[Quality gates, validation processes, and acceptance testing]

## Performance & Reliability

### Performance Requirements

[Performance targets, monitoring, and optimization strategies]

### Error Handling

[Comprehensive error handling strategy and resilience patterns]

### Monitoring & Observability

[Logging, monitoring, metrics, and debugging considerations]

## Security & Compliance

### Security Architecture

[Security framework, authentication, authorization, and data protection]

### Compliance Requirements

[Regulatory compliance, industry standards, and security policies]

## Compatibility & Migration

### Backward Compatibility

[Breaking changes analysis and migration strategy (if applicable)]

### Integration Requirements

[API compatibility, data migration, and system integration needs]

## Implementation Plan

### Development Phases

[Phased approach with clear milestones and quality gates]

### Key Dependencies

[Technical dependencies, external systems, and critical requirements]

### Risk Analysis

[Risk assessment, mitigation strategies, and contingency planning]

## Research References

### Technical References

[Documentation, frameworks, libraries, and technical resources]

### Standards & Best Practices

[Industry standards, patterns, and recommended practices]

## Specification Complete

[This specification contains all necessary information for task generation and implementation]
```

## Output

- **Format:** Markdown (`.md`)
- **Location:** `/tasks/`
- **Filename:** `research-spec-[idea-name].md`

## Key Principles

1. **Comprehensive Coverage:** Include all necessary sections for production-ready implementation
2. **Evidence-Based:** Ground recommendations in thorough research and analysis
3. **Well-Defined:** Provide sufficient detail for downstream task generation and implementation
4. **Codebase Integration:** Prioritize existing patterns and conventions in implementation recommendations
5. Production-ready focus where appropriate: emphasize reliability, performance, and operability when the feature warrants it.
