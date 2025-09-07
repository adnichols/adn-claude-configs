---
description: Execute TDD task lists with router-driven complexity detection and strict Red-Green-Refactor cycle enforcement
argument-hint: [@tdd-task-file] [NOSUBCONF]
---

# Rule: TDD Task Processing with Router Integration and Cycle Enforcement

## Goal

To guide an AI assistant through executing a TDD (Test-Driven Development) task list with router-driven complexity detection, appropriate agent selection, and strict enforcement of the Red-Green-Refactor cycle. The complexity router automatically detects the appropriate complexity level, selects suitable developer and quality agents, and applies complexity-appropriate validation requirements while ensuring tests are written first, fail appropriately, then implementation makes them pass, followed by refactoring. Think harder.

## Router Integration Process

Before starting TDD task implementation:

1. **Parse Task File Metadata:** Extract complexity information from task file YAML front-matter
2. **Call Complexity Router:** Execute `bash .claude/commands/_lib/complexity/get-complexity.sh [task-file]` to get:
   - Computed complexity level
   - Selected developer and quality-reviewer agents  
   - Required TDD validation checks for the complexity level
   - Performance and security requirements for TDD cycles
3. **Auto-select Agents:** Use router-selected agents for TDD implementation:
   - Developer agent: `@[router-selected-developer]` for TDD cycles
   - Quality reviewer: `@[router-selected-quality-reviewer]` for final validation
4. **Apply TDD Validation Requirements:** Include complexity-appropriate checks in each TDD phase:
   - **Minimum:** basic unit tests + lint + build
   - **Basic:** + comprehensive unit tests + dependency audit
   - **Moderate:** + integration tests + performance tests + basic SAST
   - **Complex:** + e2e tests + performance benchmarks + SAST+DAST + compliance validation

## Usage

```bash
/build:tdd-process-tasks @tasks/tasks-tdd-user-auth.md        # Process with confirmation
/build:tdd-process-tasks @tasks/tasks-tdd-api.md NOSUBCONF   # Process without sub-task confirmation
```

## TDD Methodology Enforcement

This command enforces strict Test-Driven Development cycles:

### Red Phase (Failing Tests)
- Write tests that define desired behavior
- Validate tests fail for the right reasons
- Ensure test failure messages are meaningful
- No implementation code exists yet

### Green Phase (Minimal Implementation)
- Write minimal code to make tests pass
- Focus on making tests green, not perfect code
- Validate tests pass one by one
- No over-engineering during this phase

### Refactor Phase (Code Improvement)
- Improve code quality while keeping tests green
- Optimize performance and design
- Ensure all tests remain passing
- Commit only when tests are green

## TDD Task Processing Protocol

### Phase Initialization
1. **Branch Management:** Ensure working on feature branch (not main)
2. **Test Environment:** Validate test infrastructure is ready
3. **Baseline:** Run existing test suite to ensure clean starting state

### Test Writing Cycle (Red Phase)
1. **Write Test Task:** Focus on one test scenario at a time
2. **Test Validation:** Ensure new test fails with meaningful error message
3. **No Implementation:** Confirm no implementation code exists for the test
4. **Test Review:** Validate test covers specification requirement accurately

### Implementation Cycle (Green Phase)
1. **Minimal Implementation:** Write smallest code to make test pass
2. **Test Execution:** Run specific test to validate it passes
3. **No Regression:** Ensure existing tests still pass
4. **Green Confirmation:** All tests in current phase must be green

### Refactoring Cycle (Refactor Phase)
1. **Code Improvement:** Enhance implementation while maintaining green tests
2. **Continuous Testing:** Run tests after each refactoring change
3. **Quality Focus:** Improve design, performance, and maintainability
4. **Green Maintenance:** All tests must remain passing throughout

## Process Flow

$ARGUMENTS

I'll process the TDD task list with strict Red-Green-Refactor cycle enforcement.

**Pre-Processing Validation:**

1. **Git Branch Check:** Ensure not on main branch
2. **Test Environment:** Validate testing infrastructure is ready  
3. **Clean State:** Run full test suite to confirm clean starting point

**TDD Task Processing Rules:**

### Test Writing Phase Rules
- MUST write tests before any implementation code
- MUST validate tests fail with meaningful error messages
- MUST confirm test covers specific specification requirement
- CANNOT proceed to implementation until test failure is confirmed

### Implementation Phase Rules  
- MUST implement minimal code to make failing test pass
- MUST validate specific test passes before proceeding
- MUST ensure no existing tests are broken
- CANNOT over-engineer during initial implementation

### Refactoring Phase Rules
- MUST maintain green test state throughout refactoring
- MUST run tests after each significant refactoring change
- MUST improve code quality without breaking functionality
- CANNOT commit unless all tests are passing

**Sub-Task Confirmation Protocol:**
- After each TDD cycle (Red-Green-Refactor), ask for user confirmation to proceed
- Exception: If NOSUBCONF specified, proceed automatically through TDD cycles within a phase
- ALWAYS require confirmation between phases regardless of NOSUBCONF

**Phase Completion Protocol:**
1. **Test Suite Validation:** Run complete test suite to ensure no regressions
2. **Performance Validation:** Run performance tests if specified in task
3. **Coverage Validation:** Ensure test coverage meets phase requirements
4. **Commit Changes:** Only if all tests pass and quality gates are met
5. **Phase Documentation:** Update task list with completion status

Let me begin processing the TDD task list:

<function_calls>
<invoke name="Read">
<parameter name="file_path">$TASK_FILE</parameter>
</invoke>

Now I'll start executing the TDD methodology:

**Phase 1: Test Environment Setup**

First, let me validate the test environment and current state:

<function_calls>
<invoke name="Bash">
<parameter name="command">git branch --show-current</parameter>
<parameter name="description">Verify not on main branch</parameter>
</invoke>

<function_calls>
<invoke name="Bash">
<parameter name="command">npm test</parameter>
<parameter name="description">Run existing test suite to establish baseline</parameter>
</invoke>

**Phase 2: TDD Cycle Execution**

I'll now begin the strict TDD cycle for each task in the list:

### Current Task: [Task Name from File]

**RED PHASE - Writing Failing Tests:**

Before writing any implementation code, I'll create the test that defines the expected behavior:

<function_calls>
<invoke name="Write">
<parameter name="file_path">[test-file-path]</parameter>
<parameter name="content">[Test implementation that should fail]</parameter>
</invoke>

<function_calls>
<invoke name="Bash">
<parameter name="command">npm test -- [specific-test-file]</parameter>
<parameter name="description">Validate test fails with meaningful error</parameter>
</invoke>

**Validation Question:** Does the test fail for the right reason? (Expected behavior not implemented)

**GREEN PHASE - Minimal Implementation:**

Now I'll write the minimal code to make the test pass:

<function_calls>
<invoke name="Write">
<parameter name="file_path">[implementation-file-path]</parameter>
<parameter name="content">[Minimal implementation to make test pass]</parameter>
</invoke>

<function_calls>
<invoke name="Bash">
<parameter name="command">npm test -- [specific-test-file]</parameter>
<parameter name="description">Validate test now passes</parameter>
</invoke>

**Validation Question:** Does the test pass with minimal implementation?

**REFACTOR PHASE - Code Improvement:**

Now I'll improve the implementation while keeping tests green:

<function_calls>
<invoke name="Edit">
<parameter name="file_path">[implementation-file-path]</parameter>
<parameter name="old_string">[minimal implementation]</parameter>
<parameter name="new_string">[improved implementation]</parameter>
</invoke>

<function_calls>
<invoke name="Bash">
<parameter name="command">npm test</parameter>
<parameter name="description">Ensure all tests still pass after refactoring</parameter>
</invoke>

**TDD Cycle Complete - Proceeding to Next Task**

[Repeat for each task in the TDD task list]

## Implementation

The AI should follow this strict protocol:

1. **Read TDD Task File:** Parse tasks and understand TDD phase structure
2. **Validate Environment:** Ensure proper git branch and test environment
3. **Process Each TDD Cycle:**
   - Write failing test (Red)
   - Implement minimal code (Green)  
   - Refactor while maintaining green tests (Refactor)
4. **Phase Completion:** Validate all tests pass before proceeding to next phase
5. **Git Management:** Commit only when all tests are passing

## Critical TDD Validation Points

### Red Phase Validations
- [ ] Test written before any implementation code
- [ ] Test fails with meaningful error message
- [ ] Test failure indicates missing functionality (not broken test)
- [ ] Test covers specific specification requirement

### Green Phase Validations  
- [ ] Minimal implementation written to make test pass
- [ ] Specific test now passes
- [ ] No existing tests broken by new implementation
- [ ] Implementation is minimal (no over-engineering)

### Refactor Phase Validations
- [ ] Code quality improved while maintaining functionality
- [ ] All tests remain passing throughout refactoring  
- [ ] Performance optimizations implemented if needed
- [ ] Code follows project conventions and standards

## Error Handling

### Test Failure Issues
- If test doesn't fail initially, review test logic and fix
- If test fails for wrong reasons, adjust test implementation
- If existing tests break, fix implementation before proceeding

### Implementation Issues
- If minimal implementation is too complex, simplify approach
- If tests don't pass, debug implementation incrementally
- If performance issues arise, address during refactor phase

### Refactoring Issues
- If tests break during refactoring, revert and retry
- If quality improvements are too complex, break into smaller steps
- If performance degrades, measure and optimize carefully

## Success Criteria

Each TDD cycle must achieve:
- ✅ Tests written first and initially failing
- ✅ Implementation makes tests pass with minimal code
- ✅ Refactored code improves quality while maintaining green tests
- ✅ No regressions in existing test suite
- ✅ Specification requirements proven through test coverage

## Git Workflow Integration

### Commit Strategy with Router Validation
- Complete TDD cycle (Red-Green-Refactor) with complexity-appropriate validation
- Run router-determined validation checks before commit:
  - Always: lint, build, unit tests
  - Basic+: dependency audit, comprehensive unit tests
  - Moderate+: integration tests, performance tests, basic SAST
  - Complex: e2e tests, performance benchmarks, advanced security scans
- Use router-selected quality reviewer agent for final validation
- Use conventional commit format with TDD phase indicator
- Example: `feat(auth): implement user login validation (TDD cycle 1)`

### Branch Management
- Work on feature branches only
- Create phase-specific branches if needed
- Merge only when full phase is complete and tested

This command ensures rigorous adherence to TDD methodology with router-driven complexity awareness, automatic agent selection, and complexity-appropriate validation while maintaining code quality and specification compliance.