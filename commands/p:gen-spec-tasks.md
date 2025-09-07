---
description: Convert a research plan into a comprehensive execution plan with router-driven complexity inheritance
argument-hint: [Files]
---

# Rule: Converting Research Plans to Execution Plans with Router Integration

## Goal

To guide an AI assistant in converting a comprehensive source document (like a strategy document, architecture plan, technical analysis, or research plan) into a detailed, step-by-step execution plan in Markdown format with YAML front-matter. The complexity router will inherit complexity information from the source specification and select appropriate agents for execution. Unlike basic task lists, this preserves ALL context from the source document to ensure the executing agent has complete understanding of the background, rationale, and implementation details. Think harder.

## Router Integration

This command integrates with the central complexity router to:

1. **Parse Source Specification Metadata:** Extract complexity information from specification YAML front-matter
2. **Inherit Complexity Level:** Use source specification's router-determined complexity for execution planning
3. **Select Appropriate Agents:** Use specification's selected agents for task implementation
4. **Scale Task Detail:** Adjust execution plan granularity based on complexity level
5. **Apply Validation Requirements:** Include complexity-appropriate testing and validation phases

## Input

The user will reference a specific source document file path that needs to be converted to an execution plan.

## Instructions

The AI will need to read and analyze the referenced source document file to create the execution plan.

## Output

- **Format:** Markdown (`.md`)
- **Location:** `/tasks/`
- **Filename:** `tasks-execution-[research-file-name].md` (e.g., `tasks-execution-claude-cli-integration-strategy.md`)

## Process

1. **Receive Source Document Reference:** The user points the AI to a specific source document file
2. **Parse Source Specification Metadata:** Extract complexity information from source specification YAML front-matter:
   - Router-determined complexity level
   - Selected agents (developer and reviewer)
   - Risk and nonfunctional requirements
   - Validation requirements
3. **Call Router for Execution Context:** Execute `bash .claude/commands/_lib/complexity/get-complexity.sh [source-spec-file]` to get:
   - Inherited complexity level
   - Validation requirements for the complexity level
   - Selected agents for implementation
4. **Read and Analyze Source Document:** The AI reads and analyzes the source document, extracting:
   - Executive summary and key requirements
   - Technical analysis and architectural decisions
   - Implementation designs and code examples
   - Security considerations and requirements
   - Performance implications and tradeoffs
   - Risk assessments and mitigation strategies
   - Success criteria and validation requirements
5. **Context Preservation with Complexity Awareness:** Unlike basic task generation, preserve the full context by:
   - Including relevant sections from the source document in the execution document
   - Maintaining code examples and technical specifications
   - Preserving rationale and decision-making context
   - Including security requirements and considerations scaled to complexity
   - Maintaining performance benchmarks and success criteria
6. **Complexity-Appropriate Execution Planning:** Convert the source document into actionable phases scaled by complexity:
   - **Minimum:** 3-5 essential phases with basic validation
   - **Basic:** 5-7 standard phases with unit testing requirements
   - **Moderate:** 7-10 comprehensive phases with integration testing
   - **Complex:** 10-15 enterprise phases with full compliance validation
7. **Phase 1: Generate High-Level Execution Plan:** Create the execution file with YAML front-matter containing:
   - Inherited metadata from source specification
   - Router-selected agents
   - Complexity-appropriate phases with clear objectives
   - Technical requirements and constraints
   - Success criteria for each phase scaled to complexity level
   - Present to user: "I have generated the high-level execution plan with full context preserved. Ready to generate the detailed sub-tasks? Respond with 'Go' to proceed."
8. **Wait for Confirmation:** Pause and wait for the user to respond with "Go"
9. **Phase 2: Generate Detailed Sub-Tasks with Validation:** Break down each phase into specific, actionable sub-tasks that:
   - Reference the preserved context and technical specifications
   - Include security requirements scaled to complexity level
   - Specify exact implementation details from the source document
   - Include complexity-appropriate validation and testing requirements
   - Include documentation tasks appropriate to complexity
   - Use router-selected agents for implementation
   - Maintain traceability back to the source document
10. **Identify Implementation Files:** Based on the source document and tasks, identify files that will need creation or modification
11. **Generate Final Output with Metadata:** Combine everything into the comprehensive execution plan with complete router metadata
12. **Save Execution Plan:** Save in `/tasks/` directory with filename `tasks-execution-[source-document-name].md` with complete metadata inheritance

## Output Format

The generated execution plan _must_ follow this structure with YAML front-matter:

```markdown
---
version: 1
complexity: [inherited from source spec]
source_spec: [path to source specification file]
agents:
  developer: [router-selected developer agent]
  reviewer: [router-selected reviewer agent]
risk: [inherited from source spec]
nonfunctional: [inherited from source spec]
routing:
  inherited_from: [source specification file]
  computed_score: [router score]
  validation_requirements: [router validation requirements]
  audit_trail: [router audit information]
---

# [Source Document Title] - Execution Plan

## 🎯 Executive Summary
[Preserve key insights and requirements from source document]

## 📋 Context & Background

### Analysis & Requirements
[Preserve relevant analysis from source document]

### Key Requirements
[Extract and list key technical requirements]

### Security Considerations
[Include security requirements and constraints]

### Performance & Quality Requirements
[Include performance benchmarks and quality criteria]

### Success Criteria
[Define clear success metrics from source document]

## 🗂️ Relevant Files

- `path/to/file1.ts` - [Description based on source document requirements]
- `path/to/file1.test.ts` - Unit tests for file1.ts
- `path/to/config.ts` - [Configuration changes needed per source document]
- `path/to/interface.ts` - [New interfaces/types from source document design]

### Notes

- Follow security hardening requirements from source document
- Implement performance monitoring as specified
- Use test commands defined in TESTING.md or CLAUDE.md

## ⚙️ Implementation Phases

### Phase 1: [Phase Name from Source Document] (Week X)
**Objective:** [Clear objective from source document]

**Technical Requirements:**
- [Specific requirement 1 from source document]
- [Specific requirement 2 from source document]

**Security Requirements:**
- [Security requirement 1 from source document]
- [Security requirement 2 from source document]

**Tasks:**
- [ ] 1.0 [High-level task name matching source document]
  - [ ] 1.1 [Specific sub-task with technical details]
  - [ ] 1.2 [Sub-task including security validation]
  - [ ] 1.3 [Sub-task with testing requirements]

### Phase 2: [Phase Name from Source Document] (Week Y)
**Objective:** [Clear objective from source document]

**Technical Requirements:**
- [Requirements specific to this phase]

**Tasks:**
- [ ] 2.0 [High-level task name]
  - [ ] 2.1 [Detailed sub-task]

### Phase N: Documentation & Integration (Final Phase)
**Objective:** Create comprehensive documentation and finalize feature integration

**Documentation Requirements:**
- Update README.md with new feature descriptions and usage
- Create/update API documentation for new interfaces  
- Generate user guides and configuration documentation
- Validate documentation accuracy against implementation

**Tasks:**
- [ ] N.0 Complete Feature Documentation
  - [ ] N.1 Run `/docs:update` to update comprehensive documentation
  - [ ] N.2 Update main README.md with feature overview and usage
  - [ ] N.3 Create/update API documentation for new endpoints/interfaces
  - [ ] N.4 Generate configuration documentation for new settings
  - [ ] N.5 Create user guides and integration examples  
  - [ ] N.6 Validate all documentation against actual implementation
  - [ ] N.7 Review documentation for completeness and accuracy

## 🔍 Technical Specifications

### [Technical Component 1]
[Preserve relevant code examples and specifications from source document]

```typescript
// Code example from source document
[Actual code block from source document]
```

### [Technical Component 2]

[Another technical specification with context]

## 🚨 Critical Requirements

### Security (MANDATORY)

[List all security requirements from source document]

### Performance Benchmarks

[Performance requirements and success metrics]

### Quality Gates

[Quality validation requirements]

## ✅ Validation & Testing Strategy

### Integration Testing Requirements

[Testing requirements from source document]

### Performance Validation

[Performance testing strategy]

### Security Validation

[Security testing requirements]

## 📊 Success Metrics

[Specific, measurable success criteria from source document]

```

## Interaction Model

The process requires a pause after generating the high-level execution plan to get user confirmation ("Go") before proceeding to generate detailed sub-tasks. This ensures the context preservation and phasing aligns with user expectations.

## Key Differences from Basic Task Generation

1. **Full Context Preservation:** Includes relevant sections, code examples, and technical specifications from the source document
2. **Technical Depth:** Maintains the technical depth and decision rationale from the source document
3. **Security Integration:** Explicitly includes security requirements and validation throughout
4. **Performance Awareness:** Includes performance benchmarks and monitoring requirements
5. **Comprehensive Validation:** Includes testing and validation strategies from the source document
6. **Traceability:** Maintains clear connections between tasks and source document rationale

## Target Audience

Assume the primary reader is a **developer** (junior to senior) who needs complete context to implement a complex technical plan without having to reference multiple documents. The execution plan should be self-contained with all necessary context.

# Task List Management

Guidelines for managing execution plans in markdown files to track progress on completing source document-driven implementations

## Task Implementation

- Do not proceed with tasks unless you are on a git branch other than main
- If needed, create a branch for the phase of work you are implementing
  - Parent agent (you) are responsible for git branch creation, not subagents
- **One sub-task at a time:** Do **NOT** start the next sub‑task until you ask the user for permission and they say "yes" or "y" UNLESS NOSUBCONF is specified by the user
- **Completion protocol:**
  1. When you finish a **sub‑task**, immediately mark it as completed by changing `[ ]` to `[x]`.
  2. If **all** subtasks underneath a parent task are now `[x]`, follow this sequence:
  - **First**: Run the full test suite as defined in TESTING.md or CLAUDE.md
  - **Only if all tests pass**: Stage changes (`git add .`)
  - **Clean up**: Remove any temporary files and temporary code before committing
  - **Commit**: Use a descriptive commit message that:
    - Uses conventional commit format (`feat:`, `fix:`, `refactor:`, etc.)
    - Summarizes what was accomplished in the parent task
    - Lists key changes and additions
    - References the phase number and source context
    - **Formats the message as a single-line command using `-m` flags**, e.g.:

      ```
      git commit -m "feat: implement CLI handler factory pattern" -m "- Add IClaudeHandler interface abstraction" -m "- Create factory for SDK/CLI toggle" -m "Related to Phase 1.3"
      ```
  3. Once all the subtasks are marked completed and changes have been committed, mark the **parent task** as completed.

- Stop after each sub‑task and wait for the user's go‑ahead UNLESS NOSUBCONF is specified by the user
- Always stop after phase completion, run full validation suite, and commit changes

## Execution Plan Maintenance

1. **Update the execution plan as you work:**
   - Mark tasks and subtasks as completed (`[x]`) per the protocol above
   - Add new tasks as they emerge during implementation
   - Update technical specifications if implementation details change

2. **Maintain the "Relevant Files" section:**
   - List every file created or modified during implementation
   - Update descriptions as implementation progresses
   - Add new files discovered during implementation

3. **Context Validation:**
   - Ensure implementation stays true to the source document's technical specifications
   - Validate security requirements are being followed
   - Confirm performance benchmarks are being met

## AI Instructions

When working with execution plans, the AI must:

1. Regularly update the execution plan file after finishing any significant work
2. Follow the enhanced completion protocol with security and performance validation
3. Reference the preserved context when making implementation decisions
4. Ensure traceability between implementation and source document rationale
5. Add newly discovered tasks while maintaining phase structure
6. Keep technical specifications updated as implementation progresses
7. Validate against success criteria throughout implementation
8. Before starting work, review the context section and technical requirements
9. After implementing a sub‑task, update the plan and pause for user approval
10. Ensure all security and performance requirements from source document are implemented
