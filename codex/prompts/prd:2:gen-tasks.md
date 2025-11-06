# Rule: Generating a Task List from a PRD with Fidelity Preservation

## Goal

To guide an AI assistant in creating a detailed, step-by-step task list in Markdown format with YAML front-matter based on an existing Product Requirements Document (PRD). The system uses fidelity-preserving agents to ensure exact scope implementation. Think harder.

## Fidelity Preservation

This command follows the fidelity-preserving approach to:

1. **Parse PRD Content:** Extract all requirements exactly as specified in the PRD
2. **Preserve Scope Boundaries:** Maintain exact scope without additions or expansions
3. **Minimal Task Detail:** Create only tasks necessary to implement specified requirements
4. **Apply Only Specified Validation:** Include testing and validation only as specified in PRD

## Output

- **Format:** Markdown (`.md`)
- **Location:** `/tasks/`
- **Filename:** `tasks-[prd-file-name].md` (e.g., `tasks-prd-user-profile-editing.md`)

## Process

1.  **Receive PRD Reference:** The user points the AI to a specific PRD file via $ARGUMENTS
2.  **Parse PRD Content:** Read and analyze the PRD completely:
    - All functional requirements exactly as specified
    - User stories and acceptance criteria
    - Explicit scope boundaries (included/excluded)
    - Testing requirements (only if specified)
    - Security requirements (only if specified)
3.  **Analyze PRD Fidelity Metadata:** Extract fidelity information from PRD YAML front-matter:
    - Scope boundaries and exclusions
    - Fidelity preservation settings
    - Explicit requirements vs assumptions
4.  **Assess Current State:** Review existing codebase for implementation context:
    - Identify relevant existing files and patterns
    - Understand current architecture for integration
    - Note files that will need modification
5.  **Phase 1: Generate Essential Parent Tasks:** Create high-level tasks that implement only specified requirements:
    - Focus on core functionality from PRD
    - Include only testing/security as specified in PRD
    - 3-7 essential tasks covering all explicit requirements
6.  **Wait for Confirmation:** Pause and wait for user to respond with "Go"
7.  **Phase 2: Generate Implementation Sub-Tasks:** Break down tasks with fidelity preservation:
    - Include testing tasks only if specified in PRD
    - Add security tasks only if specified in PRD  
    - Include documentation only if specified in PRD
8.  **Generate Task List with Fidelity Metadata:** Create file with YAML front-matter preserving PRD fidelity
9.  **Save Task List:** Save as `tasks-[prd-file-name].md` with fidelity preservation metadata

## Output Format

The generated task list _must_ follow this structure with YAML front-matter:

```markdown
---
version: 1
fidelity_mode: strict
source_prd: [path to source PRD file]
scope_preservation: true
additions_allowed: none
specification_metadata:
  source_file: [PRD file path]
  conversion_date: [timestamp]
  fidelity_level: absolute
  scope_changes: none
---

# [Feature Name] - Implementation Tasks

## Relevant Files

Document the surface area the implementation is likely to touch:

- Highlight existing files that require updates and why they matter.
- Call out new files or directories that need to be created.
- Include documentation or test assets only when the PRD explicitly requires them.

### Notes

- Use test commands defined in TESTING.md (or the repository's documented process).
- Reference AGENTS.md for available fidelity agents and support roles.
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

## Interaction Model

The process explicitly requires a pause after generating parent tasks to get user confirmation ("Go") before proceeding to generate the detailed sub-tasks. This ensures the high-level plan aligns with user expectations before diving into details.

## Target Audience

Assume the primary reader of the task list is a **junior developer** who will implement the feature with awareness of the existing codebase context.

# Task List Management

Guidelines for managing task lists in markdown files to track progress on completing a PRD

## Task Implementation

- **One sub-task at a time:** Do **NOT** start the next sub‑task until you ask the user for permission and they say "yes" or "y"
- **Completion protocol:**
  1. When you finish a **sub‑task**, immediately mark it as completed by changing `[ ]` to `[x]`.
  2. If **all** subtasks underneath a parent task are now `[x]`, follow this sequence:
  - **First**: Run the full test suite as defined in TESTING.md or the repository's documented process
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
