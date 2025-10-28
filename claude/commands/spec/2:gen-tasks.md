---
description: Convert detailed specification directly to executable task list with full fidelity preservation
argument-hint: [Specification File Path]
---

# Rule: Direct Specification to Task Conversion with Full Fidelity

## Goal

To guide an AI assistant in converting a detailed specification document (created through collaborative planning) directly into executable task lists while preserving 100% fidelity to the original specification. This command bypasses complexity systems and PRD conversion to maintain exact scope boundaries and requirements as specified.

## Core Principle: Specification Fidelity

**The specification is the absolute authority.** This command:

- Adds ZERO requirements beyond the specification
- Makes NO scope expansions or "improvements"
- Preserves ALL original decisions and constraints
- Creates tasks that implement EXACTLY what's written
- Uses fidelity-preserving agents that cannot modify scope

## Input

The user will provide:

1. **Specification File Path:** Path to the detailed specification document. This may be provided in $ARGUMENTS

## Process

1. **Validate Specification:** Before reading, verify specification is ready:
   - Check specification file exists at provided path
   - Confirm file is readable and properly formatted markdown
   - Parse YAML front-matter (if present) for:
     - `fidelity_mode`: Should be "strict"
     - `agents`: Extract developer and reviewer agent specifications
     - `complexity_level`: Note the chosen depth (simple/standard/comprehensive)
     - `codebase_analyzed`: Verify codebase analysis was performed
   - Verify specification has completion marker in final section
   - If validation fails, report specific error and halt
   - If successful, extract metadata for use in task generation

2. **Read Specification Completely:** Parse the entire specification document to understand:

   - All functional requirements
   - All technical constraints and decisions
   - Stated testing requirements (if any)
   - Stated security requirements (if any)
   - Performance requirements and success criteria
   - Implementation timeline and phases
   - Resource constraints
   - Explicit scope boundaries (what's included/excluded)

3. **Analyze Implementation Context:** Systematically discover files that will be affected:
   - Use Glob to find files matching patterns mentioned in spec: `**/*[pattern]*`
   - Use Grep to search for relevant classes, functions, and APIs mentioned in spec
   - Identify files that will need:
     - Creation (new files)
     - Modification (existing files)
     - Integration (connection points)
   - **Use parallel tool calls** for faster file discovery
   - Populate "Implementation Files" section with:
     - File paths
     - Current status (exists/new)
     - Purpose (based on spec requirements)
     - Estimated scope of changes
   - Document integration points and dependencies discovered

4. **Extract Task Structure:** Identify natural implementation phases from the specification:

   - Use specification's own phase structure if provided
   - Create logical groupings based on specification content
   - Maintain specification's dependencies
   - Preserve specification's success criteria for each phase

5. **Generate Task List:** Create tasks that implement:

   - ONLY what's explicitly stated in the specification
   - Testing ONLY as specified (not more, not less)
   - Security ONLY as specified (not more, not less)
   - Performance measures ONLY as specified
   - Documentation ONLY as specified
   - Include discovered implementation files from step 3
   - Use YAML front-matter from specification for metadata continuity

6. **Validate Task Coverage:** Before saving, verify task completeness:
   - Check all specification requirements have corresponding tasks
   - Verify no scope expansion beyond specification
   - Confirm task phases match specification structure
   - Validate that testing/security tasks match specification level
   - Ensure implementation files section is populated with discoveries
   - Check YAML front-matter is complete:
     - Source specification path
     - Fidelity mode (from spec)
     - Agent specifications (from spec)
     - Complexity level (from spec)
   - If validation finds gaps, report to user for clarification
   - If validation passes, proceed to save

7. **Save and Report:** Save validated task list:
   - Save tasks to `/tasks/tasks-fidelity-[spec-name].md`
   - Report validation results to user
   - Confirm task list is ready for processing (spec/3:process-tasks)
   - Inform user of file location for review

## Final Task File Format

The final task file at `/tasks/tasks-fidelity-[spec-name].md`:

```markdown
---
source_specification: [path to spec file]
fidelity_mode: strict
complexity_level: [simple|standard|comprehensive - from spec]
agents:
  developer: developer-fidelity
  reviewer: quality-reviewer-fidelity
created: [timestamp YYYY-MM-DD]
validated: true
---

# [Specification Title] - Fidelity Implementation Tasks

## 🎯 Implementation Authority

**Source Specification:** `[path to spec file]`
**Implementation Scope:** Exactly as specified, no additions or modifications
**Complexity Level:** [simple|standard|comprehensive]
**Validation Status:** ✅ Task coverage validated against specification

### Specification Summary

[Brief summary of what's being implemented - extracted from spec]

### Implementation Boundaries

**Included:** [What specification explicitly includes]
**Excluded:** [What specification explicitly excludes]
**Testing Level:** [As specified in original document]
**Security Level:** [As specified in original document]
**Documentation Level:** [As specified in original document]

## 🗂️ Implementation Files

*Discovered through systematic codebase analysis (Glob/Grep)*

### Files to Create
- `path/to/new/file1.ext` - [Purpose from spec]
- `path/to/new/file2.ext` - [Purpose from spec]

### Files to Modify
- `path/to/existing/file1.ext` (exists) - [Changes needed per spec]
  *Lines/functions affected: [specific locations if known]*
- `path/to/existing/file2.ext` (exists) - [Changes needed per spec]

### Integration Points
- [Existing API/service that will be integrated with]
- [Shared utility/component that will be leveraged]

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

## Key Principles

1. **Absolute Fidelity:** The specification is the complete and sole authority
2. **Zero Additions:** No requirements, tests, or features beyond specification
3. **Validation-First:** Validate spec before reading, validate tasks before saving
4. **Codebase-Aware:** Use Glob/Grep to discover actual implementation files
5. **Parallel Efficiency:** Use parallel tool calls for faster file discovery
6. **Metadata Continuity:** Preserve YAML front-matter from spec → tasks → implementation
7. **Preserve Constraints:** Maintain all limitations and boundaries from specification
8. **Context Preservation:** Include necessary specification context in task file

## Success Indicators

A well-converted task list should:

- **Validated Input:** Specification passed all validation checks before processing
- **100% Specification Match:** Every task maps directly to specification requirements
- **Zero Scope Creep:** No additions, improvements, or expansions beyond spec
- **Discovered Files:** Implementation Files section populated through systematic Glob/Grep analysis
- **Complete Metadata:** YAML front-matter includes all metadata from source specification
- **Validated Output:** Task coverage validation confirms completeness before save
- **Complete Context:** Implementer has all necessary information from specification
- **Clear Boundaries:** Explicit documentation of what's included/excluded
- **Ready for Execution:** Marked as validated and ready for spec/3:process-tasks

## Target Audience

This command serves teams that have:

- Detailed specifications from collaborative planning
- Need exact scope preservation
- Want direct specification-to-implementation workflow
- Require fidelity guarantees throughout implementation
- Must avoid scope creep or complexity-based additions
