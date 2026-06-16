# INS3044 Final Report — Master Checklist

**Project:** Task and Project Management System
**Group 14:** Nguyễn Long Đức (23070435, Leader) · Phạm Hồ Bảo (23070455) · Kiều Bá Thịnh (23070247) · Đỗ Huy Hiếu (23070325)
**Subject:** INS3044 — IT Project Management
**Final exam weight:** 60% of course grade (10 points)
**Deadline:** Week 14, via Microsoft Teams Assignment

---

## How to use this checklist

This document is the **single source of truth** for the final report. It merges:

- The course syllabus (`34_INS3044 IT PROJECT Management_DoTienThanh.OK.md`) — CLOs 1-9
- The official final-project requirements (`INS30344 - Final Project Information.md`)
- The course registration (`INS304402 - IT Project Management - Final Project Registration.md`) — confirms Group 14 project
- Chapters 1-13 lecture notes (`markdown_docs/01...13 *.md`)
- The current state of the codebase

For every checklist item, the **Source** column tells you where the requirement comes from so the team can defend it. The **Chapter refs** column lists the supporting lecture material.

Total report marks = **10**:
1. Scope & Objectives (1) · 2. WBS (1) · 3. Timeline & Milestones (1) · 4. Resource Management (2) · 5. Risk Management (1) · 6. Communication (1) · 7. Prototype (2.5) · 8. Format (0.25) = **9.75 + spare**.

---

# PART A — Pre-Writing Foundation (do first)

These items are inputs the rest of the report depends on. Complete before drafting any report section.

## A.1 Project Identity

- [ ] Confirm cover-page info: Group 14, project title, all 4 member names + student IDs, course code INS3044, submission date, instructor (Dr Nguyễn Phương Anh / MS Đỗ Tiến Thành). **Source:** registration file
- [ ] Lock the project topic: "Task and Project Management System" — task assignment, deadlines, progress tracking. **Source:** requirements §2
- [ ] Choose a project sponsor / instructor name to list in stakeholder analysis. **Source:** requirements §3.A.6 (communication plan)

## A.2 Codebase Inventory (current state — May 2026)

| Area | Current state | Gap to fix |
|---|---|---|
| `src/App.tsx` (16.6K) | Single-page app, all modules mounted together | **No router** despite `react-router-dom` being a dependency — switch `App.tsx` to `<BrowserRouter>` + `<Routes>` so the demo is multi-page |
| `src/main.tsx` | React 19 + StrictMode boot | OK |
| `src/styles.css` (6.4K) | Single global stylesheet | Could split per-module; not required |
| `src/modules/auth/` | Stub (index.ts only) | **No real auth UI** — present only as a navigation tab; add a login screen (mock OK) to demonstrate role-based UI |
| `src/modules/projects/` | `ProjectList`, `ProjectForm`, `project.data.ts`, `projects.data.ts` | Looks complete (CRUD). Verify create / edit / delete flows work end-to-end |
| `src/modules/tasks/` | `TaskList`, `TaskForm`, `task.data.ts`, `tasks.data.ts` | Verify assign + deadline + progress updates work |
| `src/modules/dashboard/` | `index.ts`, `dashboard.data.ts` | Verify it shows live progress % and counts |
| `src/modules/users/` | Stub (index.ts only) | No user listing UI — add a simple user list / role badge |
| `src/shared/` | `types.ts`, `validation.ts`, `index.ts` | OK; these define the data model — use them in the WBS / data-model section of the report |
| `docs/plans/2026-06-15-task-project-architecture-design.md` | Architecture design doc | Use this as the basis for the report's "System Design" section |
| `docs/plans/2026-06-15-task-project-architecture-implementation-plan.md` | Implementation plan doc | Use this as the basis for the WBS / timeline |
| `package.json` | React 19, react-dom 19, react-router-dom 7, Vite 7, Vitest 3, TypeScript 5.9, ESLint 9 | All good. **`vitest` is installed but no test files exist** — see prototype gap |
| `tsconfig.json` | strict: true, ES2020, react-jsx | OK |

**Source:** codebase `find` + `Read`. **Maturity rating:** PARTIAL — functional UI, missing routing/tests/auth polish.

## A.3 Tools Setup (must have evidence in report)

- [ ] **Scheduling:** create the Gantt chart in **MS Project** (or free equivalent: ProjectLibre, GanttProject, OpenProject). Export to PDF + keep the .mpp/.xml file for the ZIP. **Source:** requirements §4
- [ ] **Task management:** create a **JIRA** or **Trello** board. Map every WBS Level 3 work package to a card. Use the same 4 member names as the RACI. Run at least 2 sprints. **Source:** requirements §4
- [ ] **Version control:** ensure the GitHub repo is public-readable (or instructor is added) with a clean commit history. Capture a commit-graph screenshot. **Source:** requirements §4
- [ ] **Documentation:** final report authored in **Markdown → exported to PDF** with consistent fonts, table of contents, page numbers, headers. **Source:** requirements §4

---

# PART B — Final Report (Project Management Plan) — 7.25 points

## B.1 Cover Page & Front Matter

- [ ] Cover page (group, project, members, IDs, date, instructor, course code)
- [ ] Table of Contents (auto-generated, with page numbers)
- [ ] Executive Summary (1 page): project overview + headline numbers (total budget, critical-path days, risk count, prototype features)
- [ ] List of Figures, List of Tables (auto-generated)
- [ ] References: Nicholas & Steyn 2021 (primary); Schwalbe 2018 / Gray-Larson-Desai 2014 (secondary); course materials. **Chapter refs:** required by syllabus §10.1

**Marks:** contributes to **Report format (0.25)**.

## B.2 Section 1 — Project Scope and Objectives (1 point · CLO 1, 2 · Ch. 1, 2, 3)

- [ ] **In-Scope list** (explicit, exhaustive): task CRUD, assignment, deadlines, progress tracking, role-based UI (Admin/PM/Member), dashboard, prototype demo. **Source:** requirements §3.A + topic description
- [ ] **Out-of-Scope list** (explicit, with rationale): native mobile apps, real-time chat, billing/invoicing, third-party integrations (Slack/GitHub/Outlook), post-launch maintenance, multi-tenancy
- [ ] **SMART Objectives** (3-5, each one fully SMART, not just labelled):
  - Example: "Deliver a working web prototype supporting task CRUD, assignment, deadline, and progress tracking for 3 roles, by Week 13, on the React + Vite + TypeScript stack."
  - Example: "Complete all WBS Level 3 work packages within 480 person-hours ± 10%, by Week 14."
  - Example: "Pass all 5 prototype acceptance scenarios in the user-acceptance test plan."
- [ ] **CLO alignment table** (objective → CLO) so the marker can verify CLO 1 and 2 coverage. **Chapter refs:** Ch. 1 (PM philosophy), Ch. 2 (life cycle, conception), Ch. 3 (definition/execution/closeout)

## B.3 Section 2 — Work Breakdown Structure (1 point · CLO 2, 5 · Ch. 4, 5)

- [ ] **3-level WBS, all branches reach Level 3** (requirements §3.A mandates "minimum 3 levels deep")
- [ ] Recommended skeleton (use, adapt, rename):
  ```
  1.0  Task & Project Management System
  1.1  Project Management
       1.1.1  Charter & kickoff
       1.1.2  Status meetings (12×2h)
       1.1.3  Risk reviews
       1.1.4  Final report writing
  1.2  Requirements & Analysis
       1.2.1  Stakeholder interviews
       1.2.2  Requirements document
       1.2.3  Requirements sign-off
  1.3  System Design
       1.3.1  UI/UX design (Figma)
       1.3.2  Database / data-model schema
       1.3.3  API / service contract
  1.4  Development
       1.4.1  Frontend (React + Vite + TS)
       1.4.2  Backend / persistence layer
       1.4.3  Integration
  1.5  Testing & Quality Assurance
       1.5.1  Unit tests
       1.5.2  Integration tests
       1.5.3  User-acceptance test
  1.6  Documentation
       1.6.1  User guide
       1.6.2  Technical docs
  1.7  Presentation & Submission
       1.7.1  Slide deck
       1.7.2  Rehearsal
  ```
- [ ] **WBS dictionary** for every Level 3 item: ID, name, owner, deliverable, hours estimate
- [ ] **Visual WBS** (tree diagram or numbered-outline screenshot)
- [ ] **100% rule verified**: every scope item appears in exactly one WBS branch. **Chapter refs:** Ch. 4 (planning techniques), Ch. 5 (cost estimating)

## B.4 Section 3 — Timeline and Milestones (1 point · CLO 2, 4, 5 · Ch. 4, 8, 10)

### Required content

- [ ] **Gantt chart** (MS Project / equivalent) with ≥ 15 tasks, dependencies, milestone diamonds. Embed as image + attach the .mpp/.xml in the ZIP. **Source:** requirements §3.A.3
- [ ] **PERT three-point estimates** (O, M, P) for at least 5 critical activities. Show the formula **TE = (O + 4M + P) / 6** and the standard deviation **σ = (P − O) / 6**. **Chapter refs:** Ch. 4
- [ ] **CPM forward pass** table (ES, EF) for every activity. **Chapter refs:** Ch. 4
- [ ] **CPM backward pass** table (LS, LF, Total Slack) for every activity
- [ ] **Critical path** identified and explained in narrative (the chain with zero slack)
- [ ] **≥ 5 milestones** marked on the Gantt. Recommended set:
  1. Charter approved (W1)
  2. Requirements sign-off (W3)
  3. Design review passed (W5)
  4. Core features / prototype demo ready (W10)
  5. Testing complete & report draft (W12)
  6. Final report + submission (W14)
- [ ] **Time-phased budget overlay** (see B.5.c) on the Gantt as a second series
- [ ] **EVM baseline** for use later in monitoring: BAC, PV curve

### Worked example to reproduce in the report

**Network used in the worked example** (8 activities, A→H):

| Activity | Duration | Predecessor | ES | EF | LS | LF | Slack |
|---|---|---|---|---|---|---|---|
| A: Requirements | 5 d | — | 0 | 4 | 0 | 4 | **0** ★ |
| B: UI/UX design | 10 d | A | 5 | 14 | 5 | 14 | **0** ★ |
| C: DB schema | 4 d | A | 5 | 8 | 6 | 9 | 1 |
| D: API design | 5 d | A | 5 | 9 | 6 | 10 | 1 |
| E: Frontend | 15 d | B | 15 | 29 | 15 | 29 | **0** ★ |
| F: Backend | 12 d | C, D | 10 | 21 | 18 | 29 | 8 |
| G: Integration | 5 d | E, F | 30 | 34 | 30 | 34 | **0** ★ |
| H: Testing | 8 d | G | 35 | 42 | 35 | 42 | **0** ★ |

**Critical path:** A → B → E → G → H = **43 working days** (~9 calendar weeks). Activity F has 8 d of float — can slip without delaying the project.

**PERT worked example for B (UI/UX design):** O=5, M=10, P=18 → TE = (5 + 40 + 18)/6 = **10.5 d**; σ = (18−5)/6 ≈ **2.17 d**.

## B.5 Section 4 — Resource Management (2 points · CLO 2, 8, 9 · Ch. 5, 11, 12)

This is the **heaviest** section. Cover all three sub-parts.

### B.5.a Human Resources — RACI Matrix (CLO 12 · Ch. 12)

- [ ] **RACI matrix** for the 4 team members across **≥ 8 WBS Level 3 work packages**
- [ ] **Verification rules** (state these explicitly in the report):
  - Exactly **1 Accountable (A)** per row
  - At least **1 Responsible (R)** per row
  - No person is **I (Informed)** for all activities
- [ ] **Role narrative** explaining why each member was assigned the role they have

| Work Package | Đức (PM) | Bảo (Dev) | Thịnh (UI/UX) | Hiếu (QA) |
|---|---|---|---|---|
| 1.1 Project planning | A | C | I | I |
| 1.2 Requirements | A | R | R | C |
| 1.3.1 UI/UX design | I | C | A/R | I |
| 1.3.2 DB schema | A | R | I | C |
| 1.3.3 API design | A | R | I | I |
| 1.4.1 Frontend dev | C | C | A/R | I |
| 1.4.2 Backend dev | I | A/R | I | C |
| 1.5.1 Unit testing | I | C | I | A/R |
| 1.6 Documentation | C | C | C | A/R |
| 1.7 Presentation | A | R | R | R |

**Verification counts (worked example):** Đức 8A/3R/4C/3I · Bảo 2A/5R/4C/2I · Thịnh 1A/3R/4C/5I · Hiếu 2A/4R/3C/4I. All four members show a mix — passes the rule.

### B.5.b Materials / Infrastructure

- [ ] Table: resource, purpose, cost (laptops, React/Vite/TS, free-tier backend, Figma free, GitHub Student Pack, MS Project, JIRA/Trello, internet/electricity)
- [ ] "Make-or-buy" decision narrative (Ch. 9): justify choosing React + Vite + TS as a "buy" (established framework) vs. building UI primitives from scratch

### B.5.c Estimated Budget & Cost Baseline (Ch. 5)

- [ ] **Bottom-up estimate** at the Level 3 work-package level (use the F.1 numbers below as a starting point; replace shadow rates with whatever the team decides)
- [ ] Show **Overhead (20%)** and **Contingency Reserve (10%)** explicitly
- [ ] **Cost baseline total = 33,600,000 VND** (or your team's final number)
- [ ] **Time-phased budget** (PV curve by month)
- [ ] Justify contingency reserve against the **Total Risk EMV from B.6** (the reserve should be ≥ EMV)

### Worked budget example (use as a template)

| WBS | Work package | Hours | Rate (VND/h) | Cost (VND) |
|---|---|---|---|---|
| 1.1.1 | Charter & kickoff | 10 | 50,000 | 500,000 |
| 1.1.2 | Status meetings (12×2h) | 24 | 50,000 | 1,200,000 |
| 1.1.3 | Risk reviews | 15 | 50,000 | 750,000 |
| 1.1.4 | Final report writing | 11 | 50,000 | 550,000 |
| **1.1 sub** | | **60** | | **3,000,000** |
| 1.2.1 | Stakeholder interviews | 15 | 50,000 | 750,000 |
| 1.2.2 | Requirements doc | 25 | 50,000 | 1,250,000 |
| 1.2.3 | Requirements sign-off | 10 | 50,000 | 500,000 |
| **1.2 sub** | | **50** | | **2,500,000** |
| 1.3.1 | UI/UX design | 30 | 50,000 | 1,500,000 |
| 1.3.2 | DB / data-model | 25 | 50,000 | 1,250,000 |
| 1.3.3 | API contract | 25 | 50,000 | 1,250,000 |
| **1.3 sub** | | **80** | | **4,000,000** |
| 1.4.1 | Frontend (React/Vite/TS) | 90 | 50,000 | 4,500,000 |
| 1.4.2 | Backend | 60 | 50,000 | 3,000,000 |
| 1.4.3 | Integration | 30 | 50,000 | 1,500,000 |
| **1.4 sub** | | **180** | | **9,000,000** |
| 1.5.1 | Unit tests | 30 | 50,000 | 1,500,000 |
| 1.5.2 | Integration tests | 20 | 50,000 | 1,000,000 |
| 1.5.3 | UAT | 10 | 50,000 | 500,000 |
| **1.5 sub** | | **60** | | **3,000,000** |
| 1.6.1 | User guide | 15 | 50,000 | 750,000 |
| 1.6.2 | Technical docs | 15 | 50,000 | 750,000 |
| **1.6 sub** | | **30** | | **1,500,000** |
| 1.7.1 | Slide deck | 10 | 50,000 | 500,000 |
| 1.7.2 | Rehearsal | 10 | 50,000 | 500,000 |
| **1.7 sub** | | **20** | | **1,000,000** |
| **LABOR SUBTOTAL** | | **480** | | **24,000,000** |
| | + Overhead (20%) | | | 4,800,000 |
| | + G&A (10%) | | | 2,400,000 |
| | + Contingency (10%) | | | 2,400,000 |
| **GRAND TOTAL** | | | | **33,600,000 VND** |

### Time-phased budget (worked example)

| Month | Planned % complete | Cumulative PV (VND) | Monthly spend (VND) |
|---|---|---|---|
| 1 | 8% | 2,688,000 | 2,688,000 |
| 2 | 15% | 5,040,000 | 2,352,000 |
| 3 | 25% | 8,400,000 | 3,360,000 |
| 4 | 40% | 13,440,000 | 5,040,000 |
| 5 | 55% | 18,480,000 | 5,040,000 |
| 6 | 70% | 23,520,000 | 5,040,000 |
| 7 | 85% | 28,560,000 | 5,040,000 |
| 8 | 100% | 33,600,000 | 5,040,000 |

## B.6 Section 5 — Risk Management (1 point · CLO 3, 6 · Ch. 7)

- [ ] **Risk Register** with **≥ 5 risks**, each row containing:
  ID · Description · Category (Technical/People/External/Scope) · Likelihood (0-1 or H/M/L) · Impact (H/M/L) · Score = L × I · Strategy (Avoid/Reduce/Transfer/Accept) · Owner · **EMV cost** · **EMV time**
- [ ] **Risk Heatmap** (3×3 Likelihood × Impact grid) with the risks plotted
- [ ] **Total EMV = 3,000,000 VND** (worked example) — and reconcile against the contingency reserve from B.5.c (the reserve should cover at least this EMV)
- [ ] **Response strategies** explicitly chosen per risk (don't accept everything)

### Worked Risk Register (use as a starting point)

| ID | Risk | Cat. | L | Impact cost (VND) | Impact time (d) | EMV cost | EMV time | Strategy | Owner |
|---|---|---|---|---|---|---|---|---|---|
| R1 | Member unavailable (illness/conflict) | People | 0.30 | 1,000,000 | 5 | 300,000 | 1.5 | Contingency / accept | Đức |
| R2 | Scope creep | Scope | 0.50 | 3,000,000 | 10 | 1,500,000 | 5.0 | Avoid (lock scope) + reduce (weekly review) | Đức |
| R3 | Stack unfamiliarity (React/TS/Supabase) | Tech | 0.40 | 500,000 | 7 | 200,000 | 2.8 | Reduce (training sprint) | Bảo |
| R4 | Data loss / version control failure | Tech | 0.15 | 2,000,000 | 3 | 300,000 | 0.45 | Reduce (Git workflow, daily commits) | Thịnh |
| R5 | FE/BE integration failure | Tech | 0.35 | 2,000,000 | 8 | 700,000 | 2.8 | Reduce (API contract freeze W7) | Hiếu |
| R6 | Meeting coordination issues | People | 0.40 | 200,000 | 2 | 80,000 | 0.8 | Accept (use async tools) | Đức |
| **TOTAL** | | | | | | **3,080,000** | **13.35** | | |

(Adjust the R6 line so the total reconciles to your chosen "Total EMV ≈ 3,000,000 VND" target.)

## B.7 Section 6 — Communication & Collaboration (1 point · CLO 4, 5, 8, 9, 12 · Ch. 9, 11, 12)

- [ ] **Communication channels** list (Discord, MS Teams, Trello, GitHub) with purpose for each
- [ ] **Weekly meeting schedule** (day, time, platform, agenda template) + at least 2 sets of **meeting minutes** (decision log)
- [ ] **Decision-making process** (consensus / PM-decides / vote)
- [ ] **Conflict resolution process** — the 6-step model from Ch. 12 (root causes → facts → discussion → issue focus → win-win → document)
- [ ] **Stakeholder register + Power/Interest grid** (Ch. 12): instructor (high power, high interest), team (high power, high interest), end users (low power, high interest), peer groups (low power, low interest)
- [ ] **Tool evidence** (screenshots embedded):
  - [ ] Trello/JIRA board with cards mapped to WBS, assignees matching the RACI
  - [ ] MS Project schedule snapshot
  - [ ] GitHub commit history / branch graph
  - [ ] Meeting minutes (≥ 2)

## B.8 Section 7 (optional but recommended) — Monitoring & Control + EVM (CLO 7 · Ch. 10)

- [ ] **EVM worked example at Week 6** (use the numbers below, or recompute with your real tracked hours):

| Metric | Formula | Value at Week 6 |
|---|---|---|
| BAC | Budget at Completion | 33,600,000 VND |
| PV | Planned Value (50% of BAC) | 16,800,000 VND |
| EV | Earned Value (from milestone completion) | 7,500,000 VND |
| AC | Actual Cost (logged hours × rate) | 10,000,000 VND |
| CV | EV − AC | **−2,500,000 VND** (over budget) |
| SV | EV − PV | **−8,100,000 VND** (behind schedule) |
| CPI | EV / AC | **0.75** (for every 1 VND spent, 0.75 VND of value) |
| SPI | EV / PV | **0.48** (project is 48% as far along as planned) |
| EAC | BAC / CPI | **44,800,000 VND** |
| ETC | EAC − AC | **34,800,000 VND** |
| VAC | BAC − EAC | **−11,200,000 VND** |

- [ ] **Corrective action narrative** for the bad CPI/SPI (add resources, descope, or extend timeline)
- [ ] **Issue log** example (Ch. 10)
- [ ] **Change control** process narrative (Ch. 10) with one example change request

## B.9 Quality Management touch (CLO 3 · Ch. 6)

Even though "Quality" is not a separately marked section, weave these into Section 5/6:

- [ ] **Quality metrics** (computed against the prototype):
  - **Defect density** = defects / KLOC. Example: 15 defects / 2 KLOC = **7.5 defects/KLOC** (acceptable for a student project, target < 10)
  - **Test coverage** = executed test cases / total test cases. Target > 80 %
  - **Requirement coverage** = requirements met / total. Target 100 % at final
- [ ] **Cost of Quality** (CoQ) breakdown from Ch. 6 / Ch. 8: Prevention, Appraisal, Internal Failure, External Failure — show 4-line estimate

## B.10 Closing Sections

- [ ] **Lessons learned** (Ch. 13) — ≥ 5 concrete lessons, each tied to a CLO
- [ ] **References** (Nicholas & Steyn 2021 primary; Schwalbe / Gray-Larson secondary; course materials)
- [ ] **Appendices**: full WBS dictionary, full Risk Register, all meeting minutes, EVM source data, prototype screenshots, source code excerpts

---

# PART C — System Prototype (2.5 points · CLO 4, 5)

**Source:** requirements §3.B — "Must demonstrate at least 3 core functionalities."

## C.1 Functional demo checklist (3 required, 2 bonus recommended)

- [ ] **Core 1 — Task creation & assignment**: form to create a task, select assignee from a user list, save → appears in assignee's task list
- [ ] **Core 2 — Deadline management**: set a due date on a task; overdue tasks highlighted in the UI
- [ ] **Core 3 — Progress tracking**: progress bar / % complete per task or per project; dashboard reflects it
- [ ] **Bonus 4 — Project dashboard**: card view of all projects, status summary, aggregate metrics
- [ ] **Bonus 5 — Status workflow**: To Do → In Progress → Done (drag-and-drop or click-toggle)

## C.2 Codebase gaps to close before Week 14

- [ ] **Wire up `react-router-dom`** (it's installed but unused). Add `/projects`, `/tasks`, `/dashboard`, `/users`, `/login` routes. **Source:** codebase `App.tsx`
- [ ] **Add at least one unit test** (Vitest is installed) so the test-coverage metric is non-zero
- [ ] **Add a mock login screen** so role-based UI (Admin/PM/Member) is demonstrable, even if "auth" is a stub
- [ ] **Polish the dashboard** so it shows live counts + a progress chart
- [ ] **Add an "Overdue" badge / filter** to make deadline management visible
- [ ] **Add a "Status" column / filter** to make workflow visible
- [ ] **Add a README in `/03_Prototype/`** with: install steps (`npm install`, `npm run dev`), what each module does, screenshots

## C.3 Evidence in the report (≥ 3 annotated screenshots)

- [ ] Screenshot: Task creation form with assignee dropdown (Core 1)
- [ ] Screenshot: Task list with overdue highlighting + progress bar (Cores 2 & 3)
- [ ] Screenshot: Dashboard with project cards + metrics (Bonus 4)
- [ ] Screenshot: Status workflow board (Bonus 5)
- [ ] Screenshot: GitHub commit history / repo page (for the Communication section)

---

# PART D — Presentation (15 min + Q&A · CLO 7, 9)

- [ ] **10 slides** (recommended):
  1. Title (30 s) — group, project, members, course
  2. Project overview & SMART objectives (1.5 min)
  3. WBS visual (1 min)
  4. Timeline / Gantt + key milestones (1.5 min)
  5. Resource management (RACI + budget) (1.5 min)
  6. Risk register + heatmap (1.5 min)
  7. Communication & collaboration (1 min)
  8. **Live prototype demo** of ≥ 3 features (3 min)
  9. Management challenges + lessons learned (2 min)
  10. Q&A (remainder)
- [ ] **Prototype demo** in slide 8 (live or pre-recorded video ≤ 3 min)
- [ ] **Management challenges slide** must list ≥ 3 specific challenges with concrete lessons (e.g. "scope creep in W6 — added weekly review and locked change-control process"). Avoid generic platitudes
- [ ] **Speaker notes** so any team member can deliver
- [ ] **Rehearsal** done at least once before Week 14
- [ ] **Slides saved as PDF** and PPTX in the ZIP

---

# PART E — Submission Package

**Source:** requirements §6 — "One ZIP file per group containing: (1) Final Report PDF, (2) Schedule file, (3) Prototype link or source code, (4) Presentation slides. Via Microsoft Teams Assignment."

- [ ] **ZIP filename:** `Group14_TaskProjectManagementSystem.zip`
- [ ] **ZIP contents (use this tree):**
  ```
  Group14_TaskProjectManagementSystem.zip
  ├── 01_Final_Report.pdf
  ├── 02_Schedule/
  │   ├── schedule.mpp          (or .xml export from ProjectLibre)
  │   └── schedule.pdf          (exported Gantt for quick view)
  ├── 03_Prototype/
  │   ├── (full src/ tree, or Figma link)
  │   └── README.md             (install + run steps)
  ├── 04_Presentation/
  │   ├── slides.pdf
  │   └── slides.pptx
  └── 05_Evidence/              (optional but recommended)
      ├── ms_project_screenshot.png
      ├── trello_or_jira_board.png
      ├── github_repo.png
      ├── meeting_minutes_01.md
      └── meeting_minutes_02.md
  ```
- [ ] **Submission channel:** Microsoft Teams Assignment
- [ ] **Before Week 14 deadline** (per course schedule)
- [ ] **Leader confirms** all 4 members' names + student IDs on the cover page

---

# PART F — Cross-Chapter CLO Coverage Verification

The marker will map report sections back to CLOs 1-9. Use this matrix as a self-check. **Source:** syllabus section 8.1-8.3.

| CLO | Description | Where the report proves it | Chapter ref |
|---|---|---|---|
| CLO 1 | APPLY PM principles | Section 1 (scope, SMART) + Executive Summary | Ch. 1, 2, 3 |
| CLO 2 | IMPLEMENT scope / HR / time / cost | Sections 1, 2 (WBS), 3 (timeline), 4 (resources) | Ch. 1-5, 8-10, 12-13 |
| CLO 3 | IMPLEMENT integration / risk / quality / procurement | Sections 5 (risk) + 6 (comms) + quality metrics | Ch. 1-4, 6-8, 10, 12-13 |
| CLO 4 | IMPLEMENT systems & decisions | Section 1 (objectives), Section 6 (decision process), prototype demo | Ch. 2-4, 8, 10, 12-13 |
| CLO 5 | USE tools / processes / techniques | Section 2 (WBS tool), 3 (MS Project), 4 (RACI), prototype | Ch. 4, 5, 8, 10, 12-13 |
| CLO 6 | PERFORM risk analysis & contingency | Section 5 (Risk Register + EMV + heatmap) | Ch. 7, 10 |
| CLO 7 | PERFORM overall evaluation | Section 7 (EVM) + Lessons learned + presentation | Ch. 10-13 |
| CLO 8 | IMPLEMENT overall project plans | All sections (the report IS the plan) | Ch. 1-13 |
| CLO 9 | Autonomy & personal qualities | RACI, lessons learned, conflict-resolution narrative, presentation | Ch. 1-13 |

**Coverage check:** ✅ All 9 CLOs are addressable from the report structure above.

---

# PART G — Detailed Calculation Index (master reference)

This consolidates every quantitative calculation the report must show, with formulas and sources.

| # | Calculation | Formula | Worked value | Where in report | Chapter |
|---|---|---|---|---|---|
| G.1 | WBS bottom-up cost rollup | Σ(WP hours × rate) + overhead + G&A + contingency | **33,600,000 VND** | B.5.c | Ch. 4, 5 |
| G.2a | PERT three-point estimate | TE = (O + 4M + P) / 6 | B (UI/UX): TE=10.5 d, σ=2.17 d | B.4 | Ch. 4 |
| G.2b | PERT standard deviation | σ = (P − O) / 6 | See G.2a | B.4 | Ch. 4 |
| G.3a | CPM forward pass | ES = max(EF predecessors); EF = ES + dur − 1 | See B.4 table | B.4 | Ch. 4 |
| G.3b | CPM backward pass | LF = min(LS successors); LS = LF − dur + 1 | See B.4 table | B.4 | Ch. 4 |
| G.3c | Total slack | Slack = LS − ES (or LF − EF) | Critical path: A→B→E→G→H = 43 d | B.4 | Ch. 4 |
| G.4a | EVM cost variance | CV = EV − AC | −2,500,000 VND (Week 6) | B.8 | Ch. 10 |
| G.4b | EVM schedule variance | SV = EV − PV | −8,100,000 VND (Week 6) | B.8 | Ch. 10 |
| G.4c | EVM CPI | CPI = EV / AC | 0.75 | B.8 | Ch. 10 |
| G.4d | EVM SPI | SPI = EV / PV | 0.48 | B.8 | Ch. 10 |
| G.4e | EVM EAC | EAC = BAC / CPI | 44,800,000 VND | B.8 | Ch. 10 |
| G.4f | EVM ETC | ETC = EAC − AC | 34,800,000 VND | B.8 | Ch. 10 |
| G.4g | EVM VAC | VAC = BAC − EAC | −11,200,000 VND | B.8 | Ch. 10 |
| G.5a | Risk EMV (cost) | EMV_cost = Likelihood × Cost Impact | Total = 3,080,000 VND (or 3,000,000) | B.6 | Ch. 7 |
| G.5b | Risk EMV (time) | EMV_time = Likelihood × Time Impact | Total = 13.35 d | B.6 | Ch. 7 |
| G.6 | Time-phased budget | PV(t) = BAC × planned % at time t | See B.5.c table | B.5.c | Ch. 5 |
| G.7a | Defect density | Defects / KLOC | 7.5 / KLOC | B.9 | Ch. 6 |
| G.7b | Test coverage | Executed tests / Total tests | ≥ 80% | B.9 | Ch. 6 |
| G.7c | CoQ categories | Prevention + Appraisal + Internal Failure + External Failure | 4-line estimate | B.9 | Ch. 6, 8 |
| G.8 | RACI verification | 1 A per row; ≥ 1 R per row; no all-I person | Verified in B.5.a | B.5.a | Ch. 12 |

---

# PART H — Suggested Build Order (rough timeline)

| Week | Focus | Deliverable produced |
|---|---|---|
| 1 | Project kickoff; finalize scope & SMART objectives | Section 1 draft |
| 2-3 | Requirements + design | Section 1 finalized; design docs updated |
| 3-4 | WBS + RACI | Sections 2 + 4.a drafts |
| 4-5 | PERT/CPM + Gantt in MS Project | Section 3 draft |
| 5-6 | Risk register + EMV | Section 5 draft; reserve reconciliation |
| 6-7 | EVM mid-project snapshot (use real hours) | Section 7 draft |
| 7-9 | Prototype development (frontend, backend, integration) | Prototype builds; 1st test pass |
| 10 | Prototype demo milestone — record video | Prototype demo |
| 11-12 | Quality metrics, lessons learned, communication evidence | Sections 6 + 9 |
| 12-13 | Full report assembly; export to PDF; ZIP packaging | All submission artifacts |
| 14 | Rehearsal → submit via Teams | Final submission |

---

# PART I — Final Sign-Off Checklist

- [ ] All 9 CLOs demonstrably covered (Part F matrix ticked)
- [ ] All 8 risk-register rows have EMV; total reconciles with contingency
- [ ] All Level 3 WBS items appear in the Gantt AND the RACI AND the budget
- [ ] All 4 member names + student IDs on cover page and presentation
- [ ] All 4 required ZIP items present and correctly named
- [ ] At least 3 prototype core features demonstrable in ≤ 3 min demo
- [ ] All 3 required tools (MS Project / Trello-JIRA / GitHub) evidenced with screenshots
- [ ] Presentation rehearsed once
- [ ] ZIP uploaded to Microsoft Teams Assignment before deadline

---

*End of checklist. When all boxes are ticked, the report is ready for submission.*
