#!/bin/bash
# gemini-review.sh - Invokes Gemini CLI to review a specification
#
# Usage: gemini-review.sh <spec-path> <output-path>
#
# This script runs the Gemini CLI to review a specification
# and write the output to the specified file.

set -e

SPEC_PATH="$1"
OUTPUT_PATH="$2"

if [ -z "$SPEC_PATH" ] || [ -z "$OUTPUT_PATH" ]; then
    echo "Usage: gemini-review.sh <spec-path> <output-path>" >&2
    exit 1
fi

if [ ! -f "$SPEC_PATH" ]; then
    echo "Error: Specification file not found: $SPEC_PATH" >&2
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p "$(dirname "$OUTPUT_PATH")"

# Run Gemini CLI with -y for YOLO mode (auto-approve all actions)
gemini -y "Review the specification at $SPEC_PATH. Provide detailed structured feedback covering: implementation gaps, missing requirements, technical concerns, and questions for clarification. Write your review to $OUTPUT_PATH using this format:

# Specification Review: {spec-name}

**Reviewer:** Gemini
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
{Any document-wide issues}" 2>&1

# Verify output was created
if [ ! -f "$OUTPUT_PATH" ]; then
    echo "Warning: Gemini may not have created output file: $OUTPUT_PATH" >&2
fi

echo "Gemini review complete"
