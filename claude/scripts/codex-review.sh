#!/bin/bash
# codex-review.sh - Invokes Codex CLI to review a specification
#
# Usage: codex-review.sh <spec-path> <output-path>
#
# This script runs the Codex CLI to review a specification
# and write the output to the specified file.

set -e

SPEC_PATH="$1"
OUTPUT_PATH="$2"

if [ -z "$SPEC_PATH" ] || [ -z "$OUTPUT_PATH" ]; then
    echo "Usage: codex-review.sh <spec-path> <output-path>" >&2
    exit 1
fi

if [ ! -f "$SPEC_PATH" ]; then
    echo "Error: Specification file not found: $SPEC_PATH" >&2
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p "$(dirname "$OUTPUT_PATH")"

# Run Codex CLI with exec for non-interactive mode
# --dangerously-bypass-approvals-and-sandbox for automatic execution
codex exec "Review the specification at $SPEC_PATH. Provide detailed structured feedback covering: implementation gaps, missing requirements, technical concerns, and questions for clarification. Write your review to $OUTPUT_PATH using this format:

# Specification Review: {spec-name}

**Reviewer:** Codex
**Date:** $(date +%Y-%m-%d)
**Spec Path:** $SPEC_PATH

## Summary
- Total concerns: N
- Critical: N
- Major: N
- Minor: N

## Concerns

### 1. [Section: {section-name}] {Brief title}
**Severity:** Critical | Major | Minor
**Type:** Missing requirement | Feasibility | Ambiguity | Integration | Security | Performance

{Detailed concern description}

**Suggestion:** {Optional recommendation}

## Questions for User
- {Questions that need stakeholder input}

## Cross-Cutting Concerns
{Any document-wide issues}" --dangerously-bypass-approvals-and-sandbox 2>&1

# Verify output was created
if [ ! -f "$OUTPUT_PATH" ]; then
    echo "Warning: Codex may not have created output file: $OUTPUT_PATH" >&2
fi

echo "Codex review complete"
