import type { Task } from '../../shared/types';

export const tasks: Task[] = [
  { id: 'T-108', title: 'Design onboarding flow', status: 'in_progress', projectId: 'p-1', projectName: 'Launch Pad', dueDate: 'Jun 18' },
  { id: 'T-109', title: 'Finalize task filters', status: 'todo', projectId: 'p-1', projectName: 'Launch Pad', dueDate: 'Jun 20' },
  { id: 'T-110', title: 'Review sprint notes', status: 'done', projectId: 'p-2', projectName: 'Ops Board', dueDate: 'Jun 14' },
  { id: 'T-111', title: 'Prepare project handoff', status: 'todo', projectId: 'p-2', projectName: 'Ops Board', dueDate: 'Jun 22' },
];
