export type TaskStatus = string;

export type KanbanColumn = {
  id: string;
  title: string;
};
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
  assigneeId?: string;
};

export type Project = {
  id: string;
  name: string;
  status: ProjectStatus;
  taskCount: number;
  description?: string;
  createdAt?: string;
};

export type User = {
  id: string;
  name: string;
  email: string;
  role: UserRole;
  avatarColor?: string;
  password?: string; // Only present in API responses, stripped before session storage
};

export type Metric = {
  label: string;
  value: string;
};

export type Activity = {
  id: string;
  userId: string;
  user: string;
  action: string;
  target: string;
  time: string;
  type: 'comment' | 'status' | 'create';
};
