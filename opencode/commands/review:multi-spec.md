---
description: Launch parallel multi-agent specification review (GLM, Kimi, MiniMax)
argument-hint: <path to specification>
---

# Multi-Agent Specification Review

Orchestrate parallel specification reviews from GLM 4.7, Kimi K2, and MiniMax M2.

**Specification to review:** $ARGUMENTS

## Process

### 1. Validate Input

First, verify the specification file exists:
- Read the specification to confirm it's accessible
- Extract the filename (without path and extension) for logging
- Generate unique comment file paths for each reviewer:
  - `{spec_path}.review-glm.md`
  - `{spec_path}.review-kimi.md`
  - `{spec_path}.review-minimax.md`

### 2. Check for Existing Review Files

Verify that no previous review session is in progress:
- Check if any `{spec_path}.review-*.md` files already exist
- If found, warn the user that a previous review may be incomplete
- Get user confirmation before overwriting existing review files

### 3. Launch Parallel Reviews

Launch ALL THREE reviewers in parallel using a single message with multiple Task tool calls:

**GLM 4.7 Reviewer:**
```
Task(
  subagent_type="reviewer-glm",
  description="Review spec with GLM 4.7 thinking",
  prompt=f"""You are [GLM Reviewer] reviewing a SPECIFICATION document.

**Document to review:** {spec_path}
**Comment file to write:** {glm_comment_file}

**Review Process:**
1. Read the specification file completely. Understand:
   - The problem being solved
   - The proposed solution
   - Technical approach and architecture
   - Success criteria and constraints

2. Explore the codebase for context using Task with subagent_type=Explore to understand:
   - Existing patterns and conventions that apply
   - Related implementations that inform feasibility
   - Potential conflicts or integration challenges
   - Missing context that affects the specification

3. Write critical feedback to the comment file at {glm_comment_file}.

4. Format each comment as:
   <!-- [GLM Reviewer] SECTION "{section_name}": {your critical feedback here. Be specific and actionable.} -->

5. Replace {section_name} with the actual section heading from the specification that your comment references. This will help integration place your comment correctly.

6. Look for:
   - Missing requirements or edge cases
   - Technical feasibility issues based on codebase research
   - Integration challenges
   - Ambiguities that need clarification
   - Unrealistic assumptions
   - Gaps in requirements
   - Technical debt creation
   - Security or performance risks
   - Unclear success criteria
   - Scope creep or scope gaps

7. IMPORTANT: Do NOT modify the original specification file. Only write your comments to {glm_comment_file}.

8. IMPORTANT: Write ALL your comments to a single file at {glm_comment_file}. This file should contain only your comments, arranged in logical order (not a copy of the specification).

Focus particularly on deep architectural analysis, system design concerns, long-term technical implications, scalability considerations, and technology choice implications.

Return when you have completed your review and written all comments to {glm_comment_file}."""
)
```

**Kimi K2 Reviewer:**
```
Task(
  subagent_type="reviewer-kimi",
  description="Review spec with Kimi K2 thinking",
  prompt=f"""You are [Kimi Reviewer] reviewing a SPECIFICATION document.

**Document to review:** {spec_path}
**Comment file to write:** {kimi_comment_file}

**Review Process:**
1. Read the specification file completely. Understand:
   - The problem being solved
   - The proposed solution
   - Technical approach and architecture
   - Success criteria and constraints

2. Explore the codebase for context using Task with subagent_type=Explore to understand:
   - Existing patterns and conventions that apply
   - Related implementations that inform feasibility
   - Potential conflicts or integration challenges
   - Missing context that affects the specification

3. Write critical feedback to the comment file at {kimi_comment_file}.

4. Format each comment as:
   <!-- [Kimi Reviewer] SECTION "{section_name}": {your critical feedback here. Be specific and actionable.} -->

5. Replace {section_name} with the actual section heading from the specification that your comment references.

6. Look for:
   - Missing requirements or edge cases
   - Technical feasibility issues based on codebase research
   - Integration challenges
   - Ambiguities that need clarification
   - Unrealistic assumptions
   - Gaps in requirements
   - Technical debt creation
   - Security or performance risks
   - Unclear success criteria
   - Scope creep or scope gaps

7. IMPORTANT: Do NOT modify the original specification file. Only write your comments to {kimi_comment_file}.

8. IMPORTANT: Write ALL your comments to a single file at {kimi_comment_file}.

Focus particularly on integration feasibility, implementation details, component interactions, API design considerations, interface contracts, and dependencies and constraints.

Return when you have completed your review and written all comments to {kimi_comment_file}."""
)
```

**MiniMax M2 Reviewer:**
```
Task(
  subagent_type="reviewer-minimax",
  description="Review spec with MiniMax M2",
  prompt=f"""You are [MiniMax Reviewer] reviewing a SPECIFICATION document.

**Document to review:** {spec_path}
**Comment file to write:** {minimax_comment_file}

**Review Process:**
1. Read the specification file completely. Understand:
   - The problem being solved
   - The proposed solution
   - Technical approach and architecture
   - Success criteria and constraints

2. Explore the codebase for context using Task with subagent_type=Explore to understand:
   - Existing patterns and conventions that apply
   - Related implementations that inform feasibility
   - Potential conflicts or integration challenges
   - Missing context that affects the specification

3. Write critical feedback to the comment file at {minimax_comment_file}.

4. Format each comment as:
   <!-- [MiniMax Reviewer] SECTION "{section_name}": {your critical feedback here. Be specific and actionable.} -->

5. Replace {section_name} with the actual section heading from the specification that your comment references.

6. Look for:
   - Missing requirements or edge cases
   - Technical feasibility issues based on codebase research
   - Integration challenges
   - Ambiguities that need clarification
   - Unrealistic assumptions
   - Gaps in requirements
   - Technical debt creation
   - Security or performance risks
   - Unclear success criteria
   - Scope creep or scope gaps

7. IMPORTANT: Do NOT modify the original specification file. Only write your comments to {minimax_comment_file}.

8. IMPORTANT: Write ALL your comments to a single file at {minimax_comment_file}.

Focus particularly on requirements completeness, edge cases and failure modes, user experience considerations, error handling and recovery, performance implications, security and privacy, and testing and validation approaches.

Return when you have completed your review and written all comments to {minimax_comment_file}."""
)
```

### 4. Wait for Completion

Wait for all three Task agents to complete. They will return when finished.

### 5. Extract Review Data

Read the comment files and count comments by reviewer:

```python
# Read comment files
glm_content = read_file(glm_comment_file) if file_exists(glm_comment_file) else ""
kimi_content = read_file(kimi_comment_file) if file_exists(kimi_comment_file) else ""
minimax_content = read_file(minimax_comment_file) if file_exists(minimax_comment_file) else ""

# Count comments per reviewer
glm_count = glm_content.count("<!-- [GLM Reviewer]")
kimi_count = kimi_content.count("<!-- [Kimi Reviewer]")
minimax_count = minimax_content.count("<!-- [MiniMax Reviewer]")
```

### 6. Identify Overlapping Concerns

Analyze comment sections to identify overlapping concerns from multiple reviewers:

```python
# Extract section names from comment format
def extract_sections(comment_content):
    pattern = r'<!-- \[.*? Reviewer\] SECTION "(.*?)":'
    return re.findall(pattern, comment_content)

glm_sections = extract_sections(glm_content)
kimi_sections = extract_sections(kimi_content)
minimax_sections = extract_sections(minimax_content)

# Find overlapping sections
all_sections = set(glm_sections + kimi_sections + minimax_sections)
overlaps = []
for section in all_sections:
    section_reviewers = []
    if section in glm_sections: section_reviewers.append("GLM Reviewer")
    if section in kimi_sections: section_reviewers.append("Kimi Reviewer")
    if section in minimax_sections: section_reviewers.append("MiniMax Reviewer")
    if len(section_reviewers) > 1:
        overlaps.append({
            "section": section,
            "reviewers": section_reviewers
        })
```

### 7. Report Results

After all reviewers complete, provide a summary:

```markdown
## Multi-Agent Review Complete

**Specification:** {spec-path}
**Review Date:** {YYYY-MM-DD}

### Reviewer Status
| Reviewer | Status | Comments Added |
|----------|--------|----------------|
| GLM 4.7  | {OK/Failed} | {N} |
| Kimi K2  | {OK/Failed} | {N} |
| MiniMax M2 | {OK/Failed} | {N} |

**Total Comments:** {N}

### Overlapping Concerns
{List sections where 2+ reviewers provided feedback}

### Next Steps
Run `/review:spec-integrate {spec-path}` to:
- Integrate all feedback into the specification
- Resolve open questions
- Clean up comment files
```

## Error Handling

- If one reviewer fails, continue with others
- Report which reviewers completed successfully
- Integration can proceed with partial reviews (2 of 3 is acceptable)
- If comment files cannot be created, halt and inform user
- Original specification file is never modified during review

## Timeout Considerations

- Each Task agent uses default timeout
- No explicit timeout handling needed
- Parallel execution minimizes total wait time

---

## Next Command

After reviews complete, run:
```
/review:spec-integrate <path to specification>
```

This command integrates all feedback into the specification.
