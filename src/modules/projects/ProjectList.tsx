import type { Project } from '../../shared/types';

type ProjectListProps = {
  projects: Project[];
};

export function ProjectList({ projects }: ProjectListProps) {
  if (projects.length === 0) {
    return <p className="empty-state">No projects yet. Create the first one to get started.</p>;
  }

  return (
    <div className="stack">
      {projects.map((project) => (
        <div key={project.id} className="row-card">
          <div>
            <strong>{project.name}</strong>
            <p>{project.taskCount} tasks</p>
          </div>
          <span className={`pill pill-${project.status}`}>{project.status}</span>
        </div>
      ))}
    </div>
  );
}
