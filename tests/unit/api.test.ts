import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import type { User, Project, Task } from '../../src/shared/types';
import {
  loginUser,
  fetchProjects,
  fetchTasks,
} from '../../src/shared/api';

const BASE = 'http://localhost:3001';

function mockFetch(response: unknown, ok = true, status = 200) {
  return vi.fn(() =>
    Promise.resolve({
      ok,
      status,
      statusText: ok ? 'OK' : 'Error',
      headers: new Headers({ 'Content-Type': 'application/json' }),
      json: () => Promise.resolve(response),
    })
  ) as ReturnType<typeof fetch>;
}

function mockFetchJson(response: unknown, ok = true, status = 200) {
  return mockFetch(response, ok, status);
}

describe('loginUser', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', mockFetchJson([]));
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('returns null when no user is found (empty array)', async () => {
    vi.stubGlobal('fetch', mockFetchJson([]));

    const result = await loginUser('nobody@example.com', 'password123');

    expect(result).toBeNull();
    expect(fetch).toHaveBeenCalledWith(
      `${BASE}/users?email=nobody%40example.com`,
      expect.objectContaining({ headers: expect.any(Object) })
    );
  });

  it('returns null when password does not match', async () => {
    const userWithWrongPassword = [
      { id: '1', name: 'Alice', email: 'alice@example.com', password: 'correct', role: 'admin' },
    ];
    vi.stubGlobal('fetch', mockFetchJson(userWithWrongPassword));

    const result = await loginUser('alice@example.com', 'wrongpassword');

    expect(result).toBeNull();
  });

  it('returns user without password when credentials match', async () => {
    const matchingUser = [
      { id: '2', name: 'Bob', email: 'bob@example.com', password: 'secret123', role: 'member', avatarColor: 'blue' },
    ];
    vi.stubGlobal('fetch', mockFetchJson(matchingUser));

    const result = await loginUser('bob@example.com', 'secret123');

    expect(result).not.toBeNull();
    expect(result).toEqual({
      id: '2',
      name: 'Bob',
      email: 'bob@example.com',
      role: 'member',
      avatarColor: 'blue',
    });
    expect('password' in result!).toBe(false);
  });
});

describe('fetchProjects', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', mockFetchJson([]));
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('returns array of projects', async () => {
    const projects: Project[] = [
      { id: 'p1', name: 'Alpha', status: 'active', taskCount: 5 },
      { id: 'p2', name: 'Beta', status: 'paused', taskCount: 3 },
    ];
    vi.stubGlobal('fetch', mockFetchJson(projects));

    const result = await fetchProjects();

    expect(result).toEqual(projects);
    expect(result).toHaveLength(2);
    expect(fetch).toHaveBeenCalledWith(`${BASE}/projects`, expect.any(Object));
  });

  it('returns empty array when no projects exist', async () => {
    vi.stubGlobal('fetch', mockFetchJson([]));

    const result = await fetchProjects();

    expect(result).toEqual([]);
  });
});

describe('fetchTasks', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', mockFetchJson([]));
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('returns array of tasks', async () => {
    const tasks: Task[] = [
      { id: 't1', title: 'Write docs', status: 'todo', projectId: 'p1', projectName: 'Alpha', dueDate: '2026-06-30' },
      { id: 't2', title: 'Deploy', status: 'done', projectId: 'p1', projectName: 'Alpha', dueDate: '2026-06-25' },
    ];
    vi.stubGlobal('fetch', mockFetchJson(tasks));

    const result = await fetchTasks();

    expect(result).toEqual(tasks);
    expect(result).toHaveLength(2);
    expect(fetch).toHaveBeenCalledWith(`${BASE}/tasks`, expect.any(Object));
  });

  it('returns empty array when no tasks exist', async () => {
    vi.stubGlobal('fetch', mockFetchJson([]));

    const result = await fetchTasks();

    expect(result).toEqual([]);
  });
});

describe('API error handling', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', mockFetchJson(null, false, 404));
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('throws when API returns non-OK response', async () => {
    vi.stubGlobal('fetch', () =>
      Promise.resolve({
        ok: false,
        status: 404,
        statusText: 'Not Found',
        headers: new Headers({ 'Content-Type': 'application/json' }),
        json: () => Promise.resolve(null),
      })
    );

    await expect(fetchProjects()).rejects.toThrow('API error: 404 Not Found');
  });
});
