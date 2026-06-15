export type TaskStatus = 'todo' | 'in_progress' | 'done';
export type ProjectStatus = 'active' | 'paused' | 'archived';
export type UserRole = 'admin' | 'member' | 'viewer';

export type Task = {
  id: string;
  title: string;
  status: TaskStatus;
  projectId: string;
  projectName: string;
  dueDate: string;
  description?: string;
};

export type Project = {
  id: string;
  name: string;
  status: ProjectStatus;
  taskCount: number;
};

export type User = {
  id: string;
  name: string;
  email: string;
  role: UserRole;
};

export type Metric = {
  label: string;
  value: string;
};
