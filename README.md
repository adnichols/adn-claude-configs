# Claude Code Configuration Repository

A comprehensive Claude Code configuration system that provides specialized agents, custom commands, and complete development workflows for building software with AI assistance.

## 🚀 Quick Start

### Installation

1. **Clone this repository**:

   ```bash
   git clone <repository-url>
   cd adn-claude-configs
   ```

2. **Set up the symlink structure** (required for proper operation):

   ```bash
   # Create the symlink from .claude to .agents (if not already present)
   ln -sf agents .claude
   ```

3. **Configure Claude Code**:
   - Copy `settings.json` to your project's `.claude/` directory
   - Or copy individual agents/commands to your global `~/.claude/` directory

### First Use

```bash
# Create a new product requirement document
/build:create-prd

# Generate execution tasks from research
/build:exec-spec

# Process and execute task lists
/build:process-tasks

# Review code quality before PR
/build:review

# Generate documentation after implementation
/build:document
```

## 📁 Repository Structure

```
adn-claude-configs/
├── agents/              # Specialized AI agents for different development phases
├── commands/            # Custom slash commands for task automation
├── tasks/              # Generated PRDs, execution plans, and task lists
├── examples/           # Strategy documents and integration examples
├── .claude/            # Local Claude Code settings (symlink to agents/)
├── settings.json       # Main Claude Code configuration
└── CLAUDE.md          # Repository-specific guidance for Claude
```

## 🤖 Available Agents

### Core Development Agents

**`@developer`** - Production-ready implementation

- Implements specifications with comprehensive tests
- Enforces zero linting violations
- Follows project-specific standards from CLAUDE.md
- Handles error cases and edge conditions

**`@quality-reviewer`** - Pre-production validation

- Reviews code for security, performance, and data integrity issues
- Identifies potential production failures
- Validates test coverage and error handling
- Provides structured quality reports

**`@technical-writer`** - Post-implementation documentation

- Creates concise, actionable documentation
- Focuses on practical usage patterns
- Maintains strict token limits for readability
- Documents actual behavior, not aspirational features

### Specialized Agents

**`@simplify-planner`** - Code complexity reduction

- Analyzes codebases for simplification opportunities
- Creates structured refactoring plans
- Identifies over-engineering and technical debt
- Generates risk-assessed improvement strategies

**`@debugger`** - Systematic issue analysis

- Evidence-based bug investigation
- Step-by-step debugging workflows
- Root cause analysis with clear action items
- Handles complex, hard-to-reproduce issues

**`@plan-architect`** - High-level system design

- Creates architectural plans from requirements
- Designs scalable system structures
- Plans integration strategies and data flows
- Focuses on long-term maintainability

## 🛠️ Command Workflows

### 1. Feature Development Workflow

**PRD-Based Development** (Simple features):

```
/build:create-prd → /build:generate-tasks.md -> /build:process-tasks → /build:review → /build:document
```

**Research-Driven Development** (Complex features):

```
[Research Doc] → /build:exec-spec → /build:process-tasks → /build:review → /build:document
```

### 2. Code Quality Workflows

**Simplification Workflow**:

```
/simplify:create-plan → @quality-reviewer → /simplify:process-plan
```

**Quality Assurance**:

```
/build:review → [Fix Issues] → [Re-review] → [Approve for PR]
```

## 📋 Command Reference

### Build Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/build:create-prd` | Generate Product Requirements Documents | New feature development, clear requirements |
| `/build:exec-spec` | Convert research to execution plans | Complex implementations, architecture-heavy projects |
| `/build:generate-tasks` | Create task lists from specifications | Breaking down large projects |
| `/build:process-tasks` | Execute task lists with git management | Any task list execution, requires feature branch |
| `/build:review` | Pre-PR quality reviews | Before creating pull requests |
| `/build:document` | Generate post-implementation docs | After feature completion |

### Simplify Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/simplify:create-plan` | Analyze code for simplification | Code cleanup, technical debt reduction |
| `/simplify:process-plan` | Execute simplification plans | Implementing approved refactoring plans |

## ⚙️ Configuration Features

### Custom Status Line

Shows current directory and git branch with status:

- **Clean branch**: `➜ project-name git:(main)`
- **Dirty branch**: `➜ project-name git:(feature) ✗`

### MCP Integration

- **basic-memory** server for persistent memory across sessions
- Extensible MCP server configuration

### Model Configuration

- Uses "sonnet" model as default
- Optimized for development tasks

## 🔄 Usage Patterns

### Creating New Features

1. **Start with requirements gathering**:

   ```bash
   /build:create-prd
   # Follow interactive prompts to create detailed PRD
   ```

2. **Process the implementation**:

   ```bash
   git checkout -b feature/new-feature
   /build:process-tasks
   # Processes PRD tasks one at a time
   ```

3. **Quality review**:

   ```bash
   /build:review
   # Comprehensive pre-PR quality check
   ```

4. **Generate documentation**:

   ```bash
   /build:document
   # Creates user and technical documentation
   ```

### Working with Complex Research

1. **Convert research to execution plan**:

   ```bash
   /build:exec-spec
   # Converts strategy/research documents to detailed task lists
   ```

2. **Execute with full context**:

   ```bash
   /build:process-tasks
   # Preserves all research context during implementation
   ```

### Code Simplification

1. **Analyze for improvements**:

   ```bash
   /simplify:create-plan
   # Creates detailed simplification plan
   ```

2. **Review with quality agent**:

   ```bash
   @quality-reviewer review the simplification plan
   ```

3. **Execute approved changes**:

   ```bash
   /simplify:process-plan
   ```

## 🔧 Advanced Configuration

### Copying to New Repositories

When setting up this configuration in a new repository:

1. **Copy the directory structure**:

   ```bash
   cp -r adn-claude-configs/agents new-project/.claude/
   cp -r adn-claude-configs/commands new-project/.claude/
   cp adn-claude-configs/settings.json new-project/.claude/
   ```

2. **Create the symlink** (important for proper operation):

   ```bash
   cd new-project
   ln -sf .claude agents
   ```

3. **Customize CLAUDE.md** for project-specific standards

### Project-Specific Customization

Edit `CLAUDE.md` in your project to define:

- Language-specific conventions
- Testing requirements and commands
- Build and linting commands
- Error handling patterns
- Code style guidelines

## 📖 Best Practices

### Git Workflow Requirements

- **Always work on feature branches** (never directly on main)
- **One sub-task at a time** unless `NOSUBCONF` is specified
- **Tests must pass** before any commits
- **Conventional commit format** is automatically applied

### Task Processing Guidelines

- Use `NOSUBCONF` parameter for batch processing when appropriate
- Provide clear, actionable task descriptions
- Break complex features into phases with clear boundaries
- Include test requirements in all implementation tasks

### Quality Standards

- All agents reference CLAUDE.md for project-specific standards
- Zero linting violations are enforced by `@developer` agent
- Security and performance reviews are mandatory for production code
- Documentation is generated after implementation, not before

## 🆘 Troubleshooting

### Common Issues

**Command not found**: Ensure agents are properly symlinked and commands are in `.claude/commands/`

**Git branch errors**: `/build:process-tasks` requires working on a feature branch (not main)

**Test failures**: All commands require tests to pass before committing

**Symlink issues**: Remember to recreate the `.claude → agents` symlink when copying

### Getting Help

1. Check `CLAUDE.md` for project-specific guidance
2. Review command documentation in `commands/README.md`
3. Use agents for specific help:
   - `@developer` for implementation questions
   - `@quality-reviewer` for code quality issues
   - `@debugger` for systematic issue analysis

## 🤝 Contributing

This configuration system is designed to be:

- **Extensible**: Add new agents and commands easily
- **Adaptable**: Customize for different project types
- **Maintainable**: Clear documentation and consistent patterns

When adding new commands or agents, follow the existing patterns and update documentation accordingly.

## 📄 License

[Add your license information here]

---

**Need help?** Check the `commands/README.md` for detailed workflow documentation or use the specialized agents for guidance on specific tasks.

