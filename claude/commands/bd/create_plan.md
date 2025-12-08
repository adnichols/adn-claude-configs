---
description: Create implementation plans as beads issues
model: opus
---

# Create Plan (Beads-Only)

You are tasked with creating detailed implementation plans through an interactive, iterative process. All plan details are stored directly in beads issues - there are no separate plan files.

**Beads is the sole source of truth for implementation plans.**

## Initial Response

When this command is invoked:

1. **Check if parameters were provided**:
   - If a file path or ticket reference was provided, read it immediately and FULLY
   - Begin the research process

2. **If no parameters provided**, respond with:
   ```
   I'll help you create a detailed implementation plan tracked in beads.

   Please provide:
   1. The task/ticket description (or reference to a ticket file)
   2. Any relevant context, constraints, or specific requirements
   3. Links to related research or previous implementations

   I'll analyze this and work with you to create implementation issues in beads.

   Tip: You can invoke this command with a ticket file: `/bd:create_plan thoughts/linear/nod_1234.md`
   ```

   Then wait for the user's input.

## Process Steps

### Step 1: Context Gathering & Initial Analysis

1. **Read all mentioned files immediately and FULLY**:
   - Ticket files (e.g., `thoughts/linear/nod_1234.md`)
   - Research documents
   - Any JSON/data files mentioned
   - **IMPORTANT**: Use the Read tool WITHOUT limit/offset parameters
   - **NEVER** read files partially

2. **Spawn research tasks to gather context**:
   Before asking questions, use specialized agents in parallel:

   - **codebase-locator** - Find all files related to the task
   - **codebase-analyzer** - Understand current implementation
   - **thoughts-locator** - Find existing thoughts documents about this feature

3. **Read all files identified by research tasks** FULLY into main context

4. **Analyze and verify understanding**:
   - Cross-reference requirements with actual code
   - Identify discrepancies or misunderstandings
   - Note assumptions needing verification

5. **Present informed understanding**:
   ```
   Based on the ticket and my research, I understand we need to [summary].

   I've found that:
   - [Discovery with file:line reference]
   - [Pattern or constraint discovered]
   - [Potential complexity identified]

   Questions my research couldn't answer:
   - [Technical question requiring human judgment]
   - [Business logic clarification]
   ```

### Step 2: Research & Discovery

After getting clarifications:

1. **If the user corrects any misunderstanding**:
   - Spawn new research tasks to verify
   - Read the specific files they mention
   - Only proceed once verified

2. **Create a research tracking issue**:
   ```bash
   bd create --title "Research: [feature name]" --type task
   bd update <id> --status in_progress
   ```

3. **Spawn parallel sub-tasks** for comprehensive research:
   - **codebase-pattern-finder** - Find similar features to model after
   - **codebase-analyzer** - Understand specific components
   - **thoughts-analyzer** - Extract insights from relevant documents

4. **Close research when complete**:
   ```bash
   bd close <id> --reason "Research complete"
   ```

5. **Present findings and design options**:
   ```
   Based on my research:

   **Current State:**
   - [Key discovery about existing code]
   - [Pattern or convention to follow]

   **Design Options:**
   1. [Option A] - [pros/cons]
   2. [Option B] - [pros/cons]

   Which approach aligns best with your vision?
   ```

### Step 3: Plan Structure Development

Once aligned on approach:

1. **Present the proposed phase structure**:
   ```
   Here's my proposed implementation structure:

   ## Overview
   [1-2 sentence summary]

   ## Phases:
   1. [Phase name] - [what it accomplishes]
   2. [Phase name] - [what it accomplishes]
   3. [Phase name] - [what it accomplishes]

   Does this phasing make sense? Should I adjust the order or granularity?
   ```

2. **Get feedback on structure** before creating issues

### Step 4: Create Beads Issues

After structure approval, create detailed beads issues for each phase:

1. **Create a parent epic** (if multiple phases):
   ```bash
   bd create --title "[Feature Name] Implementation" --type epic
   ```

2. **Create phase issues with full detail**:

   Each phase issue should include ALL implementation details in the description. Use this format:

   ```bash
   bd create --title "Phase 1: [Descriptive Name]" --type task
   ```

   Then update with full description:
   ```bash
   bd update <id> --description "$(cat <<'EOF'
   ## Overview
   [What this phase accomplishes]

   ## Changes Required

   ### 1. [Component/File Group]
   **File**: `path/to/file.ext`
   **Changes**: [Summary]

   ```[language]
   // Specific code to add/modify
   ```

   ### 2. [Next Component]
   ...

   ## Success Criteria

   ### Automated Verification
   - [ ] Tests pass: `pnpm test:unit`
   - [ ] Build succeeds: `pnpm build`
   - [ ] Lint passes: `pnpm lint`

   ### Manual Verification
   - [ ] Feature works as expected in UI
   - [ ] No regressions in related features

   ## References
   - Related file: `path/to/file.ext:123`
   - Similar pattern: `path/to/example.ext:45`
   EOF
   )"
   ```

3. **Set up dependencies** between phases:
   ```bash
   bd dep add <phase-2-id> <phase-1-id>   # Phase 2 depends on Phase 1
   bd dep add <phase-3-id> <phase-2-id>   # Phase 3 depends on Phase 2
   ```

4. **Link phases to epic**:
   ```bash
   bd dep add <phase-1-id> <epic-id>
   bd dep add <phase-2-id> <epic-id>
   bd dep add <phase-3-id> <epic-id>
   ```

### Step 5: Review and Finalize

1. **Show the created structure**:
   ```bash
   bd show <epic-id>
   bd list --status=open
   ```

2. **Present for review**:
   ```
   I've created the implementation plan in beads:

   Epic: <epic-id> - [Feature Name] Implementation

   Phases (in order):
   1. <phase-1-id> - [Phase 1 name]
   2. <phase-2-id> - [Phase 2 name]
   3. <phase-3-id> - [Phase 3 name]

   Run `bd show <id>` to review any issue's full details.

   Ready to start implementation? Run `/bd:implement_plan` or `bd update <phase-1-id> --status in_progress`
   ```

3. **Iterate based on feedback** - be ready to:
   - Add missing phases
   - Adjust technical approach
   - Update success criteria
   - Add/remove scope

4. **Sync when done**:
   ```bash
   bd sync
   ```

## Important Guidelines

1. **Be Skeptical**:
   - Question vague requirements
   - Identify potential issues early
   - Don't assume - verify with code

2. **Be Interactive**:
   - Don't create all issues in one shot
   - Get buy-in at each major step
   - Allow course corrections

3. **Be Thorough**:
   - Read all context files COMPLETELY
   - Include specific file paths and line numbers in issue descriptions
   - Write measurable success criteria

4. **Be Practical**:
   - Focus on incremental, testable changes
   - Consider migration and rollback
   - Think about edge cases

5. **No Open Questions**:
   - If you encounter open questions, STOP
   - Research or ask for clarification
   - Every decision must be made before creating issues

## Issue Description Guidelines

Each phase issue should be self-contained with:

1. **Overview** - What this phase accomplishes
2. **Changes Required** - Specific files and code changes
3. **Success Criteria** - Split into:
   - **Automated**: Commands to run (`pnpm test`, `pnpm build`, etc.)
   - **Manual**: UI/UX verification steps
4. **References** - File:line references, similar patterns

**Example issue description:**
```markdown
## Overview
Add database migration for user preferences table.

## Changes Required

### 1. Migration File
**File**: `supabase/migrations/20250607_user_preferences.sql`

```sql
CREATE TABLE user_preferences (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES profiles(id),
  theme TEXT DEFAULT 'light',
  created_at TIMESTAMPTZ DEFAULT now()
);

-- RLS policies
ALTER TABLE user_preferences ENABLE ROW LEVEL SECURITY;
```

### 2. Type Definitions
**File**: `lib/db/types.ts`
Add UserPreferences type matching the new table.

## Success Criteria

### Automated Verification
- [ ] Migration applies: `pnpm db:migrate`
- [ ] Types generate: `pnpm supabase:types`
- [ ] Build passes: `pnpm build`

### Manual Verification
- [ ] Table visible in Supabase Studio
- [ ] RLS policies working correctly

## References
- Similar migration: `supabase/migrations/20250101_profiles.sql:1`
- RLS pattern: `supabase/migrations/20250102_workspaces.sql:45`
```

## Common Patterns

### For Database Changes:
1. Schema/migration phase
2. Type definitions phase
3. Query functions phase
4. API integration phase

### For New Features:
1. Data model phase
2. Backend logic phase
3. API endpoints phase
4. UI implementation phase

### For Refactoring:
1. Document current behavior
2. Create new implementation
3. Migration/switchover
4. Cleanup old code
