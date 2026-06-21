# Task Studio — User Guide

## 1. Overview

Task Studio is a task and project management prototype built for the INS3044 IT Project Management course. It lets teams manage projects, assign tasks, track progress via a Kanban board, and view a dashboard with real-time metrics and activity feeds.

## 2. Prerequisites

- Node.js 18+ installed
- npm installed
- A modern web browser (Chrome, Firefox, Safari, Edge)

## 3. Setup & Installation

Step-by-step:

1. Extract the ZIP package (`Group14_TaskStudio_Submission_W14.zip`)
2. Navigate to the project directory
3. Run: `npm install`
4. Start the API mock server: `npm run api` (runs JSON Server on port 3001)
5. In a new terminal, start the frontend: `npm run dev` (runs on port 5173)
6. Open browser: http://localhost:5173

Or use the combined command: `npm run dev:all`

## 4. Demo Credentials

| Role   | Email                | Password   |
|--------|----------------------|------------|
| Admin  | duc@taskstudio.io    | demo1234   |
| PM     | (create via Admin)   | —          |
| Member | (create via Admin)   | —          |
| Viewer | (create via Admin)   | —          |

> **Note:** Authentication is simulated — passwords are stored in plain text in `db.json` for prototype purposes only.

## 5. User Guide by Feature

### 5.1 Login

1. Go to http://localhost:5173
2. Enter email: `duc@taskstudio.io`
3. Enter password: `demo1234`
4. Click **Sign in**
5. You are redirected to the Dashboard

### 5.2 Dashboard

The dashboard shows:

- **Metrics row** — Open tasks count, In Progress count, Active projects count
- **Task Distribution** — Pie chart of tasks by status (To Do / In Progress / Done)
- **Recent Activity** — Live feed of recent actions (task created, status changed, etc.)
- **Priority Tasks** — Top 5 open tasks across all projects
- **Active Projects** — Top 5 active projects with task counts

Navigate between views using the left sidebar.

### 5.3 Projects

- View all projects in a list with status badges (Active, Paused, Archived)
- Create a new project: click **New project** → enter name, set status, set task count → click **Save project**
- Edit a project: click the edit icon on a project row → modify fields → click **Update project**
- Delete a project: click the delete icon → confirm in the dialog (removes the project and all its tasks)

### 5.4 Tasks

- View all tasks across all projects in a sortable list
- Create a task: click **New task** → enter title, select project, choose status column, set due date → click **Save task**
- Edit a task: click the edit icon on a task row → modify any field → click **Update task**
- Delete a task: click the delete icon → confirm in the dialog
- Tasks show their project name, status badge, and due date

### 5.5 Kanban Board

- Select a project from the dropdown at the top of the board
- Three default columns: **To Do**, **In Progress**, **Done**
- Tasks displayed as cards within their respective columns
- Move tasks between columns:
  - **Drag and drop** a task card from one column to another
  - The task status updates automatically
- Add a new task directly to a column by clicking **+ Add task** within the column
- Add a new column by clicking **+ Add column** at the right end of the board
- Refresh the page to see the latest board state (no real-time sync)

### 5.6 Users

- View all registered users in the workspace
- Each user card shows: name, email, role badge (Admin / Member / Viewer)
- User management is accessible via the **Auth** view in the sidebar

### 5.7 Auth Info

- View your current session details (name, email, role)
- Log out from this view or via the logout button

### 5.8 Logout

- Click the **Auth** sidebar item → click **Logout**
- You are returned to the login page

## 6. Troubleshooting

| Problem                              | Solution                                                            |
|--------------------------------------|---------------------------------------------------------------------|
| "Cannot connect to API"              | Ensure `npm run api` is running on port 3001                        |
| Blank page after login               | Ensure `npm run dev` is running on port 5173                        |
| Data not persisting after refresh    | Check that `db.json` exists in the project root and is writable     |
| Login not working                    | Use demo credentials: `duc@taskstudio.io` / `demo1234`              |
| Kanban board shows no tasks          | Select a project from the dropdown at the top of the board           |
| Changes not visible on Kanban board   | Drag-and-drop updates the API; refresh the page if unsure           |

## 7. Keyboard Shortcuts

No keyboard shortcuts are implemented in this prototype. This is a planned feature for future development.

## 8. Known Limitations

- **Simulated authentication** — passwords are stored in plain text in `db.json`. No JWT, no secure hashing.
- **No real-time updates** — the page must be refreshed after any create, update, or delete action to see changes reflected in all views.
- **Local-only data** — all data lives in `db.json` on a single machine. There is no cloud sync, no multi-user concurrent access, and no server-side persistence beyond the local file.
- **Role changes not password-protected** — any logged-in user can navigate to Auth view and modify roles.

For technical details, see [TECHNICAL_DOCUMENTATION.md](./TECHNICAL_DOCUMENTATION.md).
