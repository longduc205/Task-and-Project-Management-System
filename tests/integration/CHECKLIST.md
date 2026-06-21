# WBS 1.5.2 Integration Test Checklist — Task Studio

**Project:** Task Studio — IT Project Management System
**WBS Reference:** 1.5.2 — Integration Tests
**Estimated Effort:** 25 hours
**Budget:** 1,250,000 VND

---

## Session Information

| Field | Details |
|---|---|
| **Date** | _________________________ |
| **Operator** | _________________________ |
| **Environment** | `http://localhost:5173` + `http://localhost:3001` |
| **API Baseline (db.json)** | Hash/Snapshot: _________________________ |

---

## 1. Data Loading

| # | Test Item | Pass | Fail | WBS Ref | Notes |
|---|---|---|---|---|---|
| 1.1 | Dashboard loads and displays correct project count from `db.json` | [ ] | [ ] | 1.5.2 | |
| 1.2 | Projects view lists all projects returned by `GET /projects` | [ ] | [ ] | 1.5.2 | |
| 1.3 | Tasks view lists all tasks returned by `GET /tasks` | [ ] | [ ] | 1.5.2 | |
| 1.4 | Users view lists all users from `GET /users` | [ ] | [ ] | 1.5.2 | |
| 1.5 | Activity feed loads recent entries from `GET /activities` | [ ] | [ ] | 1.5.2 | |
| 1.6 | Dashboard charts and metrics render without JS errors | [ ] | [ ] | 1.5.2 | |

---

## 2. Task CRUD

| # | Test Item | Pass | Fail | WBS Ref | Notes |
|---|---|---|---|---|---|
| 2.1 | Create task via form → new task appears in task list immediately | [ ] | [ ] | 1.5.2 | |
| 2.2 | Create task → `POST /tasks` recorded in `db.json` | [ ] | [ ] | 1.5.2 | |
| 2.3 | Update task title → change persists after browser page refresh | [ ] | [ ] | 1.5.2 | |
| 2.4 | Update task status → `PATCH /tasks/:id` reflected in `db.json` | [ ] | [ ] | 1.5.2 | |
| 2.5 | Delete task → removed from task list UI | [ ] | [ ] | 1.5.2 | |
| 2.6 | Delete task → `DELETE /tasks/:id` confirmed in `db.json` | [ ] | [ ] | 1.5.2 | |
| 2.7 | Create task with empty title → form validation prevents submission | [ ] | [ ] | 1.5.2 | |
| 2.8 | Assign task to user → `assigneeId` stored correctly | [ ] | [ ] | 1.5.2 | |

---

## 3. Kanban Board

| # | Test Item | Pass | Fail | WBS Ref | Notes |
|---|---|---|---|---|---|
| 3.1 | Kanban board renders all three columns: To Do, In Progress, Done | [ ] | [ ] | 1.5.2 | |
| 3.2 | Tasks appear in correct column matching their `status` field | [ ] | [ ] | 1.5.2 | |
| 3.3 | Drag task from "To Do" to "In Progress" → `PATCH /tasks/:id` with `status: "in_progress"` | [ ] | [ ] | 1.5.2 | |
| 3.4 | Moving task between columns → new status persisted in `db.json` after refresh | [ ] | [ ] | 1.5.2 | |
| 3.5 | Moving task to "Done" → task appears in Done column after reload | [ ] | [ ] | 1.5.2 | |
| 3.6 | Kanban board loads without duplicate columns or missing tasks | [ ] | [ ] | 1.5.2 | |

---

## 4. Project CRUD

| # | Test Item | Pass | Fail | WBS Ref | Notes |
|---|---|---|---|---|---|
| 4.1 | Create project via form → new project appears in project list immediately | [ ] | [ ] | 1.5.2 | |
| 4.2 | Create project → `POST /projects` recorded in `db.json` | [ ] | [ ] | 1.5.2 | |
| 4.3 | Update project name → change persists after browser page refresh | [ ] | [ ] | 1.5.2 | |
| 4.4 | Update project status (active → paused → archived) → `PATCH /projects/:id` reflected in `db.json` | [ ] | [ ] | 1.5.2 | |
| 4.5 | Delete project → removed from project list UI | [ ] | [ ] | 1.5.2 | |
| 4.6 | Delete project → cascade removes associated tasks from `db.json` | [ ] | [ ] | 1.5.2 | |
| 4.7 | Create project with empty name → form validation prevents submission | [ ] | [ ] | 1.5.2 | |

---

## 5. Authentication

| # | Test Item | Pass | Fail | WBS Ref | Notes |
|---|---|---|---|---|---|
| 5.1 | Login with valid email + password → redirects to dashboard | [ ] | [ ] | 1.5.2 | |
| 5.2 | Login with invalid credentials → error message displayed, stays on login page | [ ] | [ ] | 1.5.2 | |
| 5.3 | Login with non-existent email → error "User not found" shown | [ ] | [ ] | 1.5.2 | |
| 5.4 | Login with wrong password → error "Invalid credentials" shown | [ ] | [ ] | 1.5.2 | |
| 5.5 | Admin role → sidebar shows all navigation items (Dashboard, Kanban, Projects, Tasks, Users) | [ ] | [ ] | 1.5.2 | |
| 5.6 | Viewer role → restricted views load; admin-only views hidden or inaccessible | [ ] | [ ] | 1.5.2 | |
| 5.7 | Member role → can view and interact with tasks and projects | [ ] | [ ] | 1.5.2 | |
| 5.8 | Logout → session cleared, redirected to login page | [ ] | [ ] | 1.5.2 | |

---

## 6. Navigation

| # | Test Item | Pass | Fail | WBS Ref | Notes |
|---|---|---|---|---|---|
| 6.1 | Sidebar: Dashboard link opens dashboard view | [ ] | [ ] | 1.5.2 | |
| 6.2 | Sidebar: Kanban link opens Kanban board view | [ ] | [ ] | 1.5.2 | |
| 6.3 | Sidebar: Projects link opens projects list | [ ] | [ ] | 1.5.2 | |
| 6.4 | Sidebar: Tasks link opens tasks list | [ ] | [ ] | 1.5.2 | |
| 6.5 | Sidebar: Users link opens users management view | [ ] | [ ] | 1.5.2 | |
| 6.6 | Navigating to unknown route (e.g., `/nonexistent`) → 404 fallback rendered | [ ] | [ ] | 1.5.2 | |
| 6.7 | Browser back/forward buttons maintain correct view state | [ ] | [ ] | 1.5.2 | |

---

## 7. End-to-End Demo Flow

| # | Test Item | Pass | Fail | WBS Ref | Notes |
|---|---|---|---|---|---|
| 7.1 | Full flow: Login → Create Project → Create 3 Tasks → Move tasks through Kanban → Complete one → Refresh page → Data persisted | [ ] | [ ] | 1.5.2 | |
| 7.2 | Demo flow produces no JS console errors (Error level) | [ ] | [ ] | 1.5.2 | |

---

## Summary

| Category | Total | Passed | Failed | N/A |
|---|---|---|---|---|
| Data Loading | 6 | __ | __ | __ |
| Task CRUD | 8 | __ | __ | __ |
| Kanban Board | 6 | __ | __ | __ |
| Project CRUD | 7 | __ | __ | __ |
| Authentication | 8 | __ | __ | __ |
| Navigation | 7 | __ | __ | __ |
| E2E Demo Flow | 2 | __ | __ | __ |
| **TOTAL** | **44** | **__** | **__** | **__** |

**Overall Integration Test Result:** [ ] PASS  [ ] FAIL
**Blockers:** ___________________________________________________________________

---

*Operator Signature:* _________________________  *Date:* _________________________
