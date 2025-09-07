---
version: 1
fidelity_mode: strict
source_spec: /workspace/test-spec.md
agents:
  developer: developer-fidelity
  reviewer: quality-reviewer-fidelity
scope_preservation: true
additions_allowed: none
complexity_override: disabled
specification_metadata:
  source_file: /workspace/test-spec.md
  conversion_date: 2025-09-07T11:15:00Z
  fidelity_level: absolute
  scope_changes: none
---

# Simple Task Manager API - Fidelity Implementation Tasks

## 🎯 Implementation Authority

**Source Specification:** /workspace/test-spec.md
**Conversion Mode:** Full Fidelity Preservation
**Implementation Scope:** Exactly as specified, no additions or modifications

### Specification Summary
Create a basic REST API for task management with in-memory storage using Node.js and Express.

### Implementation Boundaries  
**Included:** 4 REST endpoints, in-memory storage, basic smoke tests, JSON responses, error handling for 404/400/500
**Excluded:** Authentication, database persistence, comprehensive validation, rate limiting, security headers, API docs, logging, monitoring, Docker
**Testing Level:** Basic smoke tests for each endpoint, happy path scenarios only
**Security Level:** None specified (explicitly excluded from scope)
**Documentation Level:** None specified (explicitly excluded from scope)

## 🗂️ Implementation Files

Based on specification analysis:
- `app.js` - Main Express application with task endpoints
- `package.json` - Node.js dependencies (express)
- `test/api.test.js` - Basic smoke tests for endpoints

### Development Notes
- Use Express framework as specified
- Store tasks in JavaScript array as specified
- Use crypto.randomUUID() as specified
- Implement ONLY the 4 endpoints specified
- Add ONLY the basic smoke tests specified
- Do NOT add authentication (explicitly excluded)
- Do NOT add database (explicitly excluded)
- Do NOT add comprehensive validation (explicitly excluded)

## ⚙️ Implementation Phases

### Phase 1: Core API Implementation
**Objective:** Implement the 4 REST endpoints with in-memory storage
**Timeline:** Single phase as specified

**Specification Requirements:**
- Task model: id (string), title (string), completed (boolean)
- In-memory storage using JavaScript array
- GET /tasks endpoint returning array of all tasks
- POST /tasks endpoint creating new task with title
- PUT /tasks/{id} endpoint updating completion status
- DELETE /tasks/{id} endpoint removing task
- JSON response format for all endpoints
- UUID generation using crypto.randomUUID()

**Tasks:**
- [ ] 1.0 Setup Express Application
  - [ ] 1.1 Initialize Node.js project with package.json
  - [ ] 1.2 Install Express dependency only
  - [ ] 1.3 Create basic Express app structure
- [ ] 2.0 Implement Task Model and Storage
  - [ ] 2.1 Create in-memory array for task storage
  - [ ] 2.2 Define task structure (id, title, completed)
  - [ ] 2.3 Implement UUID generation with crypto.randomUUID()
- [ ] 3.0 Implement REST Endpoints
  - [ ] 3.1 Implement GET /tasks endpoint
  - [ ] 3.2 Implement POST /tasks endpoint
  - [ ] 3.3 Implement PUT /tasks/{id} endpoint
  - [ ] 3.4 Implement DELETE /tasks/{id} endpoint
- [ ] 4.0 Implement Error Handling
  - [ ] 4.1 Add 404 responses for non-existent tasks
  - [ ] 4.2 Add 400 responses for invalid request bodies
  - [ ] 4.3 Add 500 responses for server errors
- [ ] 5.0 Implement Basic Testing
  - [ ] 5.1 Create basic smoke test for GET /tasks
  - [ ] 5.2 Create basic smoke test for POST /tasks
  - [ ] 5.3 Create basic smoke test for PUT /tasks/{id}
  - [ ] 5.4 Create basic smoke test for DELETE /tasks/{id}
  - [ ] 5.5 Test happy path scenarios only as specified

## 📋 Specification Context

### Task Model
- Task structure: `{ id: string, title: string, completed: boolean }`
- Storage: JavaScript array in memory (no database)
- ID generation: `crypto.randomUUID()`

### API Endpoints Specification
1. **GET /tasks** - Returns array of all tasks
2. **POST /tasks** - Creates new task, requires title in request body
3. **PUT /tasks/{id}** - Updates task completion status
4. **DELETE /tasks/{id}** - Deletes specified task

### Technical Stack Requirements
- Node.js runtime
- Express framework
- Built-in crypto module for UUID generation
- Built-in Node.js test runner for testing

## 🚨 Implementation Requirements

### Fidelity Requirements (MANDATORY)
- Implement ONLY the 4 endpoints specified
- Use ONLY in-memory storage as specified
- Add ONLY basic smoke tests as specified
- Do NOT add authentication (explicitly excluded)
- Do NOT add database persistence (explicitly excluded)
- Do NOT add comprehensive validation (explicitly excluded)
- Do NOT add security headers (explicitly excluded)
- Do NOT add API documentation (explicitly excluded)
- Do NOT add logging or monitoring (explicitly excluded)

### Success Criteria (From Specification)
- All 4 endpoints working correctly
- Basic tests pass
- API returns proper JSON responses
- HTTP status codes are correct (200, 400, 404, 500)

### Testing Requirements (Exact Specification)
- Basic smoke test for each endpoint
- Test happy path scenarios only
- Use built-in Node.js test runner
- NO integration tests beyond basic smoke tests
- NO comprehensive test coverage requirements

### Error Handling Requirements (Exact Specification)
- Return 404 for non-existent tasks
- Return 400 for invalid request bodies  
- Return 500 for server errors
- NO additional error handling beyond these three

## ✅ Validation Checklist

- [ ] Implementation matches specification exactly
- [ ] Only 4 endpoints implemented (no additional routes)
- [ ] In-memory storage only (no database code)
- [ ] Basic smoke tests only (no comprehensive testing)
- [ ] No authentication code (explicitly excluded)
- [ ] No validation beyond basic existence checks
- [ ] No additional security measures
- [ ] Success criteria from specification met

## 📊 Completion Criteria

**From Specification:**
- All 4 endpoints working correctly
- Basic tests pass
- API returns proper JSON responses
- HTTP status codes are correct

**Fidelity Validation:**
- No features added beyond specification
- No security added beyond specification
- No tests added beyond specification requirements
- All specification requirements implemented exactly