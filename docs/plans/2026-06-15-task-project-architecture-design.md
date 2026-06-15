# Task & Project Management Web App Architecture Design

## Purpose

This document defines a simple, maintainable architecture for a web application used to manage projects and tasks. The goal is to keep the system easy to build and understand while leaving room for growth.

## Design Goals

- Keep the codebase easy to navigate for a small team.
- Separate business logic from UI concerns.
- Avoid unnecessary complexity such as microservices.
- Support future expansion through clear module boundaries.
- Focus on the core workflow: projects, tasks, and basic user access.

## Recommended Approach

Use a **modular monolith** architecture.

This means the app remains a single codebase and deployment unit, but the code is organized into focused modules with clear responsibilities.

### Why this approach

- Faster to build than a fully split frontend/backend system.
- Cleaner than a flat structure where everything is mixed together.
- Easier to test and maintain than a large unstructured app.
- Good fit for a task/project management product that is intentionally simple.

## High-Level Structure

The application should be split into these layers:

1. **Presentation layer**
   - Pages, views, forms, and interactive UI components.
   - Handles user interactions and display state.

2. **Application layer**
   - Orchestrates use cases such as creating tasks, updating status, and assigning users.
   - Coordinates validation, permissions, and data access.

3. **Domain layer**
   - Contains core business rules and entities.
   - Defines concepts like Project, Task, User, Priority, and Status.

4. **Infrastructure layer**
   - Handles persistence, API calls, auth integration, and logging.
   - Keeps external dependencies isolated from business logic.

## Core Modules

### `auth`

Responsible for login, logout, session handling, and basic role checks.

### `projects`

Responsible for project CRUD, project status, and project-level views.

### `tasks`

Responsible for task CRUD, status transitions, priority, due dates, and assignment.

### `users`

Responsible for user profiles, roles, and membership in projects.

### `dashboard`

Responsible for summary views such as active tasks, overdue items, and project counts.

### `shared`

Contains reusable UI components, helpers, validation schemas, types, and constants.

## Suggested Data Model

### User

- `id`
- `name`
- `email`
- `role`
- `createdAt`
- `updatedAt`

### Project

- `id`
- `name`
- `description`
- `status`
- `ownerId`
- `memberIds`
- `createdAt`
- `updatedAt`

### Task

- `id`
- `title`
- `description`
- `status`
- `priority`
- `assigneeId`
- `projectId`
- `dueDate`
- `createdAt`
- `updatedAt`

### Optional later additions

- `Comment`
- `ActivityLog`
- `Notification`

These are intentionally not part of the MVP.

## Data Flow

1. User interacts with the UI.
2. The UI calls a use case in the application layer.
3. The use case validates input and checks business rules.
4. The use case uses repositories or API adapters to load/save data.
5. The result returns to the UI.
6. The UI updates the screen state.

This flow keeps the UI thin and prevents business rules from leaking into components.

## Error Handling Strategy

- Use inline validation for form input errors.
- Use application-layer validation for business rule violations.
- Use consistent API error responses for server-side failures.
- Show user-friendly messages in the UI.
- Log technical errors in the infrastructure layer.

## Testing Strategy

### Unit tests

Cover domain rules and core use cases.

### Integration tests

Cover module-to-module behavior and data access boundaries.

### UI tests

Cover critical flows such as:

- creating a project
- creating a task
- changing task status
- filtering tasks by status or project

The test strategy should focus on business value, not exhaustive coverage.

## MVP Scope

The first version should include:

- login
- project CRUD
- task CRUD
- task filtering by project and status
- a simple dashboard

The first version should not include:

- microservices
- real-time collaboration
- Gantt charts
- complex notifications
- workflow automation

## Folder Organization Example

A simple structure could look like this:

- `src/modules/auth`
- `src/modules/projects`
- `src/modules/tasks`
- `src/modules/users`
- `src/modules/dashboard`
- `src/shared`

Inside each module, keep related files together, for example:

- UI components
- hooks or state logic
- use cases
- data access adapters
- types and validation schemas

## Implementation Principles

- One module should have one clear purpose.
- Keep dependencies pointing inward toward domain logic.
- Prefer explicit interfaces between modules.
- Keep components small and focused.
- Avoid adding features before the MVP proves the need.

## Conclusion

The modular monolith approach gives the best balance for this project: simple to start, structured enough to stay maintainable, and flexible enough to expand later without re-architecting everything.
