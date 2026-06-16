import { useCallback, useEffect, useMemo, useState } from 'react';
import { LayoutDashboard, Columns, FolderKanban, CheckSquare, ShieldCheck, Users as UsersIcon, MessageSquare, Plus, CheckCircle2, Search, Bell } from 'lucide-react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';
import { ProjectForm, ProjectList } from './modules/projects';
import { TaskForm, TaskList } from './modules/tasks';
import { LoginPage, AuthInfoView } from './modules/auth';
import { UserList } from './modules/users';
import { useAuth } from './shared/AuthContext';
import * as api from './shared/api';
import type { Project, Task, TaskStatus, ProjectStatus, Activity } from './shared/types';

type View = 'dashboard' | 'board' | 'projects' | 'tasks' | 'auth' | 'users';
type KanbanColumn = { key: TaskStatus; title: string };
type ProjectDraft = { name: string; status: ProjectStatus; taskCount: number };
type TaskDraft = { title: string; status: TaskStatus; projectId: string; projectName: string; dueDate: string };
type ModalState = { kind: 'project' | 'task'; id: string | null } | null;

const navItems: Array<{ id: View; label: string; icon: React.FC<any> }> = [
  { id: 'dashboard', label: 'Overview', icon: LayoutDashboard },
  { id: 'board', label: 'Kanban', icon: Columns },
  { id: 'projects', label: 'Projects', icon: FolderKanban },
  { id: 'tasks', label: 'Tasks', icon: CheckSquare },
  { id: 'auth', label: 'Auth', icon: ShieldCheck },
  { id: 'users', label: 'Users', icon: UsersIcon },
];


function GlobalHeader({ onCreateTask, currentView }: { onCreateTask: () => void; currentView: string }) {
  const activeNavItem = navItems.find((item) => item.id === currentView);
  const viewTitle = activeNavItem ? activeNavItem.label : 'Overview';

  return (
    <header className="global-header">
      <div className="header-left">
        <h2>{viewTitle}</h2>
      </div>
      <div className="header-search">
        <Search size={16} />
        <input type="text" placeholder="Search tasks, projects, or users..." />
      </div>
      <div className="header-actions">
        <button className="ghost-button icon-btn" title="Notifications">
          <Bell size={18} />
          <span className="badge">3</span>
        </button>
        <button className="primary-btn" onClick={onCreateTask}>
          <Plus size={16} /> <span className="btn-text">New Task</span>
        </button>
      </div>
    </header>
  );
}

function emptyProjectDraft(): ProjectDraft { return { name: '', status: 'active', taskCount: 0 }; }
function emptyTaskDraft(projects: Project[]): TaskDraft { return { title: '', status: 'todo', projectId: projects[0]?.id ?? '', projectName: projects[0]?.name ?? '', dueDate: '' }; }

export default function App() {
  const { user, isLoading: authLoading, logout } = useAuth();

  const [view, setView] = useState<View>('dashboard');
  const [tasks, setTasks] = useState<Task[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [activities, setActivities] = useState<Activity[]>([]);
  const [columns, setColumns] = useState<KanbanColumn[]>([]);
  const [dataLoading, setDataLoading] = useState(true);
  const [draggingTaskId, setDraggingTaskId] = useState<string | null>(null);
  const [dragOverColumn, setDragOverColumn] = useState<TaskStatus | null>(null);
  const [editModal, setEditModal] = useState<ModalState>(null);
  const [projectDraft, setProjectDraft] = useState<ProjectDraft>(emptyProjectDraft());
  const [taskDraft, setTaskDraft] = useState<TaskDraft>(emptyTaskDraft([]));
  const [confirmDelete, setConfirmDelete] = useState<{ kind: 'project' | 'task'; id: string; title: string } | null>(null);
  const [activeBoardProject, setActiveBoardProject] = useState<string | null>(null);

  // Fetch all data from API when authenticated
  const loadData = useCallback(async () => {
    setDataLoading(true);
    try {
      const [p, t, a, c] = await Promise.all([
        api.fetchProjects(),
        api.fetchTasks(),
        api.fetchActivities(),
        api.fetchColumns()
      ]);
      setProjects(p);
      setTasks(t);
      setActivities(a);
      setColumns(c);
    } catch {
      // Silently handle — user sees empty state
    }
    setDataLoading(false);
  }, []);

  useEffect(() => {
    if (user) loadData();
  }, [user, loadData]);

  useEffect(() => {
    if (projects.length > 0 && !activeBoardProject) {
      setActiveBoardProject(projects[0].id);
    }
  }, [projects, activeBoardProject]);

  const statusCounts = useMemo(() => [
    { label: 'Open tasks', value: String(tasks.filter((t) => t.status !== 'done').length) },
    { label: 'In progress', value: String(tasks.filter((t) => t.status === 'in_progress').length) },
    { label: 'Active projects', value: String(projects.filter((p) => p.status === 'active').length) },
  ], [tasks, projects]);

  const boardTasks = useMemo(() => tasks.filter((t) => t.projectId === activeBoardProject), [tasks, activeBoardProject]);
  const taskColumns = useMemo(() => columns.map((col) => ({ ...col, items: boardTasks.filter((t) => t.status === col.id) })), [boardTasks, columns]);

  const changeView = (v: View) => setView(v);

  const moveTask = async (taskId: string, nextStatus: TaskStatus) => {
    setTasks((cur) => cur.map((t) => t.id === taskId ? { ...t, status: nextStatus } : t));
    setDraggingTaskId(null);
    setDragOverColumn(null);
    await api.updateTask(taskId, { status: nextStatus });
  };

  const saveProject = async () => {
    if (!projectDraft.name.trim()) return;
    if (editModal?.kind === 'project' && editModal.id) {
      const updated = await api.updateProject(editModal.id, projectDraft);
      setProjects((cur) => cur.map((p) => p.id === updated.id ? updated : p));
    } else {
      const created = await api.createProject(projectDraft);
      setProjects((cur) => [...cur, created]);
    }
    setEditModal(null);
    setProjectDraft(emptyProjectDraft());
  };

  const saveTask = async () => {
    if (!taskDraft.title.trim() || !taskDraft.projectId) return;
    const projectName = projects.find((p) => p.id === taskDraft.projectId)?.name ?? taskDraft.projectName;
    if (editModal?.kind === 'task' && editModal.id) {
      const updated = await api.updateTask(editModal.id, { ...taskDraft, projectName });
      setTasks((cur) => cur.map((t) => t.id === updated.id ? updated : t));
    } else {
      const created = await api.createTask({ ...taskDraft, projectName });
      setTasks((cur) => [...cur, created]);
    }
    setEditModal(null);
    setTaskDraft(emptyTaskDraft(projects));
  };

  const openProjectModal = (project: Project | null) => {
    setEditModal({ kind: 'project', id: project?.id ?? null });
    setProjectDraft(project ? { name: project.name, status: project.status, taskCount: project.taskCount } : emptyProjectDraft());
  };
  const openTaskModal = (task: Task | null) => {
    setEditModal({ kind: 'task', id: task?.id ?? null });
    setTaskDraft(task ? { title: task.title, status: task.status, projectId: task.projectId, projectName: task.projectName, dueDate: task.dueDate } : emptyTaskDraft(projects));
  };
  const openTaskModalWithDefaults = (projectId: string, status: TaskStatus) => {
    setEditModal({ kind: 'task', id: null });
    const project = projects.find(p => p.id === projectId);
    setTaskDraft({ title: '', status, projectId, projectName: project?.name || '', dueDate: '' });
  };

  const addColumn = async (title: string) => {
    if (!title.trim()) return;
    const newCol = await api.createColumn({ id: title.toLowerCase().replace(/\s+/g, '_'), title });
    setColumns(c => [...c, newCol]);
  };

  const requestDeleteProject = (projectId: string) => setConfirmDelete({ kind: 'project', id: projectId, title: projects.find((p) => p.id === projectId)?.name ?? 'this project' });
  const requestDeleteTask = (taskId: string) => setConfirmDelete({ kind: 'task', id: taskId, title: tasks.find((t) => t.id === taskId)?.title ?? 'this task' });
  const confirmDeleteAction = async () => {
    if (!confirmDelete) return;
    if (confirmDelete.kind === 'project') {
      await api.deleteProject(confirmDelete.id);
      setProjects((cur) => cur.filter((p) => p.id !== confirmDelete.id));
      setTasks((cur) => cur.filter((t) => t.projectId !== confirmDelete.id));
    } else {
      await api.deleteTask(confirmDelete.id);
      setTasks((cur) => cur.filter((t) => t.id !== confirmDelete.id));
    }
    setConfirmDelete(null);
  };

  // Show login page if not authenticated
  if (authLoading) {
    return (
      <div className="login-page">
        <div className="login-card" style={{ textAlign: 'center' }}>
          <p>Loading…</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return <LoginPage />;
  }

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <div><p className="eyebrow">Workspace</p><h2>Task Studio</h2></div>
        <nav className="sidebar-nav">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <button key={item.id} type="button" className={`sidebar-link ${view === item.id ? 'active' : ''}`} onClick={() => changeView(item.id)}>
                <Icon size={18} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
        <div className="sidebar-user">
          <div className="user-avatar" style={{ backgroundColor: user.avatarColor ?? '#0C66E4' }}>
            {user.name.charAt(0)}
          </div>
          <div className="sidebar-user-info">
            <strong>{user.name}</strong>
            <span>{user.role}</span>
          </div>
        </div>
      </aside>
      <section className="content-shell">
        <GlobalHeader onCreateTask={() => openTaskModal(null)} currentView={view} />
        {dataLoading ? (
          <div className="empty-state" style={{ marginTop: '120px' }}>
            <p>Loading workspace data…</p>
          </div>
        ) : (
          <>
            {view === 'dashboard' ? <DashboardView statusCounts={statusCounts} tasks={tasks} projects={projects} activities={activities} changeView={changeView} /> : null}
            {view === 'board' ? <BoardView projects={projects} activeProject={activeBoardProject} onChangeProject={setActiveBoardProject} columns={taskColumns} draggingTaskId={draggingTaskId} dragOverColumn={dragOverColumn} onDragStart={setDraggingTaskId} onDragOverColumn={setDragOverColumn} onDropTask={moveTask} onCreateTask={openTaskModalWithDefaults} onAddColumn={addColumn} /> : null}
            {view === 'projects' ? <ProjectsView projects={projects} onCreate={() => openProjectModal(null)} onEdit={openProjectModal} onDelete={requestDeleteProject} /> : null}
            {view === 'tasks' ? <TasksView tasks={tasks} projects={projects} onCreate={() => openTaskModal(null)} onEdit={openTaskModal} onDelete={requestDeleteTask} /> : null}
            {view === 'auth' ? <AuthInfoView user={user} onLogout={logout} /> : null}
            {view === 'users' ? <UserList /> : null}
          </>
        )}
      </section>

      {editModal?.kind === 'project' ? <Modal title={editModal.id ? 'Edit project' : 'Create project'} onClose={() => setEditModal(null)}><form className="panel form-panel compact-panel" onSubmit={(e) => { e.preventDefault(); saveProject(); }}><div className="form-grid"><label><span>Project name</span><input value={projectDraft.name} onChange={(e) => setProjectDraft({ ...projectDraft, name: e.target.value })} type="text" placeholder="Launch Pad" /></label><label><span>Status</span><select value={projectDraft.status} onChange={(e) => setProjectDraft({ ...projectDraft, status: e.target.value as ProjectStatus })}><option value="active">Active</option><option value="paused">Paused</option><option value="archived">Archived</option></select></label></div><label><span>Task count</span><input type="number" value={projectDraft.taskCount} onChange={(e) => setProjectDraft({ ...projectDraft, taskCount: Number(e.target.value) })} /></label><button type="submit">{editModal.id ? 'Update project' : 'Save project'}</button></form></Modal> : null}
      {editModal?.kind === 'task' ? <Modal title={editModal.id ? 'Edit task' : 'Create task'} onClose={() => setEditModal(null)}><form className="panel form-panel compact-panel" onSubmit={(e) => { e.preventDefault(); saveTask(); }}><div className="form-grid"><label><span>Task title</span><input value={taskDraft.title} onChange={(e) => setTaskDraft({ ...taskDraft, title: e.target.value })} type="text" placeholder="Design onboarding flow" /></label><label><span>Status</span><select value={taskDraft.status} onChange={(e) => setTaskDraft({ ...taskDraft, status: e.target.value as TaskStatus })}>{columns.map(c => <option key={c.id} value={c.id}>{c.title}</option>)}</select></label></div><div className="form-grid"><label><span>Project</span><select value={taskDraft.projectId} onChange={(e) => { const project = projects.find((p) => p.id === e.target.value); setTaskDraft({ ...taskDraft, projectId: e.target.value, projectName: project?.name ?? taskDraft.projectName }); }}><option value="">Select a project</option>{projects.map((project) => <option key={project.id} value={project.id}>{project.name}</option>)}</select></label><label><span>Due date</span><input value={taskDraft.dueDate} onChange={(e) => setTaskDraft({ ...taskDraft, dueDate: e.target.value })} type="text" placeholder="2026-06-18" /></label></div><button type="submit">{editModal.id ? 'Update task' : 'Save task'}</button></form></Modal> : null}
      {confirmDelete ? <ConfirmDialog title={`Delete ${confirmDelete.kind}`} body={`Delete ${confirmDelete.title}? This action cannot be undone.`} onCancel={() => setConfirmDelete(null)} onConfirm={confirmDeleteAction} /> : null}
    </main>
  );
}

function DashboardView({ statusCounts, tasks, projects, activities, changeView }: { statusCounts: Array<{ label: string; value: string }>; tasks: Task[]; projects: Project[]; activities: Activity[]; changeView: (view: View) => void; }) { 
  const priorityTasks = tasks.filter(t => t.status !== 'done').slice(0, 5);
  const activeProjects = projects.filter(p => p.status === 'active').slice(0, 5);
  
  const todoCount = tasks.filter(t => t.status === 'todo').length;
  const inProgressCount = tasks.filter(t => t.status === 'in_progress').length;
  const doneCount = tasks.filter(t => t.status === 'done').length;
  
  const chartData = [
    { name: 'Todo', value: todoCount, color: '#42526E' },
    { name: 'In Progress', value: inProgressCount, color: '#0747A6' },
    { name: 'Done', value: doneCount, color: '#006644' },
  ].filter(d => d.value > 0);

  return (
    <>
      <header className="page-header">
        <h1>Good morning!</h1>
        <p className="lede">Here's what's happening in your workspace today.</p>
      </header>
      <section className="metrics-row">
        {statusCounts.map((metric) => (
          <article key={metric.label} className="metric-card">
            <span>{metric.label}</span>
            <strong>{metric.value}</strong>
          </article>
        ))}
      </section>
      <section className="dashboard-grid">
        <article className="widget-panel">
          <div className="panel-header">
            <h2>Task Distribution</h2>
          </div>
          <div className="widget-content chart-container">
            {chartData.length === 0 ? <p className="empty-state">No tasks to display.</p> : (
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie data={chartData} cx="50%" cy="50%" innerRadius={60} outerRadius={80} paddingAngle={5} dataKey="value">
                    {chartData.map((entry, index) => <Cell key={`cell-${index}`} fill={entry.color} />)}
                  </Pie>
                  <Tooltip contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 12px rgba(9, 30, 66, 0.15)', fontSize: '14px' }} itemStyle={{ color: '#172B4D' }} />
                </PieChart>
              </ResponsiveContainer>
            )}
            <div className="chart-legend">
              {chartData.map(d => (
                <div key={d.name} className="legend-item">
                  <span className="legend-color" style={{ backgroundColor: d.color }} />
                  <span className="legend-label">{d.name} ({d.value})</span>
                </div>
              ))}
            </div>
          </div>
        </article>

        <article className="widget-panel">
          <div className="panel-header">
            <h2>Recent Activity</h2>
          </div>
          <div className="widget-content activity-feed">
            {activities.length === 0 ? <p className="empty-state">No recent activity.</p> : null}
            {activities.slice(0, 6).map(activity => (
              <div key={activity.id} className="activity-item">
                <div className="activity-icon">
                  {activity.type === 'comment' ? <MessageSquare size={14} /> : activity.type === 'create' ? <Plus size={14} /> : <CheckCircle2 size={14} />}
                </div>
                <div className="activity-details">
                  <p><strong>{activity.user}</strong> {activity.action} <strong>{activity.target}</strong></p>
                  <span className="activity-time">{activity.time}</span>
                </div>
              </div>
            ))}
          </div>
        </article>

        <article className="widget-panel">
          <div className="panel-header">
            <h2>Priority Tasks</h2>
            <button type="button" className="ghost-button" onClick={() => changeView('tasks')}>View all</button>
          </div>
          <div className="widget-content">
            {priorityTasks.length === 0 ? <p className="empty-state">No open tasks.</p> : null}
            {priorityTasks.map(task => (
              <div key={task.id} className="task-row">
                <div className="task-row-main">
                  <strong>{task.title}</strong>
                  <span>{task.projectName}</span>
                </div>
                <div className="task-row-meta">
                  <span className={`pill status-${task.status}`}>{task.status.replace('_', ' ')}</span>
                  <span className="due-date">{task.dueDate}</span>
                </div>
              </div>
            ))}
          </div>
        </article>
        <article className="widget-panel">
          <div className="panel-header">
            <h2>Active Projects</h2>
            <button type="button" className="ghost-button" onClick={() => changeView('projects')}>View all</button>
          </div>
          <div className="widget-content">
            {activeProjects.length === 0 ? <p className="empty-state">No active projects.</p> : null}
            {activeProjects.map(project => (
              <div key={project.id} className="task-row">
                <div className="task-row-main">
                  <strong>{project.name}</strong>
                  <span>{project.taskCount} tasks</span>
                </div>
                <div className="task-row-meta">
                  <span className={`pill status-${project.status}`}>{project.status}</span>
                </div>
              </div>
            ))}
          </div>
        </article>
      </section>
    </>
  ); 
}

function BoardView({ projects, activeProject, onChangeProject, columns, draggingTaskId, dragOverColumn, onDragStart, onDragOverColumn, onDropTask, onCreateTask, onAddColumn }: { projects: Project[]; activeProject: string | null; onChangeProject: (id: string) => void; columns: Array<{ id: TaskStatus; title: string; items: Task[] }>; draggingTaskId: string | null; dragOverColumn: TaskStatus | null; onDragStart: (taskId: string) => void; onDragOverColumn: (status: TaskStatus | null) => void; onDropTask: (taskId: string, nextStatus: TaskStatus) => void; onCreateTask: (projectId: string, status: TaskStatus) => void; onAddColumn: (title: string) => void; }) {
  const [addingColumn, setAddingColumn] = useState(false);
  const [newColumnTitle, setNewColumnTitle] = useState('');

  return (<article className="panel board-panel"><div className="panel-header" style={{ alignItems: 'center' }}><div><span className="kicker">Kanban</span><div style={{ display: 'flex', gap: '16px', alignItems: 'center', marginTop: '4px' }}><h2>Project Board</h2><select value={activeProject || ''} onChange={(e) => onChangeProject(e.target.value)} style={{ padding: '4px 12px', fontSize: '14px', width: 'auto', minWidth: '180px', margin: 0, height: '32px' }}><option value="" disabled>Select a project</option>{projects.map((p) => <option key={p.id} value={p.id}>{p.name}</option>)}</select></div></div><span>{columns.reduce((sum, column) => sum + column.items.length, 0)} tasks</span></div><div className="kanban-board">{columns.map((column) => (<section key={column.id} className={`kanban-column ${dragOverColumn === column.id ? 'is-over' : ''}`} onDragEnter={() => onDragOverColumn(column.id)} onDragLeave={() => onDragOverColumn(null)} onDragOver={(event) => event.preventDefault()} onDrop={(event) => { event.preventDefault(); const taskId = event.dataTransfer.getData('text/plain') || draggingTaskId; if (taskId) onDropTask(taskId, column.id); }}><div className="panel-header"><h2>{column.title}</h2><span>{column.items.length}</span></div>{column.items.length === 0 ? <div className="empty-state board-empty"><strong>Drop here</strong><p>Drag a task into this column to update its status.</p><button type="button" className="ghost-button add-task-btn" onClick={() => activeProject && onCreateTask(activeProject, column.id)}>+ Add task</button></div> : <div className="stack">{column.items.map((task) => (<div key={task.id} className={`kanban-card ${draggingTaskId === task.id ? 'is-dragging' : ''}`} draggable onDragStart={(event) => { event.dataTransfer.setData('text/plain', task.id); onDragStart(task.id); }} onDragEnd={() => onDragStart('')}><div><strong>{task.title}</strong><p>{task.projectName} · due {task.dueDate}</p></div><span className={`pill status-${task.status}`}>{task.status.replace('_', ' ')}</span></div>))}<button type="button" className="ghost-button add-task-btn" onClick={() => activeProject && onCreateTask(activeProject, column.id)}>+ Add task</button></div>}</section>))}<section className="kanban-column add-column-section">{addingColumn ? <form onSubmit={(e) => { e.preventDefault(); onAddColumn(newColumnTitle); setAddingColumn(false); setNewColumnTitle(''); }}><input type="text" placeholder="Column title" value={newColumnTitle} onChange={(e) => setNewColumnTitle(e.target.value)} autoFocus style={{ marginBottom: '8px' }} /><div style={{ display: 'flex', gap: '8px' }}><button type="submit">Save</button><button type="button" className="ghost-button" onClick={() => setAddingColumn(false)}>Cancel</button></div></form> : <button type="button" className="ghost-button add-column-btn" onClick={() => setAddingColumn(true)}>+ Add column</button>}</section></div></article>);
}

function ProjectsView({ projects, onCreate, onEdit, onDelete }: { projects: Project[]; onCreate: () => void; onEdit: (project: Project) => void; onDelete: (projectId: string) => void; }) {
  return (
    <>
      <header className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: '24px' }}>
        <div>
          <h1>Projects</h1>
          <p className="lede">Manage your team's active work streams.</p>
        </div>
        <div className="kanban-actions">
          <span>{projects.length} total</span>
          <button type="button" onClick={onCreate}>New project</button>
        </div>
      </header>
      <section className="dashboard-grid screen-grid">
        <article className="widget-panel">
          <div className="widget-content">
            <ProjectList projects={projects} onEdit={onEdit} onDelete={onDelete} />
          </div>
        </article>
      </section>
    </>
  );
}

function TasksView({ tasks, projects, onCreate, onEdit, onDelete }: { tasks: Task[]; projects: Project[]; onCreate: () => void; onEdit: (task: Task) => void; onDelete: (taskId: string) => void; }) {
  return (
    <>
      <header className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: '24px' }}>
        <div>
          <h1>Tasks</h1>
          <p className="lede">Queue of all work items across projects.</p>
        </div>
        <div className="kanban-actions">
          <span>{tasks.length} items</span>
          <button type="button" onClick={onCreate}>New task</button>
        </div>
      </header>
      <section className="dashboard-grid screen-grid">
        <article className="widget-panel">
          <div className="widget-content">
            <TaskList tasks={tasks} onEdit={onEdit} onDelete={onDelete} />
          </div>
        </article>
      </section>
    </>
  );
}

function Modal({ title, onClose, children }: { title: string; onClose: () => void; children: React.ReactNode }) { return (<div className="modal-backdrop" onClick={onClose}><div className="modal-card" onClick={(e) => e.stopPropagation()}><div className="panel-header"><h2>{title}</h2><button type="button" className="ghost-button" onClick={onClose}>Close</button></div>{children}</div></div>); }

function ConfirmDialog({ title, body, onCancel, onConfirm }: { title: string; body: string; onCancel: () => void; onConfirm: () => void; }) { return (<div className="modal-backdrop" onClick={onCancel}><div className="modal-card confirm-card" onClick={(e) => e.stopPropagation()}><span className="kicker">{title}</span><h2>{body}</h2><div className="kanban-actions"><button type="button" className="ghost-button" onClick={onCancel}>Cancel</button><button type="button" className="danger-button" onClick={onConfirm}>Delete</button></div></div></div>); }
