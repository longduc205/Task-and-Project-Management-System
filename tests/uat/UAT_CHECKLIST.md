# WBS 1.5.3 User Acceptance Test Checklist — Task Studio

**Project:** Task Studio — IT Project Management System
**WBS Reference:** 1.5.3 — User Acceptance Test (UAT)
**Estimated Effort:** 15 hours
**Budget:** 750,000 VND
**Target Sign-off:** Week 12–13

---

## Session Information

| Field | Details |
|---|---|
| **UAT Session Date** | _________________________ |
| **Session #** | _________________________ |
| **Participants** | _________________________ |
| **Application Version** | _________________________ |
| **Environment** | `http://localhost:5173` + `http://localhost:3001` |

---

## Pre-Conditions

Before starting UAT, confirm all of the following are in place:

- [ ] JSON Server running: `npm run api` (port 3001)
- [ ] Dev server running: `npm run dev` (port 5173)
- [ ] `db.json` seeded with test data (projects, tasks, users)
- [ ] Test user accounts available:
  - [ ] Admin: `admin@taskstudio.com` / `admin123`
  - [ ] PM / Member: `pm@taskstudio.com` / `pm123`
  - [ ] Viewer: `viewer@taskstudio.com` / `viewer123`
- [ ] Browser console open (F12 → Console tab) for error monitoring
- [ ] Stopwatch or timer available for performance checks

---

## Section 1 — Six Quality Metrics Verification

### 1.1 Functionality

**Goal:** All CRUD scenarios work end-to-end.

| # | Test Scenario | Pass | Fail | N/A |
|---|---|---|---|---|
| F1 | Create a new project with name, description, and active status → project appears in list and db.json | [ ] | [ ] | [ ] |
| F2 | Edit an existing project's name and status → change persists after page refresh | [ ] | [ ] | [ ] |
| F3 | Delete a project → project removed from list and db.json; associated tasks removed | [ ] | [ ] | [ ] |
| F4 | Create a new task with title, assignee, and due date → task appears in list | [ ] | [ ] | [ ] |
| F5 | Edit an existing task's title and status → change persists after page refresh | [ ] | [ ] | [ ] |
| F6 | Delete a task → removed from list and db.json | [ ] | [ ] | [ ] |
| F7 | Assign a user to a task → assigneeId stored and displayed correctly | [ ] | [ ] | [ ] |
| F8 | Move a task through all Kanban statuses (todo → in_progress → done) → all changes persisted | [ ] | [ ] | [ ] |

---

### 1.2 Usability

**Goal:** 90% of test users identify the next action within 1 minute without assistance.

| # | Test Scenario | Pass | Fail | N/A |
|---|---|---|---|---|
| U1 | Test user opens the application for the first time → can locate the login form within 30 seconds | [ ] | [ ] | [ ] |
| U2 | After login, test user identifies the primary navigation (sidebar) within 30 seconds | [ ] | [ ] | [ ] |
| U3 | Test user finds the "Create Project" action without being told where it is | [ ] | [ ] | [ ] |
| U4 | Test user finds the Kanban board and understands the three-column layout | [ ] | [ ] | [ ] |
| U5 | Test user successfully creates a task without reading any instructions | [ ] | [ ] | [ ] |
| U6 | Overall: User identified next action within 1 minute on 9/10 actions | [ ] | [ ] | [ ] |

---

### 1.3 Data Consistency

**Goal:** Kanban status changes are reflected in stored task data.

| # | Test Scenario | Pass | Fail | N/A |
|---|---|---|---|---|
| DC1 | Move task from "To Do" to "In Progress" on Kanban → `status: "in_progress"` stored in db.json | [ ] | [ ] | [ ] |
| DC2 | Move task from "In Progress" to "Done" on Kanban → `status: "done"` stored in db.json | [ ] | [ ] | [ ] |
| DC3 | After Kanban drag-and-drop, refresh page → task appears in correct column (data consistent) | [ ] | [ ] | [ ] |
| DC4 | Task count on dashboard reflects actual number of tasks in db.json | [ ] | [ ] | [ ] |
| DC5 | Project task count updates after task is added or deleted | [ ] | [ ] | [ ] |

---

### 1.4 Performance

**Goal:** Page interaction responds within 2 seconds.

| # | Test Scenario | Pass | Fail | N/A |
|---|---|---|---|---|
| P1 | Dashboard loads and renders within 2 seconds (stopwatch measurement) | [ ] | [ ] | [ ] |
| P2 | Kanban board loads within 2 seconds | [ ] | [ ] | [ ] |
| P3 | Task creation form submits and UI updates within 2 seconds | [ ] | [ ] | [ ] |
| P4 | Navigation between views (sidebar click) completes within 2 seconds | [ ] | [ ] | [ ] |
| P5 | No UI freeze (>3s) during normal operations | [ ] | [ ] | [ ] |

---

### 1.5 Reliability

**Goal:** No crash during normal demo flows.

| # | Test Scenario | Pass | Fail | N/A |
|---|---|---|---|---|
| R1 | Login with valid credentials → app does not crash | [ ] | [ ] | [ ] |
| R2 | Login with invalid credentials → app does not crash; error shown gracefully | [ ] | [ ] | [ ] |
| R3 | Navigate through all views sequentially → no JS errors in console | [ ] | [ ] | [ ] |
| R4 | Perform full Kanban drag-and-drop flow → no JS errors in console | [ ] | [ ] | [ ] |
| R5 | Rapidly click "Create Project" and "Delete Project" buttons → no crash or unhandled error | [ ] | [ ] | [ ] |
| R6 | Open and close all modal dialogs → no crash | [ ] | [ ] | [ ] |
| R7 | Demo flow (login → create → edit → delete) completes without errors | [ ] | [ ] | [ ] |

---

### 1.6 Maintainability

**Goal:** Code is documented and handover-ready.

| # | Test Scenario | Pass | Fail | N/A |
|---|---|---|---|---|
| M1 | README.md exists and describes how to run the application | [ ] | [ ] | [ ] |
| M2 | Key source files contain comments explaining business logic | [ ] | [ ] | [ ] |
| M3 | API functions in `src/shared/api.ts` have JSDoc comments | [ ] | [ ] | [ ] |
| M4 | Validation functions in `src/shared/validation.ts` are documented | [ ] | [ ] | [ ] |
| M5 | TypeScript types in `src/shared/types.ts` are well-defined and named descriptively | [ ] | [ ] | [ ] |
| M6 | WBS deliverables and test checklists are present and complete | [ ] | [ ] | [ ] |

---

## Section 2 — UAT Scenarios (CRUD Flows)

### 2.1 Project Lifecycle

| Step | Action | Expected Result | Pass | Fail | Notes |
|---|---|---|---|---|---|
| 1 | Login as Admin | Redirected to Dashboard | [ ] | [ ] | |
| 2 | Navigate to Projects view | Project list displayed | [ ] | [ ] | |
| 3 | Click "Create Project" | Modal/form opens | [ ] | [ ] | |
| 4 | Fill: Name="UAT Project Alpha", Status=Active | Form populated | [ ] | [ ] | |
| 5 | Submit | Project appears in list; `POST /projects` in db.json | [ ] | [ ] | |
| 6 | Edit project name to "UAT Project Beta" | Changes saved | [ ] | [ ] | |
| 7 | Change status to "Archived" | Status updated in db.json | [ ] | [ ] | |
| 8 | Refresh page | "UAT Project Beta" archived persisted | [ ] | [ ] | |
| 9 | Delete project | Removed from list and db.json | [ ] | [ ] | |

---

### 2.2 Task Lifecycle

| Step | Action | Expected Result | Pass | Fail | Notes |
|---|---|---|---|---|---|
| 1 | Login as Admin | Redirected to Dashboard | [ ] | [ ] | |
| 2 | Navigate to Tasks view | Task list displayed | [ ] | [ ] | |
| 3 | Click "Create Task" | Modal/form opens | [ ] | [ ] | |
| 4 | Fill: Title="UAT Task 1", Status=To Do | Form populated | [ ] | [ ] | |
| 5 | Submit | Task appears in list; `POST /tasks` in db.json | [ ] | [ ] | |
| 6 | Assign task to PM user | Assignee shown in task row | [ ] | [ ] | |
| 7 | Drag task to "In Progress" on Kanban | `PATCH /tasks/:id` with `status: "in_progress"` | [ ] | [ ] | |
| 8 | Drag task to "Done" on Kanban | `PATCH /tasks/:id` with `status: "done"` | [ ] | [ ] | |
| 9 | Refresh page | Task status persisted in correct column | [ ] | [ ] | |
| 10 | Delete task | Removed from list and db.json | [ ] | [ ] | |

---

### 2.3 Role-Based Access Control

| # | Test Scenario | Expected Result | Pass | Fail | Notes |
|---|---|---|---|---|---|
| 1 | Login as **Admin** → verify sidebar shows all items (Dashboard, Kanban, Projects, Tasks, Users) | All 5 visible | [ ] | [ ] | |
| 2 | Login as **Admin** → create, edit, delete projects and tasks | All CRUD operations succeed | [ ] | [ ] | |
| 3 | Login as **PM/Member** → verify sidebar shows Dashboard, Kanban, Projects, Tasks | 4 items visible | [ ] | [ ] | |
| 4 | Login as **PM/Member** → create task and move on Kanban | Succeeds | [ ] | [ ] | |
| 5 | Login as **PM/Member** → attempt to access Users management view | Redirected or 403 | [ ] | [ ] | |
| 6 | Login as **Viewer** → verify sidebar shows Dashboard and read-only views | View-only access | [ ] | [ ] | |
| 7 | Login as **Viewer** → attempt to create or edit a task | Blocked or read-only | [ ] | [ ] | |

---

## Section 3 — Defect Log

| Defect ID | Description | Severity | Status | Assigned To | Notes / Resolution |
|---|---|---|---|---|---|
| UAT-001 | | Critical / Major / Minor | Open / Closed | | |
| UAT-002 | | Critical / Major / Minor | Open / Closed | | |
| UAT-003 | | Critical / Major / Minor | Open / Closed | | |
| UAT-004 | | Critical / Major / Minor | Open / Closed | | |
| UAT-005 | | Critical / Major / Minor | Open / Closed | | |
| UAT-006 | | Critical / Major / Minor | Open / Closed | | |
| UAT-007 | | Critical / Major / Minor | Open / Closed | | |
| UAT-008 | | Critical / Major / Minor | Open / Closed | | |

---

## Section 4 — UAT Sign-off

### 4.1 Quality Metric Summary

| Quality Metric | Overall Result |
|---|---|
| Functionality | [ ] PASS  [ ] FAIL  [ ] N/A |
| Usability | [ ] PASS  [ ] FAIL  [ ] N/A |
| Data Consistency | [ ] PASS  [ ] FAIL  [ ] N/A |
| Performance | [ ] PASS  [ ] FAIL  [ ] N/A |
| Reliability | [ ] PASS  [ ] FAIL  [ ] N/A |
| Maintainability | [ ] PASS  [ ] FAIL  [ ] N/A |

### 4.2 Defect Summary

| | Count |
|---|---|
| Critical defects open | __ |
| Major defects open | __ |
| Minor defects open | __ |
| Total defects closed | __ |

### 4.3 Sign-off

> The undersigned confirm that the User Acceptance Test has been completed for **Task Studio**, WBS 1.5.3, and the application has been evaluated against the six quality metrics defined in the project specification.

**Overall UAT Result:** [ ] **PASS**  — Ready for production deployment

**Overall UAT Result:** [ ] **FAIL**  — Blockers must be resolved before sign-off

---

| Role | Name | Signature | Date |
|---|---|---|---|
| Project Manager (PM) | _________________________ | _________________________ | _________________________ |
| Quality Assurance (QA) | _________________________ | _________________________ | _________________________ |
| Technical Lead | _________________________ | _________________________ | _________________________ |

---

*Document Version: 1.0 | WBS Reference: 1.5.3 | Generated for Week 12–13 UAT Sign-off*
