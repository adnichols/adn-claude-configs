---
date: 2026-01-11T05:01:37Z
author: claude
git_commit: fe79e9ec41d847d112f829e1415d1944d9e9ee1a
branch: main
repository: adn-claude-configs
type: research
status: complete
tags: [testing, e2e, api, auth-bypass, ltui]
last_updated: 2026-01-11
---

# Research: Test Landscape and API Surfaces

## Research Question

The user requested research to create a plan for replacing e2e tests with API tests that are fast and light. The goal was to:
- Create minimal e2e tests that validate basic UI rendering
- Create API contract tests for functional validation
- Skip authentication using auth bypass for most tests
- Have a small number of API and e2e tests that validate auth functionality

## Summary

**This repository is a configuration repository for AI coding tools (Claude Code, Codex, Gemini CLI, OpenCode) and does not contain traditional web application code.** Consequently:

- **No traditional e2e UI tests exist** (no Playwright, Cypress, or browser automation tests)
- **No web API endpoints exist** (no Express, FastAPI, or REST API routes)
- **No UI component rendering tests exist** (no React, Vue, or other frontend framework tests)
- **No API contract tests exist** (no HTTP endpoint testing)

The only tests present are:
1. **CLI integration tests** for the `ltui` tool (Linear CLI)
2. **Installation script tests** for the configuration installation process
3. **CLI output formatting tests** for terminal output validation

The `ltui` tool includes an **auth bypass mechanism** for testing that uses a mock Linear API client.

## Detailed Findings

### 1. Existing E2E Tests

#### 1.1 ltui CLI Integration Tests

**Location:** `/Users/anichols/code/adn-claude-configs/tools/ltui/src/__tests__/`

**Framework:** Node.js builtin `node:test` with `assert/strict`

**Test Files:**

| File | Lines | Description |
|------|-------|-------------|
| `cli-regression.test.ts` | 270 | Full CLI command integration tests |
| `cli-args.test.ts` | 86 | CLI argument parsing and help output validation |
| `output.test.ts` | 174 | Output formatting for TSV and JSON outputs |

**cli-regression.test.ts** validates:
- Line 64-81: Auth commands (add, list, test, remove)
- Line 83-182: Issues commands (list, view, create, update, comment, link, relate, block, saved search)
- Line 184-222: Team and project commands
- Line 224-239: Cycles, labels, and users commands
- Line 241-269: Documents, roadmaps, milestones, and notifications

**cli-args.test.ts** validates:
- Help output for all commands (auth, issues, teams, projects, cycles, labels, users, documents, roadmaps, milestones, notifications)
- Verifies all expected flags and options appear in help text

**output.test.ts** validates:
- Line 10-21: Auth command list and detail formats
- Line 23-53: Issues list TSV layout
- Line 55-72: Issues detail format with description markers
- Line 73-81: Issues JSON output format
- Line 83-96: Teams list column layout
- Line 98-108: Projects detail block markers
- Line 110-152: Cycles, labels, and users TSV layout
- Line 154-167: Projects list TSV layout
- Line 169-173: Pagination metadata emission

#### 1.2 Installation Script Tests

**Location:** `/Users/anichols/code/adn-claude-configs/test_install.sh`

**Framework:** Bash shell script with custom test framework

**Lines:** 523

**Validates:**
- Script permissions and executability
- Repository structure validation
- Cross-platform command compatibility (readlink, ln)
- Error handling with invalid repositories
- Backup functionality simulation
- Security tests (race condition prevention, malicious symlink prevention, path traversal prevention)
- POSIX compliance
- Exit codes

### 2. Existing API Tests

**No API tests exist in this repository.**

The repository does not contain web API endpoints or HTTP-based API tests. The only "API" testing is the CLI integration testing of the Linear API client via the mock client.

### 3. API Surfaces/Endpoints

**No web API endpoints exist in this repository.**

This is a configuration repository, not a web application. The only API-related code is:

#### 3.1 Linear API Client (ltui tool)

**Location:** `/Users/anichols/code/adn-claude-configs/tools/ltui/src/client.ts`

**Lines:** 26

**Purpose:** Creates Linear SDK client for interacting with Linear's API

**Key Function:**
- Line 9-26: `createLinearClient(resolved: ResolvedConfig): LinearClient`
  - Checks for `LTUI_TEST_CLIENT_MODULE` environment variable for auth bypass
  - Creates real Linear client with API key if no bypass
  - Caches client instance

**Linear SDK Methods Used (via mock client):**
- `teams()`, `team(id)` - Team queries
- `issues()`, `issue(ref)`, `searchIssues()` - Issue operations
- `createIssue(input)`, `updateIssue(id, input)` - Issue mutations
- `createComment()` - Comment creation
- `createAttachment()`, `createIssueRelation()` - Attachments and relations
- `projects()`, `project(id)` - Project operations
- `cycles()` - Cycle queries
- `issueLabels()`, `labels()` - Label operations
- `users()` - User queries
- `documents()`, `document(id)`, `searchDocuments()` - Document operations
- `roadmaps()`, `roadmap(id)` - Roadmap operations
- `projectMilestones()`, `projectMilestone(id)` - Milestone operations
- `notifications()` - Notification queries

### 4. Auth Bypass Mechanism

#### 4.1 Overview

The ltui tool implements an authentication bypass mechanism designed for testing. It allows tests to run without real Linear API keys by using a mock client that simulates Linear's API behavior.

#### 4.2 Implementation

**Bypass Trigger:** `LTUI_TEST_CLIENT_MODULE` environment variable

**Client Factory Location:** `/Users/anichols/code/adn-claude-configs/tools/ltui/src/client.ts`

**Lines:** 11-20

```typescript
export function createLinearClient(resolved: ResolvedConfig): LinearClient {
  if (cachedClient) return cachedClient;
  const mockModule = process.env.LTUI_TEST_CLIENT_MODULE;
  if (mockModule) {
    const resolvedPath = path.resolve(mockModule);
    const factory = requireFn(resolvedPath);
    if (typeof factory.createMockLinearClient !== 'function') {
      throw new Error('mock_error Invalid LTUI_TEST_CLIENT_MODULE');
    }
    cachedClient = factory.createMockLinearClient(resolved);
    return cachedClient;
  }
  if (!resolved.apiKey) {
    throw new Error('auth_missing No API key available for Linear client');
  }
  cachedClient = new LinearClient({ apiKey: resolved.apiKey });
  return cachedClient;
}
```

#### 4.3 Mock Client Implementation

**Source File:** `/Users/anichols/code/adn-claude-configs/tools/ltui/src/test-utils/mockLinearClient.ts`

**Lines:** 469

**Compiled File:** `/Users/anichols/code/adn-claude-configs/tools/ltui/dist/test-utils/mockLinearClient.js`

**Factory Function:** Lines 100-103
```typescript
export function createMockLinearClient(_resolved: ResolvedConfig): any {
  const data = buildData();
  return new MockLinearClient(data);
}
```

**Mock Data Structure:** Lines 105-205
- Teams: Engineering team (ENG)
- Projects: Project Alpha (proj-1)
- Issues: Two sample issues (ENG-1, ENG-2)
- Labels: bug, backend
- Users: Alice (alice@example.com), Bob (bob@example.com)
- Documents: Design Doc (doc-1)
- Roadmaps: Roadmap 1
- Milestones: Milestone 1
- Notifications: Sample notification
- Workflow States: Todo, In Progress

**Mock Methods:** Lines 207-468
The `MockLinearClient` class implements all Linear SDK methods with in-memory data.

#### 4.4 Usage in Tests

**Example 1: CLI Regression Test**
**File:** `/Users/anichols/code/adn-claude-configs/tools/ltui/src/__tests__/cli-regression.test.ts`
**Lines:** 30-42

```typescript
function runCli(ctx: EnvContext, args: string[], extraEnv: Record<string, string> = {}): SpawnSyncReturns<string> {
  return spawnSync('node', [CLI_PATH, ...args], {
    cwd: ctx.workDir,
    encoding: 'utf-8',
    env: {
      ...process.env,
      LTUI_CONFIG_DIR: ctx.configDir,
      LINEAR_API_KEY: 'lin_api_test',  // Fake key, but mock bypasses validation
      LTUI_TEST_CLIENT_MODULE: MOCK_CLIENT,  // ← Auth bypass trigger
      ...extraEnv,
    },
  });
}
```

**Example 2: Test Isolation Setup**
**File:** `/Users/anichols/code/adn-claude-configs/tools/ltui/src/__tests__/cli-regression.test.ts`
**Lines:** 44-58

```typescript
function createContext(): EnvContext {
  const baseDir = mkdtempSync(path.join(os.tmpdir(), 'ltui-test-'));
  const configDir = path.join(baseDir, 'config');
  const workDir = path.join(baseDir, 'workspace');
  mkdirSync(configDir, { recursive: true });
  mkdirSync(workDir, { recursive: true });
  return { baseDir, configDir, workDir };
}
```

#### 4.5 Configuration Required

**No test configuration needed** - the mock client is standalone.

**Isolation Configuration:** Tests create temporary directories for isolation using `mkdtempSync()`.

### 5. Test Infrastructure

#### 5.1 ltui Test Configuration

**Package File:** `/Users/anichols/code/adn-claude-configs/tools/ltui/package.json`

**Test Runner:** Node.js builtin `node:test`

**Test Command:** `bun run build && node --test dist/**/*.test.js`

**Framework:** Native Node.js test runner with `assert/strict`

#### 5.2 Test Utilities

**Mock Client Module:** `/Users/anichols/code/adn-claude-configs/tools/ltui/src/test-utils/mockLinearClient.ts`

**Test Context Helpers:** `/Users/anichols/code/adn-claude-configs/tools/ltui/src/__tests__/cli-regression.test.ts`
- Line 44-58: `createContext()` - Creates isolated test directories
- Line 60-62: `cleanupContext()` - Cleans up test directories
- Line 30-42: `runCli()` - Runs CLI commands with test environment
- Line 64-66: `assertOk()` - Asserts command succeeded
- Line 68-70: `expectOutput()` - Asserts output contains expected text

#### 5.3 Installation Test Framework

**File:** `/Users/anichols/code/adn-claude-configs/test_install.sh`

**Custom Bash Test Framework:**
- Test assertion functions
- Color-coded output
- Test counting and reporting
- Exit code handling

### 6. UI Rendering Tests

**No UI rendering tests exist in this repository.**

The repository does not contain web application code or UI components. The only "rendering" tests are CLI output formatting tests.

#### 6.1 CLI Output Formatting Tests

**File:** `/Users/anichols/code/adn-claude-configs/tools/ltui/src/__tests__/output.test.ts`

**Lines:** 174

**Tests:**
- TSV (tab-separated values) output formatting
- Table formatting for terminal display
- JSON output formatting
- Pagination metadata

**Code Being Tested:** `/Users/anichols/code/adn-claude-configs/tools/ltui/src/format.ts`

**Lines:** 142

**Key Functions:**
- Line 38-61: `renderList()` - Renders CLI data in TSV, table, or JSON format
- Line 93-99: `renderTsv()` - Tab-separated value formatting
- Line 101-119: `renderTable()` - Table formatting for terminal display
- Line 121-130: `renderJson()` - JSON array formatting

### 7. Playwright References (Not Tests)

The repository contains Playwright references in configuration files, but these are for **MCP server configuration** (Model Context Protocol) to enable browser automation capabilities in AI agents, not actual test files:

**File:** `/Users/anichols/code/adn-claude-configs/claude/mcp-servers.json`
**Lines:** 3-5

**File:** `/Users/anichols/code/adn-claude-configs/claude/settings.local.json`
**Lines:** 23-30

**Purpose:** Configure Playwright as an MCP server tool for AI agents to use for browser automation.

## Code References

### Test Files
- `/Users/anichols/code/adn-claude-configs/tools/ltui/src/__tests__/cli-regression.test.ts:1-270` - CLI integration tests
- `/Users/anichols/code/adn-claude-configs/tools/ltui/src/__tests__/cli-args.test.ts:1-86` - CLI argument parsing tests
- `/Users/anichols/code/adn-claude-configs/tools/ltui/src/__tests__/output.test.ts:1-174` - CLI output formatting tests
- `/Users/anichols/code/adn-claude-configs/test_install.sh:1-523` - Installation script tests

### Auth Bypass
- `/Users/anichols/code/adn-claude-configs/tools/ltui/src/client.ts:9-26` - Client factory with bypass logic
- `/Users/anichols/code/adn-claude-configs/tools/ltui/src/test-utils/mockLinearClient.ts:1-469` - Mock client implementation
- `/Users/anichols/code/adn-claude-configs/tools/ltui/src/test-utils/mockLinearClient.ts:100-103` - Mock client factory
- `/Users/anichols/code/adn-claude-configs/tools/ltui/src/test-utils/mockLinearClient.ts:105-205` - Mock data structure
- `/Users/anichols/code/adn-claude-configs/tools/ltui/src/test-utils/mockLinearClient.ts:207-468` - Mock methods

### Test Infrastructure
- `/Users/anichols/code/adn-claude-configs/tools/ltui/package.json` - Test configuration
- `/Users/anichols/code/adn-claude-configs/tools/ltui/src/__tests__/cli-regression.test.ts:30-42` - runCli helper
- `/Users/anichols/code/adn-claude-configs/tools/ltui/src/__tests__/cli-regression.test.ts:44-58` - createContext helper
- `/Users/anichols/code/adn-claude-configs/tools/ltui/src/__tests__/cli-regression.test.ts:60-62` - cleanupContext helper

### Output Formatting
- `/Users/anichols/code/adn-claude-configs/tools/ltui/src/format.ts:1-142` - CLI output formatting functions
- `/Users/anichols/code/adn-claude-configs/tools/ltui/src/format.ts:38-61` - renderList function
- `/Users/anichols/code/adn-claude-configs/tools/ltui/src/format.ts:93-99` - renderTsv function
- `/Users/anichols/code/adn-claude-configs/tools/ltui/src/format.ts:101-119` - renderTable function
- `/Users/anichols/code/adn-claude-configs/tools/ltui/src/format.ts:121-130` - renderJson function

### Configuration
- `/Users/anichols/code/adn-claude-configs/claude/mcp-servers.json:3-5` - Playwright MCP server config
- `/Users/anichols/code/adn-claude-configs/claude/settings.local.json:23-30` - Playwright settings

## Architecture Documentation

### Test Architecture

**Repository Type:** Configuration repository for AI agents

**Test Types Present:**
1. **CLI Integration Tests** - Test ltui CLI tool commands end-to-end
2. **Installation Tests** - Validate configuration installation process
3. **Output Formatting Tests** - Validate CLI terminal output

**Test Frameworks:**
- Node.js builtin `node:test` for ltui tests
- Custom Bash test framework for installation tests

**Test Isolation:**
- Temporary directories created via `mkdtempSync()`
- Separate config directories per test
- Environment variable isolation

### Auth Bypass Architecture

**Mechanism:** Environment variable-driven mock client injection

**Flow:**
1. Test sets `LTUI_TEST_CLIENT_MODULE` environment variable
2. `createLinearClient()` checks for this variable
3. If present, loads mock client module
4. Mock client provides in-memory implementations of all Linear SDK methods
5. Tests run without real API calls or API keys

**Benefits:**
- Fast execution (no network calls)
- Deterministic results (hardcoded test data)
- Isolated (no external dependencies)
- No API key management needed

### Linear API Client Architecture

**Purpose:** Interact with Linear's API via the Linear SDK

**Client Creation:** Factory pattern with caching

**Bypass Integration:** Environment variable check before real client creation

**Mock Implementation:** In-memory data store with method implementations matching Linear SDK

## Related Documents

- `/Users/anichols/code/adn-claude-configs/AGENTS.md` - Agent catalog and fidelity rules
- `/Users/anichols/code/adn-claude-configs/README.md` - Repository overview (if exists)

## Open Questions

### Critical Finding

**The research question assumes the existence of:**
- Traditional e2e UI tests (Playwright/Cypress)
- Web API endpoints to test
- UI component rendering tests

**However, this repository contains none of these.** It is a configuration repository for AI agents, not a web application.

### Clarification Needed

1. **Is this the correct repository?** The user may have intended to research a different repository that contains a web application with e2e tests and API endpoints.

2. **If this is the correct repository, what is the goal?**
   - Are you looking to add API tests for the ltui tool's Linear API client?
   - Are you looking to add e2e tests for the installation process?
   - Are you looking to test something else entirely?

3. **What does "API contract tests" mean in this context?**
   - The ltui tool uses the Linear SDK, which is a third-party library
   - There are no custom API endpoints to test
   - The mock client already provides contract-like testing of Linear SDK usage

### Potential Research Directions

If the goal is to improve testing for this repository, possible areas to explore:

1. **Expand ltui CLI integration tests** - Add more test coverage for edge cases
2. **Add unit tests** - Test individual functions in isolation
3. **Add property-based tests** - Test format.ts functions with generated inputs
4. **Add performance tests** - Benchmark CLI command execution
5. **Add security tests** - Test auth bypass cannot be triggered in production

However, these are suggestions and should only be pursued if explicitly requested by the user.
