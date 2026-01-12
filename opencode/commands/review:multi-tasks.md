---
description: Launch parallel multi-agent task list review (GLM, Kimi, MiniMax)
argument-hint: <path to task list>
---

# Multi-Agent Task List Review

Orchestrate parallel task list reviews from GLM 4.7, Kimi K2, and MiniMax M2.

**Task list to review:** $ARGUMENTS

## Process

### 1. Validate Input

First, verify the task list file exists:
- Read the task list to confirm it's accessible
- Extract the **Source Specification** path from the task list header
- Verify the source specification file exists and is readable
- Generate unique comment file paths for each reviewer:
  - `{task_path}.review-glm.md`
  - `{task_path}.review-kimi.md`
  - `{task_path}.review-minimax.md`

### 2. Check for Existing Review Files

Verify that no previous review session is in progress:
- Check if any `{task_path}.review-*.md` files already exist
- If found, warn the user that a previous review may be incomplete
- Get user confirmation before overwriting existing review files

### 3. Launch Parallel Reviews

Launch ALL THREE reviewers in parallel using a single message with multiple Task tool calls:

**GLM 4.7 Reviewer:**
```
Task(
  subagent_type="reviewer-glm",
  description="Review task list with GLM 4.7 thinking",
  prompt=f"""You are [GLM Reviewer] reviewing a TASK LIST document.

**Task list to review:** {task_path}
**Source specification:** {spec_path}
**Comment file to write:** {glm_comment_file}

**Review Process:**
1. Read the task list completely. Extract the source specification path from the task list header.
2. Read the source specification in full to understand:
   - The exact requirements as written
   - Technical decisions and constraints
   - Explicit scope boundaries
   - Success criteria
3. Compare the task list line-by-line against the specification. Look for:
   - INCORRECT: Factually wrong compared to spec (wrong paths, APIs, logic)
   - SCOPE DRIFT: Tasks that go beyond specification boundaries
   - MISINTERPRETATION: Tasks misunderstanding the spec's intent
   - CONTRADICTION: Task conflicts with another part of the spec
   - WRONG REFERENCE: File path, API, or component reference is wrong
4. Write critical feedback to the comment file at {glm_comment_file}.
5. Format each comment as:
   <!-- [GLM Reviewer] LINE {line_number}: INCORRECT: {explanation} -->
   <!-- [GLM Reviewer] LINE {line_number}: SCOPE DRIFT: {explanation} -->
   <!-- [GLM Reviewer] LINE {line_number}: MISINTERPRETATION: {explanation} -->
   <!-- [GLM Reviewer] LINE {line_number}: CONTRADICTION: {explanation} -->
   <!-- [GLM Reviewer] LINE {line_number}: WRONG REFERENCE: {explanation} -->
6. Replace {line_number} with the actual line number in the task list that your comment references.
7. Do NOT comment about missing tasks (those can be filled in from spec during implementation).
8. Do NOT modify or delete comments from other reviewers.
9. IMPORTANT: Do NOT modify the original task list file. Only write your comments to {glm_comment_file}.
10. IMPORTANT: Write ALL your comments to a single file at {glm_comment_file}.

This review is about accuracy, not completeness. Focus on details that would cause wrong implementations.

Return when you have completed your review and written all comments to {glm_comment_file}."""
)
```

**Kimi K2 Reviewer:**
```
Task(
  subagent_type="reviewer-kimi",
  description="Review task list with Kimi K2 thinking",
  prompt=f"""You are [Kimi Reviewer] reviewing a TASK LIST document.

**Task list to review:** {task_path}
**Source specification:** {spec_path}
**Comment file to write:** {kimi_comment_file}

**Review Process:**
1. Read the task list completely. Extract the source specification path from the task list header.
2. Read the source specification in full to understand:
   - The exact requirements as written
   - Technical decisions and constraints
   - Explicit scope boundaries
   - Success criteria
3. Compare the task list line-by-line against the specification. Look for:
   - INCORRECT: Factually wrong compared to spec (wrong paths, APIs, logic)
   - SCOPE DRIFT: Tasks that go beyond specification boundaries
   - MISINTERPRETATION: Tasks misunderstanding the spec's intent
   - CONTRADICTION: Task conflicts with another part of the spec
   - WRONG REFERENCE: File path, API, or component reference is wrong
4. Write critical feedback to the comment file at {kimi_comment_file}.
5. Format each comment as:
   <!-- [Kimi Reviewer] LINE {line_number}: INCORRECT: {explanation} -->
   <!-- [Kimi Reviewer] LINE {line_number}: SCOPE DRIFT: {explanation} -->
   <!-- [Kimi Reviewer] LINE {line_number}: MISINTERPRETATION: {explanation} -->
   <!-- [Kimi Reviewer] LINE {line_number}: CONTRADICTION: {explanation} -->
   <!-- [Kimi Reviewer] LINE {line_number}: WRONG REFERENCE: {explanation} -->
6. Replace {line_number} with the actual line number in the task list that your comment references.
7. Do NOT comment about missing tasks (those can be filled in from spec during implementation).
8. Do NOT modify or delete comments from other reviewers.
9. IMPORTANT: Do NOT modify the original task list file. Only write your comments to {kimi_comment_file}.
10. IMPORTANT: Write ALL your comments to a single file at {kimi_comment_file}.

This review is about accuracy, not completeness. Focus on details that would cause wrong implementations.

Return when you have completed your review and written all comments to {kimi_comment_file}."""
)
```

**MiniMax M2 Reviewer:**
```
Task(
  subagent_type="reviewer-minimax",
  description="Review task list with MiniMax M2",
  prompt=f"""You are [MiniMax Reviewer] reviewing a TASK LIST document.

**Task list to review:** {task_path}
**Source specification:** {spec_path}
**Comment file to write:** {minimax_comment_file}

**Review Process:**
1. Read the task list completely. Extract the source specification path from the task list header.
2. Read the source specification in full to understand:
   - The exact requirements as written
   - Technical decisions and constraints
   - Explicit scope boundaries
   - Success criteria
3. Compare the task list line-by-line against the specification. Look for:
   - INCORRECT: Factually wrong compared to spec (wrong paths, APIs, logic)
   - SCOPE DRIFT: Tasks that go beyond specification boundaries
   - MISINTERPRETATION: Tasks misunderstanding the spec's intent
   - CONTRADICTION: Task conflicts with another part of the spec
   - WRONG REFERENCE: File path, API, or component reference is wrong
4. Write critical feedback to the comment file at {minimax_comment_file}.
5. Format each comment as:
   <!-- [MiniMax Reviewer] LINE {line_number}: INCORRECT: {explanation} -->
   <!-- [MiniMax Reviewer] LINE {line_number}: SCOPE DRIFT: {explanation} -->
   <!-- [MiniMax Reviewer] LINE {line_number}: MISINTERPRETATION: {explanation} -->
   <!-- [MiniMax Reviewer] LINE {line_number}: CONTRADICTION: {explanation} -->
   <!-- [MiniMax Reviewer] LINE {line_number}: WRONG REFERENCE: {explanation} -->
6. Replace {line_number} with the actual line number in the task list that your comment references.
7. Do NOT comment about missing tasks (those can be filled in from spec during implementation).
8. Do NOT modify or delete comments from other reviewers.
9. IMPORTANT: Do NOT modify the original task list file. Only write your comments to {minimax_comment_file}.
10. IMPORTANT: Write ALL your comments to a single file at {minimax_comment_file}.

This review is about accuracy, not completeness. Focus on details that would cause wrong implementations.

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

Analyze comment line numbers to identify overlapping concerns from multiple reviewers:

```python
# Extract line numbers from comment format
def extract_lines(comment_content):
    pattern = r'<!-- \[.*? Reviewer\] LINE (\d+):'
    return sorted([int(line) for line in re.findall(pattern, comment_content)])

glm_lines = extract_lines(glm_content)
kimi_lines = extract_lines(kimi_content)
minimax_lines = extract_lines(minimax_content)

# Find overlapping line ranges (within 50 lines)
overlap_threshold = 50
overlaps = []
for glm_line in glm_lines:
    for kimi_line in kimi_lines:
        if abs(glm_line - kimi_line) < overlap_threshold:
            overlaps.append({
                "line_range": f"{min(glm_line, kimi_line)}-{max(glm_line, kimi_line)}",
                "reviewers": ["GLM Reviewer", "Kimi Reviewer"]
            })

# Check GLM<->MiniMax overlaps
for glm_line in glm_lines:
    for minimax_line in minimax_lines:
        if abs(glm_line - minimax_line) < overlap_threshold:
            overlaps.append({
                "line_range": f"{min(glm_line, minimax_line)}-{max(glm_line, minimax_line)}",
                "reviewers": ["GLM Reviewer", "MiniMax Reviewer"]
            })

# Check Kimi<->MiniMax overlaps
for kimi_line in kimi_lines:
    for minimax_line in minimax_lines:
        if abs(kimi_line - minimax_line) < overlap_threshold:
            overlaps.append({
                "line_range": f"{min(kimi_line, minimax_line)}-{max(kimi_line, minimax_line)}",
                "reviewers": ["Kimi Reviewer", "MiniMax Reviewer"]
            })

# Remove duplicates (same line range with same reviewers)
unique_overlaps = []
seen = set()
for overlap in overlaps:
    key = (overlap['line_range'], tuple(sorted(overlap['reviewers'])))
    if key not in seen:
        seen.add(key)
        unique_overlaps.append(overlap)
```

### 7. Report Results

After all reviewers complete, provide a summary:

```markdown
## Multi-Agent Task List Review Complete

**Task List:** {task-path}
**Source Specification:** {spec-path}
**Review Date:** {YYYY-MM-DD}

### Reviewer Status
| Reviewer | Status | Comments Added |
|----------|--------|----------------|
| GLM 4.7  | {OK/Failed} | {N} |
| Kimi K2  | {OK/Failed} | {N} |
| MiniMax M2 | {OK/Failed} | {N} |

**Total Comments:** {N}

### Overlapping Concerns
{List line ranges where 2+ reviewers provided feedback in same area}

### Comment Categories
- INCORRECT: {N}
- SCOPE DRIFT: {N}
- MISINTERPRETATION: {N}
- CONTRADICTION: {N}
- WRONG REFERENCE: {N}

### Next Steps
Run `/review:tasks-integrate {task-path}` to:
- Integrate all corrections into the task list
- Resolve open questions
- Clean up comment files
```

## Error Handling

- If one reviewer fails, continue with others
- Report which reviewers completed successfully
- Integration can proceed with partial reviews (2 of 3 is acceptable)
- If source specification cannot be found or read, halt and inform user
- If comment files cannot be created, halt and inform user
- Original task list file is never modified during review

## Timeout Considerations

- Each Task agent uses default timeout
- No explicit timeout handling needed
- Parallel execution minimizes total wait time

---

## Next Command

After reviews complete, run:
```
/review:tasks-integrate <path to task list>
```

This command integrates all corrections into the task list and prepares it for implementation.
