---
version: 1
status: DRAFT
fidelity_mode: strict
source_spec: /workspace/tasks/uibaseline/consolidated-visual-testing-spec.md
agents:
  developer: developer-fidelity
  reviewer: quality-reviewer-fidelity
scope_preservation: true
additions_allowed: none
complexity_override: disabled
specification_metadata:
  source_file: /workspace/tasks/uibaseline/consolidated-visual-testing-spec.md
  conversion_date: 2025-09-07
  fidelity_level: absolute
  scope_changes: none
fidelity_review:
  reviewed: false
  pending_review: true
  draft_created: 2025-09-07
---

# ⚠️ DRAFT - Pending Fidelity Review

# Consolidated Visual Testing Tool - Fidelity Implementation Tasks (DRAFT)

**⚠️ This is a DRAFT task list awaiting fidelity review against the original specification.**

**Specification Source:** /workspace/tasks/uibaseline/consolidated-visual-testing-spec.md
**Review Status:** Pending
**Next Step:** Fidelity review will compare this draft against the specification

## 🎯 Implementation Authority

**Source Specification:** /workspace/tasks/uibaseline/consolidated-visual-testing-spec.md
**Conversion Mode:** Full Fidelity Preservation
**Implementation Scope:** Exactly as specified, no additions or modifications

### Specification Summary
A pragmatic Playwright-based visual regression testing tool that delivers immediate value by focusing on core visual regression detection. Combines technical foundation with realistic implementation approach, optimized for headless environments and CI/CD integration.

### Implementation Boundaries  
**Included:** 
- Single Test File using Playwright's built-in `toHaveScreenshot()` API
- Git-Ignored Storage Structure in test-results/
- Three essential commands (test:visual, test:visual:update, test:visual:report)
- Desktop viewport only (1920x1080)
- Light mode only
- Single state per view (populated/default state)
- All primary application screens (Servers, Status, Configuration)
- Headless environment support
- Standard Playwright HTML reports

**Excluded:** 
- Multi-viewport testing (mobile/tablet support)
- Multi-state capture (empty/loading/error states per view)
- Custom HTML reports with thumbnail galleries
- Granular baseline updates (screen-specific management)
- Consistency Analyzer (cross-screen pattern detection)
- Advanced approval systems

**Testing Level:** As specified - visual regression testing with >95% accuracy, complete capture <5 minutes, comparison <100ms
**Security Level:** As specified - no screenshots in version control, proper file permissions
**Documentation Level:** As specified - workflow documentation in README section

## 🗂️ Implementation Files

Based on specification analysis, these files will need creation/modification:
- `tauri-app/playwright.config.ts` - Configure visual testing project
- `tauri-app/tests/ui/visual/visual-regression.spec.ts` - Main test file
- `tauri-app/tests/ui/visual/screenshot-helper.ts` - Navigation and capture utilities
- `tauri-app/package.json` - Add npm scripts
- `tauri-app/.gitignore` - Verify test-results/ directories are ignored
- `tauri-app/README.md` - Document visual testing workflow (section addition)

### Development Notes
- Follow specification requirements exactly as written
- Use only Playwright's built-in `toHaveScreenshot()` API
- Do not add testing beyond visual regression for specified screens
- Do not add security measures beyond git-ignored storage
- Do not expand scope to multi-viewport or multi-theme
- Question any ambiguity rather than assuming

## ⚙️ Implementation Phases

### Phase 1: Alpha Version (Week 1)
**Objective:** Working visual regression suite for primary viewport
**Timeline:** 1 week delivery for immediate value

**Specification Requirements:**
- Configure `playwright.config.ts` for visual testing
- Create core test file (`tests/ui/visual/visual-regression.spec.ts`)
- Add screenshot helper utilities (`screenshot-helper.ts`)
- Define npm scripts
- Generate initial baseline and documentation

**Tasks:**
- [ ] 1.0 Configure Playwright for Visual Testing
  - [ ] 1.1 Configure `playwright.config.ts` with visual testing project
  - [ ] 1.2 Set up `toHaveScreenshot` configuration (threshold: 0.2, maxDiffPixels: 1000)
  - [ ] 1.3 Configure headless mode and viewport settings (1920x1080)
  - [ ] 1.4 Set up test results directory structure in git-ignored locations
  - [ ] 1.5 Configure snapshotPathTemplate for test-results/visual-* directories

- [ ] 2.0 Create Core Visual Regression Test
  - [ ] 2.1 Create `tests/ui/visual/visual-regression.spec.ts` with test structure
  - [ ] 2.2 Implement Servers view screenshot test
  - [ ] 2.3 Implement Status view screenshot test  
  - [ ] 2.4 Implement Configuration view screenshot test
  - [ ] 2.5 Add proper wait conditions and page state verification for each test
  - [ ] 2.6 Configure dynamic content masking for timestamps and loading indicators

- [ ] 3.0 Add Screenshot Helper Utilities
  - [ ] 3.1 Create `screenshot-helper.ts` with common navigation patterns
  - [ ] 3.2 Implement `captureServersView()` function with robust wait conditions
  - [ ] 3.3 Implement `captureStatusView()` function with status-specific waits
  - [ ] 3.4 Implement `captureConfigurationView()` function with form loading waits
  - [ ] 3.5 Implement `waitForAppStable()` utility function
  - [ ] 3.6 Add viewport and theme utilities for desktop/light mode

- [ ] 4.0 Define NPM Scripts
  - [ ] 4.1 Add `test:visual` script to run visual regression tests
  - [ ] 4.2 Add `test:visual:update` script to update baseline screenshots
  - [ ] 4.3 Add `test:visual:report` script to show Playwright HTML reports
  - [ ] 4.4 Verify scripts use `--project=visual-regression` flag

- [ ] 5.0 Generate Initial Baseline and Documentation
  - [ ] 5.1 Capture initial baseline screenshots for desktop viewport
  - [ ] 5.2 Verify git-ignored storage working correctly (test-results/ not in git)
  - [ ] 5.3 Document workflow in README section
  - [ ] 5.4 Verify directory structure matches specification requirements
  - [ ] 5.5 Test baseline update workflow functionality

## 📋 Specification Context

### Technical Configuration Requirements

**Playwright Configuration (`playwright.config.ts`):**
```typescript
// Based on specification requirements
export default defineConfig({
  timeout: 30 * 1000,  // Short timeout for visual regression tests
  expect: {
    timeout: 5000,
    toHaveScreenshot: {
      threshold: 0.2,
      maxDiffPixels: 1000,
      animations: 'disabled',
      caret: 'hide',
    }
  },
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
  reporter: 'html',
  use: {
    headless: process.env.CI ? true : false,
    ignoreHTTPSErrors: true,
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [{
    name: 'visual-regression',
    testDir: './tests/ui/visual/',
    use: {
      ...devices['Desktop Chrome'],
      viewport: { width: 1920, height: 1080 },
    },
    snapshotPathTemplate: '{testFileDir}/../../test-results/visual-{arg}{ext}',
  }],
});
```

**Directory Structure:**
```
tauri-app/
├── test-results/              # Already in .gitignore
│   ├── visual-baseline/       # Approved baseline screenshots
│   ├── visual-current/        # Latest test run screenshots
│   └── visual-diff/           # Difference images
├── playwright-report/         # Already in .gitignore
│   └── visual-report/         # Standard Playwright HTML reports
└── tests/ui/visual/           # Test code (in git)
    ├── visual-regression.spec.ts
    └── screenshot-helper.ts
```

### Implementation Patterns

**Test Structure Pattern:**
- One test per view (Servers, Status, Configuration)
- Explicit screenshot naming (`servers-view.png`, `status-view.png`, `configuration-view.png`)
- Robust wait strategies using `waitForLoadState('networkidle')`
- Role-based locators preferred over CSS selectors
- Helper abstraction for navigation and waiting logic

**Stability Patterns:**
- Dynamic content masking for timestamps, loading indicators, real-time counters
- Animation and movement control via global config
- Robust wait conditions for content stability before screenshots
- Network idle waiting and element-specific validation

### Headless Environment Requirements

**Docker/CI Compatibility:**
- Playwright headless mode runs by default in CI environments
- No display dependencies (no X11 or display server required)
- Consistent rendering across containers
- Compatible with GitHub Actions, GitLab CI, Jenkins
- Automatic headless detection in CI environments
- Screenshot artifacts can be uploaded for review

## 🚨 Implementation Requirements

### Fidelity Requirements (MANDATORY)
- Implement ONLY what's explicitly specified
- Use Playwright's built-in `toHaveScreenshot()` API (no custom comparison engine)
- Single viewport only (Desktop 1920x1080)
- Light mode only
- Single state per view (populated/default state)
- Do not add multi-viewport, multi-theme, or multi-state capabilities
- Do not add advanced features marked as "deferred" or "future phases"
- Question ambiguities rather than making assumptions
- Preserve all specification constraints and limitations

### Success Criteria (From Specification)
- ✅ Capture all primary application screens (Servers, Status, Configuration)
- ✅ Detect visual regressions with >95% accuracy  
- ✅ Generate reports in <30 seconds
- ✅ Zero screenshots committed to git repository
- ✅ Full headless/Docker compatibility
- ✅ Working baseline update workflow
- ✅ Complete capture <5 minutes, comparison <100ms

### Testing Requirements (From Specification)
- Visual regression testing using Playwright's `toHaveScreenshot()`
- Standard Playwright HTML report generation
- Headless mode compatibility for CI environments
- Three essential commands: test:visual, test:visual:update, test:visual:report

### Security Requirements (From Specification)
- All screenshots in git-ignored `test-results/` directory
- No screenshots committed to version control
- Proper file permissions and access controls
- No sensitive data exposure in visual captures

## ✅ Validation Checklist

- [ ] Implementation matches specification exactly
- [ ] No scope additions or "improvements" made
- [ ] All specification constraints preserved
- [ ] Success criteria from specification met
- [ ] No testing beyond what specification requires
- [ ] No security measures beyond specification requirements
- [ ] Uses only Playwright built-in APIs as specified
- [ ] Single viewport/theme/state as specified
- [ ] Git-ignored storage structure implemented correctly
- [ ] All three npm scripts implemented as specified

## 📊 Completion Criteria

**Phase 1 (Alpha Version) Complete When:**
- Visual regression test suite runs successfully for all three primary views
- Baseline screenshots can be captured and updated
- All screenshots stored in git-ignored directories
- Standard Playwright HTML reports generate correctly
- All npm scripts function as specified
- Headless mode works in CI environments
- Performance targets met (capture <5 minutes, comparison <100ms)
- Documentation added to README as specified

**Success Indicators:**
- 100% application screen coverage (Servers, Status, Configuration views)
- >95% visual difference detection accuracy
- Zero screenshots in git repository
- Actionable reports generated in <30 seconds
- Complete Docker/CI compatibility