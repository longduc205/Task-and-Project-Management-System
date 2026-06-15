import type { ProjectStatus, TaskStatus, UserRole } from './types';

export function isTaskStatus(value: string): value is TaskStatus {
  return value === 'todo' || value === 'in_progress' || value === 'done';
}

export function isProjectStatus(value: string): value is ProjectStatus {
  return value === 'active' || value === 'paused' || value === 'archived';
}

export function isUserRole(value: string): value is UserRole {
  return value === 'admin' || value === 'member' || value === 'viewer';
}

export function validateProjectName(name: string) {
  return name.trim().length > 0;
}

export function validateTaskTitle(title: string) {
  return title.trim().length > 0;
}
