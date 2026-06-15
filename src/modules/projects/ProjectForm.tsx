import { useState } from 'react';
import { isProjectStatus, validateProjectName } from '../../shared/validation';

export function ProjectForm() {
  const [name, setName] = useState('');
  const [status, setStatus] = useState('active');
  const [description, setDescription] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!validateProjectName(name) || !isProjectStatus(status)) {
      setMessage('Please enter a valid project name and status.');
      return;
    }
    setMessage(`Saved project: ${name}`);
    setName('');
    setStatus('active');
    setDescription('');
  };

  return (
    <form className="panel form-panel" onSubmit={handleSubmit}>
      <div className="panel-header">
        <div>
          <span className="kicker">Project form</span>
          <h2>Create a project</h2>
        </div>
      </div>

      <div className="form-grid">
        <label>
          <span>Project name</span>
          <input value={name} onChange={(e) => setName(e.target.value)} type="text" placeholder="Launch Pad" />
        </label>
        <label>
          <span>Status</span>
          <select value={status} onChange={(e) => setStatus(e.target.value)}>
            <option value="active">Active</option>
            <option value="paused">Paused</option>
            <option value="archived">Archived</option>
          </select>
        </label>
      </div>

      <label>
        <span>Description</span>
        <textarea value={description} onChange={(e) => setDescription(e.target.value)} rows={4} placeholder="Describe the goal, scope, and owner." />
      </label>

      {message ? <p className="form-message">{message}</p> : null}
      <button type="submit">Save project</button>
    </form>
  );
}
