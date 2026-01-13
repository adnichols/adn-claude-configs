---
description: Integrate spec review comments into the specification
argument-hint: "<path to specification>"
---

# Integrate Specification Review Comments

Integrate all reviewer comments from a multi-model specification review into the specification itself, resolving all open questions and concerns.

**Specification to integrate:** $ARGUMENTS

## Process

### 0. Gather Comment Files

Locate and read all comment files from reviewers:

**Option 1 - Review file pattern** (if review files are in the same directory as spec):
- `{spec_path}.review-qwen.md`
- `{spec_path}.review-kimi.md`
- `{spec_path}.review-deepseek.md`

**Option 2 - Filename-based pattern** (if review files match spec filename without extension):
- Extract the filename (without path and extension) from `spec_path`
- `{spec_filename}.review-qwen.md`
- `{spec_filename}.review-kimi.md`
- `{spec_filename}.review-deepseek.md`

Check both patterns and read any files that exist.

If a reviewer failed or produced no comments, that comment file may be missing - this is acceptable.

Read all available comment files. If none exist, inform the user that no review data was found and abort.

### 1. Read and Catalog All Comments

From the comment files, extract all reviewer feedback and parse each comment to extract:
- **Reviewer**: Qwen, Kimi, or DeepSeek
- **Section**: Which section of the spec it references (from `SECTION "..."` format)
- **Content**: The actual comment feedback

Create a working list of all feedback items to address.

### 2. Read the Original Specification

Read the original specification file to:
- Understand the full context of the document
- Locate the sections referenced in comments
- Have the proper content to update

### 3. Explore Codebase for Resolution Context

Before resolving comments, gather codebase context that informs decisions:
- Existing patterns that answer feasibility questions
- Related implementations that inform technical decisions
- Constraints or conventions that resolve ambiguities

Use the Task tool with `subagent_type=Explore` to efficiently research.

### 4. Triage Comments by Confidence

For each comment, determine your confidence level in resolving it:

**High Confidence (Resolve Autonomously):**
- Clear technical questions with definitive answers from codebase research
- Missing details that have obvious correct answers
- Concerns already addressed elsewhere in the spec
- Suggestions that align with established patterns
- Inconsistencies with clear resolutions

**Low Confidence (Ask User):**
- Business logic decisions with multiple valid options
- Scope decisions (include/exclude features)
- Priority or phasing decisions
- Trade-offs between competing concerns
- Requirements that need stakeholder input
- Ambiguities where codebase doesn't provide guidance

### 5. Batch User Questions

Collect all low-confidence items and ask the user. Group related questions together. For each question:
- Provide context from the reviewer comments
- Explain the options or trade-offs
- Indicate which reviewers raised the concern
- Suggest a recommendation if you have one

Example:
```
Multiple reviewers raised concerns about error handling scope:

[GLM] SECTION "Error Handling": Should we handle network timeouts differently from API errors?
[Kimi] noted: Error retry logic not specified - is this in scope?

Options:
A) Unified error handling - treat all errors the same way
B) Differentiated handling - separate strategies for network vs API errors
C) Defer to existing patterns - use whatever error handling exists in codebase

Recommendation: B seems appropriate given the complexity, but this affects scope.
```

### 6. Integrate Resolutions

For each resolved comment:

1. **Locate the section** in the specification that was referenced
2. **Update the specification** - Insert an HTML comment at the beginning of the referenced section with the integrated feedback:
   ````markdown
   <!-- [Integrated {reviewer_name} feedback]: {resolved feedback} -->
   ````
3. **Add clarifying content** - Where comments identified gaps, add the missing information to the specification text
4. **Modify the relevant section** - Update to address the feedback directly in the section content

Integration principles:
- Preserve the spec's voice and structure
- Add detail where reviewers identified gaps
- Clarify ambiguous language
- Add constraints or requirements that were missing
- Update technical approach based on feasibility feedback

### 7. Document Decisions

At the end of the specification, add or update a "Review Resolution Log" section:

```markdown
## Review Resolution Log

### Integrated Feedback - [Date]

**Reviewers:** Qwen, Kimi, DeepSeek

**Key Decisions Made:**
- [Decision 1]: [Rationale]
- [Decision 2]: [Rationale]

**User Decisions:**
- [Question]: [User's decision]

**Deferred Items:**
- [Item]: [Reason for deferral]
```

### 8. Clean Up Temporary Files

After successful integration, delete the comment files:

```bash
rm -f {spec_path}.review-qwen.md
rm -f {spec_path}.review-kimi.md
rm -f {spec_path}.review-deepseek.md
```

The reviews are preserved in git history if committed, and the summary report documents all decisions.

If integration fails (e.g., due to an error mid-process), KEEP the comment files so the user can debug or manually reconcile.

### 9. Final Validation

After integration:
- Re-read the full specification for coherence
- Verify all sections referenced in comments have been addressed
- Check that all reviewer concerns are addressed
- Ensure the spec is internally consistent

### 10. Summary Report

Provide the user with:
- Number of comments integrated
- Number of comments from each reviewer
- Key decisions made autonomously (with brief rationale)
- Decisions made based on user input
- Any items deferred or flagged for future consideration
- Confirmation that comment files were deleted (or preserved if integration failed)
- Confirmation that spec is ready for next phase

## Decision-Making Guidelines

**Resolve autonomously when:**
- The codebase clearly indicates the correct approach
- Industry best practices apply unambiguously
- The concern is about clarity, not direction
- One option is clearly superior given constraints
- The feedback is about missing detail, not missing decisions

**Ask the user when:**
- Multiple valid approaches exist with real trade-offs
- The decision affects scope, timeline, or resources
- Business logic is involved
- You're genuinely uncertain
- Reviewers disagreed and both have valid points

## Output

The specification file should be updated in place with:
- All feedback integrated from comment files
- Review Resolution Log added/updated
- Clean, coherent specification ready for implementation

The temporary comment files should be deleted after successful integration. If integration fails, comment files are preserved for debugging.

---

## ➡️ Next Steps

After integration completes, the specification is ready for:
- `/spec:2:gen-tasks` - Generate implementation tasks
- Additional review cycles if significant changes were made
