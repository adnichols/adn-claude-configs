# Quick Setup Guide

## Installation Options

### Option 1: Global Installation (Recommended)

Install these configurations globally to use across all your Claude Code projects:

```bash
# Clone the repository
git clone <repository-url> ~/claude-configs
cd ~/claude-configs

# Copy agents and commands to global Claude directory
cp -r agents/* ~/.claude/agents/
cp -r commands/* ~/.claude/commands/
cp -r scripts/* ~/.claude/scripts/
cp settings.json ~/.claude/

# Update your global settings (merge with existing if present)
```

### Option 3: Symlink Setup (Development)

For developing and testing these configurations:

```bash
# Clone and link directly
git clone <repository-url> ~/claude-configs
cd your-project

# Create symlinks to development directory
ln -sf ~/claude-configs/.claude .claude
ln -sf ~/claude-configs/agents agents
```

## Verification

Test your installation:

```bash
# Open Claude Code in your project
# Try running a command:
/plan:create-prd

# Verify agents are available:
@developer
@quality-reviewer
@technical-writer
```

## First Usage

1. **Create your first PRD**:

   ```bash
   /plan:create-prd
   ```

2. **Set up a feature branch**:

   ```bash
   git checkout -b feature/test-feature
   ```

3. **Process tasks**:
   ```bash
   /build:process-tasks
   ```

## Troubleshooting

**Commands not found**: Ensure the files are in the right location and restart Claude Code

**Agent not found**: Check that agents are properly copied and accessible

**Git branch error**: Commands require working on a feature branch (not main)

**Symlink issues**: Use absolute paths when creating symlinks, ensure they point to existing directories
