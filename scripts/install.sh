#!/bin/bash

# Installation script for Claude Code and Codex configurations
# Usage: ./scripts/install.sh [--claude|--codex|--all] [target-directory]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
TARGET_DIR="${2:-.}"
INSTALL_MODE="${1:---all}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_usage() {
    echo "Usage: $0 [--claude|--codex|--all] [target-directory]"
    echo ""
    echo "Options:"
    echo "  --claude    Install Claude Code configuration only"
    echo "  --codex     Install Codex configuration only"
    echo "  --all       Install both (default)"
    echo ""
    echo "Examples:"
    echo "  $0 --claude              # Install Claude to current directory"
    echo "  $0 --codex ~/my-project  # Install Codex to ~/my-project"
    echo "  $0 --all                 # Install both to current directory"
}

install_claude() {
    local target="$1/.claude"

    echo -e "${GREEN}Installing Claude Code configuration to $target${NC}"

    # Create .claude directory if it doesn't exist
    mkdir -p "$target"

    # Copy agents
    echo "  - Copying agents..."
    cp -r "$REPO_ROOT/claude/agents" "$target/"

    # Copy commands
    echo "  - Copying commands..."
    cp -r "$REPO_ROOT/claude/commands" "$target/"

    # Copy scripts
    echo "  - Copying scripts..."
    cp -r "$REPO_ROOT/claude/scripts" "$target/"

    # Copy settings.local.json
    if [ -f "$target/settings.local.json" ]; then
        echo -e "  ${YELLOW}- settings.local.json already exists, skipping${NC}"
    else
        echo "  - Installing settings.local.json..."
        cp "$REPO_ROOT/claude/settings.local.json" "$target/"
    fi

    # Copy MCP servers configuration
    echo "  - Installing mcp-servers.json..."
    cp "$REPO_ROOT/claude/mcp-servers.json" "$target/"

    echo -e "${GREEN}✓ Claude Code installation complete${NC}"
    echo ""
    echo "Note: CLAUDE.md is NOT installed - codex will generate this file."
    echo "To merge MCP servers with Claude Desktop, see: $target/mcp-servers.json"
}

install_codex() {
    local target="$1/.codex"

    echo -e "${GREEN}Installing Codex configuration to $target${NC}"

    # Create .codex directory if it doesn't exist
    mkdir -p "$target"

    # Copy prompts
    echo "  - Copying prompts..."
    cp -r "$REPO_ROOT/codex/prompts" "$target/"

    # Copy scripts
    echo "  - Copying scripts..."
    cp -r "$REPO_ROOT/codex/scripts" "$target/"

    # Merge config.toml if it exists
    if [ -f "$target/config.toml" ]; then
        echo -e "  ${YELLOW}- config.toml already exists${NC}"
        echo "  - Review $REPO_ROOT/codex/config.toml for settings to merge"
    else
        echo "  - Installing config.toml..."
        cp "$REPO_ROOT/codex/config.toml" "$target/"
    fi

    # Copy MCP servers configuration
    echo "  - Installing mcp-servers.toml..."
    cp "$REPO_ROOT/codex/mcp-servers.toml" "$target/"

    echo -e "${GREEN}✓ Codex installation complete${NC}"
    echo ""
    echo "Note: CODEX.md is NOT installed - codex will generate this file."
    echo "To add MCP servers to Codex, merge mcp-servers.toml into ~/.codex/config.toml"
}

# Main installation logic
case "$INSTALL_MODE" in
    --claude)
        install_claude "$TARGET_DIR"
        ;;
    --codex)
        install_codex "$TARGET_DIR"
        ;;
    --all)
        install_claude "$TARGET_DIR"
        echo ""
        install_codex "$TARGET_DIR"
        ;;
    --help|-h)
        print_usage
        exit 0
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
echo "  3. Run 'bash $SCRIPT_DIR/update.sh' to sync future updates"
