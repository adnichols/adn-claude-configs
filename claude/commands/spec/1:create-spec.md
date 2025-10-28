---
description: Research an idea and produce a specification document
argument-hint: [Idea/Feature Description]
---

# Rule: Research and Generate Specification Document

## Goal

To guide an AI assistant in researching a user's idea and creating a focused, practical specification document in Markdown format with YAML front-matter. This document will serve as input to downstream task generation commands.

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

## Determine Specification Depth

Before starting research, determine the appropriate level of detail:

**Ask the user:**
"What level of specification detail do you need for this feature?

A) **Simple** - Basic technical approach, core functionality, and integration points only
B) **Standard** - Full technical design with testing, security, and implementation planning
C) **Comprehensive** - Enterprise-grade with compliance, monitoring, risk analysis, and migration
D) **Let me assess** - Analyze the feature and recommend appropriate depth"

**Depth Guidelines:**

- **Simple**: 6-8 sections (Executive Summary, Problem/Solution, Technical Design, Testing, Implementation Plan, References)
- **Standard**: 10-12 sections (adds Security, Performance, Compatibility)
- **Comprehensive**: Full 14-section template (adds Compliance, Monitoring, Risk Analysis, Migration)

## Instructions

The AI will need to:

1. Determine specification depth based on user input or feature analysis
2. Analyze the user's idea for completeness and scope
3. Conduct research appropriate to the chosen depth level
4. Ask clarifying questions if critical information is missing
5. Generate a complete specification document tailored to the depth level

## Process

1. **Initial Research:** Conduct preliminary research to understand the idea's scope and characteristics

2. **Codebase Analysis:** Systematically analyze the existing codebase for context:
   - Use Glob to find similar implementations: `**/*[feature-pattern]*`
   - Use Grep to locate relevant patterns, utilities, and conventions
   - Identify existing APIs, services, and integration points
   - Review testing infrastructure and patterns
   - Document build, deployment, and configuration patterns
   - **Use parallel tool calls** to read multiple files simultaneously for faster analysis
   - Compile findings into "Integration Points" section of spec

3. **Requirements Analysis:** Based on research findings and codebase analysis:
   - Analyze impact scope and integration needs
   - Identify functional requirements
   - Assess technical constraints and decisions
   - Evaluate integration complexity

4. **Deep Research Phase:** Conduct comprehensive research appropriate to chosen depth level:
   - Core functionality and integration patterns (all depths)
   - Testing approaches and security considerations (standard and comprehensive)
   - Performance considerations and reliability features (standard and comprehensive)
   - Implementation planning and dependencies (all depths)
   - Compliance, monitoring, and risk analysis (comprehensive only)

5. **Generate Specification:** Create complete document with sections appropriate to depth level

6. **Validate Specification Completeness:**
   - Verify all required sections for chosen depth level are present
   - Check that codebase analysis findings are incorporated
   - Confirm YAML front-matter is complete and correct
   - Validate that research addresses the user's original idea
   - Mark specification as complete in final section

7. **Save Specification:** Save as `research-spec-[idea-name].md` in `/tasks/` directory

8. **End Command:** The command completes after saving the specification. Task generation and implementation are separate phases.

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

The specification document uses this structure (sections vary by depth level):

```markdown
---
spec_type: technical_specification
complexity_level: [simple|standard|comprehensive]
fidelity_mode: strict
agents:
  developer: developer-fidelity
  reviewer: quality-reviewer-fidelity
created: [timestamp YYYY-MM-DD]
version: 1.0
source_type: research_specification
codebase_analyzed: true
---

# [Idea Name] - Research Specification

## 🎯 Executive Summary
*[All depths]*

[Comprehensive problem, solution, value, and success criteria]

## 🔍 Core Research Findings
*[All depths]*

### Technical Approach

[Implementation patterns and architecture decisions from codebase research]

### Integration Points

[System integration considerations and existing code patterns]

### Performance Considerations

[Performance requirements, scalability needs, and optimization approach]

## 📊 Problem & Solution
*[All depths]*

### Core Problem

[Detailed problem analysis with context and background]

### Target Users

[User personas and detailed use cases]

### Success Criteria

[Measurable success indicators and acceptance criteria]

## 🏗️ Technical Design
*[All depths]*

### Implementation Strategy

[Comprehensive technical architecture and approach]

### Data Requirements

[Detailed data modeling, storage, and management considerations]

### Security & Reliability
*[Standard and Comprehensive only]*

[Security best practices, reliability features, and compliance requirements]

## 🎨 User Interface
*[All depths - if applicable]*

### User Flow

[Detailed user journeys and interaction patterns]

### Interface Needs

[Comprehensive UI/UX requirements and design considerations]

## 🧪 Testing Approach
*[All depths]*

### Test Strategy

[Testing including unit, integration tests; e2e and performance for standard/comprehensive]

### Quality Assurance

[Quality gates, validation processes, and acceptance testing]

## ⚡ Performance & Reliability
*[Standard and Comprehensive only]*

### Performance Requirements

[Performance targets, monitoring, and optimization strategies]

### Error Handling

[Comprehensive error handling strategy and resilience patterns]

### Monitoring & Observability
*[Comprehensive only]*

[Logging, monitoring, metrics, and debugging considerations]

## 🔒 Security & Compliance
*[Comprehensive only]*

### Security Architecture

[Security framework, authentication, authorization, and data protection]

### Compliance Requirements

[Regulatory compliance, industry standards, and security policies]

## 🔄 Compatibility & Migration
*[Standard and Comprehensive - if applicable]*

### Backward Compatibility

[Breaking changes analysis and migration strategy (if applicable)]

### Integration Requirements

[API compatibility, data migration, and system integration needs]

## 📈 Implementation Plan
*[All depths]*

### Development Phases

[Phased approach with clear milestones and quality gates]

### Key Dependencies

[Technical dependencies, external systems, and critical requirements]

### Risk Analysis
*[Comprehensive only]*

[Risk assessment, mitigation strategies, and contingency planning]

## 📚 Research References
*[All depths]*

### Technical References

[Documentation, frameworks, libraries, and technical resources]

### Standards & Best Practices

[Industry standards, patterns, and recommended practices]

## 📋 Specification Complete
*[Required for all depths]*

✅ This specification has been validated and contains all necessary information for task generation and implementation:
- All required sections for `[complexity_level]` depth are present
- Codebase analysis findings have been incorporated
- YAML front-matter is complete and accurate
- Specification addresses the original user requirement
- Ready for handoff to task generation (spec/2:gen-tasks)
```

## Output

- **Format:** Markdown (`.md`)
- **Location:** `/tasks/`
- **Filename:** `research-spec-[idea-name].md`

## Key Principles

1. **Tailored Depth:** Match specification detail level to feature complexity (simple/standard/comprehensive)
2. **Codebase-Driven:** Use systematic Glob/Grep analysis to discover and leverage existing patterns
3. **Evidence-Based:** Ground recommendations in thorough research and codebase analysis
4. **Metadata Continuity:** Include YAML front-matter for fidelity tracking through workflow
5. **Parallel Efficiency:** Use parallel tool calls for faster codebase analysis
6. **Validated Output:** Verify specification completeness before handoff to task generation
7. **Production-Ready:** Focus on creating specifications suitable for reliable production systems

## Target Audience

This command is designed for feature development with flexible depth levels:

**Simple specs** for:
- Quick prototypes and proof-of-concept features
- Well-understood features with clear implementation patterns
- Internal tools with minimal compliance requirements

**Standard specs** for:
- Production features with typical security and performance needs
- Integration with existing systems requiring analysis
- Features needing comprehensive testing coverage

**Comprehensive specs** for:
- Enterprise-grade features with compliance requirements
- Complex integrations requiring risk analysis
- Features needing full observability and monitoring
- Mission-critical systems requiring extensive planning

## Success Indicators

A well-researched specification should:

- **Appropriate Depth:** Contain all sections required for chosen complexity level (simple/standard/comprehensive)
- **Codebase Integration:** Include findings from systematic codebase analysis (Glob/Grep results)
- **Complete Metadata:** Include YAML front-matter with fidelity settings and agent specifications
- **Validated Structure:** Pass all completeness checks before handoff to task generation
- **Solve Core Problem:** Address the user's stated problem with thorough analysis
- **Enable Execution:** Provide sufficient context for downstream task generation commands
- **Ready for Handoff:** Marked as complete and ready for spec/2:gen-tasks
