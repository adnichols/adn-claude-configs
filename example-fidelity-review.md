# Example Enhanced Fidelity Review Workflow

## Scenario
User runs: `/p:spec-to-tasks test-spec.md`

## Step 1: Draft Creation
```
✅ Draft task list saved to: /workspace/tasks/tasks-fidelity-test-spec-DRAFT.md
Running fidelity review...
```

User can now open both files:
- `/workspace/test-spec.md` (original specification)  
- `/workspace/tasks/tasks-fidelity-test-spec-DRAFT.md` (generated draft)

## Step 2: Fidelity Review Results

---

## ⚠️ Fidelity Review: ISSUES FOUND

**Files Reviewed:**
- **Specification:** `/workspace/test-spec.md`
- **Draft Task List:** `/workspace/tasks/tasks-fidelity-test-spec-DRAFT.md`

*You can open both files to review the context for these issues.*

### ✅ Validated Elements
- **Task Model Requirements**: Correctly represented in task 2.2 (id, title, completed fields)
- **Express Framework**: Properly specified in task 1.2
- **In-Memory Storage**: Accurately captured in task 2.1
- **UUID Generation**: Correctly included in task 2.3
- **Error Handling Requirements**: All three error types (404, 400, 500) covered in tasks 4.1-4.3
- **Basic Testing Requirements**: Smoke tests for each endpoint properly scoped in tasks 5.1-5.4

### ❌ Issues Requiring Decisions

**1. Missing Requirement: Response Format Specification**
**Specification** (line 15): "All responses use JSON format"
**Draft Task List** (Task 4.1-4.3): Error handling tasks don't specify JSON content-type
**Issue:** No explicit task ensures JSON response format for all endpoints

Options:
a) Add task: "4.4 Set JSON content-type headers and return proper HTTP status codes (200 for GET/PUT, 201 for POST, 204 for DELETE)"
b) This is implicitly covered by Express default JSON handling
c) Add minimal task: "4.4 Ensure all responses return JSON format"
d) This level of detail not needed in task list

**2. Ambiguous Requirement: PUT Endpoint Functionality**
**Specification** (API Endpoints section): "PUT /tasks/{id} - Updates task completion status"
**Draft Task List** (Task 3.3): "Implement PUT /tasks/{id} endpoint" (no specificity)
**Issue:** Ambiguous whether PUT updates only completion status or any task fields

Options:
a) Interpret as: "Updates only the 'completed' boolean field"
b) Interpret as: "Updates any task fields (title and/or completed)"
c) Split into two tasks: one for completion updates, one for general updates
d) Request clarification from specification author

**3. Potential Scope Addition: Package.json Dependencies**
**Specification** (Technical Requirements): "Use Node.js with Express framework"
**Draft Task List** (Task 1.2): "Install Express dependency only"
**Issue:** The word "only" may be too restrictive given testing requirements also specified

Options:
a) Keep as is - "only" means no unnecessary dependencies
b) Modify to: "Install Express and necessary test dependencies"
c) Add separate task for test dependencies installation
d) Remove "only" qualifier to allow necessary testing dependencies

**Please respond with your decisions in format: "1a, 2a, 3b"**

---

## Step 3: User Review and Decision

User opens both files to examine:
- `/workspace/test-spec.md` - sees original requirements
- `/workspace/tasks/tasks-fidelity-test-spec-DRAFT.md` - sees generated tasks

User responds: **"1c, 2a, 3b"**

## Step 4: Resolution and Final Save

System applies decisions:
- Issue 1c: Adds task to ensure JSON format
- Issue 2a: Clarifies PUT endpoint updates only completion status  
- Issue 3b: Modifies dependency task to include test dependencies

## ✅ Fidelity Review: VALIDATED (Second Pass)

All specification requirements are now accurately represented in the updated task list.

**Final Task List Saved:**
```
✅ Final task list saved to: /workspace/tasks/tasks-fidelity-test-spec.md
✅ Draft file archived: /workspace/tasks/tasks-fidelity-test-spec-DRAFT.md → .archived/
```

**Metadata Included:**
```yaml
fidelity_review:
  reviewed: true
  reviewer_agent: fidelity-reviewer
  issues_found: 3
  decisions_made:
    - issue: "Missing JSON response format specification"
      decision: "1c"
      resolution: "Added task 4.4 to ensure JSON format"
    - issue: "Ambiguous PUT endpoint functionality"
      decision: "2a"  
      resolution: "Clarified PUT updates only completion status"
    - issue: "Package dependencies scope"
      decision: "3b"
      resolution: "Modified to include test dependencies"
  review_iterations: 2
  final_validation: passed
  review_date: 2025-09-07T12:30:00Z
```