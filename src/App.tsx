import { useMemo, useState } from 'react';
import { projects, ProjectForm, ProjectList } from './modules/projects';
import { TaskForm, TaskList } from './modules/tasks';
import { statusCounts as baseStatusCounts } from './modules/dashboard';
import type { Task, TaskStatus } from './shared/types';

type View = 'dashboard' | 'board' | 'projects' | 'tasks' | 'auth' | 'users';

type KanbanColumn = {
  key: TaskStatus;
  title: string;
};

const navItems: Array<{ id: View; label: string }> = [
  { id: 'dashboard', label: 'Overview' },
  { id: 'board', label: 'Kanban' },
  { id: 'projects', label: 'Projects' },
  { id: 'tasks', label: 'Tasks' },
  { id: 'auth', label: 'Auth' },
  { id: 'users', label: 'Users' },
];

const kanbanColumns: KanbanColumn[] = [
  { key: 'todo', title: 'Todo' },
  { key: 'in_progress', title: 'In Progress' },
  { key: 'done', title: 'Done' },
];

const initialTasks: Task[] = [
  { id: 'T-108', title: 'Design onboarding flow', status: 'in_progress', projectId: 'p-1', projectName: 'Launch Pad', dueDate: 'Jun 18' },
  { id: 'T-109', title: 'Finalize task filters', status: 'todo', projectId: 'p-1', projectName: 'Launch Pad', dueDate: 'Jun 20' },
  { id: 'T-110', title: 'Review sprint notes', status: 'done', projectId: 'p-2', projectName: 'Ops Board', dueDate: 'Jun 14' },
  { id: 'T-111', title: 'Prepare project handoff', status: 'todo', projectId: 'p-2', projectName: 'Ops Board', dueDate: 'Jun 22' },
];

export default function App() {
  const [view, setView] = useState<View>('dashboard');
  const [tasks, setTasks] = useState<Task[]>(initialTasks);
  const [draggingTaskId, setDraggingTaskId] = useState<string | null>(null);

  const statusCounts = useMemo(() => [
    { label: 'Open tasks', value: String(tasks.filter((task) => task.status !== 'done').length) },
    { label: 'Due this week', value: '5' },
    { label: 'Active projects', value: String(projects.filter((project) => project.status === 'active').length) },
  ], [tasks]);

  const taskColumns = useMemo(() => kanbanColumns.map((column) => ({
    ...column,
    items: tasks.filter((task) => task.status === column.key),
  })), [tasks]);

  const moveTask = (taskId: string, nextStatus: TaskStatus) => {
    setTasks((current) => current.map((task) => (task.id === taskId ? { ...task, status: nextStatus } : task)));
    setDraggingTaskId(null);
  };

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <div>
          <p className="eyebrow">Workspace</p>
          <h2>Task Studio</h2>
        </div>
        <nav className="sidebar-nav">
          {navItems.map((item) => (
            <button key={item.id} type="button" className={`sidebar-link ${view === item.id ? 'active' : ''}`} onClick={() => setView(item.id)}>
              {item.label}
            </button>
          ))}
        </nav>
      </aside>

      <section className="content-shell">
        {view === 'dashboard' ? <DashboardView statusCounts={statusCounts} /> : null}
        {view === 'board' ? <BoardView columns={taskColumns} draggingTaskId={draggingTaskId} onDragStart={setDraggingTaskId} onDropTask={moveTask} /> : null}
        {view === 'projects' ? <ProjectsView /> : null}
        {view === 'tasks' ? <TasksView tasks={tasks} /> : null}
        {view === 'auth' ? <ModulePlaceholder title="Auth module" body="login, session handling, and access control" /> : null}
        {view === 'users' ? <ModulePlaceholder title="Users module" body="user profiles, roles, and team membership" /> : null}
      </section>
    </main>
  );
}

function DashboardView({ statusCounts }: { statusCounts: typeof baseStatusCounts }) {
  return (
    <>
      <section className="hero">
        <div className="hero-copy">
          <p className="eyebrow">Task & Project Management</p>
          <h1>One focused workspace for projects, tasks, and delivery.</h1>
          <p className="lede">A modular monolith foundation with a calm editorial interface: clear hierarchy, low friction, and enough structure to scale without becoming heavy.</p>
        </div>

        <aside className="hero-card">
          <div className="card-head">
            <span>Live snapshot</span>
            <strong>Today</strong>
          </div>
          <div className="metric-stack">
            {statusCounts.map((metric) => (
              <div key={metric.label} className="metric">
                <span>{metric.label}</span>
                <strong>{metric.value}</strong>
              </div>
            ))}
          </div>
        </aside>
      </section>
      <section className="dashboard-band">
        <article className="overview-card accent-left"><span className="kicker">Project health</span><h2>Keep scope visible, always.</h2><p>Each module owns a clear responsibility so the app stays easy to reason about, test, and extend.</p></article>
        <article className="overview-card muted-right"><span className="kicker">Board</span><h2>Todo · In Progress · Done</h2><p>Tasks are organized as a Kanban board so you can move work between statuses without losing context.</p></article>
      </section>
    </>
  );
}

function BoardView({ columns, draggingTaskId, onDragStart, onDropTask }: { columns: Array<{ key: TaskStatus; title: string; items: Task[] }>; draggingTaskId: string | null; onDragStart: (taskId: string) => void; onDropTask: (taskId: string, nextStatus: TaskStatus) => void; }) {
  return (
    <article className="panel">
      <div className="panel-header">
        <div>
          <span className="kicker">Kanban</span>
          <h2>Drag tasks between columns</h2>
        </div>
        <span>{columns.reduce((sum, column) => sum + column.items.length, 0)} tasks</span>
      </div>
      <div className="kanban-board">
        {columns.map((column) => (
          <section
            key={column.key}
            className="kanban-column"
            onDragOver={(event) => event.preventDefault()}
            onDrop={(event) => {
              event.preventDefault();
              const taskId = event.dataTransfer.getData('text/plain') || draggingTaskId;
              if (taskId) onDropTask(taskId, column.key);
            }}
          >
            <div className="panel-header">
              <h2>{column.title}</h2>
              <span>{column.items.length}</span>
            </div>
            <div className="stack">
              {column.items.map((task) => (
                <div
                  key={task.id}
                  className="kanban-card"
                  draggable
                  onDragStart={(event) => {
                    event.dataTransfer.setData('text/plain', task.id);
                    onDragStart(task.id);
                  }}
                  onDragEnd={() => onDragStart('')}
                >
                  <div>
                    <strong>{task.title}</strong>
                    <p>{task.projectName} · due {task.dueDate}</p>
                  </div>
                  <span className={`pill status-${task.status}`}>{task.status.replace('_', ' ')}</span>
                </div>
              ))}
            </div>
          </section>
        ))}
      </div>
    </article>
  );
}

function ProjectsView() {
  return (
    <section className="grid two-up">
      <article className="panel">
        <div className="panel-header">
          <div><span className="kicker">Projects</span><h2>Simple ownership</h2></div>
          <span>{projects.length} total</span>
        </div>
        <ProjectList projects={projects} />
      </article>
      <ProjectForm />
    </section>
  );
}

function TasksView({ tasks }: { tasks: Task[] }) {
  return (
    <section className="grid two-up">
      <article className="panel">
        <div className="panel-header">
          <div><span className="kicker">Tasks</span><h2>Queue</h2></div>
          <span>{tasks.length} items</span>
        </div>
        <TaskList tasks={tasks} />
      </article>
      <TaskForm />
    </section>
  );
}

function ModulePlaceholder({ title, body }: { title: string; body: string }) {
  return (
    <article className="panel">
      <span className="kicker">Module skeleton</span>
      <h2>{title}</h2>
      <p className="lede">{body}</p>
    </article>
  );
}
