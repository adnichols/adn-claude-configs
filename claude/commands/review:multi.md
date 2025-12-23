---
description: Launch parallel multi-agent specification review (Claude, Codex, Gemini)
argument-hint: <path to specification>
---

# Multi-Agent Specification Review

Orchestrate parallel specification reviews from Claude (Task agent), Codex (shell), and Gemini (shell).

**Specification to review:** $ARGUMENTS

## Process

### 1. Validate Input

First, verify the specification file exists:
- Read the specification to confirm it's accessible
- Extract the filename (without path and extension) for output naming

### 2. Set Up Output Directory

Create the reviews directory if it doesn't exist:

```bash
mkdir -p thoughts/reviews
```

### 3. Launch Parallel Reviews

Launch ALL THREE reviewers in parallel using a single message with multiple tool calls:

**Claude (Task agent):**
```
Use Task tool with subagent_type=multi-reviewer
Prompt: "Review the specification at {spec-path} and write your structured review to thoughts/reviews/{spec-name}-claude.md"
```

**Codex (shell wrapper):**
```
Use Bash tool with run_in_background=true
Command: bash claude/scripts/codex-review.sh "{spec-path}" "thoughts/reviews/{spec-name}-codex.md"
```

**Gemini (shell wrapper):**
```
Use Bash tool with run_in_background=true
Command: bash claude/scripts/gemini-review.sh "{spec-path}" "thoughts/reviews/{spec-name}-gemini.md"
```

### 4. Wait for Completion

After launching all three:
1. The Task agent (Claude) will return when complete
2. Use TaskOutput to wait for both background shells (Codex and Gemini) to complete

### 5. Report Results

After all reviewers complete, provide a summary:

```markdown
## Multi-Agent Review Complete

**Specification:** {spec-path}

### Reviewer Status
| Reviewer | Status | Output File |
|----------|--------|-------------|
| Claude   | {OK/Failed} | thoughts/reviews/{spec-name}-claude.md |
| Codex    | {OK/Failed} | thoughts/reviews/{spec-name}-codex.md |
| Gemini   | {OK/Failed} | thoughts/reviews/{spec-name}-gemini.md |

### Next Steps
Run `/review:multi-integrate {spec-path}` to:
- Synthesize all feedback
- Resolve open questions
- Update the specification
```

## Error Handling

- If one reviewer fails, continue with others
- Report which reviewers completed successfully
- Integration can proceed with partial reviews (2 of 3 is acceptable)

## Timeout Considerations

- Use the Bash tool's `timeout` parameter (600000ms = 10 minutes) for background shells
- Do NOT use the `timeout` command in scripts (not available on macOS)
- Claude Task agent uses default timeout

---

## Next Command

After reviews complete, run:
```
/review:multi-integrate <path to specification>
```
