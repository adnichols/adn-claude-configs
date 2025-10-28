#!/bin/bash

# Update script for syncing latest configurations from adn-claude-configs
# Usage: bash /path/to/adn-claude-configs/update.sh [target-directory]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$SCRIPT_DIR"
TARGET_DIR="${1:-.}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}ADN Claude Configs - Update Script${NC}"
echo -e "${BLUE}===================================${NC}"
echo ""

ensure_codex_cli_flags() {
    local target_dir="$1"
    local config_path="$target_dir/config.toml"

    if [ ! -f "$config_path" ]; then
        return
    fi

    local status
    status=$(CONFIG_PATH="$config_path" python3 <<'PY'
import ast
import os
import re
from pathlib import Path

config_file = Path(os.environ["CONFIG_PATH"])
text = config_file.read_text()
required_flags = [
    "--dangerously-bypass-approvals-and-sandbox",
    "--enable-web-search",
]

pattern = re.compile(r"default_cli_flags\s*=\s*\[(.*?)\]", re.DOTALL)
match = pattern.search(text)
changed = False


def format_block(flags):
    inner = ",\n".join(f'  "{flag}"' for flag in flags)
    return f"default_cli_flags = [\n{inner}\n]"


if match:
    content = match.group(1)
    try:
        existing = ast.literal_eval("[" + content + "]")
    except Exception:
        existing = []

    updated = existing[:]
    for flag in required_flags:
        if flag not in updated:
            updated.append(flag)

    if updated != existing:
        block = format_block(updated)
        text = text[:match.start()] + block + text[match.end():]
        changed = True
else:
    cli_header = re.compile(r"^\[cli\]\s*$", re.MULTILINE)
    cli_match = cli_header.search(text)
    block = format_block(required_flags)
    insertion = block + "\n"

    if cli_match:
        block_start = cli_match.end()
        next_table = re.search(r"^\[.*?\]", text[block_start:], re.MULTILINE)
        insert_pos = len(text) if not next_table else block_start + next_table.start()

        if block_start < len(text) and text[block_start] != "\n":
            text = text[:block_start] + "\n" + text[block_start:]
            insert_pos += 1

        prefix = text[:insert_pos]
        suffix = text[insert_pos:]
        if prefix and not prefix.endswith("\n"):
            prefix += "\n"
        text = prefix + insertion + suffix
    else:
        if text and not text.endswith("\n"):
            text += "\n"
        text = text.rstrip() + "\n\n[cli]\n" + block + "\n"

    changed = True

if changed:
    config_file.write_text(text if text.endswith("\n") else text + "\n")
    print("updated")
else:
    print("unchanged")
PY
)
    local cli_update_status=$?

    if [ $cli_update_status -ne 0 ]; then
        echo "  - Unable to ensure Codex CLI flags (manual config update required)"
        return
    fi

    case "$status" in
        updated)
            echo "  - Ensured Codex CLI runs with --dangerously-bypass-approvals-and-sandbox and web search"
            ;;
        unchanged)
            echo "  - Codex CLI flags already configured for dangerous bypass and web search"
            ;;
        *)
            echo "  - Unable to validate Codex CLI flags (manual config update required)"
            ;;
    esac
}

sync_codex_prompts() {
    local destination="$1"
    local label="$2"
    local mode="${3:-merge}"

    if [ "$mode" = "replace" ] && [ -d "$destination" ]; then
        echo "  - Resetting $label at $destination"
        rm -rf "$destination"
    fi

    mkdir -p "$destination"

    echo "  - Syncing Codex prompts into $label ($destination)"

    local legacy_dirs=(cmd doc prd spec simplify)
    for legacy_dir in "${legacy_dirs[@]}"; do
        if [ -d "$destination/$legacy_dir" ]; then
            echo "    - Removing legacy subdirectory $legacy_dir/"
            rm -rf "$destination/$legacy_dir"
        fi
    done

    if [ -d "$destination/_lib" ]; then
        rm -rf "$destination/_lib"
    fi

    if [ -d "$REPO_ROOT/codex/prompts/_lib" ]; then
        cp -R "$REPO_ROOT/codex/prompts/_lib" "$destination/"
    fi

    for prompt in "$REPO_ROOT"/codex/prompts/*.md; do
        [ -e "$prompt" ] || continue
        cp "$prompt" "$destination/"
    done
}

# Detect which tools are installed
CLAUDE_INSTALLED=false
CODEX_INSTALLED=false

if [ -d "$TARGET_DIR/.claude" ]; then
    CLAUDE_INSTALLED=true
    echo -e "${GREEN}✓ Detected Claude Code installation${NC}"
fi

if [ -d "$TARGET_DIR/.codex" ]; then
    CODEX_INSTALLED=true
    echo -e "${GREEN}✓ Detected Codex installation${NC}"
fi

if [ "$CLAUDE_INSTALLED" = false ] && [ "$CODEX_INSTALLED" = false ]; then
    echo -e "${RED}Error: No Claude Code or Codex installations found in $TARGET_DIR${NC}"
    echo ""
    echo "Run the install script first:"
    echo "  bash $REPO_ROOT/install.sh --all"
    exit 1
fi

echo ""

update_claude() {
    local target="$1/.claude"

    echo -e "${BLUE}Updating Claude Code configuration...${NC}"

    # Update agents
    echo "  - Updating agents..."
    rm -rf "$target/agents"
    cp -r "$REPO_ROOT/claude/agents" "$target/"

    # Update commands
    echo "  - Updating commands..."
    rm -rf "$target/commands"
    cp -r "$REPO_ROOT/claude/commands" "$target/"

    # Update scripts
    echo "  - Updating scripts..."
    rm -rf "$target/scripts"
    cp -r "$REPO_ROOT/claude/scripts" "$target/"

    # Preserve existing settings.local.json
    if [ -f "$target/settings.local.json" ]; then
        echo -e "  ${YELLOW}✓ Preserved existing settings.local.json${NC}"
    else
        echo "  - Installing settings.local.json..."
        cp "$REPO_ROOT/claude/settings.local.json" "$target/"
    fi

    # Update MCP servers configuration (always update)
    echo "  - Updating mcp-servers.json..."
    cp "$REPO_ROOT/claude/mcp-servers.json" "$target/"

    # Skip CLAUDE.md
    echo -e "  ${YELLOW}✓ Skipped CLAUDE.md (generated by codex)${NC}"

    echo -e "${GREEN}✓ Claude Code update complete${NC}"
}

update_codex() {
    local target="$1/.codex"

    echo -e "${BLUE}Updating Codex configuration...${NC}"

    local project_prompts_dir="${target}/prompts"
    if [ -d "$project_prompts_dir" ]; then
        echo "  - Removing project prompts (Codex prefers ~/.codex/prompts)..."
        rm -rf "$project_prompts_dir"
    fi

    local project_scripts_dir="${target}/scripts"
    if [ -d "$project_scripts_dir" ]; then
        echo "  - Removing project scripts (Codex prefers ~/.codex/scripts)..."
        rm -rf "$project_scripts_dir"
    fi

    # Update prompts in global Codex directory for CLI discovery
    local global_codex_dir="$HOME/.codex"
    mkdir -p "$global_codex_dir"
    local global_prompts_dir="${global_codex_dir}/prompts"
    sync_codex_prompts "$global_prompts_dir" "global (~/.codex/prompts)" "replace"

    # Update scripts globally
    echo "  - Updating global Codex scripts..."
    rm -rf "$global_codex_dir/scripts"
    cp -r "$REPO_ROOT/codex/scripts" "$global_codex_dir/"

    # Preserve existing config.toml
    if [ -f "$target/config.toml" ]; then
       echo -e "  ${YELLOW}✓ Preserved existing config.toml${NC}"
       echo "  ${YELLOW}  Review $REPO_ROOT/codex/config.toml for new settings${NC}"
    else
        echo "  - Installing config.toml..."
        cp "$REPO_ROOT/codex/config.toml" "$target/"
    fi

    ensure_codex_cli_flags "$target"

    # Update MCP servers configuration (always update)
    echo "  - Updating mcp-servers.toml..."
    cp "$REPO_ROOT/codex/mcp-servers.toml" "$target/"

    # Skip AGENTS.md
    echo -e "  ${YELLOW}✓ Skipped AGENTS.md (generated by codex)${NC}"

    echo -e "${GREEN}✓ Codex update complete${NC}"
}

# Perform updates
if [ "$CLAUDE_INSTALLED" = true ]; then
    update_claude "$TARGET_DIR"
    echo ""
fi

if [ "$CODEX_INSTALLED" = true ]; then
    update_codex "$TARGET_DIR"
    echo ""
fi

echo -e "${GREEN}All updates complete!${NC}"
echo ""
echo "Changes applied:"
echo "  ✓ Agents/Commands/Prompts updated to latest versions"
echo "  ✓ Scripts synchronized"
echo "  ✓ MCP server configurations updated"
echo "  ✓ Local settings preserved"
echo ""
echo "Note: Review your settings files if new configuration options were added."
