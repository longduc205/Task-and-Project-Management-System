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
    <div className="stack">
      {projects.map((project) => (
        <div key={project.id} className="row-card">
          <div>
            <strong>{project.name}</strong>
            <p>{project.taskCount} tasks</p>
          </div>
          <div className="kanban-actions">
            <span className={`pill pill-${project.status}`}>{project.status}</span>
            <button type="button" onClick={() => onEdit(project)}>Edit</button>
            <button type="button" className="danger-button" onClick={() => onDelete(project.id)}>Delete</button>
          </div>
        </div>
      ))}
    </div>
  );
}
