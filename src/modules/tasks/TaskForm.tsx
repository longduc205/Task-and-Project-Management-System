import { useState } from 'react';
import { isTaskStatus, validateTaskTitle } from '../../shared/validation';

export function TaskForm() {
  const [title, setTitle] = useState('');
  const [status, setStatus] = useState('todo');
  const [projectName, setProjectName] = useState('');
  const [dueDate, setDueDate] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!validateTaskTitle(title) || !isTaskStatus(status)) {
      setMessage('Please enter a valid task title and status.');
      return;
    }
    setMessage(`Saved task: ${title}`);
    setTitle('');
    setStatus('todo');
    setProjectName('');
    setDueDate('');
  };

  return (
    <form className="panel form-panel" onSubmit={handleSubmit}>
      <div className="panel-header">
        <div>
          <span className="kicker">Task form</span>
          <h2>Create a task</h2>
        </div>
      </div>

      <div className="form-grid">
        <label>
          <span>Task title</span>
          <input value={title} onChange={(e) => setTitle(e.target.value)} type="text" placeholder="Design onboarding flow" />
        </label>
        <label>
          <span>Status</span>
          <select value={status} onChange={(e) => setStatus(e.target.value)}>
            <option value="todo">Todo</option>
            <option value="in_progress">In progress</option>
            <option value="done">Done</option>
          </select>
        </label>
      </div>

      <div className="form-grid">
        <label>
          <span>Project</span>
          <input value={projectName} onChange={(e) => setProjectName(e.target.value)} type="text" placeholder="Launch Pad" />
        </label>
        <label>
          <span>Due date</span>
          <input value={dueDate} onChange={(e) => setDueDate(e.target.value)} type="text" placeholder="Jun 18" />
        </label>
      </div>

      <label>
        <span>Description</span>
        <textarea rows={4} placeholder="List the scope and acceptance notes." />
      </label>

      {message ? <p className="form-message">{message}</p> : null}
      <button type="submit">Save task</button>
    </form>
  );
}
