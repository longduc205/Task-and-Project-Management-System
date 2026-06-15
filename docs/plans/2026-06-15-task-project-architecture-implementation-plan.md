# Task & Project Management Web App Implementation Plan

**Goal:** Build a simple, maintainable task/project management web app using a modular monolith structure.

**Architecture:** The app stays in a single React + Vite codebase and deployment unit, but its code is split into focused feature modules such as `auth`, `projects`, `tasks`, `users`, and `dashboard`. Business rules live outside the UI so the app remains easy to test and extend.

**Tech Stack:** React 19, Vite, TypeScript, Vitest, ESLint.

---

## File Structure Map

Before coding, confirm the existing repo layout and then create or modify files in these responsibilities:

- `src/modules/auth/*` — login, session, role checks
- `src/modules/projects/*` — project CRUD and project-specific views
- `src/modules/tasks/*` — task CRUD, status, priority, assignment, due dates
- `src/modules/users/*` — user profiles, roles, memberships
- `src/modules/dashboard/*` — overview counts and summaries
- `src/shared/*` — reusable types, validation helpers, base UI components
- `tests/*` or `src/**/__tests__/*` — tests aligned with each module

If the repo already uses a different structure, keep the same style and map these responsibilities into the existing conventions.

## Task 1: Confirm the current app structure and create the module skeleton

**Files:**
- Modify: `src/App.tsx`
- Modify: `src/styles.css`
- Modify: `src/main.tsx`
- Modify: `index.html`
- Modify: `README.md`

- [ ] **Step 1: Inspect the current structure**

Run:

```bash
pwd && git status --short && rg -n "src/|app/|pages/|modules/" -g '!node_modules' .
```

Expected: You can identify the app root and whether the repo already uses `src`, `app`, or `pages` conventions.

- [ ] **Step 2: Create module entry points**

Add minimal exports so each module has a stable boundary. For example:

```ts
export * from "./auth.types";
```

- [ ] **Step 3: Run a sanity check**

Run the project’s normal type/lint command, for example one of:

```bash
npm test
npm run lint
npm run build
```

Expected: The project still builds or, if it is not yet set up, the command should fail only because the repository lacks that script and not because of the new module files.

- [ ] **Step 4: Commit**

```bash
git add src/modules src/shared

git commit -m "feat: scaffold modular app structure"
```

## Task 2: Define the core domain types and validation rules

**Files:**
- Create: `src/shared/types.ts`
- Create: `src/shared/validation.ts`
- Create: `src/modules/projects/project.types.ts`
- Create: `src/modules/tasks/task.types.ts`
- Create: `src/modules/users/user.types.ts`

- [ ] **Step 1: Write the failing tests for domain rules**

Create tests that assert the core entities and validation rules exist. Example:

```ts
import { describe, it, expect } from "vitest";
import { validateTaskInput } from "@/src/shared/validation";

describe("validateTaskInput", () => {
  it("rejects an empty title", () => {
    const result = validateTaskInput({ title: "", projectId: "p1" });
    expect(result.ok).toBe(false);
    expect(result.error).toBe("Title is required");
  });
});
```

- [ ] **Step 2: Run the tests and confirm they fail**

Run:

```bash
npm test -- --runInBand path/to/the/new/test
```

Expected: Fail because the validation function does not exist yet.

- [ ] **Step 3: Implement the minimal types and validation**

Add explicit types for `User`, `Project`, and `Task`, then implement validation helpers for:

- non-empty task title
- valid status transition input
- project name required
- allowed role values

Example implementation shape:

```ts
export type TaskStatus = "todo" | "in_progress" | "done";

export function validateTaskInput(input: { title: string; projectId: string }) {
  if (!input.title.trim()) return { ok: false as const, error: "Title is required" };
  if (!input.projectId.trim()) return { ok: false as const, error: "Project is required" };
  return { ok: true as const };
}
```

- [ ] **Step 4: Run the tests again**

Run the same test command.

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/shared src/modules/*/*.ts tests

git commit -m "feat: add core domain types and validation"
```

## Task 3: Implement the project and task use cases

**Files:**
- Create: `src/modules/projects/project.service.ts`
- Create: `src/modules/tasks/task.service.ts`
- Create: `src/modules/projects/project.repository.ts`
- Create: `src/modules/tasks/task.repository.ts`
- Modify: `src/modules/projects/index.ts`
- Modify: `src/modules/tasks/index.ts`

- [ ] **Step 1: Write tests for the use cases first**

Create tests for these behaviors:

```ts
import { describe, it, expect, vi } from "vitest";
import { createTask } from "@/src/modules/tasks/task.service";

describe("createTask", () => {
  it("stores a task with todo status by default", async () => {
    const repo = { create: vi.fn().mockResolvedValue({ id: "t1", status: "todo" }) };
    const result = await createTask(repo, { title: "Write plan", projectId: "p1" });
    expect(repo.create).toHaveBeenCalled();
    expect(result.status).toBe("todo");
  });
});
```

- [ ] **Step 2: Run the tests and confirm they fail**

Run:

```bash
npm test -- --runInBand path/to/task.service.test.ts
```

Expected: Fail because the service functions do not exist yet.

- [ ] **Step 3: Implement the minimal repository interfaces and services**

Add functions for:

- `createProject`
- `updateProject`
- `listProjects`
- `createTask`
- `updateTask`
- `changeTaskStatus`
- `listTasksByProject`

Keep the service layer thin and ensure all validation happens before calling repository methods.

Example shape:

```ts
export async function createTask(repo: { create(input: TaskInput): Promise<TaskRecord> }, input: TaskInput) {
  const validation = validateTaskInput(input);
  if (!validation.ok) throw new Error(validation.error);
  return repo.create({ ...input, status: "todo" });
}
```

- [ ] **Step 4: Re-run tests**

Run the same tests.

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/modules/projects src/modules/tasks tests

git commit -m "feat: add project and task use cases"
```

## Task 4: Add UI for project and task management

**Files:**
- Modify: `src/App.tsx`
- Modify: `src/styles.css`
- Modify: `index.html`
- Modify: `src/main.tsx`
- Create: `src/modules/projects/ProjectList.tsx`
- Create: `src/modules/projects/ProjectForm.tsx`
- Create: `src/modules/tasks/TaskList.tsx`
- Create: `src/modules/tasks/TaskForm.tsx`
- Create: `src/modules/dashboard/DashboardSummary.tsx`

- [ ] **Step 1: Write UI tests for the main flows**

Create tests that verify the UI can render and accept the core actions. Example:

```tsx
import { render, screen } from "@testing-library/react";
import { ProjectForm } from "@/src/modules/projects/ProjectForm";

describe("ProjectForm", () => {
  it("shows the project name field", () => {
    render(<ProjectForm onSubmit={() => undefined} />);
    expect(screen.getByLabelText(/project name/i)).toBeInTheDocument();
  });
});
```

- [ ] **Step 2: Confirm the UI tests fail**

Run:

```bash
npm test -- --runInBand path/to/ui.test.tsx
```

Expected: Fail because the components do not exist yet.

- [ ] **Step 3: Implement the UI components**

Create simple, reusable forms and lists with a clean layout:

- project list with create/edit actions
- task list with status badges and due dates
- task form with title, description, status, priority, assignee, and project fields
- dashboard summary cards for counts and overdue items

Keep the UI minimal and avoid unnecessary visual complexity.

- [ ] **Step 4: Re-run UI tests**

Run the same test command.

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/modules src/shared tests

git commit -m "feat: add basic project and task UI"
```

## Task 5: Wire dashboard and app-level data flow

**Files:**
- Modify: `src/App.tsx`
- Create or modify: `src/modules/dashboard/dashboard.service.ts`
- Modify: shared state or data-fetching layer if the repo already has one

- [ ] **Step 1: Write tests for dashboard aggregation**

Example:

```ts
import { describe, it, expect } from "vitest";
import { buildDashboardSummary } from "@/src/modules/dashboard/dashboard.service";

describe("buildDashboardSummary", () => {
  it("counts overdue tasks", () => {
    const summary = buildDashboardSummary([
      { id: "t1", status: "todo", dueDate: "2026-06-10" },
      { id: "t2", status: "done", dueDate: "2026-06-14" },
    ]);
    expect(summary.overdueCount).toBe(1);
  });
});
```

- [ ] **Step 2: Run the tests and confirm failure**

Run:

```bash
npm test -- --runInBand path/to/dashboard.test.ts
```

Expected: Fail because the aggregation function does not exist yet.

- [ ] **Step 3: Implement the dashboard aggregation and wire the view**

Add summary logic for:

- total projects
- open tasks
- overdue tasks
- tasks done this week if easy to derive from existing data

Connect the app root to display the dashboard alongside the project/task areas.

- [ ] **Step 4: Re-run tests and smoke-check the page**

Run the same tests, then start the app and verify the main page loads without runtime errors.

Expected: PASS and the dashboard renders.

- [ ] **Step 5: Commit**

```bash
git add src/modules src/shared tests

git commit -m "feat: wire dashboard summaries into the app"
```

## Task 6: Add error handling, loading states, and empty states

**Files:**
- Modify: project and task forms/components
- Modify: dashboard and list views
- Modify: shared UI components if needed

- [ ] **Step 1: Write tests for empty/error states**

Example:

```tsx
import { render, screen } from "@testing-library/react";
import { TaskList } from "@/src/modules/tasks/TaskList";

describe("TaskList", () => {
  it("shows an empty state when there are no tasks", () => {
    render(<TaskList tasks={[]} />);
    expect(screen.getByText(/no tasks yet/i)).toBeInTheDocument();
  });
});
```

- [ ] **Step 2: Run the tests and confirm failure**

Run:

```bash
npm test -- --runInBand path/to/empty-state.test.tsx
```

Expected: Fail if empty states are not implemented.

- [ ] **Step 3: Implement consistent loading and error UI**

Add explicit states for:

- loading data
- no data available
- validation error
- server or fetch error

Use the same message pattern across modules so the UX feels consistent.

- [ ] **Step 4: Re-run tests**

Run the same tests.

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/modules src/shared tests

git commit -m "feat: add consistent loading and error states"
```

## Task 7: Final verification and cleanup

**Files:**
- Modify: any file reported by tests, lint, or type checks

- [ ] **Step 1: Run the full quality check**

Run the repository’s standard validation commands, for example:

```bash
npm run lint
npm test
npm run build
```

Expected: all commands pass.

- [ ] **Step 2: Fix any issues reported**

Only address failures directly related to the changes above.

- [ ] **Step 3: Re-run the checks**

Run the same commands again.

Expected: PASS.

- [ ] **Step 4: Commit final cleanup**

```bash
git add -A
git commit -m "chore: finalize task project implementation"
```

## Spec Coverage Check

This implementation plan covers the architecture spec as follows:

- Modular monolith structure: Tasks 1, 3, 4, and 5
- Core domain entities: Task 2
- Data flow and use cases: Tasks 2 and 3
- Error handling: Task 6
- Testing strategy: Tasks 2 through 7
- MVP scope: Tasks 3, 4, and 5
- Folder organization: Task 1 and the file structure map above

## Notes

If the repository already has an established framework, routing approach, or data layer, keep that foundation and map these tasks onto it instead of introducing a new stack.
