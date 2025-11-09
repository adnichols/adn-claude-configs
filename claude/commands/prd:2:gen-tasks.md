---
description: Convert PRD to executable task list with full fidelity preservation
argument-hint: [PRD File Path]
---

# Rule: Generating a Task List from a PRD with Fidelity Preservation

## Goal

To guide an AI assistant in creating a detailed, step-by-step task list in Markdown format with YAML front-matter based on an existing Product Requirements Document (PRD). The system uses fidelity-preserving agents to ensure exact scope implementation.

## Fidelity Preservation

This command follows the fidelity-preserving approach to:

1. **Parse PRD Content:** Extract all requirements exactly as specified in the PRD
2. **Preserve Scope Boundaries:** Maintain exact scope without additions or expansions
3. **Use Fidelity Agents:** Always use developer-fidelity and quality-reviewer-fidelity agents
4. **Minimal Task Detail:** Create only tasks necessary to implement specified requirements
5. **Apply Only Specified Validation:** Include testing and validation only as specified in PRD

## Output

- **Format:** Markdown (`.md`)
- **Location:** `/tasks/`
- **Filename:** `tasks-[prd-file-name].md` (e.g., `tasks-prd-user-profile-editing.md`)

## Process

1. **Validate PRD:** Before reading, verify PRD is ready:
   - Check PRD file exists at provided path
   - Confirm file is readable markdown format
   - Parse YAML front-matter for:
     - `fidelity_mode`: Should be "strict"
     - `agents`: Extract developer and reviewer agent names
     - `scope_preservation`: Should be `true`
     - `codebase_analyzed`: Verify codebase analysis was performed
     - `validated`: Should be `true` (indicates PRD was validated)
   - Verify PRD has Document Status completion marker
   - If validation fails, report specific error and halt
   - If successful, extract metadata for task generation

2. **Receive PRD Reference:** The user points the AI to a specific PRD file via $ARGUMENTS

3. **Parse PRD Content:** Read and analyze the PRD completely:
    - All functional requirements exactly as specified
    - User stories and acceptance criteria
    - Explicit scope boundaries (included/excluded)
    - Testing requirements (only if specified)
    - Security requirements (only if specified)

4. **Analyze PRD Fidelity Metadata:** Extract fidelity information from validated PRD YAML front-matter:
   - Scope boundaries and exclusions
   - Fidelity preservation settings
   - Explicit requirements vs assumptions

5. **Systematically Discover Implementation Files:** Analyze codebase for affected files:
   - Use Glob to find files matching patterns mentioned in PRD: `**/*[pattern]*`
   - Use Grep to search for relevant classes, functions, and APIs mentioned in PRD
   - Identify files that will need:
     - Creation (new files)
     - Modification (existing files)
     - Integration (connection points)
   - **Use parallel tool calls** for faster file discovery
   - Populate "Relevant Files" section with:
     - File paths
     - Current status (exists/new)
     - Purpose (based on PRD requirements)
     - Estimated scope of changes
   - Document integration points and dependencies discovered

6. **Generate Task List:** Create comprehensive task list with fidelity preservation:
   - Generate parent tasks (3-7 essential tasks covering all requirements)
   - Generate detailed sub-tasks for each parent
   - Include testing tasks only if specified in PRD
   - Add security tasks only if specified in PRD
   - Include documentation only if specified in PRD
   - Use discovered implementation files for Relevant Files section
   - Preserve fidelity metadata from PRD in YAML front-matter

7. **Validate Task Coverage:** Before saving, verify task completeness:
   - Check all PRD requirements have corresponding tasks
   - Verify no scope expansion beyond PRD
   - Confirm testing/security tasks match PRD specifications
   - Ensure Relevant Files section is populated with discoveries
   - Check YAML front-matter is complete:
     - Source PRD path
     - Fidelity mode (from PRD)
     - Agent specifications (from PRD)
   - Add `validated: true` flag to YAML
   - If validation finds gaps, report to user for clarification
   - If validation passes, proceed to save

8. **Save and Report:** Save validated task list:
   - Save tasks to `/tasks/tasks-[prd-file-name].md`
   - Report validation results to user
   - Confirm task list is ready for processing (prd/3:process-tasks)
   - Inform user of file location for review

## Output Format

The generated task list _must_ follow this structure with YAML front-matter:

```markdown
---
version: 1
fidelity_mode: strict
source_prd: [path to source PRD file]
agents:
  developer: developer-fidelity
  reviewer: quality-reviewer-fidelity
scope_preservation: true
additions_allowed: none
specification_metadata:
  source_file: [PRD file path]
  conversion_date: [timestamp YYYY-MM-DD]
  fidelity_level: absolute
  scope_changes: none
validated: true
---

# [Feature Name] - Implementation Tasks

## Relevant Files

*Discovered through systematic codebase analysis (Glob/Grep)*

### Files to Create
- `path/to/new/file1.ts` - [Purpose from PRD]
- `path/to/new/file1.test.ts` - Unit tests for file1.ts

### Files to Modify
- `path/to/existing/component.tsx` (exists) - [Changes needed per PRD]
  *Lines/functions affected: [specific locations if known]*
- `path/to/existing/service.ts` (exists) - [Changes needed per PRD]

### Integration Points
- [Existing API/service that will be integrated with]
- [Shared utility/component that will be leveraged]

### Documentation
- `README.md` - Update with feature description and usage
- `docs/api/[feature].md` - API documentation (if applicable)
- `docs/guides/[feature]-usage.md` - User guide (if complex)

### Notes

- Use test commands defined in TESTING.md or CLAUDE.md.
- Use `/docs:update` command for comprehensive documentation updates.
- Integrate technical-writer agent for complex documentation tasks.

## Tasks

- [ ] 1.0 Parent Task Title
  - [ ] 1.1 [Sub-task description 1.1]
  - [ ] 1.2 [Sub-task description 1.2]
- [ ] 2.0 Parent Task Title
  - [ ] 2.1 [Sub-task description 2.1]
- [ ] 3.0 Parent Task Title (may not require sub-tasks if purely structural or configuration)
- [ ] N.0 Complete Feature Documentation
  - [ ] N.1 Run `/docs:update` to update comprehensive documentation
  - [ ] N.2 Update README.md with feature overview and usage examples
  - [ ] N.3 Create/update API documentation for new endpoints or interfaces  
  - [ ] N.4 Create user guides for complex features or workflows
  - [ ] N.5 Validate documentation accuracy against implementation
  - [ ] N.6 Review documentation for completeness and clarity
```

## Key Principles

1. **Single-Phase Generation:** Generate complete task list (parent + sub-tasks) with validation gates
2. **Validation-First:** Validate PRD before reading, validate tasks before saving
3. **Codebase-Aware:** Use Glob/Grep to discover actual implementation files
4. **Parallel Efficiency:** Use parallel tool calls for faster file discovery
5. **Metadata Continuity:** Preserve YAML front-matter from PRD → tasks
6. **Absolute Fidelity:** No scope expansion beyond PRD specifications
7. **Task Coverage:** Every PRD requirement has corresponding tasks

## Target Audience

Assume the primary reader of the task list is a **junior developer** who will implement the feature with awareness of the existing codebase context.

# Task List Management

Guidelines for managing task lists in markdown files to track progress on completing a PRD

## Task Implementation

- **One sub-task at a time:** Do **NOT** start the next sub‑task until you ask the user for permission and they say "yes" or "y"
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
    - References the task number and PRD context
    - **Formats the message as a single-line command using `-m` flags**, e.g.:

      ```
      git commit -m "feat: add payment validation logic" -m "- Validates card type and expiry" -m "- Adds unit tests for edge cases" -m "Related to T123 in PRD"
      ```
  3. Once all the subtasks are marked completed and changes have been committed, mark the **parent task** as completed.

- Stop after each sub‑task and wait for the user's go‑ahead.

## Task List Maintenance

1. **Update the task list as you work:**
   - Mark tasks and subtasks as completed (`[x]`) per the protocol above.
   - Add new tasks as they emerge.

2. **Maintain the "Relevant Files" section:**
   - List every file created or modified.
   - Give each file a one‑line description of its purpose.

## AI Instructions

When working with task lists, the AI must:

1. Regularly update the task list file after finishing any significant work.
2. Follow the completion protocol:
   - Mark each finished **sub‑task** `[x]`.
   - Mark the **parent task** `[x]` once **all** its subtasks are `[x]`.
3. Add newly discovered tasks.
4. Keep "Relevant Files" accurate and up to date.
5. Before starting work, check which sub‑task is next.
6. After implementing a sub‑task, update the file and then pause for user approval.
