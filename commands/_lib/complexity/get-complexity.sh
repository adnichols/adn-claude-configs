#!/bin/bash
# Simple complexity detector with zero dependencies
# Extracts YAML front-matter and calculates complexity score
# Usage: ./get-complexity.sh <markdown-file-with-yaml-frontmatter>

set -e

# Extract YAML values from file
get_yaml_value() {
    local key="$1"
    local file="$2"
    local default="$3"
    
    # Look for YAML front-matter between --- markers
    if [[ -f "$file" ]]; then
        # Extract front-matter section
        frontmatter=$(sed -n '/^---$/,/^---$/p' "$file" | sed '1d;$d')
        
        # Get value for key
        value=$(echo "$frontmatter" | grep "^[[:space:]]*$key:" | sed 's/^[[:space:]]*[^:]*:[[:space:]]*//' | sed 's/[[:space:]]*$//' | tr -d '"')
        
        if [[ -n "$value" ]]; then
            echo "$value"
        else
            echo "$default"
        fi
    else
        echo "$default"
    fi
}

# Validate input
FILE="$1"
if [[ -z "$FILE" ]]; then
    echo '{"error":"No file provided","usage":"get-complexity.sh <file>"}' >&2
    exit 1
fi

if [[ ! -f "$FILE" ]]; then
    echo '{"error":"File not found","file":"'"$FILE"'"}' >&2
    exit 1
fi

# Extract complexity factors from YAML front-matter
blast_radius=$(get_yaml_value "blast_radius" "$FILE" "package")
data_sensitivity=$(get_yaml_value "data_sensitivity" "$FILE" "none")
backward_compat=$(get_yaml_value "backward_compat_required" "$FILE" "false")
migration=$(get_yaml_value "migration" "$FILE" "false")
external_api=$(get_yaml_value "external_api_change" "$FILE" "false")
perf_budget=$(get_yaml_value "perf_budget_ms_p95" "$FILE" "0")

# Check for explicit complexity override
explicit_complexity=$(get_yaml_value "complexity" "$FILE" "auto")

# Calculate complexity score using same weights as original system
score=0

# Blast radius scoring (weight: 2)
case "$blast_radius" in
    "file") score=$((score + 0 * 2)) ;;
    "package") score=$((score + 1 * 2)) ;;
    "service") score=$((score + 2 * 2)) ;;
    "org") score=$((score + 3 * 2)) ;;
esac

# Data sensitivity scoring (weight: 2)
case "$data_sensitivity" in
    "none") score=$((score + 0 * 2)) ;;
    "pii") score=$((score + 2 * 2)) ;;
    "regulated") score=$((score + 3 * 2)) ;;
esac

# Backward compatibility (weight: 1)
[[ "$backward_compat" == "true" ]] && score=$((score + 2 * 1))

# Migration required (weight: 2)
[[ "$migration" == "true" ]] && score=$((score + 2 * 2))

# External API change (weight: 1)
[[ "$external_api" == "true" ]] && score=$((score + 1 * 1))

# Performance budget (weight: 1)
if [[ "$perf_budget" != "0" ]] && [[ "$perf_budget" =~ ^[0-9]+$ ]]; then
    if [[ $perf_budget -le 100 ]]; then
        score=$((score + 4 * 1))
    elif [[ $perf_budget -le 200 ]]; then
        score=$((score + 3 * 1))
    elif [[ $perf_budget -le 300 ]]; then
        score=$((score + 2 * 1))
    else
        score=$((score + 1 * 1))
    fi
fi

# Map score to complexity level (using original thresholds)
if [[ "$explicit_complexity" != "auto" ]]; then
    level="$explicit_complexity"
    override_applied="true"
else
    if [[ $score -le 2 ]]; then
        level="minimum"
    elif [[ $score -le 4 ]]; then
        level="basic"
    elif [[ $score -le 7 ]]; then
        level="moderate"
    else
        level="complex"
    fi
    override_applied="false"
fi

# Get agents from mapping file
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
agent_line=$(grep "^$level:" "$SCRIPT_DIR/agent-map.txt" 2>/dev/null || echo "")

if [[ -n "$agent_line" ]]; then
    developer=$(echo "$agent_line" | cut -d: -f2)
    reviewer=$(echo "$agent_line" | cut -d: -f3)
else
    # Fallback defaults
    developer="developer"
    reviewer="quality-reviewer"
fi

# Get validation requirements
validation_line=$(grep "^$level:" "$SCRIPT_DIR/validation-map.txt" 2>/dev/null || echo "")
if [[ -n "$validation_line" ]]; then
    validation_checks=$(echo "$validation_line" | cut -d: -f2)
else
    validation_checks="lint,build"
fi

# Output JSON result compatible with original system
cat <<EOF
{
  "complexity_level": "$level",
  "total_score": $score,
  "override_applied": $override_applied,
  "selected_agents": {
    "developer": "$developer",
    "quality_reviewer": "$reviewer"
  },
  "validation_requirements": {
    "required_checks": ["$(echo "$validation_checks" | sed 's/,/","/g')"]
  },
  "input_file": "$FILE",
  "timestamp": "$(date -Iseconds)",
  "router_version": "bash-1.0.0"
}
EOF