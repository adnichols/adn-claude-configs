---
description: Create a complexity-aware code simplification plan with router-driven analysis and agent selection
argument-hint: [Target directory/files to analyze]
---

# Rule: Generating a Complexity-Aware Code Simplification Plan

## Goal

To guide an AI assistant in creating a detailed Code Simplification Plan with router-driven complexity detection, appropriate agent selection, and cleanup aggressiveness scaled to project complexity. The system automatically detects project complexity from existing files, selects appropriate agents, and scales cleanup recommendations while ensuring absolute preservation of core functionality. Think harder.

## Router Integration for Complexity Detection

This command integrates with the complexity router to:

1. **Detect Project Complexity:** Analyze existing project files to determine overall complexity level
2. **Scale Cleanup Aggressiveness:** Adjust simplification approach based on complexity:
   - **Minimum:** Very aggressive cleanup allowed (prototype-level)
   - **Basic:** Moderate cleanup with standard precautions
   - **Moderate:** Conservative cleanup with comprehensive testing
   - **Complex:** Very conservative cleanup with enterprise-grade validation
3. **Auto-select Quality Reviewer:** Use router-selected quality reviewer agent appropriate to complexity
4. **Apply Complexity-Appropriate Safeguards:** Include validation requirements matching the project complexity level

## Process

1. **Receive Target Scope:** The user provides a directory path, file pattern, or specific files to analyze for simplification opportunities. If not provided, review entire current directory.
2. **Detect Project Complexity:** Call router to analyze existing project files and determine complexity:
   - Scan for PRDs, specs, and task files with metadata
   - Execute `bash .claude/commands/_lib/complexity/get-complexity.sh [discovered-files]` to get project complexity
   - If no metadata found, analyze codebase characteristics to estimate complexity level
3. **Complexity-Aware Planning:** Scale simplification approach based on router-determined complexity:
   - **Minimum:** Allow aggressive refactoring, minimal validation requirements
   - **Basic:** Standard refactoring with unit test validation
   - **Moderate:** Conservative refactoring with integration test requirements
   - **Complex:** Very conservative approach with full regression testing
4. **Check Backward Compatibility Requirements:** Block aggressive cleanup if router detects `backward_compat_required: true`
5. **Assure working branch:** Assure we are operating on a feature branch and if we aren't, create an appropriate branch for these changes
6. **Review Recent Changes:** Leverage git history to identify recent changes to the current repository
7. **Test Coverage Assessment:** Verify existing test coverage scaled to complexity level
8. **Generate Simplification Plan:** Use the @simplify-planner agent to analyze the codebase and create a detailed plan scaled to complexity
9. **Quality Review:** Use router-selected quality reviewer agent for plan review appropriate to complexity level
10. **Save Plan:** Save the generated plan as `simplify-plan-[area-name].md` inside the `/tasks` directory with router metadata

## Pre-Simplification Requirements

Before generating any simplification plan, apply complexity-appropriate requirements:

1. **Complexity-Appropriate Test Coverage Verification:**
   - **Minimum:** Basic test coverage for core functionality only
   - **Basic:** Standard unit test coverage for main paths
   - **Moderate:** Comprehensive test coverage including integration tests
   - **Complex:** Full test coverage including e2e and regression tests
   - Analyze existing test coverage for the target area
   - Identify gaps in test coverage for core functionality
   - Document current test structure and quality
   - Favor fewer end to end tests over detailed unit tests
   - Minimize mocks and stubs where possible, use real scenarios

2. **Recent Change Analysis:**
   - Review git history for recent modifications
   - Identify areas of frequent change or bug fixes
   - Understand evolution patterns and complexity accumulation

3. **Dependency Mapping:**
   - Identify all external dependencies on the target code
   - Map integration points and API contracts
   - Document concurrent behavior and thread safety requirements

## Simplification Plan Structure

The generated plan should include the following sections as a checklist:

### Phase 1: Preparation and Safety Verification
- [ ] **P1.1: Baseline Test Execution**
  - [ ] Run full test suite to establish baseline
  - [ ] Document current test coverage percentage
  - [ ] Identify any existing test failures

- [ ] **P1.2: Test Coverage Enhancement** (if needed)
  - [ ] Create missing unit tests for core functionality
  - [ ] Add integration tests for critical paths
  - [ ] Implement regression tests for identified edge cases

- [ ] **P1.3: Complexity Analysis**
  - [ ] Complete @simplify-planner codebase archaeology
  - [ ] Document evidence of unused/deprecated code
  - [ ] Identify consolidation opportunities
  - [ ] Map preservation requirements

### Phase 2: Plan Review and Validation
- [ ] **P2.1: Complexity-Appropriate Quality Review**
  - [ ] Submit plan to router-selected quality reviewer agent (e.g., @quality-reviewer-moderate)
  - [ ] Apply complexity-appropriate review depth and safety checks
  - [ ] Update plan to address safety concerns or gaps as appropriate
  - [ ] Confirm preservation guarantees scaled to project complexity level

- [ ] **P2.2: Risk Assessment**
  - [ ] Document all identified risks
  - [ ] Create mitigation strategies
  - [ ] Define success criteria
  - [ ] Establish monitoring approach

- [ ] **P2.3: Plan Summary and User Review**
  - [ ] Provide comprehensive summary of proposed changes
  - [ ] Highlight all areas to be modified and cleanup targets
  - [ ] Present risk assessment and mitigation strategies
  - [ ] Wait for explicit user approval before proceeding
  - [ ] Address any user concerns or modifications
  - [ ] Do NOT proceed to Phase 3 without user confirmation

### Phase 3: Implementation Steps
- [ ] **P3.1: Pre-Implementation Verification**
  - [ ] Re-run full test suite
  - [ ] Create git branch for simplification work
  - [ ] Document current system state

- [ ] **P3.2: Surgical Cleanup Execution**
  - [ ] [Specific cleanup step 1]
  - [ ] [Specific cleanup step 2]
  - [ ] [Specific cleanup step N]

- [ ] **P3.3: Post-Cleanup Validation**
  - [ ] Run full test suite after each major cleanup
  - [ ] Verify functionality preservation
  - [ ] Performance regression testing
  - [ ] Integration point validation

### Phase 4: Completion and Documentation
- [ ] **P4.1: Final Verification**
  - [ ] Complete system integration testing
  - [ ] User acceptance criteria validation
  - [ ] Performance benchmarking

- [ ] **P4.2: Documentation and Cleanup**
  - [ ] Update code documentation
  - [ ] Remove temporary files and artifacts
  - [ ] Create deployment notes
  - [ ] Archive simplification artifacts

## Agent Responsibilities

### Current Agent (Orchestrator)
- Plan creation and coordination
- Git branch management
- Progress tracking and checklist updates
- Quality gates and safety verification

### @simplify-planner Agent
- Codebase complexity analysis
- Evidence-based cleanup recommendations
- Preservation strategy design
- Risk identification and mitigation planning

### @quality-reviewer Agent
- Plan safety review
- Risk assessment validation
- Quality gate approval

## Safety Requirements

1. **Unconditional Functionality Preservation:**
   - All user-facing behavior must remain identical
   - No core functionality degradation allowed
   - All integration points must remain intact

2. **Evidence-Based Decisions:**
   - Concrete proof required for all removal decisions
   - Usage analysis with grep/git evidence
   - Deprecation timeline documentation

3. **Comprehensive Testing:**
   - Test coverage must be adequate before cleanup
   - Performance benchmarks maintained

4. **Rollback Preparedness:**
   - Git branch strategy for safe experimentation
   - Rollback involves reverting git changes, keep risky changes on their own commit

## Output

- **Format:** Markdown (`.md`)
- **Location:** `/tasks/`
- **Filename:** `simplify-plan-[area-name].md`

## Final Instructions

1. Do NOT start implementing any simplification
2. Ensure all checklist items are specific and actionable
3. Verify @simplify-planner agent provides evidence for all recommendations
4. Incorporate @quality-reviewer feedback into the plan where appropriate before proceeding
5. Remember: This creates the PLAN only - execution happens via simplify:process-plan.md
