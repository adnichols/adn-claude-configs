---
description: Update existing core documentation (README, TESTING, CLAUDE.md) for completed features
argument-hint: [@feature-files]
---

# Rule: Core Documentation Updates

## Goal

To update existing core documentation files (README.md, TESTING.md, CLAUDE.md) and any pre-existing documentation for completed features using the technical-writer agent.

Also follow this repository's `AGENTS.md` for project-specific documentation and review expectations.

## Usage

```bash
/docs:update                              # Update core docs based on recent changes
/docs:update @src/components/auth/        # Update docs for specific feature/module
/docs:update @tasks/tasks-user-auth.md    # Update docs based on completed task list
```

**Parameters:**
- `@feature-files` (optional): Specific files, directories, or task lists to document
- If no parameters provided, analyze recent git changes for core documentation updates

## Target Files

Primary focus on existing core documentation:

1. **README.md** - Main project documentation
2. **TESTING.md** - Test documentation and procedures  
3. **CLAUDE.md** - Project instructions and configuration
4. **Pre-existing docs** - Update any other existing documentation files only

## Process

1. **Identify Changes**: Determine what features/changes need documentation updates
2. **Review Implementation**: Analyze the actual code changes and functionality
3. **Find Existing Docs**: Locate README.md, TESTING.md, CLAUDE.md and any other existing documentation
4. **Update Documentation**: Use technical-writer agent to update existing files only
5. **Validate Updates**: Ensure documentation accurately reflects current implementation

## Implementation

The AI should:

1. **Change Analysis**:
   - If no feature files are provided, inspect recent git history (for example, using `git log` and `git diff --name-only`) to find changed areas that may need documentation updates.

2. **Find Existing Documentation**:
   - Locate core documentation files (README.md, TESTING.md, CLAUDE.md).
   - Identify any other existing documentation files that may be relevant.

3. **Launch technical-writer agent** with focused context:

   - Provide the technical-writer agent with:
     - A summary of changes to document.
     - The current contents of README.md, TESTING.md, CLAUDE.md, and any other relevant docs.
     - A clear instruction to update only existing docs, not create new ones.

4. **Documentation Updates**:
   - Update existing README.md sections as needed
   - Update TESTING.md if test procedures changed  
   - Update CLAUDE.md if project instructions changed
   - Update any other existing documentation files

5. **Validation**:
   - Verify documentation accuracy against implementation
   - Ensure consistency with existing documentation style
   - Validate that information is current and correct

## Output

The command updates existing documentation and provides a summary:

```
# Documentation Update Summary

## Changes Documented
- [List of features/changes that were documented]

## Files Updated
- README.md - [Description of updates made]
- TESTING.md - [Updated test procedures if applicable]  
- CLAUDE.md - [Updated project instructions if applicable]
- [Other existing files updated]

## Validation Results
- [x] Documentation accuracy verified against implementation
- [x] Consistency with existing documentation style maintained
- [x] All updates reflect current implementation

## Next Steps
- Review updated documentation for accuracy
- Ensure any related existing docs are also current
```

## Integration Notes

- Works with any codebase and programming language
- Updates existing documentation only - does not create new files
- Respects existing documentation structure and style
- Integrates with technical-writer agent for consistent updates
- Focuses on core documentation: README, TESTING, CLAUDE files

## Quality Standards

- **Accuracy**: Updates must match actual implementation
- **Existing Focus**: Only update existing documentation files
- **Consistency**: Follow established documentation patterns and style
- **Maintainability**: Keep existing documentation current and accurate
