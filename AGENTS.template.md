# AGENTS.md Template (Project-Level)

> Copy this file into a project repo as `AGENTS.md` and fill in the sections marked **PROJECT-SPECIFIC**. Sections marked **PREPOPULATED** can usually be reused as-is or lightly adjusted.

## Project Overview  <!-- PROJECT-SPECIFIC -->

- **Project name:** TODO
- **Primary purpose / domain:** TODO
- **Critical constraints (latency, compliance, SLAs, etc.):** TODO
- **Environments:** TODO (local, staging, production, etc.)

## Stack & Tooling  <!-- PROJECT-SPECIFIC -->

- **Languages:** TODO (e.g., TypeScript, Python)
- **Frameworks / libraries:** TODO (e.g., Next.js, Django)
- **Package managers & build tools:** TODO (e.g., npm, pnpm, Poetry, Make)
- **Entry points / run commands:**
  - Dev server: `TODO`
  - Build: `TODO`
  - Start: `TODO`

## Tool Selection (Codex Environment)  <!-- PREPOPULATED, ADJUST IF NEEDED -->

When agents run within Codex, they should prioritize native Codex tools over MCP server tools:

**DO:**
- Use native `Grep` / `Glob` / `Read` tools when available.
- Use direct shell commands (`rg`, `fd`, `find`, etc.) for filesystem operations.
- Prefer local scripts and CLIs already defined in the repo (e.g., `npm test`, `make test`).

**DO NOT:**
- Call MCP-prefixed tools for basic filesystem operations when native tools exist.
- Route through remote MCP servers for simple local searches or file reads.

**Rationale:** Native Codex tools are optimized for the local filesystem and are faster and more predictable than remote wrappers.

## Fidelity & Execution Rules  <!-- PREPOPULATED, TUNE PER PROJECT -->

These rules apply to fidelity-oriented workflows (PRDs/specs → tasks → implementation, simplification plans, etc.).

### Fidelity

- Treat the source document (user requirements, PRD, specification, or task file) as the single source of truth.
- Do not add requirements, tests, or security work beyond what is explicitly specified, unless this project section explicitly allows it.
- Do not broaden scope; when something is ambiguous or missing, ask for clarification instead of guessing.
- Preserve stated constraints and limitations unless this file explicitly authorizes changing them.

### Execution

- **Branches**
  - Do implementation work on a non-`main` branch.
  - Branch naming convention: `TODO` (e.g., `feature/<short-summary>`, `issue/<ticket-id>`).

- **Testing & Validation**
  - Primary test command(s): `TODO` (e.g., `npm test`, `pytest`, `cargo test`).
  - Additional checks (fill in as relevant):
    - Lint: `TODO` (e.g., `npm run lint`)
    - Typecheck: `TODO`
    - Build: `TODO`
    - Security / SAST: `TODO`
  - Before committing behavior changes, run the primary tests and any required additional checks for the touched area.

- **Task Lists & Plans**
  - When working from markdown task lists or simplification plans:
    - After completing a listed sub-task or step, immediately change its checkbox from `[ ]` to `[x]` in the same file.
    - Verify that the change is present in the file (avoid batching updates at the end).
    - Keep any “Relevant Files” / “Changed Files” sections accurate as files are created or modified.

## Security & Data Handling  <!-- PROJECT-SPECIFIC -->

- **Data classifications:** TODO (what data is sensitive, PII, etc.)
- **Forbidden behaviors:** TODO (e.g., never log secrets, never write to certain directories)
- **AuthN/AuthZ expectations:** TODO (e.g., always enforce permission checks in certain layers)
- **External services / secrets management:** TODO (e.g., how to access APIs, where secrets live)

## Testing Philosophy  <!-- PROJECT-SPECIFIC, WITH HINTS -->

- **Preferred test types:** TODO (unit vs integration vs e2e)
- **Coverage expectations:** TODO (e.g., “no new code without tests near 80%+ coverage in this module”)
- **Flaky / slow tests:** TODO (list known problematic suites, how to handle them)

## Git & Review Workflow  <!-- PROJECT-SPECIFIC -->

- **Branch protection rules:** TODO (what’s protected, and how)
- **Commit style:** TODO (e.g., Conventional Commits)
- **Review expectations:** TODO (e.g., when to request a human review, which files are high-risk)
- **CI / CD:** TODO (what pipelines run on PRs, what must be green before merge)

## Documentation & Task Files  <!-- PROJECT-SPECIFIC -->

- **Key docs:** TODO (e.g., `README.md`, `TESTING.md`, `ARCHITECTURE.md`, any API docs)
- **Task / PRD locations:** TODO (e.g., `/tasks/prd-*.md`, `/tasks/tasks-*.md`)
- **Doc update expectations:** TODO (e.g., “update README and API docs whenever public behavior changes”)

---

Agents should treat this `AGENTS.md` as authoritative for project-specific rules and combine it with any instructions in prompt files that are invoked from Codex. When in doubt, prefer the stricter rule (safer choice) and surface ambiguities to the human operator.
