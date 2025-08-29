---
description: Convert a research plan into a comprehensive execution plan with full context
argument-hint: [Research Plan File]
---

# Rule: Converting Research Plans to Execution Plans

## Goal

To guide an AI assistant in converting a comprehensive research plan (like a strategy document, architecture plan, or technical analysis) into a detailed, step-by-step execution plan in Markdown format. Unlike basic task lists, this preserves ALL context from the research plan to ensure the executing agent has complete understanding of the background, rationale, and implementation details. Think harder.

## Output

- **Format:** Markdown (`.md`)
- **Location:** `/tasks/`
- **Filename:** `tasks-execution-[research-file-name].md` (e.g., `tasks-execution-claude-cli-integration-strategy.md`)

## Process

1. **Receive Research Plan Reference:** The user points the AI to a specific research plan file
2. **Deep Analysis:** The AI reads and analyzes the entire research document, extracting:
   - Executive summary and key insights
   - Technical analysis and architectural decisions
   - Implementation designs and code examples
   - Security considerations and requirements
   - Performance implications and tradeoffs
   - Risk assessments and mitigation strategies
   - Success criteria and validation requirements
3. **Context Preservation:** Unlike basic task generation, preserve the full context by:
   - Including relevant sections from the research plan in the execution document
   - Maintaining code examples and technical specifications
   - Preserving rationale and decision-making context
   - Including security requirements and considerations
   - Maintaining performance benchmarks and success criteria
4. **Execution Planning:** Convert the research plan into actionable phases:
   - Break down the implementation plan into logical phases
   - Identify dependencies between phases
   - Extract specific technical requirements for each phase
   - Maintain the original phasing and sequencing from research
5. **Phase 1: Generate High-Level Execution Plan:** Create the execution file with:
   - Full context section (preserving key research insights)
   - High-level phases with clear objectives
   - Technical requirements and constraints
   - Success criteria for each phase
   - Present to user: "I have generated the high-level execution plan with full context preserved. Ready to generate the detailed sub-tasks? Respond with 'Go' to proceed."
6. **Wait for Confirmation:** Pause and wait for the user to respond with "Go"
7. **Phase 2: Generate Detailed Sub-Tasks:** Break down each phase into specific, actionable sub-tasks that:
   - Reference the preserved context and technical specifications
   - Include security requirements where applicable
   - Specify exact implementation details from the research
   - Include validation and testing requirements
   - Maintain traceability back to the research plan
8. **Identify Implementation Files:** Based on the research and tasks, identify files that will need creation or modification
9. **Generate Final Output:** Combine everything into the comprehensive execution plan
10. **Save Execution Plan:** Save in `/tasks/` directory with filename `tasks-execution-[research-file-name].md`

## Output Format

The generated execution plan _must_ follow this structure:

```markdown
# [Research Plan Title] - Execution Plan

## 🎯 Executive Summary
[Preserve key insights and objectives from research plan]

## 📋 Context & Background

### Technical Analysis
[Preserve relevant technical analysis from research plan]

### Key Requirements
[Extract and list key technical requirements]

### Security Considerations
[Include security requirements and constraints]

### Performance & Quality Requirements
[Include performance benchmarks and quality criteria]

### Success Criteria
[Define clear success metrics from research plan]

## 🗂️ Relevant Files

- `path/to/file1.ts` - [Description based on research plan requirements]
- `path/to/file1.test.ts` - Unit tests for file1.ts
- `path/to/config.ts` - [Configuration changes needed per research]
- `path/to/interface.ts` - [New interfaces/types from research design]

### Notes

- Follow security hardening requirements from research plan
- Implement performance monitoring as specified
- Use test commands defined in TESTING.md or CLAUDE.md

## ⚙️ Implementation Phases

### Phase 1: [Phase Name from Research] (Week X)
**Objective:** [Clear objective from research plan]

**Technical Requirements:**
- [Specific requirement 1 from research]
- [Specific requirement 2 from research]

**Security Requirements:**
- [Security requirement 1 from research]
- [Security requirement 2 from research]

**Tasks:**
- [ ] 1.0 [High-level task name matching research plan]
  - [ ] 1.1 [Specific sub-task with technical details]
  - [ ] 1.2 [Sub-task including security validation]
  - [ ] 1.3 [Sub-task with testing requirements]

### Phase 2: [Phase Name from Research] (Week Y)
**Objective:** [Clear objective from research plan]

**Technical Requirements:**
- [Requirements specific to this phase]

**Tasks:**
- [ ] 2.0 [High-level task name]
  - [ ] 2.1 [Detailed sub-task]

## 🔍 Technical Specifications

### [Technical Component 1]
[Preserve relevant code examples and specifications from research]

```typescript
// Code example from research plan
[Actual code block from research]
```

### [Technical Component 2]
[Another technical specification with context]

## 🚨 Critical Requirements

### Security (MANDATORY)
[List all security requirements from research plan]

### Performance Benchmarks
[Performance requirements and success metrics]

### Quality Gates
[Quality validation requirements]

## ✅ Validation & Testing Strategy

### Integration Testing Requirements
[Testing requirements from research plan]

### Performance Validation
[Performance testing strategy]

### Security Validation
[Security testing requirements]

## 📊 Success Metrics
[Specific, measurable success criteria from research plan]
```

## Interaction Model

The process requires a pause after generating the high-level execution plan to get user confirmation ("Go") before proceeding to generate detailed sub-tasks. This ensures the context preservation and phasing aligns with user expectations.

## Key Differences from Basic Task Generation

1. **Full Context Preservation:** Includes relevant sections, code examples, and technical specifications from the research plan
2. **Technical Depth:** Maintains the technical depth and decision rationale from the research
3. **Security Integration:** Explicitly includes security requirements and validation throughout
4. **Performance Awareness:** Includes performance benchmarks and monitoring requirements
5. **Comprehensive Validation:** Includes testing and validation strategies from the research
6. **Traceability:** Maintains clear connections between tasks and research rationale

## Target Audience

Assume the primary reader is a **developer** (junior to senior) who needs complete context to implement a complex technical plan without having to reference multiple documents. The execution plan should be self-contained with all necessary context.

# Task List Management

Guidelines for managing execution plans in markdown files to track progress on completing research-driven implementations

## Task Implementation

- Do not proceed with tasks unless you are on a git branch other than main
- If needed, create a branch for the phase of work you are implementing
  - Parent agent (you) are responsible for git branch creation, not subagents
- **One sub-task at a time:** Do **NOT** start the next sub‑task until you ask the user for permission and they say "yes" or "y" UNLESS NOSUBCONF is specified by the user
- **Completion protocol:**
  1. When you finish a **sub‑task**, immediately mark it as completed by changing `[ ]` to `[x]`.
  2. If **all** subtasks underneath a parent task are now `[x]`, follow this sequence:
  - **First**: Run the full test suite as defined in TESTING.md or CLAUDE.md
  - **Security Validation**: Run any security validation tests specified in the execution plan
  - **Performance Validation**: Run performance tests if specified in the phase requirements
  - **Only if all tests pass**: Stage changes (`git add .`)
  - **Clean up**: Remove any temporary files and temporary code before committing
  - **Commit**: Use a descriptive commit message that:
    - Uses conventional commit format (`feat:`, `fix:`, `refactor:`, etc.)
    - Summarizes what was accomplished in the parent task
    - Lists key changes and additions
    - References the phase number and research context
    - **Formats the message as a single-line command using `-m` flags**, e.g.:

      ```
      git commit -m "feat: implement CLI handler factory pattern" -m "- Add IClaudeHandler interface abstraction" -m "- Create factory for SDK/CLI toggle" -m "- Include security hardening measures" -m "Phase 1.3 of Claude CLI Integration Strategy"
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
   - Ensure implementation stays true to the research plan's technical specifications
   - Validate security requirements are being followed
   - Confirm performance benchmarks are being met

## AI Instructions

When working with execution plans, the AI must:

1. Regularly update the execution plan file after finishing any significant work
2. Follow the enhanced completion protocol with security and performance validation
3. Reference the preserved context when making implementation decisions
4. Ensure traceability between implementation and research plan rationale
5. Add newly discovered tasks while maintaining phase structure
6. Keep technical specifications updated as implementation progresses
7. Validate against success criteria throughout implementation
8. Before starting work, review the context section and technical requirements
9. After implementing a sub‑task, update the plan and pause for user approval
10. Ensure all security and performance requirements from research are implemented
