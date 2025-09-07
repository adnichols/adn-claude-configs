# Simple Task Manager API - Specification

## Overview

Create a basic REST API for task management with the following exact requirements.

## Functional Requirements

### 1. Task Model
- Task has: id (string), title (string), completed (boolean)
- Tasks are stored in memory (no database required)

### 2. API Endpoints
- GET /tasks - Returns array of all tasks
- POST /tasks - Creates new task, requires title in body
- PUT /tasks/{id} - Updates task completion status
- DELETE /tasks/{id} - Deletes task

### 3. Response Format
- All responses use JSON format
- Successful operations return appropriate HTTP status codes
- Error responses include error message

## Technical Requirements

### Implementation
- Use Node.js with Express framework
- Store tasks in memory using JavaScript array
- Generate UUIDs for task IDs using crypto.randomUUID()

### Testing Requirements
- Basic smoke test for each endpoint
- Test happy path scenarios only
- Use built-in Node.js test runner

### Error Handling
- Return 404 for non-existent tasks
- Return 400 for invalid request bodies
- Return 500 for server errors

## Success Criteria

- All 4 endpoints working correctly
- Basic tests pass
- API returns proper JSON responses
- HTTP status codes are correct

## Out of Scope

- Authentication or authorization
- Database persistence
- Input validation beyond basic existence checks
- Rate limiting or security headers
- API documentation
- Logging or monitoring
- Docker or deployment configuration