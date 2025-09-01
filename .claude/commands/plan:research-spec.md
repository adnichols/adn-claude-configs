---
description: Research an idea and produce a comprehensive specification document for execution planning
argument-hint: [Idea/Feature Description]
---

# Rule: Research and Generate Comprehensive Specification Document

## Goal

To guide an AI assistant in researching a user's idea and creating a detailed, comprehensive specification document in Markdown format. This document will serve as input to the `build:exec-spec.md` command and should contain all necessary context, research findings, technical analysis, and implementation guidance. Think harder. Avoid enterprise features unless specifically requested. Minimize scope additions beyond what is requested and focus on a viable increment that delivers on the request.

## Input

The user will provide an initial idea, feature concept, or problem statement that needs research and specification development.

## Instructions

The AI will need to:

1. Analyze the user's idea for completeness
2. Conduct comprehensive research (web search, codebase analysis, best practices)
3. Ask clarifying questions ONLY if critical information is missing
4. Generate a specification document with full research context

## Process

1. **Analyze Initial Idea:** Evaluate if the user's input contains sufficient detail for research
2. **Conditional Clarification:** Ask targeted questions ONLY if essential information is missing:
   - Target audience/users (if not clear from context)
   - Core problem being solved (if ambiguous)
   - Scope boundaries (if undefined)
   - Technical constraints (if relevant and unknown)
3. **Comprehensive Research Phase:**
   - **Industry Analysis:** Research current solutions, competitors, best practices
   - **Technical Research:** Investigate implementation patterns, frameworks, libraries
   - **Codebase Analysis:** Examine existing code for integration patterns and conventions
   - **Security Research:** Identify security considerations and requirements
   - **Performance Research:** Analyze performance implications and benchmarks
   - **User Experience Research:** Study UX patterns and accessibility requirements
4. **Specification Generation:** Create comprehensive document with research findings
5. **Save Specification:** Save as `research-spec-[idea-name].md` in `/tasks/` directory

## Research Areas (Think Harder)

For each idea, research should cover:

### Technical Research

- Existing implementations and design patterns
- Framework and library recommendations
- Architecture considerations
- Integration requirements with existing systems
- Data modeling and storage requirements
- API design patterns
- Performance optimization strategies

### Industry & Best Practices Research

- Current market solutions and approaches
- Industry standards and compliance requirements
- Accessibility standards (WCAG, etc.)
- Security best practices and threat models
- Testing strategies and quality assurance
- Deployment and monitoring considerations

### User Experience Research

- User journey mapping
- Interface design patterns
- Usability heuristics
- Mobile and responsive considerations
- Error handling and edge case UX

### Codebase Integration Research

- Existing code patterns and conventions
- Available utilities and shared components
- Configuration management approach
- Testing framework and patterns
- Build and deployment processes

## Clarifying Questions (Only When Needed)

Ask questions using letter/number lists for easy selection. Examples:

**If problem scope is unclear:**
"To better research this idea, I need to understand the scope. Which best describes your vision?
A) A complete standalone application
B) A feature addition to existing system  
C) An enhancement to current functionality
D) A developer tool or utility"

**If target users are ambiguous:**
"Who is the primary user for this feature?
A) End users (customers/clients)
B) Internal team members
C) Developers/technical users
D) System administrators"

**If technical constraints are unknown:**
"Are there any technical constraints I should research?
A) Must integrate with existing auth system
B) Performance requirements (high traffic/low latency)
C) Mobile-first or responsive requirements
D) Specific technology stack preferences
E) None/No constraints"

## Output Format

The specification document must follow this structure:

```markdown
# [Idea Name] - Research Specification

## 🎯 Executive Summary

[Concise overview of the idea and its value proposition]

## 🔍 Research Findings

### Industry Analysis

[Current solutions, competitors, market approaches]

### Technical Landscape

[Implementation patterns, frameworks, best practices found through research]

### User Experience Patterns

[UX research findings, design patterns, accessibility considerations]

## 📊 Problem Statement & Opportunity

### Problem Analysis

[Detailed analysis of the problem being solved]

### Target Users

[User personas and use cases based on research]

### Success Metrics

[How success will be measured]

## 🏗️ Technical Architecture

### Recommended Approach

[Technical strategy based on research findings]

### Integration Requirements

[How this integrates with existing systems based on codebase analysis]

### Data Architecture

[Data modeling and storage recommendations]

### Security Architecture

[Security requirements and implementation approach]

## 🎨 User Experience Design

### User Journey

[Step-by-step user interaction flow]

### Interface Requirements

[UI/UX specifications based on research]

### Accessibility Requirements

[WCAG compliance and accessibility considerations]

## ⚡ Performance & Scalability

### Performance Requirements

[Performance benchmarks and optimization strategies]

### Scalability Considerations

[How the solution scales based on research]

## 🔒 Security & Compliance

### Security Requirements

[Security analysis and requirements]

### Compliance Considerations

[Regulatory or compliance requirements if applicable]

## 🧪 Testing Strategy

### Testing Approach

[Comprehensive testing strategy based on best practices]

### Quality Assurance

[QA requirements and validation approach]

## 📈 Implementation Strategy

### Development Phases

[Logical breakdown of implementation phases]

### Risk Assessment

[Potential risks and mitigation strategies]

### Dependencies

[External dependencies and requirements]

## 📚 Research References

### Technical References

[Links to technical documentation, patterns, examples researched]

### Industry References

[Market research, competitor analysis, industry standards]

### Best Practice References

[Security, performance, accessibility guidelines researched]

## 🎯 Success Criteria

### Functional Success

[What the feature must accomplish]

### Technical Success

[Performance, security, quality metrics]

### User Success

[User satisfaction and adoption metrics]

## 📋 Next Steps

[Clear path to execution planning phase]
```

## Output

- **Format:** Markdown (`.md`)
- **Location:** `/tasks/`
- **Filename:** `research-spec-[idea-name].md`

## Key Principles

1. **Research First:** Conduct thorough research before specification
2. **Evidence-Based:** Ground all recommendations in research findings
3. **Implementation-Ready:** Provide sufficient detail for execution planning
4. **Context-Rich:** Include all necessary background and rationale
5. **Actionable:** Focus on specific, implementable requirements
6. **Quality-Focused:** Include security, performance, and accessibility from the start

## Target Audience

The specification document should be comprehensive enough that:

- A developer can understand the full context and requirements
- The `build:exec-spec.md` command has all necessary input
- Implementation decisions are grounded in research and best practices
- Security and performance considerations are built-in from the start

## Success Indicators

A well-researched specification should:

- Demonstrate thorough understanding of the problem space
- Provide evidence-based technical recommendations
- Include comprehensive security and performance analysis
- Offer clear implementation guidance based on research
- Serve as a complete input for execution planning
