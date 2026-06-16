import type { Project, Task, User, Activity, KanbanColumn } from './types';

const BASE = 'http://localhost:3001';

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    throw new Error(`API error: ${res.status} ${res.statusText}`);
  }
  // DELETE returns empty body
  if (res.status === 204 || options?.method === 'DELETE') {
    return undefined as T;
  }
  return res.json() as Promise<T>;
}

// Columns
export function fetchColumns(): Promise<KanbanColumn[]> {
  return request<KanbanColumn[]>('/columns');
}

export function createColumn(draft: Omit<KanbanColumn, 'id'>): Promise<KanbanColumn> {
  return request<KanbanColumn>('/columns', {
    method: 'POST',
    body: JSON.stringify(draft),
  });
}

// Projects
export function fetchProjects(): Promise<Project[]> {
  return request<Project[]>('/projects');
}

export function createProject(draft: Omit<Project, 'id'>): Promise<Project> {
  return request<Project>('/projects', {
    method: 'POST',
    body: JSON.stringify(draft),
  });
}

export function updateProject(id: string, data: Partial<Project>): Promise<Project> {
  return request<Project>(`/projects/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(data),
  });
}

export function deleteProject(id: string): Promise<void> {
  return request<void>(`/projects/${id}`, { method: 'DELETE' });
}

// Tasks
export function fetchTasks(): Promise<Task[]> {
  return request<Task[]>('/tasks');
}

export function createTask(draft: Omit<Task, 'id'>): Promise<Task> {
  return request<Task>('/tasks', {
    method: 'POST',
    body: JSON.stringify(draft),
  });
}

export function updateTask(id: string, data: Partial<Task>): Promise<Task> {
  return request<Task>(`/tasks/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(data),
  });
}

export function deleteTask(id: string): Promise<void> {
  return request<void>(`/tasks/${id}`, { method: 'DELETE' });
}

// Users
export function fetchUsers(): Promise<User[]> {
  return request<User[]>('/users');
}

// Activities
export function fetchActivities(): Promise<Activity[]> {
  return request<Activity[]>('/activities');
}

// Auth
// TODO(security): Move login validation to server-side. Currently fetches user by email
// and compares password client-side. Replace with bcrypt/Argon2 server-side hashing.
export async function loginUser(email: string, password: string): Promise<User | null> {
  const users = await request<User[]>(`/users?email=${encodeURIComponent(email)}`);
  if (users.length === 0) return null;
  const user = users[0];
  if (user.password !== password) return null;
  // Strip password before returning
  const { password: _, ...safeUser } = user;
  return safeUser;
}
