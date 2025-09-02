---
description: Convert a specification into a comprehensive TDD execution plan with test-first development cycles
argument-hint: [Files]
---

# Rule: Converting Specifications to TDD Execution Plans

## Goal

To guide an AI assistant in converting a comprehensive source document (specification, architecture plan, or research plan) into a detailed, test-driven development (TDD) execution plan. Unlike traditional implementation plans, this follows strict TDD methodology: write tests first, make them pass, then refactor. Think harder.

## Input

The user will reference a specific specification document file path that needs to be converted to a TDD execution plan.

## Instructions

The AI will need to read and analyze the referenced specification document to create a TDD-focused execution plan.

## Output

- **Format:** Markdown (`.md`)
- **Location:** `/tasks/`
- **Filename:** `tasks-tdd-[spec-file-name].md` (e.g., `tasks-tdd-user-auth-system.md`)

## TDD Methodology

This command enforces strict Test-Driven Development:

1. **Red Phase:** Write failing tests that define the desired behavior
2. **Green Phase:** Write minimal code to make tests pass
3. **Refactor Phase:** Improve code while keeping tests green
4. **End-to-End Focus:** Minimize mocking, favor integration and E2E tests
5. **Phase Isolation:** Complete all tests for a phase before moving to next

## Process

1. **Receive Specification Reference:** The user points to a specific specification document
2. **Read and Analyze Specification:** Extract requirements, user stories, and acceptance criteria
3. **Context Preservation:** Maintain full specification context in the execution plan
4. **TDD Phase Planning:** Convert specification into logical TDD phases with clear test boundaries
5. **Test Strategy Design:** Define comprehensive test scenarios that prove specification compliance
6. **Phase 1: Generate High-Level TDD Plan:** Create execution file with test-first phases
7. **Wait for Confirmation:** User responds "Go" to proceed with detailed test breakdown
8. **Phase 2: Generate Detailed Test Tasks:** Break down each phase into specific test scenarios and implementation cycles

## Output Format

The generated TDD execution plan _must_ follow this structure:

```markdown
# [Specification Title] - TDD Execution Plan

## 🎯 Executive Summary
[Preserve key insights and requirements from specification document]

## 📋 Context & Background

### Specification Analysis
[Preserve relevant analysis from specification document]

### Key Requirements
[Extract and list key functional requirements that need test coverage]

### Acceptance Criteria
[List all acceptance criteria that tests must validate]

### Success Criteria
[Define clear success metrics from specification document]

## 🧪 TDD Testing Strategy

### Test Philosophy
- **End-to-End First:** Favor integration and E2E tests over unit tests with mocks
- **Real Data:** Use real databases, APIs, and services where possible
- **User Journey Focus:** Tests should mirror actual user workflows
- **Specification Compliance:** Every test maps directly to specification requirements

### Test Infrastructure Requirements
[Define test databases, test environments, fixture management, etc.]

### Testing Tools & Frameworks
[Specify testing frameworks, tools, and utilities needed]

## 🗂️ Relevant Files

### Test Files
- `tests/e2e/[feature].test.ts` - End-to-end tests for [feature]
- `tests/integration/[component].test.ts` - Integration tests for [component]
- `tests/unit/[module].test.ts` - Unit tests for [module] (minimal mocking)

### Implementation Files
- `src/[feature]/[component].ts` - Implementation for [component]
- `src/[feature]/types.ts` - Type definitions from specification
- `src/[feature]/config.ts` - Configuration for [feature]

### Notes
- Follow TDD cycle: Red → Green → Refactor
- Use test commands defined in TESTING.md or CLAUDE.md
- All tests must pass before phase completion

## ⚙️ TDD Implementation Phases

### Phase 1: [Phase Name from Specification] 
**Objective:** [Clear objective from specification]

**Test Coverage Requirements:**
- [Specific test scenario 1 from specification]
- [Specific test scenario 2 from specification]
- [Error/edge case scenarios]

**TDD Cycle Tasks:**
- [ ] 1.0 Write Comprehensive Tests for Phase 1
  - [ ] 1.1 Write E2E tests for primary user journey: [specific journey]
  - [ ] 1.2 Write integration tests for [component] with real dependencies
  - [ ] 1.3 Write unit tests for [business logic] with minimal mocking
  - [ ] 1.4 Validate all tests fail (Red phase confirmed)
  
- [ ] 1.5 Implement Code to Pass Tests
  - [ ] 1.5.1 Make test [specific test name] pass with minimal implementation
  - [ ] 1.5.2 Make test [specific test name] pass with minimal implementation
  - [ ] 1.5.3 [Continue for each test]
  - [ ] 1.5.N Validate all Phase 1 tests pass (Green phase confirmed)
  
- [ ] 1.6 Refactor Phase 1 Implementation
  - [ ] 1.6.1 Refactor [component] while maintaining green tests
  - [ ] 1.6.2 Optimize performance while maintaining test coverage
  - [ ] 1.6.3 Run full test suite to ensure no regressions

### Phase 2: [Phase Name from Specification]
**Objective:** [Clear objective from specification]

**Test Coverage Requirements:**
- [Requirements specific to this phase]

**TDD Cycle Tasks:**
- [ ] 2.0 Write Comprehensive Tests for Phase 2
  - [ ] 2.1 [Detailed test writing tasks]
  
- [ ] 2.5 Implement Code to Pass Tests
  - [ ] 2.5.1 [Detailed implementation tasks]
  
- [ ] 2.6 Refactor Phase 2 Implementation
  - [ ] 2.6.1 [Detailed refactoring tasks]

### Phase N: Integration Testing & Documentation
**Objective:** Validate complete system integration and create documentation

**Integration Requirements:**
- Full end-to-end user journeys working
- Performance benchmarks met under test conditions
- Security requirements validated through tests
- All specification requirements proven through test coverage

**Tasks:**
- [ ] N.0 Complete System Integration Testing
  - [ ] N.1 Run comprehensive E2E test suite covering all user journeys
  - [ ] N.2 Validate performance requirements through automated testing
  - [ ] N.3 Execute security test scenarios
  - [ ] N.4 Generate test coverage report showing specification compliance
  - [ ] N.5 Run `/docs:update` to update comprehensive documentation
  - [ ] N.6 Document test scenarios and their specification traceability

## 🔍 Technical Specifications

### [Technical Component 1]
[Preserve relevant examples and specifications from source document]

**Test Scenarios:**
```typescript
// Test example from specification requirements
describe('[Component Name]', () => {
  it('should [specific behavior from specification]', async () => {
    // E2E test implementation
  });
});
```

### [Technical Component 2]
[Another technical specification with test focus]

## 🚨 Critical TDD Requirements

### Test-First Mandatory Rules
1. **No Implementation Before Tests:** All code must be written to make failing tests pass
2. **Real Dependencies:** Minimize mocking, use real databases/APIs in test environment  
3. **Specification Traceability:** Every test must map to specific specification requirement
4. **Red-Green-Refactor:** Strict adherence to TDD cycle

### Quality Gates
- All tests must pass before phase completion
- Test coverage must prove specification compliance
- Performance benchmarks validated through automated tests
- Security requirements verified through test scenarios

## ✅ Validation & Testing Strategy

### Pre-Implementation Validation
- All tests written and failing (Red phase)
- Test scenarios cover all specification requirements
- Test environment properly configured

### Implementation Validation  
- Tests pass one by one as code is implemented (Green phase)
- No test regressions during implementation
- Full test suite passes before refactoring

### Post-Implementation Validation
- Refactored code maintains all test coverage
- Performance tests validate specification benchmarks
- Integration tests prove end-to-end functionality

## 📊 Success Metrics

[Specific, measurable success criteria from specification document proven through tests]

- Test Coverage: X% of specification requirements covered by automated tests
- Performance: All benchmarks validated through automated testing
- User Journeys: All primary user workflows validated end-to-end
- Specification Compliance: All acceptance criteria proven through test execution
```

## Interaction Model

The process requires a pause after generating the high-level TDD plan to get user confirmation ("Go") before proceeding to generate detailed test tasks. This ensures the test strategy and phasing aligns with user expectations.

## Key Differences from Traditional Implementation Plans

1. **Test-First Approach:** Tests written before any implementation code
2. **Specification-Test Traceability:** Direct mapping between requirements and test scenarios
3. **Real Dependency Focus:** Minimal mocking, favor integration testing
4. **Strict TDD Cycles:** Red-Green-Refactor methodology enforced
5. **End-to-End Validation:** User journeys tested comprehensively
6. **Quality Gates:** Phase completion requires all tests passing

## Target Audience

Assume the primary reader is a **developer** (junior to senior) who needs to implement features using strict TDD methodology. The execution plan should provide clear test scenarios that prove specification compliance through automated testing.

## Usage with build:tdd-process-tasks.md

After generating the TDD execution plan, use `/build:tdd-process-tasks.md @tasks/tasks-tdd-[spec-name].md` to execute the TDD workflow with proper cycle enforcement and validation.