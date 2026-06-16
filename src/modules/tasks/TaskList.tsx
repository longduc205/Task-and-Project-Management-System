import type { Task } from '../../shared/types';

type TaskListProps = {
  tasks: Task[];
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => void;
};

export function TaskList({ tasks, onEdit, onDelete }: TaskListProps) {
  if (tasks.length === 0) {
    return (
      <div className="empty-state empty-illustrated">
        <strong>No tasks yet</strong>
        <p>Add a task to start filling the queue and move work across the board.</p>
      </div>
    );
  }

  return (
    <div className="stack" style={{ padding: 0, gap: 0 }}>
      {tasks.map((task) => (
        <div key={task.id} className="task-row">
          <div className="task-row-main">
            <strong>{task.title}</strong>
            <span>{task.projectName} · due {task.dueDate}</span>
          </div>
          <div className="kanban-actions">
            <span className={`pill status-${task.status}`}>{task.status.replace('_', ' ')}</span>
            <button type="button" onClick={() => onEdit(task)}>Edit</button>
            <button type="button" className="danger-button" onClick={() => onDelete(task.id)}>Delete</button>
          </div>
        </div>
      ))}
    </div>
  );
}
