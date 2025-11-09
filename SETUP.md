# Quick Setup Guide

This guide provides quick installation instructions for the Claude Code and Codex configuration system.

## Installation

### Option 1: Project-Level Installation (Recommended)

Install configurations to a specific project:

```bash
# Clone the repository (if not already done)
git clone <repository-url> ~/adn-claude-configs
cd ~/adn-claude-configs

# Install Python dependencies for doc:fetch commands
pip3 install -r requirements.txt

# Navigate to your project
cd /path/to/your/project

# Install Claude Code and/or Codex
bash ~/adn-claude-configs/install.sh --all
```

This creates `.claude/` and `.codex/` directories in your project with all agents, commands/prompts, and configurations.

### Option 2: Global Installation

Install to your home directory for use across all projects:

```bash
# Install to ~/.claude and ~/.codex
bash ~/adn-claude-configs/install.sh --all ~
```

### Option 3: Development Setup (Symlinks)

For developing and testing these configurations:

```bash
# Clone the repository
git clone <repository-url> ~/adn-claude-configs
cd ~/adn-claude-configs

# Create symlink for local testing
ln -sf ~/adn-claude-configs/claude .claude
```

## Updating Existing Installations

Simply run the install script again - it auto-detects existing installations:

```bash
cd /path/to/your/project
bash ~/adn-claude-configs/install.sh --all
```

The script will:
- Update agents, commands/prompts, and scripts
- Clean up legacy directory structures
- Preserve your local settings files

## Verification

Test your installation:

```bash
# In Claude Code, try running a command:
/prd:1:create-prd

# Or fetch documentation:
/doc:fetch react

# Verify agents are available:
@developer-fidelity
@quality-reviewer-fidelity
@technical-writer
```

## First Usage

### PRD-Based Development

1. **Create a PRD**:
   ```bash
   /prd:1:create-prd
   ```

2. **Generate task list**:
   ```bash
   /prd:2:gen-tasks @path/to/prd.md
   ```

3. **Process tasks** (creates branch automatically):
   ```bash
   /3:process-tasks @path/to/tasks.md
   ```

### Specification-Based Development

1. **Create specification from research**:
   ```bash
   /spec:1:create-spec @research-notes.md
   ```

2. **Generate task list**:
   ```bash
   /spec:2:gen-tasks @path/to/spec.md
   ```

3. **Process tasks**:
   ```bash
   /3:process-tasks @path/to/tasks.md
   ```

## Command Reference

### Workflow Commands
- `/prd:1:create-prd` - Create Product Requirements Document
- `/prd:2:gen-tasks` - Generate tasks from PRD
- `/spec:1:create-spec` - Create specification from research
- `/spec:2:gen-tasks` - Generate tasks from specification
- `/3:process-tasks` - Process tasks (unified for both PRD and spec)

### Documentation Commands
- `/doc:fetch` - Fetch library/framework documentation
- `/doc:fetch-batch` - Batch fetch multiple libraries
- `/doc:update` - Update project documentation

### Simplification Commands
- `/simplify:create-plan` - Analyze code for simplification
- `/simplify:process-plan` - Execute simplification plan

### Git Utilities
- `/commit-push` - Commit and push changes
- `/create-pr` - Create pull request
- `/start-linear-issue` - Start work on Linear issue

## Troubleshooting

**Commands not found**:
- Ensure installation completed successfully
- Restart Claude Code
- Check that `.claude/commands/` directory exists and contains `.md` files

**Agent not found**:
- Verify agents are in `.claude/agents/` directory
- Check agent file names match expected format
- Restart Claude Code

**Git branch error**:
- Commands require working on a feature branch (not main)
- Use `/3:process-tasks` which can create branches automatically

**Legacy subdirectories**:
- If you have old `cmd/`, `doc/`, `prd/`, `spec/` subdirectories, run the install script again
- It will automatically flatten the structure

**Documentation fetch errors**:
- Ensure Python dependencies are installed: `pip3 install -r requirements.txt`
- Check that `_lib/` directory exists in `.claude/commands/`

## Advanced Usage

### Autonomous Processing

Process tasks without confirmation prompts:

```bash
/3:process-tasks @path/to/tasks.md NOSUBCONF
```

### Batch Documentation Fetching

Fetch multiple libraries at once:

```bash
/doc:fetch-batch --file README.md --section "Dependencies"
```

### Fidelity-Preserving Workflow

The system uses specialized agents for exact scope implementation:

- **@developer-fidelity** - Implements only what's specified
- **@quality-reviewer-fidelity** - Reviews against specification only
- **@fidelity-reviewer** - Validates specification compliance

## Need Help?

- **Full documentation**: See [README.md](README.md)
- **Command details**: See [commands/README.md](commands/README.md)
- **Project guidance**: See [CLAUDE.md](CLAUDE.md)
