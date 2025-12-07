---
description: Research an idea and produce a specification document
argument-hint: [Idea/Feature Description]
---

# Rule: Research and Generate Specification Document

## Goal

To guide an AI assistant in researching a user's idea and creating a focused, practical specification document in Markdown format with YAML front-matter. This document will serve as input to downstream task generation commands. Think harder.

## Research Approach

This command uses a standard research depth approach to create comprehensive specification documents that include:

1. **Core functionality analysis** based on research findings and feature characteristics
2. **Appropriate technical depth** matching the requirements
3. **Integration considerations** for existing codebase patterns
4. **Standard quality requirements** for production-ready features

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
5. **Save Specification:** Save as `spec-[idea-name].md` in `thoughts/specs/` directory
6. **End Command:** The command completes after saving the specification. Task generation and implementation are separate phases.

## Research Areas

The research should comprehensively cover:

### Core Research (Always Include)

- Existing implementations and design patterns
- Framework and library recommendations (from current codebase)
- Integration with existing systems
- User journey and interface patterns
- Existing code patterns and conventions
- Available utilities and shared components

### Technical Research

- Data modeling requirements
- Security considerations (input validation, authentication, authorization)
- Testing approaches (unit, integration, e2e tests)
- Error handling patterns and edge cases
- Configuration and environment requirements

### Production Readiness Research

- Performance considerations and optimization opportunities
- Security best practices and compliance needs
- Reliability and resilience features
- Monitoring and observability requirements
- Deployment considerations and CI/CD integration
- Backward compatibility requirements (if applicable)

## Clarifying Questions (Only When Needed)

Ask questions using letter/number lists for easy selection. Examples:

**If problem scope is unclear:**
"To better research this idea, I need to understand the scope. Which best describes your vision?
A) A simple feature addition to existing system  
B) An enhancement to current functionality
C) A complete standalone application
D) A developer tool or utility"

**If target users are ambiguous:**
"Who is the primary user for this feature?
A) End users (customers/clients)
B) Internal team members
C) Developers/technical users
D) System administrators"

**If backward compatibility might be relevant:**
"Are there backward compatibility requirements?
A) No - can break existing interfaces
B) Yes - must maintain existing API compatibility
C) Partial - some breaking changes acceptable
D) Not applicable"

## Specification Template

The specification document uses this comprehensive structure:

```markdown
# [Idea Name] - Research Specification

## 🎯 Executive Summary

[Comprehensive problem, solution, value, and success criteria]

## 🔍 Core Research Findings

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

## 🎨 User Interface

### User Flow

[Detailed user journeys and interaction patterns]

### Interface Needs

[Comprehensive UI/UX requirements and design considerations]

## 🧪 Testing Approach

### Test Strategy

[Comprehensive testing including unit, integration, e2e, and performance tests]

### Quality Assurance

[Quality gates, validation processes, and acceptance testing]

## ⚡ Performance & Reliability

### Performance Requirements

[Performance targets, monitoring, and optimization strategies]

### Error Handling

[Comprehensive error handling strategy and resilience patterns]

### Monitoring & Observability

[Logging, monitoring, metrics, and debugging considerations]

## 🔒 Security & Compliance

### Security Architecture

[Security framework, authentication, authorization, and data protection]

### Compliance Requirements

[Regulatory compliance, industry standards, and security policies]

## 🔄 Compatibility & Migration

### Backward Compatibility

[Breaking changes analysis and migration strategy (if applicable)]

### Integration Requirements

[API compatibility, data migration, and system integration needs]

## 📈 Implementation Plan

### Development Phases

[Phased approach with clear milestones and quality gates]

### Key Dependencies

[Technical dependencies, external systems, and critical requirements]

### Risk Analysis

[Risk assessment, mitigation strategies, and contingency planning]

## 📚 Research References

### Technical References

[Documentation, frameworks, libraries, and technical resources]

### Standards & Best Practices

[Industry standards, patterns, and recommended practices]

## 📋 Specification Complete

[This specification contains all necessary information for task generation and implementation]
```

## Output

- **Format:** Markdown (`.md`)
- **Location:** `thoughts/specs/`
- **Filename:** `spec-[idea-name].md`

## Key Principles

1. **Comprehensive Coverage:** Include all necessary sections for production-ready implementation
2. **Evidence-Based:** Ground recommendations in thorough research and analysis
3. **Well-Defined:** Provide sufficient detail for downstream task generation and implementation
4. **Codebase Integration:** Prioritize existing patterns and conventions in implementation recommendations
5. **Production-Ready:** Focus on creating specifications suitable for reliable production systems

## Target Audience

This command is designed for standard feature development requiring:

- Production-ready quality with reliability and performance considerations
- Comprehensive technical planning and risk assessment
- Integration with existing systems and codebases
- Full testing, security, and monitoring coverage

## Success Indicators

A well-researched specification should:

- **Comprehensive Coverage:** Contain all sections needed for production implementation
- **Solve Core Problem:** Address the user's stated problem with thorough analysis
- **Enable Execution:** Provide sufficient context for downstream task generation commands
- **Technical Depth:** Include all necessary technical, security, and performance considerations
- **Follow Template:** Use the standardized comprehensive template structure
