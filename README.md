# Claude Code Configuration Repository

A comprehensive Claude Code configuration system that provides specialized agents, custom commands, and complete development workflows for building software with AI assistance.

## 🚀 Quick Start

### Installation

1. **Clone this repository**:

   ```bash
   git clone <repository-url>
   cd adn-claude-configs
   ```

2. **Install Python dependencies**:

   ```bash
   pip3 install -r requirements.txt
   ```

3. **Generate complexity-aware agents**:

   ```bash
   python3 scripts/gen_agents.py --validate
   ```

4. **Run the installer** (if available):

   ```bash
   ./install.sh
   ```

   The installer will automatically set up symlinks from `~/.claude/` to this repository, backing up any existing configuration.

## 🧠 Complexity Inheritance System

This repository features an advanced **Complexity Inheritance System** that automatically:

- **Detects complexity levels** based on objective scoring criteria
- **Selects appropriate agents** for each complexity level
- **Applies validation requirements** matching the complexity level
- **Inherits metadata** through PRD → spec → tasks → implementation pipeline

### Complexity Levels

| Level | Score | Agent Type | Validation Requirements |
|-------|-------|------------|------------------------|
| **Minimum** | 0-2 | `developer-minimum` | Lint + Build + Secrets |
| **Basic** | 3-4 | `developer-basic` | + Unit Tests + Audit |
| **Moderate** | 5-7 | `developer-moderate` | + Integration + SAST |
| **Complex** | 8+ | `developer-complex` | + E2E + Advanced Security |

See [Complexity Inheritance Documentation](docs/complexity-inheritance.md) for complete details.

## 📁 Repository Structure

```
adn-claude-configs/
├── agents/                   # Generated complexity-aware AI agents
│   ├── templates/           # Jinja2 templates for agent generation
│   ├── developer-*.md       # Generated developer agents by complexity
│   └── quality-reviewer-*.md # Generated reviewer agents by complexity
├── commands/                 # Router-integrated slash commands
│   ├── p:create-prd.md      # PRD creation with complexity detection
│   ├── p:gen-tasks.md       # Task generation with metadata inheritance
│   └── b:process-tasks.md   # Implementation with auto agent selection
├── config/                   # Complexity inheritance configuration
│   └── complexity-map.yaml  # Central complexity scoring and mapping
├── scripts/                  # Core system scripts
│   ├── route_complexity.py  # Central complexity router
│   ├── gen_agents.py       # Agent generation from templates
│   └── schemas.py          # Pydantic models for validation
├── test/                     # Test fixtures and validation
│   └── fixtures/           # Sample PRDs for testing
├── docs/                     # System documentation
│   └── complexity-inheritance.md # Complete system documentation
├── .logs/                    # Telemetry and audit logs
├── tasks/                    # Generated PRDs, specs, and task lists
├── .claude/                  # Local Claude Code settings (symlink)
└── CLAUDE.md                 # Repository-specific guidance
```

## 🤖 Available Agents

The system automatically generates complexity-aware agents from templates. All agents are generated via `python3 scripts/gen_agents.py` to prevent maintenance drift.

### Developer Agents (Auto-Selected by Complexity)

**`@developer-minimum`** - Prototype implementation
- Basic functionality focus
- Simple unit tests
- Prototype-level quality acceptable

**`@developer-basic`** - Production-ready implementation  
- Comprehensive unit and integration tests
- Follows project standards from CLAUDE.md
- Zero linting violations enforced

**`@developer-moderate`** - Enterprise-grade implementation
- Advanced testing including performance tests
- Security validation and monitoring
- Full error handling and edge cases

**`@developer-complex`** - Mission-critical implementation
- Comprehensive test coverage (>90%)
- Advanced security and compliance validation
- Performance benchmarking and scalability

### Quality Reviewer Agents (Auto-Selected by Complexity)

**`@quality-reviewer-minimum`** - Basic validation
- Code correctness and simple security checks
- Basic error handling review

**`@quality-reviewer-basic`** - Production validation
- Security vulnerabilities (OWASP Top 10)
- Performance anti-patterns
- Test coverage adequacy

**`@quality-reviewer-moderate`** - Comprehensive validation
- Advanced security analysis
- Performance bottlenecks and scalability
- Integration testing adequacy

**`@quality-reviewer-complex`** - Enterprise validation
- Full security audit and compliance
- Advanced performance analysis
- Disaster recovery and business continuity
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
/plan:create-prd → /plan:generate-tasks.md -> /build:process-tasks → /plan:review
```

**Research-Driven Development** (Complex features):

```
[Research Doc] → /plan:generate-tasks-from-spec → /build:process-tasks → /plan:review
```

### 3. Code Quality Workflows

**Simplification Workflow**:

```
/simplify:create-plan → @quality-reviewer → /simplify:process-plan
```

**Quality Assurance**:

```
/plan:review → [Fix Issues] → [Re-review] → [Approve for PR]
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
   /plan:create-prd
   # Follow interactive prompts to create detailed PRD
   ```

2. Build out the task lists
  
  ```bash
   git checkout -b feature/new-feature # optional, claude should do this
  /plan:generate-tasks @path-to-prd.md
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
   /plan:review
   # Comprehensive pre-PR quality check
   ```

4. **Generate documentation**:

   ```bash
   /docs:update
   # Creates user and technical documentation
   ```

### Working with Research

1. **Convert research to execution plan**:

   ```bash
   /plan:generate-tasks-from-spec @research-markdown-file.md
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
