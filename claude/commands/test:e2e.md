---
description: Run Playwright e2e tests using dedicated test runner subagent
argument-hint: [test pattern, grep filter, or empty for full suite]
---

# Run Playwright E2E Tests

Execute Playwright tests using a dedicated **read-only subagent** that captures full output and provides detailed results.

$ARGUMENTS

## Process

### Step 1: Spawn Test Runner Subagent

Use the Task tool to spawn a `@playwright-runner` subagent:

```
Task: Run Playwright e2e tests and report results.

Arguments: $ARGUMENTS

Execute the Playwright test suite with the given arguments (or full suite if none provided).
Capture ALL output - do not truncate error messages or stack traces.
Return a detailed report of results including:
- Summary of pass/fail/skip counts
- Complete error details for each failure
- File:line locations for all failures
- Analysis of any patterns in failures

IMPORTANT: You are read-only. Do NOT attempt to fix any failures.
```

### Step 2: Receive Results

The subagent will return a structured test report. Review it for:

1. **Overall status** - Did tests pass or fail?
2. **Failure details** - What specifically failed and why?
3. **Patterns** - Are failures related (same component, same error type)?
4. **Actionable info** - File:line locations for investigation

### Step 3: Present to User

Summarize the test results for the user, including:
- High-level pass/fail status
- Key failures with context
- Suggested next steps (if failures exist)

## Why a Subagent?

This command uses a dedicated subagent because:

1. **Full Output Capture**: The subagent watches ALL Playwright output without shell piping issues
2. **Isolation**: Test execution happens in a separate context, preserving parent context
3. **Read-Only Safety**: The subagent cannot accidentally modify code while investigating
4. **Structured Return**: Results come back in a parseable format, not raw console output

## Examples

```bash
# Run full e2e suite
/test:e2e

# Run specific test file
/test:e2e document-tree-operations.test.ts

# Run tests matching pattern
/test:e2e --grep "sidebar"

# Run quick smoke tests
/test:e2e tests/e2e/promptbench-mentions.test.ts tests/e2e/promptbench-export.test.ts
```
