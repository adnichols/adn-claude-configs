# Complexity System Removal - Completed

## 🎯 Executive Summary

~~Implement a complexity inheritance system that flows from initial specification (PRD or research-spec) through task generation to implementation, with automatic selection of appropriate developer and quality agents based on objective complexity scoring criteria. Uses centralized routing, template-based agent generation, and clear precedence rules to prevent maintenance drift and ensure consistent behavior.~~

**SYSTEM REMOVED:** The complexity inheritance system has been completely removed and replaced with a simplified fidelity-preserving approach using developer-fidelity and quality-reviewer-fidelity agents for all implementations.

## 📋 Implementation Metadata

**Complexity Level:** moderate
**Developer Agent:** @developer
**Quality Agent:** @quality-reviewer
**Estimated Duration:** 3-4 days

## 🗂️ Relevant Files

### Core Infrastructure (New)

- `config/complexity-map.yaml` - Central configuration for complexity levels and routing
- `scripts/route_complexity.ts` - Central router for all complexity decisions
- `scripts/gen_agents.ts` - Agent generation script from templates
- `.logs/complexity-routing.jsonl` - Telemetry logging for routing decisions

### Agent Templates (New)

- `agents/templates/developer.hbs` - Handlebars template for developer agents
- `agents/templates/quality-reviewer.hbs` - Handlebars template for quality reviewer agents

### Generated Agent Files

- `agents/developer-minimum.md` - Generated from template
- `agents/developer-basic.md` - Generated from template  
- `agents/developer-moderate.md` - Generated from template
- `agents/developer-complex.md` - Generated from template
- `agents/quality-reviewer-minimum.md` - Generated from template
- `agents/quality-reviewer-basic.md` - Generated from template
- `agents/quality-reviewer-moderate.md` - Generated from template
- `agents/quality-reviewer-complex.md` - Generated from template

### Command Files (Existing - To Modify)

- `commands/p:create-prd.md` - Add YAML front-matter support
- `commands/p:research-spec.md` - Add YAML front-matter support
- `commands/p:gen-tasks.md` - Use router for complexity inheritance
- `commands/p:gen-spec-tasks.md` - Use router for complexity inheritance
- `commands/b:process-tasks.md` - Use router for auto-detection and validation
- `commands/b:process-tdd-tasks.md` - Use router for auto-detection and validation
- `commands/simplify:create-plan.md` - Use router for complexity detection

### Testing and Documentation

- `test/complexity-routing.test.ts` - Router and scoring tests
- `test/fixtures/` - Sample PRDs, specs, and tasks for each complexity level
- `docs/complexity-inheritance.md` - System documentation with scoring rubric
- `README.md` - Update with complexity inheritance overview

### Python Requirements

- `requirements.txt` - Python dependencies (pydantic, jinja2, PyYAML)

## ⚙️ Implementation Phases

### Phase 0: Python Toolchain Setup

**Objective:** Establish Python-based toolchain consistent with existing scripts

**Tasks:**

- [ ] 0.1 Choose Python implementation (aligns with existing scripts/*.py)
  - [ ] 0.1.1 Use pydantic for schema validation
  - [ ] 0.1.2 Use jinja2 for agent template generation  
  - [ ] 0.1.3 Use PyYAML for configuration parsing
  - [ ] 0.1.4 Add requirements.txt with dependencies

### Phase 1: Core Infrastructure

**Objective:** Build the foundational components for centralized routing and configuration

**Tasks:**

- [ ] 1.0 Create complexity scoring rubric and mapping configuration
  - [ ] 1.1 Create `config/complexity-map.yaml` with:
    - Explicit ordinal mappings for all enum fields:
      - blast_radius: file=0, package=1, service=2, org=3
      - data_sensitivity: none=0, pii=2, regulated=3
      - perf_budget_ms: ≤100=4, 101-200=3, 201-300=2, >300=1, none=0
      - backward_compat: false=0, true=2
    - Level thresholds (0-2: minimum, 3-4: basic, 5-7: moderate, 8+: complex)
    - Agent mappings per complexity level
    - Security/performance check definitions per level
    - Precedence rules: task > spec > prd > repo-config > default
  - [ ] 1.2 Define YAML front-matter schema with:
    - version, complexity (auto/explicit), agents (auto/explicit)
    - risk parameters (blast_radius, external_api_change, migration)
    - nonfunctional requirements (perf_budget_ms_p95, data_sensitivity)
    - routing controls (allow_override, override_reason)
  - [ ] 1.3 Create formal schemas with validation
    - [ ] 1.3.1 Define pydantic models for front-matter validation
    - [ ] 1.3.2 Define pydantic models for config/complexity-map.yaml
    - [ ] 1.3.3 Implement validation modes:
      - Strict mode (CI): fail on invalid metadata
      - Lenient mode (local): default to "basic" with audit note
    - [ ] 1.3.4 Add schema version field for evolution
  - [ ] 1.4 Add calibration dataset with golden fixtures
    - [ ] 1.4.1 Create test fixtures for each complexity level
    - [ ] 1.4.2 Define expected outcomes for each fixture
    - [ ] 1.4.3 Tune scoring weights until fixtures pass validation

- [ ] 2.0 Build central complexity router
  - [ ] 2.1 Create `scripts/route_complexity.py` with stable JSON interface:
    - Input: `--input <paths>`, `--stdin`, or file list arguments
    - Functions: parseComplexityMetadata, scoreComplexity, resolveComplexity, selectAgents
    - Output JSON structure with version, computed_level, per_axis scores, agents, checks, audit
    - CLI flags: `--dry-run`, `--strict`, `--audit-detail minimal|full`
    - Exit codes: 0=success, 1=validation error, 2=policy violation
  - [ ] 2.2 Implement field-level precedence logic with audit trail
    - [ ] 2.2.1 Define merge strategy per field type
    - [ ] 2.2.2 Create conflict resolution table for common cases
    - [ ] 2.2.3 Add deterministic tie-breakers (no timestamps)
  - [ ] 2.3 Add per-axis complexity tracking
    - [ ] 2.3.1 Compute security, performance, change_scope axes independently
    - [ ] 2.3.2 Global level = max(axis levels)
    - [ ] 2.3.3 Map validation requirements by dominant axis
  - [ ] 2.4 Add override validation (require reason if downgrading complexity)
  - [ ] 2.5 Add telemetry logging to `.logs/complexity-routing.jsonl`

- [ ] 3.0 Set up agent template system
  - [ ] 3.1 Create `agents/templates/developer.j2` (Jinja2 template) with:
    - Conditional blocks for each complexity level
    - Testing requirements varied by complexity
    - Security requirements varied by complexity
    - Performance requirements varied by complexity
  - [ ] 3.2 Create `agents/templates/quality-reviewer.j2` (Jinja2 template) with:
    - Review depth varied by complexity
    - Security validation varied by complexity
    - Performance validation varied by complexity
  - [ ] 3.3 Create `scripts/gen_agents.py` to generate all 8 agent files
  - [ ] 3.4 Add generation script (no package.json needed)

### Phase 2: Generate Agents from Templates

**Objective:** Replace manual agent maintenance with template-based generation

**Tasks:**

- [ ] 4.0 Implement agent generation pipeline
  - [ ] 4.1 Run `python scripts/gen_agents.py` to create all 8 agent files
  - [ ] 4.2 Verify generated agents have appropriate complexity-specific requirements:
    - Minimum: Basic validation only, prototype warnings
    - Basic: Unit tests for core logic, basic error handling
    - Moderate: Full testing, performance considerations
    - Complex: Enterprise validation, compliance checks
  - [ ] 4.3 Add golden tests to verify key requirements exist per level
  - [ ] 4.4 Remove old manually maintained agent files (after backup)

### Phase 3: Update Commands to Use Router

**Objective:** Modify all commands to use centralized routing instead of embedded logic

**Tasks:**

- [ ] 5.0 Update specification commands
  - [ ] 5.1 Modify `p:create-prd.md`:
    - Replace metadata sections with YAML front-matter
    - Use router to determine agents and next steps
    - Include inheritance source and computed complexity in output
    - Add audit trail showing scoring rationale
  - [ ] 5.2 Modify `p:research-spec.md`:
    - Replace metadata sections with YAML front-matter
    - Use router for agent selection and complexity validation
    - Add override reason requirement for manual complexity downgrade

- [ ] 6.0 Update task generation commands
  - [ ] 6.1 Modify `p:gen-tasks.md`:
    - Call router to parse PRD metadata and inherit complexity
    - Use router to select appropriate agents
    - Scale task detail based on router complexity determination
    - Embed routing decisions in task file front-matter
  - [ ] 6.2 Modify `p:gen-spec-tasks.md`:
    - Call router to parse spec metadata and inherit complexity
    - Use router for agent selection and validation requirements
    - Include routing audit in execution plan header

- [ ] 7.0 Update build commands
  - [ ] 7.1 Modify `b:process-tasks.md`:
    - Call router to detect complexity from task file metadata
    - Auto-select developer and quality agents from router
    - Apply complexity-appropriate validation from config/complexity-map.yaml:
      - Minimum: lint + build + secrets scan only
      - Basic: + unit-core + dep audit
      - Moderate: + integration tests + perf smoke + basic SAST
      - Complex: + e2e + perf benchmark + SAST+DAST + SBOM
    - Log routing decisions to telemetry
  - [ ] 7.2 Modify `b:process-tdd-tasks.md`:
    - Add same router integration
    - Adjust TDD requirements based on complexity level

- [ ] 8.0 Update simplification command
  - [ ] 8.1 Modify `simplify:create-plan.md`:
    - Use router to detect project complexity from existing files
    - Scale cleanup aggressiveness based on complexity:
      - Minimum: Very aggressive cleanup allowed
      - Basic: Moderate cleanup
      - Moderate: Conservative cleanup
      - Complex: Very conservative cleanup
    - Block aggressive cleanup if `backward_compat_required: true`
    - Auto-select appropriate quality reviewer agent

### Phase 4: Testing and Telemetry Infrastructure

**Objective:** Ensure system reliability with comprehensive testing and feedback loops

**Tasks:**

- [ ] 9.0 Build test matrix
  - [ ] 9.1 Create test fixtures in `test/fixtures/`:
    - Sample PRDs for each complexity level
    - Sample specs for each complexity level
    - Sample task files for each complexity level
    - Files with conflicting metadata for precedence testing
  - [ ] 9.2 Create `test/complexity-routing.test.ts`:
    - Test complexity scoring with various metadata combinations
    - Test precedence rules with conflicting metadata
    - Test agent selection for each complexity level
    - Test override validation and audit trail
    - Test backward compatibility with files lacking front-matter
  - [ ] 9.3 Add end-to-end integration tests:
    - Complete workflow tests for each complexity level
    - Metadata inheritance tests through the full pipeline
    - Agent selection validation at each stage

- [ ] 10.0 Implement telemetry and monitoring
  - [ ] 10.1 Add telemetry collection to router:
    - Log routing decisions with timestamp, command, levels, agents
    - Track overrides and reasons
    - Record conflicts and precedence resolutions
  - [ ] 10.2 Create telemetry analysis script:
    - Summarize adoption rates by complexity level
    - Track override frequency and reasons
    - Identify common precedence conflicts
  - [ ] 10.3 Add success metrics tracking:
    - Percentage of auto-routed decisions without override
    - Review defect rates by complexity level
    - Build failure rates by complexity level

### Phase 5: Documentation and Migration

**Objective:** Provide clear documentation and migration path for existing projects

**Tasks:**

- [ ] 11.0 Create comprehensive documentation
  - [ ] 11.1 Create `docs/complexity-inheritance.md`:
    - Detailed scoring rubric with examples
    - Front-matter schema documentation
    - Precedence rules explanation
    - Agent selection logic
    - Migration guide for existing projects
  - [ ] 11.2 Update main `README.md`:
    - Overview of complexity inheritance system
    - Quick start guide with examples
    - Links to detailed documentation
  - [ ] 11.3 Create Mermaid flow diagram showing:
    - Metadata flow from PRD → spec → tasks → build
    - Router decision points
    - Agent selection process
    - Precedence resolution

- [ ] 12.0 Implement migration tooling
  - [ ] 12.1 Create migration detection script:
    - Scan existing files for old-style metadata
    - Identify files needing front-matter conversion
    - Suggest appropriate complexity levels based on content
  - [ ] 12.2 Create lint rules:
    - Flag missing front-matter in new files
    - Warn about invalid complexity metadata
    - Suggest autofix for common issues
  - [ ] 12.3 Add backward compatibility mode:
    - Gracefully handle files without front-matter
    - Default to "basic" complexity with audit note
    - Provide migration suggestions in output

### Phase 6: Final Validation and Optimization

**Objective:** Ensure system works end-to-end and optimize for real-world usage

**Tasks:**

- [ ] 13.0 End-to-end validation
  - [ ] 13.1 Test complete workflows for each complexity level:
    - Minimum: Simple feature from PRD to implementation
    - Basic: Standard feature with testing requirements
    - Moderate: Production feature with full validation
    - Complex: Enterprise feature with compliance checks
  - [ ] 13.2 Test edge cases and error conditions:
    - Missing front-matter handling
    - Invalid complexity metadata
    - Agent selection failures
    - Precedence conflicts
  - [ ] 13.3 Performance testing:
    - Router performance with large metadata
    - Agent generation speed
    - Template rendering performance

- [ ] 14.0 System optimization and cleanup
  - [ ] 14.1 Optimize router performance for common cases
  - [ ] 14.2 Add caching for frequently accessed configurations
  - [ ] 14.3 Clean up temporary files and migration artifacts
  - [ ] 14.4 Final documentation review and updates
  - [ ] 14.5 Create demo examples for each complexity level

## 📊 Success Metrics

- **Objective Complexity Scoring:** Complexity levels determined by measurable criteria
- **Zero Agent Maintenance Drift:** All agents generated from templates
- **Consistent Routing Decisions:** Single router used by all commands
- **Clear Precedence Handling:** Predictable conflict resolution
- **Comprehensive Audit Trail:** Full visibility into routing decisions
- **High Auto-Routing Rate:** >80% of decisions made automatically without override
- **Backward Compatibility:** Existing files work without modification

## 🚨 Critical Requirements

- **Centralized Configuration:** All complexity logic in `config/complexity-map.yaml`
- **Template-Based Agents:** Zero manual agent file maintenance
- **Objective Scoring:** Measurable criteria for complexity determination
- **Clear Precedence Rules:** task > spec > prd > repo-config > default
- **Audit Trail:** Full logging of routing decisions and rationale
- **Override Validation:** Require explicit reason for complexity downgrades
- **Backward Compatibility:** Graceful handling of legacy files

## ✅ Validation Strategy

1. **Scoring Validation:** Test rubric with diverse project examples
2. **Precedence Testing:** Verify conflict resolution in all scenarios
3. **Agent Generation:** Golden tests ensure template consistency
4. **End-to-End Flows:** Complete workflows for each complexity level
5. **Migration Testing:** Legacy project compatibility validation
6. **Performance Testing:** Router and generation pipeline performance
7. **Telemetry Validation:** Logging accuracy and analysis capability

## 🔧 Technical Architecture

### Complexity Scoring Formula

```
Score = (blast_radius_ordinal × 2) + (data_sensitivity_ordinal × 2) + (backward_compat_ordinal × 1) + 
        (perf_budget_ordinal × 1) + (migration_ordinal × 2) + (external_api_change_ordinal × 1)

Ordinal Mappings:
- blast_radius: file=0, package=1, service=2, org=3
- data_sensitivity: none=0, pii=2, regulated=3  
- perf_budget_ms: ≤100=4, 101-200=3, 201-300=2, >300=1, none=0
- backward_compat: false=0, true=2
- migration: false=0, true=2
- external_api_change: false=0, true=1

Levels: 0-2: minimum, 3-4: basic, 5-7: moderate, 8+: complex
```

### Front-Matter Schema

```yaml
---
version: 1
complexity: auto  # or minimum|basic|moderate|complex
agents:
  developer: auto  # or explicit agent name
  reviewer: auto   # or explicit agent name
risk:
  blast_radius: service     # file|package|service|org
  external_api_change: true
  migration: false
nonfunctional:
  perf_budget_ms_p95: 200
  data_sensitivity: pii     # none|pii|regulated
  backward_compat_required: true
routing:
  allow_override: true
  override_reason: ""       # required if overriding computed level
---
```

### Precedence Rules

1. **task.md** metadata (highest priority)
2. **spec.md** metadata
3. **prd.md** metadata
4. **repo-config** defaults
5. **hard default** ("basic") (lowest priority)

## 📋 Notes

- Template-based approach eliminates agent maintenance drift
- Objective scoring removes subjectivity from complexity determination
- Centralized router ensures consistent behavior across all commands
- Telemetry enables continuous improvement of the system
- Clear precedence rules prevent metadata conflicts
- Backward compatibility ensures smooth adoption for existing projects