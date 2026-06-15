import { useMemo, useState } from 'react';
import { projects as seedProjects, ProjectForm, ProjectList } from './modules/projects';
import { TaskForm, TaskList } from './modules/tasks';
import { statusCounts as baseStatusCounts } from './modules/dashboard';
import type { Project, Task, TaskStatus, ProjectStatus } from './shared/types';

type View = 'dashboard' | 'board' | 'projects' | 'tasks' | 'auth' | 'users';
type KanbanColumn = { key: TaskStatus; title: string };
type StoredState = { view: View; tasks: Task[]; projects: Project[] };
type ProjectDraft = { name: string; status: ProjectStatus; taskCount: number };
type TaskDraft = { title: string; status: TaskStatus; projectId: string; projectName: string; dueDate: string };
type ModalState = { kind: 'project' | 'task'; id: string | null } | null;

const STORAGE_KEY = 'task-studio-state';
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
const initialProjects: Project[] = seedProjects;

function readStoredState(): StoredState | null {
  if (typeof window === 'undefined') return null;
  const raw = window.localStorage.getItem(STORAGE_KEY);
  if (!raw) return null;
  try { return JSON.parse(raw) as StoredState; } catch { return null; }
}

function createProjectId(projects: Project[]) { return `p-${projects.length + 1}`; }
function createTaskId(tasks: Task[]) { return `T-${String(tasks.length + 108)}`; }
function emptyProjectDraft(): ProjectDraft { return { name: '', status: 'active', taskCount: 0 }; }
function emptyTaskDraft(projects: Project[]): TaskDraft { return { title: '', status: 'todo', projectId: projects[0]?.id ?? '', projectName: projects[0]?.name ?? '', dueDate: '' }; }

export default function App() {
  const storedState = readStoredState();
  const [view, setView] = useState<View>(storedState?.view ?? 'dashboard');
  const [tasks, setTasks] = useState<Task[]>(storedState?.tasks ?? initialTasks);
  const [projects, setProjects] = useState<Project[]>(storedState?.projects ?? initialProjects);
  const [draggingTaskId, setDraggingTaskId] = useState<string | null>(null);
  const [dragOverColumn, setDragOverColumn] = useState<TaskStatus | null>(null);
  const [editModal, setEditModal] = useState<ModalState>(null);
  const [projectDraft, setProjectDraft] = useState<ProjectDraft>(emptyProjectDraft());
  const [taskDraft, setTaskDraft] = useState<TaskDraft>(emptyTaskDraft(projects));
  const [confirmDelete, setConfirmDelete] = useState<{ kind: 'project' | 'task'; id: string; title: string } | null>(null);

  const persist = (nextView: View, nextTasks: Task[], nextProjects: Project[]) => {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify({ view: nextView, tasks: nextTasks, projects: nextProjects } satisfies StoredState));
  };

  const statusCounts = useMemo(() => [
    { label: 'Open tasks', value: String(tasks.filter((task) => task.status !== 'done').length) },
    { label: 'Due this week', value: '5' },
    { label: 'Active projects', value: String(projects.filter((project) => project.status === 'active').length) },
  ], [tasks, projects]);

  const taskColumns = useMemo(() => kanbanColumns.map((column) => ({ ...column, items: tasks.filter((task) => task.status === column.key) })), [tasks]);

  const changeView = (nextView: View) => { setView(nextView); persist(nextView, tasks, projects); };
  const moveTask = (taskId: string, nextStatus: TaskStatus) => { setTasks((current) => { const nextTasks = current.map((task) => task.id === taskId ? { ...task, status: nextStatus } : task); persist(view, nextTasks, projects); return nextTasks; }); setDraggingTaskId(null); setDragOverColumn(null); };

  const saveProject = () => {
    if (!projectDraft.name.trim()) return;
    const nextProjects = editModal?.kind === 'project' && editModal.id
      ? projects.map((project) => project.id === editModal.id ? { ...project, ...projectDraft } : project)
      : [...projects, { id: createProjectId(projects), ...projectDraft }];
    setProjects(nextProjects);
    persist(view, tasks, nextProjects);
    setEditModal(null);
    setProjectDraft(emptyProjectDraft());
  };

  const saveTask = () => {
    if (!taskDraft.title.trim() || !taskDraft.projectId) return;
    const projectName = projects.find((project) => project.id === taskDraft.projectId)?.name ?? taskDraft.projectName;
    const existingTask = editModal?.kind === 'task' && editModal.id ? tasks.find((task) => task.id === editModal.id) : undefined;
    const nextTask: Task = existingTask ? { ...existingTask, ...taskDraft, projectName } : { id: createTaskId(tasks), ...taskDraft, projectName };
    const nextTasks = existingTask ? tasks.map((task) => task.id === existingTask.id ? nextTask : task) : [...tasks, nextTask];
    setTasks(nextTasks);
    persist(view, nextTasks, projects);
    setEditModal(null);
    setTaskDraft(emptyTaskDraft(projects));
  };

  const openProjectModal = (project: Project | null) => { setEditModal({ kind: 'project', id: project?.id ?? null }); setProjectDraft(project ? { name: project.name, status: project.status, taskCount: project.taskCount } : emptyProjectDraft()); };
  const openTaskModal = (task: Task | null) => { setEditModal({ kind: 'task', id: task?.id ?? null }); setTaskDraft(task ? { title: task.title, status: task.status, projectId: task.projectId, projectName: task.projectName, dueDate: task.dueDate } : emptyTaskDraft(projects)); };

  const requestDeleteProject = (projectId: string) => setConfirmDelete({ kind: 'project', id: projectId, title: projects.find((project) => project.id === projectId)?.name ?? 'this project' });
  const requestDeleteTask = (taskId: string) => setConfirmDelete({ kind: 'task', id: taskId, title: tasks.find((task) => task.id === taskId)?.title ?? 'this task' });
  const confirmDeleteAction = () => {
    if (!confirmDelete) return;
    if (confirmDelete.kind === 'project') {
      const nextProjects = projects.filter((project) => project.id !== confirmDelete.id);
      const nextTasks = tasks.filter((task) => task.projectId !== confirmDelete.id);
      setProjects(nextProjects); setTasks(nextTasks); persist(view, nextTasks, nextProjects);
    } else {
      const nextTasks = tasks.filter((task) => task.id !== confirmDelete.id);
      setTasks(nextTasks); persist(view, nextTasks, projects);
    }
    setConfirmDelete(null);
  };

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <div><p className="eyebrow">Workspace</p><h2>Task Studio</h2></div>
        <nav className="sidebar-nav">
          {navItems.map((item) => <button key={item.id} type="button" className={`sidebar-link ${view === item.id ? 'active' : ''}`} onClick={() => changeView(item.id)}>{item.label}</button>)}
        </nav>
      </aside>
      <section className="content-shell">
        {view === 'dashboard' ? <DashboardView statusCounts={statusCounts} /> : null}
        {view === 'board' ? <BoardView columns={taskColumns} draggingTaskId={draggingTaskId} dragOverColumn={dragOverColumn} onDragStart={setDraggingTaskId} onDragOverColumn={setDragOverColumn} onDropTask={moveTask} /> : null}
        {view === 'projects' ? <ProjectsView projects={projects} onCreate={() => openProjectModal(null)} onEdit={openProjectModal} onDelete={requestDeleteProject} /> : null}
        {view === 'tasks' ? <TasksView tasks={tasks} projects={projects} onCreate={() => openTaskModal(null)} onEdit={openTaskModal} onDelete={requestDeleteTask} /> : null}
        {view === 'auth' ? <ModulePlaceholder title="Auth module" body="login, session handling, and access control" /> : null}
        {view === 'users' ? <ModulePlaceholder title="Users module" body="user profiles, roles, and team membership" /> : null}
      </section>

      {editModal?.kind === 'project' ? <Modal title={editModal.id ? 'Edit project' : 'Create project'} onClose={() => setEditModal(null)}><form className="panel form-panel compact-panel" onSubmit={(e) => { e.preventDefault(); saveProject(); }}><div className="form-grid"><label><span>Project name</span><input value={projectDraft.name} onChange={(e) => setProjectDraft({ ...projectDraft, name: e.target.value })} type="text" placeholder="Launch Pad" /></label><label><span>Status</span><select value={projectDraft.status} onChange={(e) => setProjectDraft({ ...projectDraft, status: e.target.value as ProjectStatus })}><option value="active">Active</option><option value="paused">Paused</option><option value="archived">Archived</option></select></label></div><label><span>Task count</span><input type="number" value={projectDraft.taskCount} onChange={(e) => setProjectDraft({ ...projectDraft, taskCount: Number(e.target.value) })} /></label><button type="submit">{editModal.id ? 'Update project' : 'Save project'}</button></form></Modal> : null}
      {editModal?.kind === 'task' ? <Modal title={editModal.id ? 'Edit task' : 'Create task'} onClose={() => setEditModal(null)}><form className="panel form-panel compact-panel" onSubmit={(e) => { e.preventDefault(); saveTask(); }}><div className="form-grid"><label><span>Task title</span><input value={taskDraft.title} onChange={(e) => setTaskDraft({ ...taskDraft, title: e.target.value })} type="text" placeholder="Design onboarding flow" /></label><label><span>Status</span><select value={taskDraft.status} onChange={(e) => setTaskDraft({ ...taskDraft, status: e.target.value as TaskStatus })}><option value="todo">Todo</option><option value="in_progress">In progress</option><option value="done">Done</option></select></label></div><div className="form-grid"><label><span>Project</span><select value={taskDraft.projectId} onChange={(e) => { const project = projects.find((p) => p.id === e.target.value); setTaskDraft({ ...taskDraft, projectId: e.target.value, projectName: project?.name ?? taskDraft.projectName }); }}><option value="">Select a project</option>{projects.map((project) => <option key={project.id} value={project.id}>{project.name}</option>)}</select></label><label><span>Due date</span><input value={taskDraft.dueDate} onChange={(e) => setTaskDraft({ ...taskDraft, dueDate: e.target.value })} type="text" placeholder="Jun 18" /></label></div><button type="submit">{editModal.id ? 'Update task' : 'Save task'}</button></form></Modal> : null}
      {confirmDelete ? <ConfirmDialog title={`Delete ${confirmDelete.kind}`} body={`Delete ${confirmDelete.title}? This action cannot be undone.`} onCancel={() => setConfirmDelete(null)} onConfirm={confirmDeleteAction} /> : null}
    </main>
  );
}

function DashboardView({ statusCounts }: { statusCounts: typeof baseStatusCounts }) { return (<><section className="hero"><div className="hero-copy"><p className="eyebrow">Task & Project Management</p><h1>One focused workspace for projects, tasks, and delivery.</h1><p className="lede">A modular monolith foundation with a calm editorial interface: clear hierarchy, low friction, and enough structure to scale without becoming heavy.</p></div><aside className="hero-card"><div className="card-head"><span>Live snapshot</span><strong>Today</strong></div><div className="metric-stack">{statusCounts.map((metric) => (<div key={metric.label} className="metric"><span>{metric.label}</span><strong>{metric.value}</strong></div>))}</div></aside></section><section className="dashboard-band"><article className="overview-card accent-left"><span className="kicker">Project health</span><h2>Keep scope visible, always.</h2><p>Each module owns a clear responsibility so the app stays easy to reason about, test, and extend.</p></article><article className="overview-card muted-right"><span className="kicker">Board</span><h2>Todo · In Progress · Done</h2><p>Tasks are organized as a Kanban board so you can move work between statuses without losing context.</p></article></section></>); }

function BoardView({ columns, draggingTaskId, dragOverColumn, onDragStart, onDragOverColumn, onDropTask }: { columns: Array<{ key: TaskStatus; title: string; items: Task[] }>; draggingTaskId: string | null; dragOverColumn: TaskStatus | null; onDragStart: (taskId: string) => void; onDragOverColumn: (status: TaskStatus | null) => void; onDropTask: (taskId: string, nextStatus: TaskStatus) => void; }) {
  return (<article className="panel board-panel"><div className="panel-header"><div><span className="kicker">Kanban</span><h2>Drag tasks between columns</h2></div><span>{columns.reduce((sum, column) => sum + column.items.length, 0)} tasks</span></div><div className="kanban-board">{columns.map((column) => (<section key={column.key} className={`kanban-column ${dragOverColumn === column.key ? 'is-over' : ''}`} onDragEnter={() => onDragOverColumn(column.key)} onDragLeave={() => onDragOverColumn(null)} onDragOver={(event) => event.preventDefault()} onDrop={(event) => { event.preventDefault(); const taskId = event.dataTransfer.getData('text/plain') || draggingTaskId; if (taskId) onDropTask(taskId, column.key); }}><div className="panel-header"><h2>{column.title}</h2><span>{column.items.length}</span></div>{column.items.length === 0 ? <div className="empty-state board-empty"><strong>Drop here</strong><p>Drag a task into this column to update its status.</p></div> : <div className="stack">{column.items.map((task) => (<div key={task.id} className={`kanban-card ${draggingTaskId === task.id ? 'is-dragging' : ''}`} draggable onDragStart={(event) => { event.dataTransfer.setData('text/plain', task.id); onDragStart(task.id); }} onDragEnd={() => onDragStart('')}><div><strong>{task.title}</strong><p>{task.projectName} · due {task.dueDate}</p></div><span className={`pill status-${task.status}`}>{task.status.replace('_', ' ')}</span></div>))}</div>}</section>))}</div></article>);
}

function ProjectsView({ projects, onCreate, onEdit, onDelete }: { projects: Project[]; onCreate: () => void; onEdit: (project: Project) => void; onDelete: (projectId: string) => void; }) {
  return (<section className="screen-grid"><article className="panel panel-wide"><div className="panel-header"><div><span className="kicker">Projects</span><h2>Simple ownership</h2></div><div className="kanban-actions"><span>{projects.length} total</span><button type="button" onClick={onCreate}>New project</button></div></div><ProjectList projects={projects} onEdit={onEdit} onDelete={onDelete} /></article></section>);
}

function TasksView({ tasks, projects, onCreate, onEdit, onDelete }: { tasks: Task[]; projects: Project[]; onCreate: () => void; onEdit: (task: Task) => void; onDelete: (taskId: string) => void; }) {
  return (<section className="screen-grid"><article className="panel panel-wide"><div className="panel-header"><div><span className="kicker">Tasks</span><h2>Queue</h2></div><div className="kanban-actions"><span>{tasks.length} items</span><button type="button" onClick={onCreate}>New task</button></div></div><TaskList tasks={tasks} onEdit={onEdit} onDelete={onDelete} /></article></section>);
}

function ModulePlaceholder({ title, body }: { title: string; body: string }) { return (<article className="panel panel-wide"><span className="kicker">Module skeleton</span><h2>{title}</h2><p className="lede">{body}</p></article>); }

function Modal({ title, onClose, children }: { title: string; onClose: () => void; children: React.ReactNode }) { return (<div className="modal-backdrop" onClick={onClose}><div className="modal-card" onClick={(e) => e.stopPropagation()}><div className="panel-header"><h2>{title}</h2><button type="button" className="ghost-button" onClick={onClose}>Close</button></div>{children}</div></div>); }

function ConfirmDialog({ title, body, onCancel, onConfirm }: { title: string; body: string; onCancel: () => void; onConfirm: () => void; }) { return (<div className="modal-backdrop" onClick={onCancel}><div className="modal-card confirm-card" onClick={(e) => e.stopPropagation()}><span className="kicker">{title}</span><h2>{body}</h2><div className="kanban-actions"><button type="button" className="ghost-button" onClick={onCancel}>Cancel</button><button type="button" className="danger-button" onClick={onConfirm}>Delete</button></div></div></div>); }
