---
description: Research an idea and produce a specification document with router-driven complexity determination
argument-hint: [Idea/Feature Description] [manual-complexity: minimum|basic|moderate|complex] (optional - router auto-detects)
---

# Rule: Research and Generate Specification Document

## Goal

To guide an AI assistant in researching a user's idea and creating a focused, practical specification document in Markdown format with YAML front-matter, using the complexity inheritance router for automatic complexity determination. This document will serve as input to downstream task generation commands with appropriate complexity-specific research depth. Think harder.

## Router Integration

This command integrates with the central complexity router (`scripts/route_complexity.py`) to:

1. **Auto-detect complexity** based on research findings and feature characteristics
2. **Select appropriate research depth** matching the complexity level
3. **Choose downstream agents** for task generation and implementation
4. **Apply validation requirements** for the specification quality

## Complexity Level Definitions

The specification scope is determined by the complexity level parameter:

### Minimum Level
**Scope:** Only functional requirements needed to solve the core problem
**Include:** Basic problem statement, simple technical approach, essential user interface
**Exclude:** Testing beyond validation, security beyond input handling, performance considerations, risk analysis

### Basic Level (DEFAULT)
**Scope:** Core functionality with essential quality measures
**Include:** Functional requirements, basic testing approach, essential security, simple error handling
**Exclude:** Performance optimization, backward compatibility, enterprise features, industry analysis

### Moderate Level  
**Scope:** Production-ready feature with appropriate quality measures
**Include:** Comprehensive design, testing strategy, security best practices, performance considerations, reliability features
**Exclude:** Enterprise compliance, complex backward compatibility, advanced deployment strategies

### Complex Level
**Scope:** Enterprise-grade implementation with full robustness
**Include:** All sections including backward compatibility, enterprise security, scalability planning, industry standards, comprehensive risk analysis

<simplicity_protocol>
MANDATORY PROTOCOL for complexity-appropriate scoping:

- Default to "basic" level unless complexity level is explicitly specified
- Never exceed the requested complexity level 
- Ask permission before researching areas beyond the specified complexity level
- Match research depth and specification detail to the complexity level

**This protocol applies throughout the research and specification process.**
  </simplicity_protocol>

## Input

The user will provide:
1. **Idea/Feature Description:** Initial concept or problem statement that needs research
2. **Complexity Level (Optional):** One of minimum|basic|moderate|complex (defaults to "basic")

## Instructions

The AI will need to:

1. Determine the complexity level (default to "basic" if not specified)
2. Analyze the user's idea for completeness within the complexity scope
3. Conduct research appropriate to the complexity level
4. Ask clarifying questions ONLY if critical information is missing for the specified complexity
5. Generate a specification document scoped to the complexity level

## Process

1. **Initial Research:** Conduct preliminary research to understand the idea's scope and characteristics
2. **Complexity Assessment:** Based on research findings, create initial complexity assessment:
   - Analyze impact scope (file/package/service/org level)
   - Identify performance requirements
   - Assess data sensitivity and security needs
   - Evaluate integration complexity
3. **Router Determination:** 
   - Call complexity router with assessment metadata
   - Get computed complexity level and agent selections
   - Apply manual override if specified (with justification)
4. **Deep Research Phase:** Conduct research appropriate to router-determined complexity:
   - **Minimum:** Core functionality and basic integration
   - **Basic:** Add testing approaches and essential security
   - **Moderate:** Add performance considerations and reliability features  
   - **Complex:** Add enterprise requirements and comprehensive analysis
5. **Generate Specification:** Create document with YAML front-matter containing router metadata
6. **Save Specification:** Save as `research-spec-[idea-name].md` in `/tasks/` directory
7. **End Command:** The command completes after saving the specification. Task generation and implementation are separate phases.

## Research Areas by Complexity Level

Research depth and breadth varies by complexity level:

### Core Research (All Complexity Levels)

**Always Include:**
- Existing implementations and design patterns  
- Framework and library recommendations (from current codebase)
- Basic integration with existing systems
- Core user journey and interface patterns
- Existing code patterns and conventions
- Available utilities and shared components

### Basic Level Research (Basic/Moderate/Complex)

**Add for Basic+ complexity:**
- Simple data modeling requirements
- Basic security considerations (input validation, authentication)
- Basic testing approaches (unit/integration tests)
- Essential error handling patterns
- Simple configuration patterns

### Moderate Level Research (Moderate/Complex Only)

**Add for Moderate+ complexity:**
- Performance considerations and optimization opportunities
- Comprehensive security best practices
- Reliability and resilience features
- Advanced testing strategies (E2E, load testing)
- Monitoring and observability basics
- Deployment considerations

### Complex Level Research (Complex Only)

**Add for Complex complexity:**
- Enterprise architecture considerations
- Industry standards and compliance requirements  
- Scalability and enterprise features
- Advanced deployment and monitoring strategies
- Backward compatibility analysis
- Comprehensive risk assessment
- Competitive and industry analysis

## Clarifying Questions (Only When Needed)

Ask questions using letter/number lists for easy selection. Examples:

**If complexity level needs clarification:**
"What complexity level should I target for this specification?
A) Minimum - Just core functionality, no testing/security considerations
B) Basic - Core functionality with basic testing and security (DEFAULT)
C) Moderate - Production-ready with performance and reliability features
D) Complex - Enterprise-grade with full robustness and compliance"

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

**If backward compatibility is relevant (Moderate/Complex levels only):**
"Are there backward compatibility requirements?
A) No - can break existing interfaces
B) Yes - must maintain existing API compatibility
C) Partial - some breaking changes acceptable
D) Not applicable"

## Output Format by Complexity Level

The specification document structure varies by complexity level:

### Minimum Level Template

```markdown
# [Idea Name] - Research Specification (Complexity: Minimum)

## 🎯 Executive Summary
[Basic problem and solution overview]

## 📊 Problem & Solution
### Core Problem
[Clear problem statement]

### Target Users  
[Primary users]

### Success Criteria
[What must work]

## 🏗️ Technical Design
### Implementation Strategy
[Simple technical approach]

### Data Requirements
[Basic data needs]

## 🎨 User Interface
### User Flow
[Core user steps]

### Interface Needs
[Essential UI elements]

## 📋 Specification Complete
[This specification is ready for task generation]
```

### Basic Level Template (DEFAULT)

```markdown
# [Idea Name] - Research Specification (Complexity: Basic)

## 🎯 Executive Summary
[Problem, solution, and core value]

## 🔍 Core Research Findings
### Technical Approach
[Implementation patterns from codebase]

### Integration Points
[Existing code pattern integration]

## 📊 Problem & Solution
### Core Problem
[Clear problem statement]

### Target Users
[Primary users and use cases]

### Success Criteria
[Success measurement]

## 🏗️ Technical Design
### Implementation Strategy
[Technical approach based on codebase]

### Data Requirements
[Data modeling needs]

### Basic Security
[Essential security considerations]

## 🎨 User Interface
### User Flow
[User interaction steps]

### Interface Needs
[UI requirements]

## 🧪 Testing Approach
### Test Strategy
[Basic testing approach]

## 📈 Implementation Plan
### Development Phases
[Simple phased approach]

### Key Dependencies
[Critical requirements]

## 📋 Specification Complete
[This specification is ready for task generation]
```

### Moderate Level Template

```markdown
# [Idea Name] - Research Specification (Complexity: Moderate)

## 🎯 Executive Summary
[Comprehensive problem, solution, value, and success criteria]

## 🔍 Core Research Findings
### Technical Approach
[Production-ready implementation patterns]

### Integration Points
[System integration considerations]

### Performance Considerations
[Performance requirements and approach]

## 📊 Problem & Solution
### Core Problem
[Detailed problem analysis]

### Target Users
[User personas and detailed use cases]

### Success Criteria
[Measurable success indicators]

## 🏗️ Technical Design
### Implementation Strategy
[Comprehensive technical architecture]

### Data Requirements
[Detailed data modeling and storage]

### Security & Reliability
[Security best practices and reliability features]

## 🎨 User Interface
### User Flow
[Detailed user journeys]

### Interface Needs
[Comprehensive UI/UX requirements]

## 🧪 Testing Approach
### Test Strategy
[Comprehensive testing including automation]

## ⚡ Performance & Reliability
### Performance Requirements
[Performance targets and monitoring]

### Error Handling
[Comprehensive error handling strategy]

## 📈 Implementation Plan
### Development Phases
[Phased approach with quality gates]

### Key Dependencies
[Technical and external dependencies]

### Risk Analysis
[Key risks and mitigation strategies]

## 📚 Research References
[Technical documentation and references]

## 📋 Specification Complete
[This specification is ready for task generation]
```

### Complex Level Template

```markdown
# [Idea Name] - Research Specification (Complexity: Complex)

## 🎯 Executive Summary
[Strategic overview including business impact]

## 🔍 Core Research Findings
### Technical Approach
[Enterprise-grade implementation architecture]

### Integration Points
[Comprehensive system integration strategy]

### Industry Analysis
[Competitive landscape and standards]

## 📊 Problem & Solution
### Core Problem
[Comprehensive problem analysis with context]

### Target Users
[Detailed user personas and enterprise use cases]

### Success Criteria
[Strategic and operational success metrics]

## 🏗️ Technical Design
### Implementation Strategy
[Enterprise architecture with scalability]

### Data Requirements
[Enterprise data modeling with governance]

### Security & Compliance
[Enterprise security and regulatory compliance]

## 🎨 User Interface
### User Flow
[Comprehensive user experience design]

### Interface Needs
[Enterprise UI/UX with accessibility]

## 🧪 Testing Approach
### Test Strategy
[Full testing pyramid including performance/security]

## ⚡ Performance & Scalability
### Performance Requirements
[Enterprise performance and scalability planning]

### Monitoring & Observability
[Comprehensive monitoring strategy]

## 🔒 Advanced Security & Compliance
### Security Architecture
[Enterprise security framework]

### Compliance Requirements
[Regulatory and industry compliance]

## 🔄 Backward Compatibility
### Compatibility Analysis
[Breaking changes and migration strategy]

### Migration Planning
[Enterprise migration approach]

## 📈 Implementation Plan
### Development Phases
[Enterprise project plan with risk management]

### Key Dependencies
[Comprehensive dependency analysis]

### Risk Analysis
[Enterprise risk assessment and mitigation]

## 📚 Research References
### Technical References
[Comprehensive technical documentation]

### Industry Standards
[Relevant standards and best practices]

## 📋 Specification Complete
[This specification is ready for task generation]
```

## Output

- **Format:** Markdown (`.md`)
- **Location:** `/tasks/`
- **Filename:** `research-spec-[complexity]-[idea-name].md`

## Key Principles

1. **Complexity Alignment:** Match specification depth exactly to requested complexity level
2. **Default to Basic:** Use "basic" complexity when level is not specified
3. **No Complexity Creep:** Never exceed the requested complexity level without permission
4. **Evidence-Based:** Ground recommendations in research appropriate to complexity level  
5. **Well-Defined:** Provide detail sufficient for downstream task generation at the target complexity
6. **Codebase Integration:** Prioritize existing patterns and conventions at all complexity levels

## Target Audience by Complexity Level

**Minimum:** Quick prototyping, proof-of-concept work
**Basic (Default):** Standard feature development with essential quality measures
**Moderate:** Production systems requiring reliability and performance
**Complex:** Enterprise systems with comprehensive requirements

## Success Indicators

A well-researched specification should:

- **Match Complexity Level:** Contain exactly the sections and detail appropriate to the specified complexity
- **Solve Core Problem:** Address the user's stated problem at the appropriate depth
- **Enable Execution:** Provide sufficient context for the `plan:generate-tasks-from-spec.md` command
- **Respect Constraints:** Stay within complexity boundaries and ask permission to exceed them
- **Follow Templates:** Use the complexity-appropriate template structure
