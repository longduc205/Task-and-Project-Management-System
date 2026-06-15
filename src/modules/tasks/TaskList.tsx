import type { Task, TaskStatus } from '../../shared/types';
import { boardColumns } from '../dashboard';

type TaskListProps = {
  tasks: Task[];
  onMoveTask?: (taskId: string, status: TaskStatus) => void;
};

const columnTasks = (tasks: Task[], status: TaskStatus) => tasks.filter((task) => task.status === status);

export function TaskList({ tasks, onMoveTask }: TaskListProps) {
  return (
    <div className="kanban-board">
      {boardColumns.map((column) => {
        const items = columnTasks(tasks, column.id);
        return (
          <section key={column.id} className="kanban-column">
            <header className="kanban-column__header">
              <div>
                <span className="kicker">{column.title}</span>
                <h3>{items.length} tasks</h3>
              </div>
            </header>
            <div className="stack">
              {items.length === 0 ? (
                <p className="empty-state">Drop a task here.</p>
              ) : (
                items.map((task) => (
                  <article key={task.id} className="kanban-card">
                    <div>
                      <strong>{task.title}</strong>
                      <p>
                        {task.projectName} · due {task.dueDate}
                      </p>
                    </div>
                    <div className="kanban-actions">
                      {boardColumns
                        .filter((next) => next.id !== column.id)
                        .map((next) => (
                          <button key={next.id} type="button" onClick={() => onMoveTask?.(task.id, next.id)}>
                            Move to {next.title}
                          </button>
                        ))}
                    </div>
                  </article>
                ))
              )}
            </div>
          </section>
        );
      })}
    </div>
  );
}
