import type { Project } from '../../shared/types';

type ProjectListProps = {
  projects: Project[];
  onEdit: (project: Project) => void;
  onDelete: (projectId: string) => void;
};

export function ProjectList({ projects, onEdit, onDelete }: ProjectListProps) {
  if (projects.length === 0) {
    return (
      <div className="empty-state empty-illustrated">
        <strong>No projects yet</strong>
        <p>Create the first project to start organizing tasks, ownership, and delivery.</p>
      </div>
    );
  }

  return (
    <div className="stack" style={{ padding: 0, gap: 0 }}>
      {projects.map((project) => (
        <div key={project.id} className="task-row">
          <div className="task-row-main">
            <strong>{project.name}</strong>
            <span>{project.taskCount} tasks</span>
          </div>
          <div className="kanban-actions">
            <span className={`pill status-${project.status}`}>{project.status.replace('_', ' ')}</span>
            <button type="button" onClick={() => onEdit(project)}>Edit</button>
            <button type="button" className="danger-button" onClick={() => onDelete(project.id)}>Delete</button>
          </div>
        </div>
      ))}
    </div>
  );
}
