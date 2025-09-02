---
description: Research an idea and produce a comprehensive specification document for execution planning
argument-hint: [Idea/Feature Description]
---

# Rule: Research and Generate Comprehensive Specification Document

## Goal

To guide an AI assistant in researching a user's idea and creating a focused, practical specification document in Markdown format. This document will serve as input to the `plan:generate-tasks-from-spec.md` command and should contain core functionality context, essential research findings, and straightforward implementation guidance. Think harder.

<simplicity_protocol>
MANDATORY PROTOCOL for scoping specifications:

- Avoid enterprise features unless specifically requested
- Avoid backward compatability unless requested.
- Avoid additional scope that was not requested
- Ask for permission before adding scope that you feel is critical or missing

**This protocol applies throughout the research and specification process.**
  </simplicity_protocol>

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
3. **Focused Research Phase:**
   - **Codebase Analysis:** Examine existing patterns and conventions (priority)
   - **Technical Research:** Find simple implementation approaches using existing tools
   - **Basic Security:** Identify essential security considerations only
   - **Extended Research:** Ask permission before researching enterprise features
4. **Specification Generation:** Create focused document with core research findings
5. **Save Specification:** Save as `research-spec-[idea-name].md` in `/tasks/` directory

## Research Areas (Think Harder)

Start with core research, ask permission before expanding to enterprise features:

### Core Technical Research

- Existing implementations and design patterns
- Framework and library recommendations (from current codebase)
- Basic integration with existing systems
- Simple data modeling requirements
- Basic security considerations

### Extended Research (Ask Permission First)

**Ask user before researching these areas:**
- Complex architecture considerations
- Performance optimization strategies
- Industry standards and compliance requirements
- Deployment and monitoring considerations
- Scalability and enterprise features

### User Experience Research

- Core user journey mapping
- Essential interface patterns
- Basic accessibility considerations
- Error handling for core functionality

### Codebase Integration Research

- Existing code patterns and conventions
- Available utilities and shared components
- Current testing approaches
- Existing configuration patterns

## Clarifying Questions (Only When Needed)

Ask questions using letter/number lists for easy selection. Examples:

**If problem scope is unclear:**
"To better research this idea, I need to understand the scope. Which best describes your vision?
A) A simple feature addition to existing system  
B) An enhancement to current functionality
C) A complete standalone application
D) A developer tool or utility"

**If additional scope might be needed:**
"Should I research additional enterprise features?
A) Keep it simple - core functionality only
B) Research performance optimization needs
C) Research compliance and security requirements  
D) Research scalability and enterprise features"

**If target users are ambiguous:**
"Who is the primary user for this feature?
A) End users (customers/clients)
B) Internal team members
C) Developers/technical users
D) System administrators"

**If backward compatibility is relevant:**
"Are there backward compatibility requirements?
A) No - can break existing interfaces
B) Yes - must maintain existing API compatibility
C) Partial - some breaking changes acceptable
D) Not applicable"

## Output Format

The specification document follows this structure (include only relevant sections):

```markdown
# [Idea Name] - Research Specification

## 🎯 Executive Summary

[Concise overview of the idea and its core value]

## 🔍 Core Research Findings

### Technical Approach

[Simple implementation patterns and framework recommendations from codebase]

### Integration Points

[How this fits with existing code patterns]

## 📊 Problem & Solution

### Core Problem

[Clear problem statement]

### Target Users

[Primary users and basic use cases]

### Success Criteria

[How success will be measured - keep simple]

## 🏗️ Technical Design

### Implementation Strategy

[Straightforward technical approach based on existing codebase]

### Data Requirements

[Simple data modeling needs]

### Basic Security

[Essential security considerations only]

## 🎨 User Interface

### User Flow

[Core user interaction steps]

### Interface Needs

[Essential UI requirements]

## 🧪 Testing Approach

### Test Strategy

[Basic testing approach based on current patterns]

---

## 📋 Enterprise Sections (Include only if requested)

### ⚡ Performance & Scalability (Optional)
[Include only if performance requirements specified]

### 🔒 Advanced Security & Compliance (Optional)
[Include only if compliance requirements specified]

### 📈 Industry Analysis (Optional)
[Include only if competitor research requested]

## 📈 Implementation Plan

### Development Phases

[Simple breakdown - typically MVP first, then iterations]

### Key Dependencies

[Critical external requirements only]

### Basic Risks

[Major risks and simple mitigation approaches]

## 📚 Research References

### Technical References

[Key documentation and examples found]

### Framework References

[Library and framework documentation used]

## 🎯 Success Criteria

### Core Functionality

[What the feature must accomplish]

### Quality Standards

[Basic performance and security requirements]

## 📋 Next Steps

[Clear path to execution planning phase]
```

## Output

- **Format:** Markdown (`.md`)
- **Location:** `/tasks/`
- **Filename:** `research-spec-[idea-name].md`

## Key Principles

1. **Simplicity First:** Start with core functionality, avoid enterprise features unless requested
2. **Ask Permission:** Get approval before adding scope beyond the original request  
3. **Evidence-Based:** Ground recommendations in codebase analysis and simple research
4. **Implementation-Ready:** Provide sufficient detail for execution planning
5. **Avoid Over-Engineering:** Focus on specific, simple, implementable requirements
6. **Essential Quality:** Include basic security and testing, advanced features only if requested

## Target Audience

The specification document should be focused enough that:

- A developer can understand the core requirements without complexity overload
- The `plan:generate-tasks-from-spec.md` command has necessary input for simple implementation
- Implementation decisions prioritize existing codebase patterns
- Enterprise features are clearly separated and optional

## Success Indicators

A well-researched specification should:

- Focus on solving the core problem stated by the user
- Provide simple, implementable technical recommendations
- Include only essential security and quality considerations
- Ask permission before adding enterprise scope
- Serve as input for straightforward execution planning
