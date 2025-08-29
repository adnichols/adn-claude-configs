---
description: Create comprehensive documentation for completed features using technical-writer agent
argument-hint: [@feature-files]
---

# Rule: Post-Implementation Documentation

## Goal

To automatically create and update comprehensive documentation for completed features, including README files, API specifications, user guides, and application documentation using the technical-writer agent.

## Usage

```bash
/build:document                           # Auto-detect completed features needing documentation
/build:document @src/components/auth/     # Document specific feature/module
/build:document @tasks/tasks-user-auth.md # Document based on completed task list
```

**Parameters:**
- `@feature-files` (optional): Specific files, directories, or task lists to document
- If no parameters provided, auto-detect recently implemented features from git history

## Detection Logic

The command follows this priority order to identify what needs documentation:

1. **Explicit Input**: If files/directories provided, document those features
2. **Recent Commits**: Analyze recent commits for new features (`feat:` commits in last 10 commits)
3. **Completed Task Lists**: Look for recently completed task files in `/tasks/` directory
4. **Modified Files**: Identify significant code changes that need documentation updates

## Process

1. **Detect Features**: Identify completed features that need documentation
2. **Analyze Implementation**: Review the actual code implementation and functionality
3. **Identify Documentation Targets**:
   - Main README.md updates
   - API documentation files
   - Feature-specific documentation
   - Configuration documentation
   - User guides or tutorials
4. **Generate Documentation**: Use technical-writer agent to create comprehensive documentation
5. **Update Existing Docs**: Ensure existing documentation is updated to reflect new features
6. **Validate Documentation**: Check that documentation accurately reflects implementation

## Implementation

The AI should:

1. **Feature Detection**:
   ```bash
   # Check for recent feature commits
   git log --oneline -10 --grep="^feat:"
   
   # Look for completed task files
   find tasks/ -name "tasks-*.md" -newer $(date -d '7 days ago' +%Y%m%d) 2>/dev/null
   
   # Identify recently modified significant files
   git diff --name-only HEAD~7..HEAD | grep -E '\.(js|ts|jsx|tsx|py|go|rs)$'
   
   # Check for new API endpoints or significant functionality
   git log --stat --since="1 week ago" --grep="^feat:"
   ```

2. **Implementation Analysis**:
   ```bash
   # Read implementation files to understand functionality
   # Analyze public APIs, configuration options, and user-facing features
   # Extract key usage patterns and integration points
   ```

3. **Documentation Target Identification**:
   ```bash
   # Check for existing documentation files
   find . -name "README*.md" -o -name "API*.md" -o -name "USAGE*.md" -o -name "docs/*"
   
   # Identify documentation that needs updates based on changes
   # Look for configuration files that might need documentation updates
   ```

4. **Launch technical-writer agent** with comprehensive context:

   **Agent Prompt Structure:**
   ```
   Task: Create comprehensive documentation for the completed feature implementation.
   
   IMPLEMENTATION ANALYSIS:
   [Detailed analysis of the implemented feature, its functionality, and integration points]
   
   CODE EXAMPLES:
   [Key code snippets showing usage patterns and API interfaces]
   
   EXISTING DOCUMENTATION CONTEXT:
   [Current state of README, API docs, and other relevant documentation]
   
   DOCUMENTATION TARGETS:
   [Specific files that need creation or updates]
   
   Please create:
   1. Updated README sections for new features
   2. API documentation for new endpoints/interfaces  
   3. Configuration documentation for new options
   4. Usage examples and integration guides
   5. Any feature-specific documentation files needed
   
   Follow the technical-writer agent guidelines for concise, actionable documentation.
   Ensure documentation accurately reflects the actual implementation.
   ```

5. **Documentation Generation**:
   - Create new documentation files as needed
   - Update existing README.md with new features
   - Generate API documentation for new interfaces
   - Create usage examples and integration guides
   - Update configuration documentation

6. **Validation and Integration**:
   - Verify documentation accuracy against implementation
   - Ensure consistency with existing documentation style
   - Check that all user-facing features are documented
   - Validate that examples actually work

## Documentation Types

The command should handle these documentation categories:

### Core Documentation
- **README.md updates**: Feature descriptions, installation, basic usage
- **API Documentation**: Interface definitions, endpoint documentation
- **Configuration Files**: Environment variables, config options, settings

### User-Facing Documentation  
- **Usage Guides**: Step-by-step instructions for new features
- **Integration Examples**: How to integrate with existing systems
- **Troubleshooting**: Common issues and solutions

### Developer Documentation
- **Architecture Notes**: How the feature fits into the overall system
- **Extension Points**: How to extend or customize the feature
- **Testing Documentation**: How to test the new functionality

## Output

The command creates/updates documentation files and provides a summary:

```
# Documentation Update Summary

## Features Documented
- [List of features that were documented]

## Files Created/Updated
- README.md - Added section on [feature name]
- docs/api/[feature].md - New API documentation  
- docs/guides/[feature]-usage.md - Usage guide created
- [Other updated files]

## Validation Results
- [x] Documentation accuracy verified against implementation
- [x] Examples tested and working
- [x] Consistency with existing docs confirmed
- [x] All user-facing features documented

## Next Steps
- Review generated documentation for completeness
- Consider adding screenshots or diagrams if needed
- Update any related tutorial or getting-started guides
```

## Integration Notes

- Works with any codebase and programming language
- Respects existing documentation structure and style
- Can be run after feature completion or during development
- Integrates with technical-writer agent for consistent output
- Supports both auto-detection and explicit feature specification

## Quality Standards

- **Accuracy**: Documentation must match actual implementation
- **Completeness**: All user-facing features must be documented
- **Usability**: Documentation should enable users to successfully use features
- **Maintainability**: Documentation should be easy to keep updated
- **Consistency**: Follow established documentation patterns and style