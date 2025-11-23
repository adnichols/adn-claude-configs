#!/bin/bash

# Installation script for Claude Code and Codex configurations
# Usage: ./install.sh [--claude|--codex|--all|--tools|--skills] [--append-agents] [target-directory]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$SCRIPT_DIR"
TARGET_DIR="."
INSTALL_MODE="--all"
APPEND_AGENTS=false
INSTALL_TOOLS=false
INSTALL_SKILLS=false

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_usage() {
    echo "Usage: $0 [--claude|--codex|--tools|--skills|--all] [--append-agents] [target-directory]"
    echo ""
    echo "Options:"
    echo "  --claude    Install Claude Code configuration only"
    echo "  --codex     Install Codex configuration only"
    echo "  --tools     Install CLI tools only (e.g., ltui)"
    echo "  --skills    Install Claude skills only (to ~/.claude/skills/)"
    echo "  --all       Install everything: Claude, Codex, tools, and skills (default)"
    echo "  --append-agents"
    echo "             Ensure a project-level AGENTS.md exists in the target directory."
    echo "             If AGENTS.md exists and is missing the Fidelity & Execution rules,"
    echo "             append that section from AGENTS.template.md. Also offers to append"
    echo "             ltui (Linear) usage guidance from this repository."
    echo ""
    echo "Examples:"
    echo "  $0 --claude                        # Install Claude to current directory"
    echo "  $0 --codex ~/my-project            # Install Codex to ~/my-project"
    echo "  $0 --tools                         # Install CLI tools globally"
    echo "  $0 --skills                        # Install Claude skills globally"
    echo "  $0 --codex --append-agents ~/proj  # Install Codex and ensure AGENTS.md in ~/proj"
    echo "  $0 --all --append-agents           # Install everything and ensure AGENTS.md in current dir"
}

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

append_ltui_guidance() {
    local agents_path="$1"
    local agents_created="$2"
    local ltui_marker="## Linear Integration (ltui)"

    if [ ! -f "$agents_path" ] || grep -q "$ltui_marker" "$agents_path"; then
        return
    fi

    local should_append=false

    if [ "$agents_created" = true ]; then
        should_append=true
    elif [ "$APPEND_AGENTS" = true ]; then
        should_append=true
    elif [ -t 0 ]; then
        printf "  - Add ltui (Linear) guidance to AGENTS.md now? [Y/n] "
        read -r reply
        case "$reply" in
            ""|"Y"|"y")
                should_append=true
                ;;
            *)
                echo "  - Skipping ltui guidance append (re-run with --append-agents to add automatically)."
                ;;
        esac
    else
        echo "  - Skipping ltui guidance append (non-interactive; run with --append-agents or edit manually)."
    fi

    if [ "$should_append" = true ]; then
        echo "  - Appending ltui Linear guidance to AGENTS.md..."
        cat <<'EOF' >> "$agents_path"

## Linear Integration (ltui)

`ltui` is the token-efficient Linear CLI for AI agents (replaces the legacy linear CLI/MCP). Use it for all Linear interactions.

### Setup
1. Get a Linear API key: https://linear.app/settings/api
2. Configure authentication:
   ```bash
   ltui auth add --name default --key <api-key>
   ltui auth list
   ltui teams list
   ```

### Project Alignment (.ltui.json)
Create a `.ltui.json` in the repo root so agents target the right team/project by default:
```json
{
  "profile": "default",
  "team": "ENG",
  "project": "Doc Thingy",
  "defaultIssueState": "Todo",
  "defaultLabels": ["bug"],
  "defaultAssignee": "me"
}
```
Commit this file so everyone shares the defaults.

### Common Commands
```bash
ltui issues view <ISSUE_KEY> --format detail
ltui issues create --team <TEAM> --project "Project Name" --title "Issue title" --description "Description" --state "Backlog" --label bug
ltui issues update <ISSUE_KEY> --state "In Review"
ltui issues comment <ISSUE_KEY> --body "Comment text"
ltui issues link <ISSUE_KEY> --url <pr-url> --title "PR #123"
```

For more, run `ltui --help` or see the ltui README in this configuration repo.
EOF
    fi
}

ensure_project_agents() {
    # Ensure a project-level AGENTS.md exists and, optionally, append the Fidelity & Execution rules.
    local project_root="$1"
    local template_path="$REPO_ROOT/AGENTS.template.md"
    local agents_path="$project_root/AGENTS.md"
    local agents_created=false

    # Do not touch the config repo's own AGENTS.md via this path
    if [ "$project_root" = "$REPO_ROOT" ]; then
        return
    fi

    if [ ! -f "$template_path" ]; then
        return
    fi

    if [ ! -f "$agents_path" ]; then
        echo "  - No project AGENTS.md found; installing from template..."
        cp "$template_path" "$agents_path"
        agents_created=true
    fi

    if grep -q "Fidelity & Execution Rules" "$agents_path"; then
        append_ltui_guidance "$agents_path" "$agents_created"
        return
    fi

    echo "  - Existing AGENTS.md found without Fidelity & Execution rules section."
    if [ "$APPEND_AGENTS" = true ]; then
        echo "  - Appending Fidelity & Execution rules block from template..."
        awk 'BEGIN{flag=0} /^## Fidelity & Execution Rules/{flag=1} flag {print}' "$template_path" >> "$agents_path"
        echo "" >> "$agents_path"
        append_ltui_guidance "$agents_path" "$agents_created"
    else
        if [ -t 0 ]; then
            printf "  - Add Fidelity & Execution rules section to AGENTS.md now? [Y/n] "
            read -r reply
            case "$reply" in
                ""|"Y"|"y")
                    echo "  - Appending Fidelity & Execution rules block from template..."
                    awk 'BEGIN{flag=0} /^## Fidelity & Execution Rules/{flag=1} flag {print}' "$template_path" >> "$agents_path"
                    echo "" >> "$agents_path"
                    append_ltui_guidance "$agents_path" "$agents_created"
                    ;;
                *)
                    echo "  - Skipping append to AGENTS.md (you can re-run with --append-agents or edit manually)."
                    append_ltui_guidance "$agents_path" "$agents_created"
                    ;;
            esac
        else
            echo "  - Skipping automatic append to AGENTS.md (non-interactive; run with --append-agents or edit manually)."
            append_ltui_guidance "$agents_path" "$agents_created"
        fi
    fi
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

install_claude() {
    local target="$1/.claude"
    local is_update=false

    # Detect if this is an update
    if [ -d "$target" ]; then
        is_update=true
        echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
        echo -e "${GREEN}  Updating Claude Code Configuration${NC}"
        echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
        echo ""
        echo -e "${GREEN}Updating Claude Code configuration at $target${NC}"
    else
        echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
        echo -e "${GREEN}  Installing Claude Code Configuration${NC}"
        echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
        echo ""
        echo -e "${GREEN}Installing Claude Code configuration to $target${NC}"
        mkdir -p "$target"
    fi

    # Update agents (remove first to ensure clean state)
    echo "  - Installing agents..."
    if [ -d "$target/agents" ]; then
        rm -rf "$target/agents"
    fi
    cp -r "$REPO_ROOT/claude/agents" "$target/"

    # Update commands (remove first to ensure clean state)
    if [ -d "$target/commands" ]; then
        # Check for legacy subdirectories
        local has_legacy=false
        local legacy_dirs=(cmd doc prd spec)
        for legacy_dir in "${legacy_dirs[@]}"; do
            if [ -d "$target/commands/$legacy_dir" ]; then
                has_legacy=true
                break
            fi
        done

        if [ "$has_legacy" = true ]; then
            echo "  - Cleaning up legacy command structure (subdirectories will be flattened)..."
        fi
    fi

    echo "  - Installing commands..."
    if [ -d "$target/commands" ]; then
        rm -rf "$target/commands"
    fi
    cp -r "$REPO_ROOT/claude/commands" "$target/"

    # Update scripts (remove first to ensure clean state)
    echo "  - Installing scripts..."
    if [ -d "$target/scripts" ]; then
        rm -rf "$target/scripts"
    fi
    cp -r "$REPO_ROOT/claude/scripts" "$target/"

    # Handle settings.local.json (preserve if exists)
    if [ -f "$target/settings.local.json" ]; then
        echo -e "  ${YELLOW}✓ Preserved existing settings.local.json${NC}"
    else
        echo "  - Installing settings.local.json..."
        cp "$REPO_ROOT/claude/settings.local.json" "$target/"
    fi

    # Update MCP servers configuration
    echo "  - Installing mcp-servers.json..."
    cp "$REPO_ROOT/claude/mcp-servers.json" "$target/"

    if [ "$is_update" = true ]; then
        echo -e "${GREEN}✓ Claude Code update complete${NC}"
    else
        echo -e "${GREEN}✓ Claude Code installation complete${NC}"
    fi
    echo ""
    echo "Note: CLAUDE.md is NOT installed - codex will generate this file."
    if [ "$is_update" = false ]; then
        echo "To merge MCP servers with Claude Desktop, see: $target/mcp-servers.json"
    fi
}

install_tools() {
    echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  Installing CLI Tools${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
    echo ""

    # Install ltui
    if [ -d "$REPO_ROOT/tools/ltui" ]; then
        echo "Installing ltui..."

        # Check for Bun
        if ! command -v bun &> /dev/null; then
            echo -e "${RED}Error: Bun is required to build ltui${NC}"
            echo "Install from: https://bun.sh"
            return 1
        fi

        local current_dir=$(pwd)
        cd "$REPO_ROOT/tools/ltui"

        echo "  - Installing dependencies..."
        bun install

        echo "  - Building ltui..."
        bun run build

        echo "  - Linking ltui globally..."
        bun link

        cd "$current_dir"
        echo -e "${GREEN}✓ ltui installed successfully${NC}"
        echo ""

        # Check if ~/.bun/bin is in PATH
        if [[ ":$PATH:" != *":$HOME/.bun/bin:"* ]]; then
            echo -e "${YELLOW}⚠  NOTE: ~/.bun/bin is not in your PATH${NC}"
            echo "  Add this to your shell profile (~/.bashrc, ~/.zshrc, etc.):"
            echo "    export PATH=\"\$HOME/.bun/bin:\$PATH\""
            echo ""
            echo "  After updating, run: source ~/.zshrc  (or restart your shell)"
            echo "  Then verify with: ltui --help"
        else
            echo "  ltui is now available globally. Try: ltui --help"
        fi
    else
        echo -e "${YELLOW}No tools directory found, skipping...${NC}"
    fi
}

install_skills() {
    echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  Installing Claude Skills${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
    echo ""

    local skills_dir="$HOME/.claude/skills"
    mkdir -p "$skills_dir"

    if [ -d "$REPO_ROOT/skills" ]; then
        echo "  - Installing skills to ~/.claude/skills/..."

        # Copy each skill directory
        for skill_path in "$REPO_ROOT/skills/"*/; do
            if [ -d "$skill_path" ]; then
                local skill_name=$(basename "$skill_path")
                echo "    - Installing skill: $skill_name"
                cp -r "$skill_path" "$skills_dir/"
            fi
        done

        echo -e "${GREEN}✓ Skills installed successfully${NC}"
        echo ""
        echo "  Skills are now available in Claude Code"
    else
        echo -e "${YELLOW}No skills directory found, skipping...${NC}"
    fi
}

install_codex() {
    local target="$1/.codex"
    local is_update=false

    # Ensure project-level AGENTS.md / house rules if requested
    ensure_project_agents "$1"

    # Detect if this is an update
    if [ -d "$target" ]; then
        is_update=true
        echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
        echo -e "${GREEN}  Updating Codex Configuration${NC}"
        echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
        echo ""
        echo -e "${GREEN}Updating Codex configuration at $target${NC}"
    else
        echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
        echo -e "${GREEN}  Installing Codex Configuration${NC}"
        echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
        echo ""
        echo -e "${GREEN}Installing Codex configuration to $target${NC}"
        mkdir -p "$target"
    fi

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

    local global_codex_dir="$HOME/.codex"
    mkdir -p "$global_codex_dir"
    local global_prompts_dir="${global_codex_dir}/prompts"
    sync_codex_prompts "$global_prompts_dir" "global (~/.codex/prompts)" "replace"

    echo "  - Syncing Codex scripts globally..."
    rm -rf "$global_codex_dir/scripts"
    cp -r "$REPO_ROOT/codex/scripts" "$global_codex_dir/"

    # Merge config.toml if it exists
    if [ -f "$target/config.toml" ]; then
        echo -e "  ${YELLOW}- config.toml already exists${NC}"
        echo "  - Review $REPO_ROOT/codex/config.toml for settings to merge"
    else
        echo "  - Installing config.toml..."
        cp "$REPO_ROOT/codex/config.toml" "$target/"
    fi

    ensure_codex_cli_flags "$target"

    # Copy MCP servers configuration
    echo "  - Installing mcp-servers.toml..."
    cp "$REPO_ROOT/codex/mcp-servers.toml" "$target/"

    if [ "$is_update" = true ]; then
        echo -e "${GREEN}✓ Codex update complete${NC}"
    else
        echo -e "${GREEN}✓ Codex installation complete${NC}"
    fi
    echo ""
    if [ "$APPEND_AGENTS" = true ]; then
        echo "Note: Project AGENTS.md was created or updated; review it to tailor project-specific rules."
    else
        echo "Note: To ensure a project-level AGENTS.md with Fidelity & Execution rules, re-run with --append-agents."
    fi
    if [ "$is_update" = false ]; then
        echo "To add MCP servers to Codex, merge mcp-servers.toml into ~/.codex/config.toml"
    fi
}

# Argument parsing
while [ "$#" -gt 0 ]; do
    case "$1" in
        --claude|--codex|--tools|--skills|--all)
            INSTALL_MODE="$1"
            shift
            ;;
        --append-agents)
            APPEND_AGENTS=true
            shift
            ;;
        --help|-h)
            print_usage
            exit 0
            ;;
        *)
            if [[ "$1" == -* ]]; then
                echo -e "${RED}Error: Unknown option $1${NC}"
                echo ""
                print_usage
                exit 1
            fi
            TARGET_DIR="$1"
            shift
            ;;
    esac
done

# Main installation logic
case "$INSTALL_MODE" in
    --claude)
        install_claude "$TARGET_DIR"
        ;;
    --codex)
        install_codex "$TARGET_DIR"
        ;;
    --tools)
        install_tools
        ;;
    --skills)
        install_skills
        ;;
    --all)
        install_claude "$TARGET_DIR"
        echo ""
        install_codex "$TARGET_DIR"
        echo ""
        install_tools
        echo ""
        install_skills
        ;;
    *)
        echo -e "${RED}Error: Unknown option $INSTALL_MODE${NC}"
        echo ""
        print_usage
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}Installation complete!${NC}"
echo ""
echo "Next steps:"
echo "  1. Review and customize settings as needed"
echo "  2. Configure MCP servers (see mcp-servers.json/toml files)"
echo "  3. Run this script again to sync future updates (it auto-detects existing installations)"
