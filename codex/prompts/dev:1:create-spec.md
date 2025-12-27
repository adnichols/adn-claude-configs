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
2. **Documentation Discovery:** Identify and optionally fetch documentation for key technologies (see Documentation Discovery section below)
3. **Requirements Analysis:** Based on research findings:
   - Analyze impact scope and integration needs
   - Identify functional requirements
   - Assess technical constraints and decisions
   - Evaluate integration complexity
4. **Deep Research Phase:** Conduct comprehensive research covering:
   - Core functionality and integration patterns
   - Testing approaches and security considerations
   - Performance considerations and reliability features
   - Implementation planning and dependencies
5. **Generate Specification:** Create complete document with all necessary sections
6. **Save Specification:** Save as `spec-[idea-name].md` in `thoughts/specs/` directory
7. **End Command:** The command completes after saving the specification. Task generation and implementation are separate phases.

## Parallel Research Strategy

Use the Task tool to spawn parallel research subagents for efficient codebase exploration. This accelerates research while preserving orchestrator context for synthesis.

### Subagent Delegation

Spawn parallel Task agents with `subagent_type=Explore`:

```
Task 1: Core Functionality Research
- Find existing implementations and patterns in codebase
- Locate relevant utilities and shared components
- Document integration points with existing systems

Task 2: Technical Research
- Analyze data modeling requirements
- Review security patterns used in codebase
- Identify testing approaches from existing tests
- **Identify paired dependencies requiring version alignment** (client/server packages, protocol pairs)
- **Flag infrastructure that may need smoke testing** before feature work

Task 3: Production Readiness Research
- Find performance patterns and optimization examples
- Locate monitoring/observability implementations
- Review deployment and configuration patterns
```

### Orchestrator Responsibilities

The parent agent (you) handles:
- Initial scope analysis and question formulation
- Synthesizing findings from all subagents
- Generating the final specification document
- User communication and clarifications

Wait for ALL subagents to complete before synthesizing findings into the specification.

## Documentation Discovery

After Initial Research identifies the technologies involved, proactively evaluate documentation needs before proceeding with deep research.

### Step 1: Identify Key Technologies

From Initial Research findings, extract:
- **Frameworks**: React, Vue, Next.js, Express, FastAPI, etc.
- **Libraries**: Lodash, Axios, Zod, Prisma, etc.
- **Languages/Runtimes**: TypeScript, Python, Rust, Node.js, etc.
- **Infrastructure**: PostgreSQL, Redis, Docker, Kubernetes, etc.

Focus on technologies that are:
- Core to the feature implementation
- Not already well-understood from codebase patterns
- Likely to require API reference during implementation

### Step 2: Check Existing Documentation

Check the `docs/` directory for existing documentation:

```bash
# Check what documentation is already available
ls -la docs/
```

Also check CLAUDE.md's "Available Documentation" section for reference.

### Step 3: Assess Documentation Needs

For each identified technology, determine:
1. **Already Available**: Documentation exists in `docs/` - no action needed
2. **Codebase Sufficient**: Existing code provides enough patterns - no action needed
3. **Should Fetch**: Would benefit from official documentation - offer to fetch
4. **Manual Required**: Documentation source not supported - guide user

### Step 4: Request User Permission

Use **AskUserQuestion** to present documentation options:

```
Question: "Should I fetch documentation for the following libraries to improve implementation guidance?"
Header: "Fetch docs"
multiSelect: true
Options:
- [Library 1] - Available via Context7 MCP
- [Library 2] - Available via Context7 MCP
- [Library 3] - Requires manual URL (not in Context7)
- Skip documentation fetching for now
```

**Checking Context7 Availability:**

Before presenting options, verify which libraries are available in Context7:
```
Use mcp__context7__resolve-library-id for each library
- If successful: Library is available via Context7
- If fails: Library requires manual URL or is not available
```

**Important Notes:**
- Always make documentation fetching optional
- The user may prefer to proceed without it
- Some documentation may require manual fetching

### Step 5: Fetch or Guide

**If user approves fetching:**

For libraries available in Context7, fetch directly using MCP tools:

```
1. mcp__context7__resolve-library-id(library_name)
2. mcp__context7__get-library-docs(resolved_id, topic="getting started")
3. Save to docs/libraries/[library-name]/
4. Update CLAUDE.md references
```

Alternatively, use the `/doc:fetch` command which handles this automatically:

```bash
/doc:fetch [library-name]
# or with version/topic
/doc:fetch [library-name] --version [version] --topic [topic]
```

Example:
```bash
/doc:fetch react --topic hooks
/doc:fetch prisma --version 5
/doc:fetch zod
```

**If documentation source is not available in Context7:**

Guide the user to fetch documentation manually:

```
The documentation for [library] is not available in Context7.

To add it manually:
1. Find the official documentation URL
2. Run: /doc:fetch [library] --url [documentation-url]

Or provide the URL and I can attempt to fetch it.
```

**Note:** Even without local documentation, you can still use Context7 directly during implementation by adding "use context7" to prompts.

### Step 6: Continue with Research

After documentation is fetched (or skipped), proceed to Requirements Analysis with enhanced context from:
- Newly fetched documentation in `docs/`
- Updated CLAUDE.md references
- Better API understanding for implementation decisions

### Documentation Discovery Best Practices

1. **Be Selective**: Only suggest fetching documentation that will meaningfully improve the specification
2. **Respect User Time**: Don't block on documentation - make it optional
3. **Batch Requests**: If multiple libraries need fetching, present them together
4. **Version Awareness**: Fetch documentation for the versions used in the project
5. **Fallback Gracefully**: If fetching fails, continue with codebase research

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

Use the **AskUserQuestion tool** when critical information is missing. This provides a better user experience than plain text questions.

### When to Ask

Only ask clarifying questions when:
- Research cannot proceed without the information
- The scope is fundamentally ambiguous
- Critical technical decisions need user input

### Example Questions

Use AskUserQuestion with structured options:

**If problem scope is unclear:**
```
Question: "Which best describes your vision for this feature?"
Header: "Scope"
Options:
- A simple feature addition to existing system
- An enhancement to current functionality
- A complete standalone application
- A developer tool or utility
```

**If target users are ambiguous:**
```
Question: "Who is the primary user for this feature?"
Header: "User type"
Options:
- End users (customers/clients)
- Internal team members
- Developers/technical users
- System administrators
```

**If backward compatibility might be relevant:**
```
Question: "Are there backward compatibility requirements?"
Header: "Compat"
Options:
- No - can break existing interfaces
- Yes - must maintain existing API compatibility
- Partial - some breaking changes acceptable
```

### AskUserQuestion Usage Notes

- Keep headers short (max 12 chars) - they appear as chips/tags
- Use `multiSelect: true` when choices aren't mutually exclusive
- Provide clear descriptions for each option
- Users always have an "Other" option for custom responses
- Ask 1-4 questions at a time, grouped logically

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

### Paired Dependencies (Version Alignment Required)

[List any client/server packages, protocol pairs, or infrastructure dependencies that MUST have matching versions]

| Package Pair | Required Alignment | Verification Notes |
|--------------|-------------------|-------------------|
| (e.g., @hocuspocus/provider ↔ @hocuspocus/server) | Same major version | Smoke test connectivity before feature work |

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

---

## ➡️ Next Steps

### Recommended: Multi-Model Review

Before generating tasks, consider having multiple AI models review the specification for critical feedback:

```bash
# Run in each tool (Claude, Gemini, Codex) to gather diverse perspectives
/review:spec thoughts/specs/spec-[idea-name].md
```

Each reviewer adds inline HTML comments with their identity (e.g., `<!-- [Claude] ... -->`). Reviews can respond to each other's feedback.

After all reviews complete, integrate the feedback:
```bash
/review:spec-integrate thoughts/specs/spec-[idea-name].md
```

This resolves all comments, asks for user decisions on ambiguous items, and produces a refined specification.

### Generate Tasks

When the specification is complete (and optionally reviewed), run:
```
/dev:2:gen-tasks thoughts/specs/spec-[idea-name].md
```
