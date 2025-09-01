# Claude Code Configuration Repository

A comprehensive Claude Code configuration system that provides specialized agents, custom commands, and complete development workflows for building software with AI assistance.

## 🚀 Quick Start

### Installation

1. **Clone this repository**:

   ```bash
   git clone <repository-url>
   cd adn-claude-configs
   ```

2. **Run the installer**:

   ```bash
   ./install.sh
   ```

   The installer will automatically set up symlinks from `~/.claude/` to this repository, backing up any existing configuration.

## 📁 Repository Structure

```
adn-claude-configs/
├── agents/                   # Specialized AI agents for different development phases
├── commands/                 # Custom slash commands for task automation
├── tasks/                    # Generated PRDs, execution plans, and task lists
├── reports/                  # Generated Reports from quality review
├── .claude/                  # Local Claude Code settings (symlink to agents/)
├── settings.template.json    # Example full autonomy Claude Config
└── CLAUDE.md                 # Repository-specific guidance for Claude
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

- NOTE: Uses `opus` model - higher cost
- Creates architectural plans from requirements
- Designs scalable system structures
- Plans integration strategies and data flows
- Focuses on long-term maintainability

## 🛠️ Command Workflows

### 1. Documentation Fetch Workflow

**Fetch Library Documentation**:

```
/docs:fetch react                    # Fetch React documentation
/docs:fetch typescript --version 5.3 # Specific version
/docs:fetch lodash --sections api    # API reference only
/docs:fetch vue --update             # Update existing docs
/docs:fetch express --format minimal # Condensed format
```

### 2. Feature Development Workflow

**PRD-Based Development** (Simple features):

```
/build:create-prd → /build:generate-tasks.md -> /build:process-tasks → /build:review
```

**Research-Driven Development** (Complex features):

```
[Research Doc] → /build:exec-spec → /build:process-tasks → /build:review
```

### 3. Code Quality Workflows

**Simplification Workflow**:

```
/simplify:create-plan → @quality-reviewer → /simplify:process-plan
```

**Quality Assurance**:

```
/build:review → [Fix Issues] → [Re-review] → [Approve for PR]
```

## 🔄 Usage Patterns

### Fetching Documentation

The `/docs:fetch` command transforms scattered online documentation into locally stored, AI-friendly Markdown files for enhanced Claude Code integration:

1. **Basic usage**:

   ```bash
   /docs:fetch react
   # Fetches React documentation to /workspace/docs/frameworks/react/
   ```

2. **Advanced options**:

   ```bash
   /docs:fetch typescript --version 5.3
   # Fetch specific version

   /docs:fetch lodash --sections api
   # Fetch only API reference sections
   
   /docs:fetch vue --update
   # Update existing documentation
   
   /docs:fetch express --format minimal
   # Use condensed format
   ```

3. **Generated structure**:

   ```
   /workspace/docs/
   ├── libraries/lodash/
   ├── frameworks/react/
   └── languages/typescript/
       ├── index.md              # Overview and navigation
       ├── api-reference.md      # Complete API documentation  
       ├── best-practices.md     # Current patterns and conventions
       └── examples/             # Code examples and tutorials
   ```

**Features:**
- **AI-Optimized**: Content processed by Technical Writer agent for Claude Code understanding
- **Self-Learning**: Automatically discovers and saves site patterns for future use
- **Quality Validation**: Comprehensive content analysis with completeness metrics
- **Error Recovery**: Robust retry logic with exponential backoff
- **Enhanced Fetching**: Smart handling of JavaScript-heavy documentation sites

### Creating New Features

1. **Start with requirements gathering**:

   ```bash
   /build:create-prd
   # Follow interactive prompts to create detailed PRD
   ```

2. Build out the task lists
  
  ```bash
   git checkout -b feature/new-feature # optional, claude should do this
  /build:generate-tasks @path-to-prd.md
  # Generate parent tasks, review, and then say "Go" to build sub-tasks.
  # Should detect if you are on a branch and create one if not
  ```

2. **Process the implementation**:

   ```bash
   /build:process-tasks @path-to-task-list.md
   # Processes PRD tasks one at a time

   # Or, if you want no configuration
   /build:process-tasks @path-to-task-list.md NOSUBCONF
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

### Working with Research

1. **Convert research to execution plan**:

   ```bash
   /build:exec-spec @research-markdown-file.md
   # Converts strategy/research documents to detailed task lists
   ```

2. **Execute with full context**:

   ```bash
   /build:process-tasks @research-task-list.md
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
   @quality-reviewer @refactor-plan.md
   ```

3. **Execute approved changes**:

   ```bash
   /simplify:process-plan @refactor-task-list.md
   ```

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
- Documentation is generated after implementation, not before

## 📚 Documentation

- **[CLAUDE.md](CLAUDE.md)** - Repository-specific guidance for Claude Code integration

---

**Need help?** Check the documentation files above, review `commands/README.md` for detailed workflow guidance, or use the specialized agents for specific tasks.
