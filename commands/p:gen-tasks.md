# Rule: Generating a Task List from a PRD with Router Integration

## Goal

To guide an AI assistant in creating a detailed, step-by-step task list in Markdown format with YAML front-matter based on an existing Product Requirements Document (PRD). The complexity router will determine appropriate task detail level, agent selection, and validation requirements based on the PRD's complexity metadata. Think harder.

## Router Integration

This command integrates with the central complexity router to:

1. **Parse PRD Metadata:** Extract complexity information from PRD YAML front-matter
2. **Inherit Complexity Level:** Use PRD's router-determined complexity for task planning
3. **Select Appropriate Agents:** Use PRD's selected agents for task implementation
4. **Scale Task Detail:** Adjust task granularity based on complexity level
5. **Apply Validation Requirements:** Include complexity-appropriate testing and validation tasks

## Output

- **Format:** Markdown (`.md`)
- **Location:** `/tasks/`
- **Filename:** `tasks-[prd-file-name].md` (e.g., `tasks-prd-user-profile-editing.md`)

## Process

1.  **Receive PRD Reference:** The user points the AI to a specific PRD file
2.  **Parse PRD Metadata:** Extract complexity information from PRD YAML front-matter:
    - Router-determined complexity level
    - Selected agents (developer and reviewer)
    - Risk and nonfunctional requirements
    - Validation requirements
3.  **Call Router for Task Context:** Execute `bash .claude/commands/_lib/complexity/get-complexity.sh [prd-file]` to get:
    - Inherited complexity level
    - Validation requirements for the complexity level
    - Selected agents for implementation
4.  **Analyze PRD Content:** Read and analyze functional requirements, user stories, and other sections
5.  **Assess Current State:** Review existing codebase with complexity-appropriate depth:
    - **Minimum:** Basic pattern identification
    - **Basic:** Standard architecture analysis
    - **Moderate:** Comprehensive integration analysis
    - **Complex:** Enterprise architecture and compliance review
6.  **Phase 1: Generate Complexity-Appropriate Parent Tasks:** Create high-level tasks scaled to complexity:
    - **Minimum:** 3-5 essential tasks
    - **Basic:** 5-7 standard tasks
    - **Moderate:** 7-10 comprehensive tasks
    - **Complex:** 10-15 enterprise-grade tasks
7.  **Wait for Confirmation:** Pause and wait for user to respond with "Go"
8.  **Phase 2: Generate Sub-Tasks with Validation:** Break down tasks including complexity-appropriate validation:
    - Include testing tasks matching router validation requirements
    - Add security tasks based on complexity level
    - Include documentation tasks appropriate to complexity
9.  **Generate Task List with Metadata:** Create file with YAML front-matter containing router metadata
10. **Save Task List:** Save as `tasks-[prd-file-name].md` with complete metadata inheritance

## Output Format

The generated task list _must_ follow this structure with YAML front-matter:

```markdown
---
version: 1
complexity: [inherited from PRD]
source_prd: [path to source PRD file]
agents:
  developer: [router-selected developer agent]
  reviewer: [router-selected reviewer agent]
risk: [inherited from PRD]
nonfunctional: [inherited from PRD]
routing:
  inherited_from: [source PRD file]
  computed_score: [router score]
  validation_requirements: [router validation requirements]
  audit_trail: [router audit information]
---

# [Feature Name] - Implementation Tasks

## Relevant Files

- `path/to/potential/file1.ts` - Brief description of why this file is relevant (e.g., Contains the main component for this feature).
- `path/to/file1.test.ts` - Unit tests for `file1.ts`.
- `path/to/another/file.tsx` - Brief description (e.g., API route handler for data submission).
- `path/to/another/file.test.tsx` - Unit tests for `another/file.tsx`.
- `lib/utils/helpers.ts` - Brief description (e.g., Utility functions needed for calculations).
- `lib/utils/helpers.test.ts` - Unit tests for `helpers.ts`.
- `README.md` - Update main documentation with feature description and usage.
- `docs/api/[feature].md` - API documentation for new endpoints/interfaces (if applicable).
- `docs/guides/[feature]-usage.md` - User guide for the new feature (if complex).

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
