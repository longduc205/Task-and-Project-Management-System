# Task Studio — Technical Documentation

## 1. Technology Stack

| Layer           | Technology      | Version    | Purpose                                 |
|-----------------|-----------------|------------|-----------------------------------------|
| Frontend        | React           | 19.1.0     | SPA UI framework                        |
| Build tool      | Vite            | 7.1.2      | Fast dev server + bundler               |
| Language        | TypeScript      | 5.9.2      | Compile-time type safety                |
| Routing         | React Router    | 7.9.1      | SPA client-side routing                 |
| Backend         | JSON Server     | 1.0.0-beta | REST API mock                           |
| Database        | db.json         | —          | Local JSON file persistence             |
| Testing         | Vitest          | 3.2.4      | Unit test runner                        |
| Charts          | Recharts        | 3.8.1      | Dashboard data visualization            |
| Icons           | Lucide React    | 1.18.0     | Icon library                            |
| Package manager | npm             | —          | Dependency management                    |

## 2. Architecture Overview

Task Studio is a single-page application (SPA) with a split frontend/backend architecture:

```
Browser (React SPA, port 5173)
    │
    │ HTTP/REST (fetch API)
    ▼
JSON Server (port 3001)
    │
    ▼
db.json (local file — CRUD persistence)
```

The frontend communicates with the JSON Server via standard REST calls using `fetch`. No custom backend server is required.

### Directory Structure

```
src/
├── modules/
│   ├── auth/
│   │   ├── LoginPage.tsx      # Login form
│   │   └── AuthInfoView.tsx   # Current user session display
│   ├── dashboard/
│   │   └── (DashboardView rendered in App.tsx)
│   ├── projects/
│   │   ├── ProjectForm.tsx    # Create/edit project form
│   │   └── ProjectList.tsx    # Project list table
│   ├── tasks/
│   │   ├── TaskForm.tsx       # Create/edit task form
│   │   └── TaskList.tsx       # Task list table
│   └── users/
│       └── UserList.tsx       # User list display
├── shared/
│   ├── api.ts                 # All REST API calls (fetch wrappers)
│   ├── types.ts               # TypeScript type definitions
│   ├── validation.ts          # Form validation helpers
│   ├── AuthContext.tsx        # React context for auth state (sessionStorage)
│   └── index.ts               # Barrel exports
├── App.tsx                    # Router + main layout + all view components
└── main.tsx                   # React entry point
```

### Key Design Decisions

- **Single-file App.tsx** — All view components (`DashboardView`, `BoardView`, `ProjectsView`, `TasksView`) are defined in `App.tsx` for simplicity. In a larger codebase these would be split into `src/modules/*`.
- **Centralized state in App** — Task Studio uses a single top-level `App` component that owns all state (`tasks`, `projects`, `columns`, `activities`). No external state library is used.
- **Optimistic UI updates** — Drag-and-drop and form submissions update local React state immediately, then fire the API call in the background.

## 3. API Reference

**Base URL:** `http://localhost:3001`

### Projects

| Method | Endpoint         | Request Body                                                    | Response  |
|--------|------------------|-----------------------------------------------------------------|-----------|
| GET    | `/projects`      | —                                                               | `Project[]` |
| POST   | `/projects`      | `{ name, status, taskCount, description? }`                    | `Project`  |
| PATCH  | `/projects/:id` | `Partial<Project>`                                              | `Project`  |
| DELETE | `/projects/:id`  | —                                                               | void      |

### Tasks

| Method | Endpoint       | Request Body                                                                        | Response |
|--------|----------------|-------------------------------------------------------------------------------------|----------|
| GET    | `/tasks`       | —                                                                                   | `Task[]` |
| POST   | `/tasks`       | `{ title, status, projectId, projectName, dueDate, assigneeId? }`                  | `Task`   |
| PATCH  | `/tasks/:id`   | `Partial<Task>`                                                                    | `Task`   |
| DELETE | `/tasks/:id`   | —                                                                                   | void     |

### Kanban Columns

| Method | Endpoint      | Request Body           | Response        |
|--------|---------------|-----------------------|-----------------|
| GET    | `/columns`    | —                     | `KanbanColumn[]` |
| POST   | `/columns`    | `{ id, title }`      | `KanbanColumn`  |

### Users

| Method | Endpoint             | Notes                                  |
|--------|----------------------|----------------------------------------|
| GET    | `/users`             | Returns all registered users           |
| POST   | `/users?email=...`   | Login lookup — returns matching users  |

### Activities

| Method | Endpoint        | Response        |
|--------|-----------------|-----------------|
| GET    | `/activities`   | `Activity[]`    |

### Authentication Flow

`loginUser(email, password)` in `src/shared/api.ts`:

1. `GET /users?email=<email>` — fetches all users matching the email
2. Compares the plain-text password client-side
3. Strips the `password` field before returning the user object
4. The caller stores the result in `sessionStorage` via `AuthContext`

## 4. Type Definitions

All types are defined in `src/shared/types.ts`.

```typescript
// src/shared/types.ts

export type TaskStatus = string;
// Note: actual values used in the app are: 'todo' | 'in_progress' | 'done'

export type ProjectStatus = 'active' | 'paused' | 'archived';

export type UserRole = 'admin' | 'member' | 'viewer';

export interface Task {
  id: string;
  title: string;
  status: TaskStatus;
  projectId: string;
  projectName: string;
  dueDate: string;
  description?: string;
  assigneeId?: string;
}

export interface Project {
  id: string;
  name: string;
  status: ProjectStatus;
  taskCount: number;
  description?: string;
  createdAt?: string;
}

export interface User {
  id: string;
  name: string;
  email: string;
  role: UserRole;
  avatarColor?: string;
  password?: string; // Present in db.json; stripped before session storage
}

export interface Activity {
  id: string;
  userId: string;
  user: string;
  action: string;
  target: string;
  time: string;
  type: 'comment' | 'status' | 'create';
}

export interface KanbanColumn {
  id: string;
  title: string;
}
```

### Validation Helpers (`src/shared/validation.ts`)

```typescript
isTaskStatus(value: string): value is TaskStatus
isProjectStatus(value: string): value is ProjectStatus
isUserRole(value: string): value is UserRole
validateProjectName(name: string): boolean
validateTaskTitle(title: string): boolean
```

## 5. Running the Application

### Development

```bash
# Install dependencies
npm install

# Start JSON Server mock API (port 3001)
npm run api

# Start Vite dev server (port 5173) — in a new terminal
npm run dev

# Or start both simultaneously
npm run dev:all
```

### Production Build

```bash
npm run build    # outputs to dist/
npm run preview  # preview production build locally on port 4173
```

### Running Tests

```bash
npm test         # runs Vitest in watch mode
npm test -- --run  # runs Vitest once (CI mode)
```

### Linting

```bash
npm run lint     # ESLint with TypeScript and React Hooks support
```

## 6. Limitations & Scope Boundaries

The following are **intentionally documented limitations** — not bugs:

| #  | Limitation                     | Impact                                              | Mitigation                                              |
|----|--------------------------------|-----------------------------------------------------|---------------------------------------------------------|
| 1  | Simulated API environment      | JSON Server is not a production backend             | Suitable for prototype/demo; documented honestly        |
| 2  | Mock authentication             | No real passwords, no JWT, plain-text in `db.json`   | `sessionStorage` stores role only; documented honestly  |
| 3  | No real-time updates           | Page must be manually refreshed after changes        | Standard SPA behavior; all views update on next load    |
| 4  | Local-only data                | No cloud sync, no multi-user concurrent access     | Single-user demo environment; `db.json` is file-based   |
| 5  | Role changes not protected     | Any logged-in user can change roles via Auth view   | Password-gated role management is a future improvement  |

## 7. Future Improvements

| #  | Improvement                           | Priority | Effort |
|----|---------------------------------------|----------|--------|
| 1  | Automated unit + integration tests (Vitest + React Testing Library) with CI/CD | High | Medium |
| 2  | Real-time updates via WebSocket        | Medium   | High   |
| 3  | Production authentication (OAuth2/JWT) | High     | High   |
| 4  | Cloud database (PostgreSQL / Firebase)| Medium   | High   |
| 5  | Production deployment pipeline        | Medium   | Medium |
| 6  | Password-protected role management     | Medium   | Low    |
| 7  | Keyboard shortcuts for power users    | Low      | Low    |

## 8. Testing

Unit tests are located in `tests/unit/` (if present) and run via Vitest:

```bash
npm test
```

Integration test checklist: `tests/integration/CHECKLIST.md` (if present)
UAT checklist: `tests/uat/UAT_CHECKLIST.md` (if present)

## 9. Configuration Notes

| Item                      | Value / Location                                      |
|---------------------------|-------------------------------------------------------|
| API base URL              | `http://localhost:3001` (`src/shared/api.ts`)         |
| Auth storage              | `sessionStorage`, key: `task-studio-session`          |
| db.json location          | Project root (must exist for JSON Server to start)    |
| JSON Server port          | `3001` (`package.json` + `src/shared/api.ts`)         |
| Vite dev server port      | `5173` (default)                                     |
| Vite preview server port  | `4173`                                                |

### Environment Variables

No environment variables are currently used. All configuration is hardcoded in `src/shared/api.ts` and `package.json`.

## 10. Security Notes

> **For course project prototype only — not acceptable for production.**

- Passwords are stored in plain text in `db.json` — this is intentional for prototype simplicity
- Client-side password comparison in `loginUser()` (`src/shared/api.ts`)
- No CSRF protection (no server-side sessions)
- No rate limiting
- No input sanitization on the API layer (client-side validation only)
- `sessionStorage` is used instead of `HttpOnly` cookies — vulnerable to XSS
- A `TODO` security comment is present in `src/shared/api.ts` and `src/shared/AuthContext.tsx` flagging these issues

These are acceptable for a course project prototype demonstration. A production deployment would require a real backend with bcrypt/Argon2 password hashing, JWT or HttpOnly cookie sessions, HTTPS, and input validation.
