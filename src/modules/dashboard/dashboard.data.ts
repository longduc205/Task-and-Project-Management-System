import type { Metric, Project, Task } from '../../shared/types';

export const tasks: Task[] = [
  { id: 'T-108', title: 'Design onboarding flow', status: 'in_progress', projectId: 'p-1', projectName: 'Launch Pad', dueDate: 'Jun 18' },
  { id: 'T-109', title: 'Finalize task filters', status: 'todo', projectId: 'p-1', projectName: 'Launch Pad', dueDate: 'Jun 20' },
  { id: 'T-110', title: 'Review sprint notes', status: 'done', projectId: 'p-2', projectName: 'Ops Board', dueDate: 'Jun 14' },
  { id: 'T-111', title: 'Prepare project handoff', status: 'todo', projectId: 'p-2', projectName: 'Ops Board', dueDate: 'Jun 22' },
];

export const boardColumns = [
  { key: 'todo', title: 'Todo', items: tasks.filter((task) => task.status === 'todo') },
  { key: 'in_progress', title: 'In Progress', items: tasks.filter((task) => task.status === 'in_progress') },
  { key: 'done', title: 'Done', items: tasks.filter((task) => task.status === 'done') },
] as const;

export const projects: Project[] = [
  { id: 'p-1', name: 'Launch Pad', status: 'active', taskCount: 12 },
  { id: 'p-2', name: 'Ops Board', status: 'active', taskCount: 8 },
  { id: 'p-3', name: 'Archive', status: 'archived', taskCount: 24 },
];

export const statusCounts: Metric[] = [
  { label: 'Open tasks', value: String(tasks.filter((task) => task.status !== 'done').length) },
  { label: 'Due this week', value: '5' },
  { label: 'Active projects', value: String(projects.filter((project) => project.status === 'active').length) },
];
