---
description: Convert detailed specification directly to executable task list with full fidelity preservation
argument-hint: [Specification File Path]
---

# Rule: Direct Specification to Task Conversion with Full Fidelity

## Goal

To guide an AI assistant in converting a detailed specification document (created through collaborative planning) directly into executable task lists while preserving 100% fidelity to the original specification. This command bypasses complexity systems and PRD conversion to maintain exact scope boundaries and requirements as specified. Think harder.

## Core Principle: Specification Fidelity

**The specification is the absolute authority.** This command:

- Adds ZERO requirements beyond the specification
- Makes NO scope expansions or "improvements"
- Preserves ALL original decisions and constraints
- Creates tasks that implement EXACTLY what's written
- Uses fidelity-preserving agents that cannot modify scope

## MANDATORY: Complete Review Output Display

**CRITICAL REQUIREMENT:** When running fidelity review, you MUST display the complete fidelity-reviewer output to the user. Never summarize or hide the review findings - the user needs to see all numbered issues with their lettered options to make informed decisions.

## Input

The user will provide:

1. **Specification File Path:** Path to the detailed specification document

## Process

1. **Read Specification Completely:** Parse the entire specification document to understand:

   - All functional requirements
   - All technical constraints and decisions
   - Stated testing requirements (if any)
   - Stated security requirements (if any)
   - Performance requirements and success criteria
   - Implementation timeline and phases
   - Resource constraints
   - Explicit scope boundaries (what's included/excluded)

2. **Extract Task Structure:** Identify natural implementation phases from the specification:

   - Use specification's own phase structure if provided
   - Create logical groupings based on specification content
   - Maintain specification's timeline and dependencies
   - Preserve specification's success criteria for each phase

3. **Create and Save Draft Task List:** Generate and save initial tasks that implement:

   - ONLY what's explicitly stated in the specification
   - Testing ONLY as specified (not more, not less)
   - Security ONLY as specified (not more, not less)
   - Performance measures ONLY as specified
   - Documentation ONLY as specified
   - Save draft to `/tasks/tasks-fidelity-[spec-name]-DRAFT.md` with clear draft marking
   - Inform user of draft location for review

4. **Automatic Fidelity Review:** Use fidelity-reviewer agent to:

   - Compare original specification file against saved draft task file
   - Identify missing requirements, scope additions, and ambiguities
   - **CRITICAL: Display the COMPLETE fidelity-reviewer output to the user**
   - **DO NOT summarize or hide the review findings**
   - **Show ALL issues with their numbered format and lettered options**
   - Present structured decisions with references to both files for user review
   - Wait for user response to the displayed questions

5. **Apply User Decisions:** If issues were found and user provided decisions:

   - Parse decision responses (e.g., "1a, 2c, 3b")
   - Apply chosen resolutions to update task list
   - Re-run fidelity review to validate changes
   - Continue until task list achieves perfect fidelity

6. **Preserve Context:** Include relevant specification sections to ensure implementer has complete context without needing to reference external documents

7. **Generate Fidelity Metadata:** Create task file with strict fidelity preservation settings and review audit trail

8. **Save Final Validated Task File:**
   - Save validated version to `/tasks/tasks-fidelity-[spec-name].md` with complete review metadata
   - Archive or remove draft file (user preference)
   - Confirm final task list location to user

## Draft Task File Format

The initial draft task file saved to `/tasks/tasks-fidelity-[spec-name]-DRAFT.md`:

```markdown
---
version: 1
status: DRAFT
fidelity_mode: strict
source_spec: [path to original specification file]
agents:
  developer: developer-fidelity
  reviewer: quality-reviewer-fidelity
scope_preservation: true
additions_allowed: none
fidelity_mode: strict
specification_metadata:
  source_file: [specification file path]
  conversion_date: [timestamp]
  fidelity_level: absolute
  scope_changes: none
fidelity_review:
  reviewed: false
  pending_review: true
  draft_created: [timestamp]
---

# ⚠️ DRAFT - Pending Fidelity Review

# [Specification Title] - Fidelity Implementation Tasks (DRAFT)

**⚠️ This is a DRAFT task list awaiting fidelity review against the original specification.**

**Specification Source:** [path to spec file]
**Review Status:** Pending
**Next Step:** Fidelity review will compare this draft against the specification

[Rest of task content...]
```

## Final Task File Format

After fidelity review and validation, the final file at `/tasks/tasks-fidelity-[spec-name].md`:

```markdown
---
version: 1
fidelity_mode: strict
source_spec: [path to original specification file]
agents:
  developer: developer-fidelity
  reviewer: quality-reviewer-fidelity
scope_preservation: true
additions_allowed: none
fidelity_mode: strict
specification_metadata:
  source_file: [specification file path]
  conversion_date: [timestamp]
  fidelity_level: absolute
  scope_changes: none
fidelity_review:
  reviewed: true
  reviewer_agent: fidelity-reviewer
  issues_found: [number of issues identified]
  decisions_made:
    - issue: "[brief description of issue]"
      decision: "[user decision - e.g., '1a']"
      resolution: "[how decision was applied]"
  review_iterations: [number of review cycles]
  final_validation: passed
  review_date: [timestamp]
---

# [Specification Title] - Fidelity Implementation Tasks

## 🎯 Implementation Authority

**Source Specification:** [path to spec file]
**Conversion Mode:** Full Fidelity Preservation
**Implementation Scope:** Exactly as specified, no additions or modifications

### Specification Summary

[Brief summary of what's being implemented - extracted from spec]

### Implementation Boundaries

**Included:** [What specification explicitly includes]
**Excluded:** [What specification explicitly excludes]  
**Testing Level:** [As specified in original document]
**Security Level:** [As specified in original document]
**Documentation Level:** [As specified in original document]

## 🗂️ Implementation Files

[List of files that will need creation/modification based on specification analysis]

### Development Notes

- Follow specification requirements exactly as written
- Do not add testing beyond what's specified
- Do not add security measures beyond what's specified
- Do not expand scope or "improve" requirements
- Question any ambiguity rather than assuming

## ⚙️ Implementation Phases

[Extract phases directly from specification structure]

### Phase 1: [Phase Name from Specification]

**Objective:** [Exact objective from specification]
**Timeline:** [As specified in original document]

**Specification Requirements:**
[List requirements exactly as written in specification]

**Tasks:**

- [ ] 1.0 [High-level task matching specification]
  - [ ] 1.1 [Specific implementation task from spec]
  - [ ] 1.2 [Another specific task from spec]
  - [ ] 1.3 [Validation task as specified]

### Phase N: Final Phase

**Objective:** Complete implementation as specified

**Tasks:**

- [ ] N.0 Finalize Implementation
  - [ ] N.1 Complete all specified deliverables
  - [ ] N.2 Validate against specification success criteria
  - [ ] N.3 Document implementation (if specified in original spec)

## 📋 Specification Context

### [Technical Section 1 from Spec]

[Preserve relevant technical details from specification]

### [Technical Section 2 from Spec]

[Preserve architectural decisions from specification]

## 🚨 Implementation Requirements

### Fidelity Requirements (MANDATORY)

- Implement ONLY what's explicitly specified
- Do not add features, tests, or security beyond specification
- Question ambiguities rather than making assumptions
- Preserve all specification constraints and limitations

### Success Criteria

[Extract success criteria exactly from specification]

### Testing Requirements

[Extract testing requirements exactly as specified - do not add more]

### Security Requirements

[Extract security requirements exactly as specified - do not add more]

## ✅ Validation Checklist

- [ ] Implementation matches specification exactly
- [ ] No scope additions or "improvements" made
- [ ] All specification constraints preserved
- [ ] Success criteria from specification met
- [ ] No testing beyond what specification requires
- [ ] No security measures beyond specification requirements

## 📊 Completion Criteria

[Extract completion criteria exactly from specification]
```

## CRITICAL: Review Output Display Requirements

### Mandatory Display Protocol

When the fidelity-reviewer agent completes its analysis, you MUST:

1. **Display the COMPLETE fidelity-reviewer output** to the user, including:

   - "Files Reviewed" section with both file paths
   - "Validated Elements" section listing what's correct
   - **ALL issues** in their full numbered format with lettered options
   - The complete request for user input

2. **NEVER summarize, condense, or hide** the review findings

3. **CORRECT Display Example:**

   ```
   ## ⚠️ Fidelity Review: ISSUES FOUND

   **Files Reviewed:**
   - **Specification:** /path/to/spec.md
   - **Draft Task List:** /path/to/draft.md

   ### ❌ Issues Requiring Decisions

   **1. Missing Requirement: Response Format**
   **Specification** (line 15): "All responses use JSON format"
   **Draft Task List** (Task 4.1-4.3): Error handling tasks don't specify JSON
   **Issue:** No explicit task ensures JSON response format

   Options:
   a) Add task: "4.4 Set JSON content-type headers"
   b) This is implicitly covered by Express defaults
   c) Add minimal task: "4.4 Ensure JSON format"
   d) This level of detail not needed

   **Please respond with your decisions: "1a, 2c, 3b"**
   ```

4. **INCORRECT Display (DO NOT DO THIS):**
   ```
   The review found 6 issues requiring decisions. Please respond with choices.
   ```

### Automatic Review Workflow

1. **Initial Task Generation:** Create task list based on specification analysis
2. **Fidelity Review:** fidelity-reviewer agent compares specification vs tasks
3. **Complete Output Display:** Show ALL review findings to user with full details
4. **User Decision Collection:** Wait for structured decisions based on displayed issues
5. **Resolution Application:** Apply user choices and regenerate tasks
6. **Validation Loop:** Repeat until perfect fidelity achieved
7. **Final Output:** Save validated task list with complete audit trail

### File-Based Review Workflow

The enhanced workflow provides full file visibility:

1. **Draft Creation**: `tasks-fidelity-[spec-name]-DRAFT.md` is saved immediately after generation
2. **User Notification**: "✅ Draft task list saved to: [path]. Running fidelity review..."
3. **File References**: Review output includes paths to both specification and draft files
4. **Side-by-Side Review**: You can open both files to examine the comparison context
5. **Final Replacement**: After validation, draft is replaced with final version

### Decision Format

When issues are found, they are presented with file references:

```
**Files Reviewed:**
- **Specification:** [path to original spec file]
- **Draft Task List:** [path to draft task file]

**1. [Issue Type]: [Brief Description]**
**Specification** (section/line): "[exact quote]"
**Draft Task List** (Task X.Y): "[relevant task or 'missing']"
**Issue:** [explanation of discrepancy]

Options:
a) [Option 1 description]
b) [Option 2 description]
c) [Option 3 description]
d) [Other/specify]

**2. [Next Issue]...**
```

**User Response Format:** "1a, 2c, 3b" (issue number + letter choice)

### Issue Types

- **Missing Requirement:** Specification element not represented in tasks
- **Scope Addition:** Task goes beyond specification requirements
- **Ambiguous Requirement:** Multiple valid interpretations possible
- **Implementation Mismatch:** Task doesn't accurately represent spec intent

## Key Principles

1. **Absolute Fidelity:** The specification is the complete and sole authority
2. **Zero Additions:** No requirements, tests, or features beyond specification
3. **Preserve Constraints:** Maintain all limitations and boundaries from specification
4. **Validated Conversion:** Automatic review ensures perfect specification representation
5. **User-Controlled Decisions:** All ambiguities resolved through explicit user choices
6. **Context Preservation:** Include necessary specification context in task file
7. **Fidelity Agents:** Always use developer-fidelity and quality-reviewer-fidelity
8. **Audit Trail:** Document all review decisions for transparency

## Success Indicators

A well-converted task list should:

- **100% Specification Match:** Every task maps directly to specification requirements
- **Zero Scope Creep:** No additions, improvements, or expansions beyond spec
- **Complete Context:** Implementer has all necessary information from specification
- **Clear Boundaries:** Explicit documentation of what's included/excluded
- **Fidelity Metadata:** Proper agent selection and preservation settings
- **Validation Criteria:** Clear success measures extracted from specification

## Target Audience

This command serves teams that have:

- Detailed specifications from collaborative planning
- Need exact scope preservation
- Want direct specification-to-implementation workflow
- Require fidelity guarantees throughout implementation
- Must avoid scope creep or complexity-based additions
