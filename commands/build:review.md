---
description: Review pending changes using quality-reviewer agent before creating PR
argument-hint: [@specification-file]
---

# Rule: Pre-PR Quality Review

## Goal

To automatically identify and review pending changes in a repository using the quality-reviewer agent, focusing on production-ready code quality, security, performance, and potential data loss issues before creating a pull request.

## Usage

```bash
/build:review                              # Auto-detect context and changes
/build:review @tasks/tasks-feature-xyz.md  # Use specific specification file
/build:review @prd/user-authentication.md  # Use PRD as context
```

**Parameters:**
- `@specification-file` (optional): Explicit context file containing original requirements, specifications, or task list
- If no specification provided, the command auto-detects context from branch name, recent task files, and commit history

## Change Detection Logic

The command follows this priority order to identify what to review:

1. **Staged Changes**: If there are staged files (`git diff --cached --name-only`), review those changes
2. **Unstaged Changes**: If no staged changes but unstaged modifications exist (`git diff --name-only`), review those
3. **Recent Commits**: If working directory is clean, review the most recent commit(s) on the current branch that aren't on main

## Input Processing

If a specification file is provided via `@filename` syntax, the file content will be automatically included and used as the primary context. Otherwise, the command will auto-detect context as described below.

## Process

1. **Determine Context Source**: 
   - If specification file provided: Use that as primary context
   - If no specification: Auto-detect context using the priority order below

2. **Detect Changes**: Run git commands to identify what changes need review based on the logic above
3. **Gather Context**: Collect the actual diff content for the identified changes  
4. **Quality Review**: Use the quality-reviewer agent to analyze the changes for:
   - Security vulnerabilities
   - Potential data loss scenarios  
   - Performance issues
   - Production failure risks
   - Code quality and maintainability
5. **Generate Report**: Present findings with severity levels and actionable recommendations

## Implementation

The AI should:

1. **Run git status checks** to determine what changes exist:
   ```bash
   # Check for staged changes
   git diff --cached --name-only
   
   # Check for unstaged changes  
   git diff --name-only
   
   # Check for untracked files
   git ls-files --others --exclude-standard
   
   # Get recent commits if working directory is clean
   git log --oneline main..HEAD
   ```

2. **Collect diff content** for the identified changes:
   ```bash
   # For staged changes
   git diff --cached
   
   # For unstaged changes
   git diff
   
   # For recent commits
   git diff main..HEAD
   ```

3. **Gather context** to understand original intent:

   **If specification file provided via @filename:**
   ```bash
   # Use the provided file as primary context
   # File content is automatically available from the @filename syntax
   echo "Using provided specification: [filename]"
   ```

   **If no specification provided, auto-detect (in priority order):**

   **Primary Context Sources:**
   ```bash
   # 1. Check if current branch has associated task file
   BRANCH=$(git branch --show-current)
   find tasks/ -name "*${BRANCH}*" -o -name "*$(echo $BRANCH | tr '-' '_')*" 2>/dev/null
   
   # 2. Look for commit messages referencing specifications
   git log --oneline -10 | grep -E "(feat:|fix:|refactor:)" | head -5
   
   # 3. Check for recent task files that match modified files
   MODIFIED_FILES=$(git diff --name-only HEAD~5..HEAD)
   # Match task files to modified components
   ```

   **Secondary Context Sources:**
   ```bash
   # 4. Most recent task files as fallback
   ls -t tasks/tasks-*.md 2>/dev/null | head -2
   
   # 5. Look for PRD files in common locations
   find . -name "*.md" -path "*/prd*" -o -name "*prd*.md" -o -path "*/specs*" 2>/dev/null | head -3
   
   # 6. Check CLAUDE.md or README for project context
   [ -f CLAUDE.md ] && echo "CLAUDE.md" || [ -f README.md ] && echo "README.md"
   ```

   **Context Validation:**
   ```bash
   # Read and validate context files exist and are relevant
   # Pass file contents to quality-reviewer agent along with changes
   ```

4. **Launch quality-reviewer agent** with comprehensive context package:

   **Agent Prompt Structure:**
   ```
   Task: Review the following code changes for production readiness, security, and quality issues.
   
   ORIGINAL CONTEXT & INTENT:
   [If @specification provided: Include full content of specified file]
   [If auto-detected: Include contents of detected task files, PRDs, or specifications]
   [If no context found: Note "No original specification context available"]
   
   IMPLEMENTATION CHANGES:
   [Full git diff output]
   
   COMMIT HISTORY CONTEXT:
   [Recent commit messages and branch context]
   
   Please categorize findings as:
   - Critical Issues (blocking for production)
   - Recommended Improvements (important quality concerns) 
   - Optional Enhancements (nice-to-have optimizations)
   
   [If context available: Consider whether changes align with original specifications and requirements]
   [If no context: Focus on general code quality, security, and production readiness]
   ```

   **Context Integration:**
   - **Explicit specification**: Use provided @file content as primary context
   - **Auto-detected context**: Read detected context files and include full content in agent prompt  
   - **Fallback mode**: If no context available, focus on general quality review
   - Provide git diff alongside original intent (when available) for comparison
   - Enable agent to assess specification compliance vs. just code quality

5. **Write report** to `/reports/quality-review-[timestamp].md` with structured sections
   - What changes were reviewed
   - Critical issues found (if any)
   - Recommendations for fixes
   - Overall assessment of PR readiness

## Quality Focus Areas

The quality-reviewer agent should focus on:

- **Security**: Authentication, authorization, input validation, secrets exposure
- **Data Loss**: Database operations, file operations, state management
- **Performance**: N+1 queries, memory leaks, inefficient algorithms
- **Reliability**: Error handling, edge cases, race conditions
- **Maintainability**: Code complexity, documentation, testing coverage

## Output Format

The command writes a detailed Markdown report to `/reports/quality-review-[timestamp].md`:

```markdown
# Quality Review Report - [Date/Time]

## 📋 Changes Reviewed
- **Scope**: [staged changes / unstaged changes / recent commits]
- **Files**: [Number] files, [Number] lines changed
- **Branch**: [current branch name]

## 🎯 Context & Original Intent
[If detected: original specification, task list, or PRD context]

## 🚨 Critical Issues (Must Fix)
[Blocking issues that could cause production failures, security vulnerabilities, or data loss]

## ⚠️ Recommended Improvements (Should Consider)  
[Important quality issues that should be addressed but aren't blocking]

## 💡 Optional Enhancements (Nice to Have)
[Suggestions for code quality, maintainability, or performance optimizations]

## 📊 Overall Assessment
- **PR Readiness**: [Ready / Needs Critical Fixes / Needs Review]
- **Risk Level**: [Low / Medium / High]
- **Recommended Actions**: [Specific next steps]

## 🔧 Suggested Actions
- [ ] **Create task list for critical fixes**: `/user:generate-tasks @reports/quality-review-[timestamp].md`
- [ ] **Review recommendations and create selective task list**
- [ ] **Re-run quality review after fixes**
```

## Error Handling

- If no changes are detected, inform user that working directory is clean
- If git commands fail, provide clear error messages
- If quality-reviewer agent encounters issues, fall back to basic change summary

## Integration Notes

- Works with any git repository
- Respects .gitignore patterns
- Can be run multiple times as changes are made
- Complements existing CI/CD quality gates