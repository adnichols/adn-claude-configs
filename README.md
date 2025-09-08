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

3. **Verify agent configurations** (if needed):

   ```bash
   # Agents are already configured and ready to use
   ls agents/

4. **Run the installer** (if available):

   ```bash
   ./install.sh
   ```

   The installer will automatically set up symlinks from `~/.claude/` to this repository, backing up any existing configuration.

## 🧠 Fidelity-Preserving System

This repository features a **Fidelity-Preserving System** that automatically:

- **Preserves exact scope** from requirements through implementation
- **Uses fidelity-preserving agents** for implementation and quality review
- **Prevents scope creep** by maintaining strict adherence to specifications
- **Ensures quality** through comprehensive validation while staying within scope

### Agent Types

| Purpose | Agent Type | Validation Requirements |
|---------|------------|------------------------|
| **Implementation** | `developer-fidelity` | Lint + Build + Secrets + Unit Tests |
| **Quality Review** | `quality-reviewer-fidelity` | Production readiness validation |
| **Fidelity Check** | `fidelity-reviewer` | Specification compliance validation |

The system emphasizes scope preservation and exact requirement implementation over complexity-based branching.

## 📁 Repository Structure

```
adn-claude-configs/
├── agents/                   # Fidelity-preserving AI agents
│   ├── developer-fidelity.md      # Exact scope implementation
│   ├── quality-reviewer-fidelity.md # Fidelity-preserving quality review
│   ├── fidelity-reviewer.md       # Specification compliance validation
│   └── [other specialized agents] # Additional agents for specific tasks
├── commands/                 # Fidelity-preserving slash commands
│   ├── p:create-prd.md      # PRD creation with scope preservation
│   ├── p:gen-tasks.md       # Task generation with fidelity preservation
│   └── b:process-tasks.md   # Implementation with fidelity agents
├── tools/                    # Repository maintenance tools
│   └── gen_agents.py        # Agent generation from templates
├── test/                     # Test fixtures and validation
│   └── fixtures/           # Sample PRDs for testing
├── docs/                     # System documentation
├── .logs/                    # Telemetry and audit logs
├── tasks/                    # Generated PRDs, specs, and task lists
├── .claude/                  # Local Claude Code settings (symlink)
└── CLAUDE.md                 # Repository-specific guidance
```

## 🤖 Available Agents

The system uses carefully configured agents that focus on exact scope implementation and quality validation.

### Core Implementation Agents

**`@developer-fidelity`** - Fidelity-preserving implementation
- Implements only what's explicitly specified in source documents
- Comprehensive unit and integration tests as required
- Follows project standards from CLAUDE.md
- Zero linting violations enforced
- Questions ambiguities rather than making assumptions

**`@quality-reviewer-fidelity`** - Fidelity-preserving quality review
- Reviews against source specifications for exact compliance
- Security vulnerabilities and production readiness
- Performance analysis within specified scope
- Test coverage validation for specified requirements
- Prevents scope creep during review process

**`@fidelity-reviewer`** - Specification compliance validation  
- Compares implementations against original specifications
- Identifies missing requirements and scope additions
- Provides structured decision options for ambiguities
- Ensures 100% fidelity to source documents
- Used in spec-to-tasks conversion process

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

**PRD-Based Development** (Standard workflow):

```
/p:create-prd → /p:gen-tasks → /b:process-tasks → /p:review
```

**Specification-Based Development** (Direct from specs):

```
[Detailed Spec] → /p:spec-to-tasks → /b:process-tasks → /p:review
```

**Research-Based Development** (From research documents):

```
[Research Doc] → /p:research-spec → /p:spec-to-tasks → /b:process-tasks → /p:review
```

### 3. Code Quality Workflows

**Simplification Workflow**:

```
/simplify:create-plan → @quality-reviewer → /simplify:process-plan
```

**Quality Assurance**:

```
/p:review → [Fix Issues] → [Re-review] → [Approve for PR]
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
   /p:create-prd
   # Follow interactive prompts to create detailed PRD
   ```

2. **Build out the task lists**:
  
   ```bash
   git checkout -b feature/new-feature # optional, claude should do this
   /p:gen-tasks @path-to-prd.md
   # Generate parent tasks, review, and then say "Go" to build sub-tasks.
   # Should detect if you are on a branch and create one if not
   ```

3. **Process the implementation**:

   ```bash
   /b:process-tasks @path-to-task-list.md
   # Processes PRD tasks one at a time with fidelity preservation

   # Or, if you want no confirmation prompts
   /b:process-tasks @path-to-task-list.md NOSUBCONF
   ```

4. **Quality review**:

   ```bash
   /p:review
   # Comprehensive pre-PR quality check
   ```

5. **Generate documentation**:

   ```bash
   /docs:update
   # Creates user and technical documentation
   ```

### Working with Research

1. **Convert research to specification**:

   ```bash
   /p:research-spec @research-idea-description.md
   # Converts research ideas into comprehensive specification documents
   ```

2. **Convert specification to tasks**:

   ```bash
   /p:spec-to-tasks @research-spec-file.md
   # Converts specifications to detailed task lists with fidelity preservation
   ```

3. **Execute with full context**:

   ```bash
   /b:process-tasks @fidelity-task-list.md
   # Preserves all specification context during implementation
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
