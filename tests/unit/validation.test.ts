import { describe, it, expect } from 'vitest';
import {
  isTaskStatus,
  isProjectStatus,
  isUserRole,
  validateProjectName,
  validateTaskTitle,
} from '../../src/shared/validation';

describe('isTaskStatus', () => {
  it('returns true for "todo"', () => {
    expect(isTaskStatus('todo')).toBe(true);
  });

  it('returns true for "in_progress"', () => {
    expect(isTaskStatus('in_progress')).toBe(true);
  });

  it('returns true for "done"', () => {
    expect(isTaskStatus('done')).toBe(true);
  });

  it('returns false for any other string', () => {
    expect(isTaskStatus('')).toBe(false);
    expect(isTaskStatus('completed')).toBe(false);
    expect(isTaskStatus('in-progress')).toBe(false);
    expect(isTaskStatus('DONE')).toBe(false);
    expect(isTaskStatus('in progress')).toBe(false);
    expect(isTaskStatus('pending')).toBe(false);
  });

  it('returns false for non-string inputs', () => {
    expect(isTaskStatus('unknown')).toBe(false);
    expect(isTaskStatus('blocked')).toBe(false);
  });
});

describe('isProjectStatus', () => {
  it('returns true for "active"', () => {
    expect(isProjectStatus('active')).toBe(true);
  });

  it('returns true for "paused"', () => {
    expect(isProjectStatus('paused')).toBe(true);
  });

  it('returns true for "archived"', () => {
    expect(isProjectStatus('archived')).toBe(true);
  });

  it('returns false for any other string', () => {
    expect(isProjectStatus('')).toBe(false);
    expect(isProjectStatus('completed')).toBe(false);
    expect(isProjectStatus('ACTIVE')).toBe(false);
    expect(isProjectStatus('active ')).toBe(false);
    expect(isProjectStatus('on_hold')).toBe(false);
  });
});

describe('isUserRole', () => {
  it('returns true for "admin"', () => {
    expect(isUserRole('admin')).toBe(true);
  });

  it('returns true for "member"', () => {
    expect(isUserRole('member')).toBe(true);
  });

  it('returns true for "viewer"', () => {
    expect(isUserRole('viewer')).toBe(true);
  });

  it('returns false for any other string', () => {
    expect(isUserRole('')).toBe(false);
    expect(isUserRole('ADMIN')).toBe(false);
    expect(isUserRole('moderator')).toBe(false);
    expect(isUserRole('guest')).toBe(false);
    expect(isUserRole('superuser')).toBe(false);
  });
});

describe('validateProjectName', () => {
  it('returns true for a non-empty string', () => {
    expect(validateProjectName('Task Studio')).toBe(true);
    expect(validateProjectName('A')).toBe(true);
    expect(validateProjectName('Project 123')).toBe(true);
  });

  it('returns false for an empty string', () => {
    expect(validateProjectName('')).toBe(false);
  });

  it('returns false for a whitespace-only string', () => {
    expect(validateProjectName('   ')).toBe(false);
    expect(validateProjectName('\t')).toBe(false);
    expect(validateProjectName('\n')).toBe(false);
    expect(validateProjectName(' \t \n ')).toBe(false);
  });

  it('returns true for a string with surrounding whitespace (non-empty after trim)', () => {
    expect(validateProjectName('  Alpha  ')).toBe(true);
    expect(validateProjectName('\tBeta\n')).toBe(true);
  });
});

describe('validateTaskTitle', () => {
  it('returns true for a non-empty string', () => {
    expect(validateTaskTitle('Fix login bug')).toBe(true);
    expect(validateTaskTitle('X')).toBe(true);
    expect(validateTaskTitle('Task #42')).toBe(true);
  });

  it('returns false for an empty string', () => {
    expect(validateTaskTitle('')).toBe(false);
  });

  it('returns false for a whitespace-only string', () => {
    expect(validateTaskTitle('      ')).toBe(false);
    expect(validateTaskTitle('\t\t')).toBe(false);
    expect(validateTaskTitle('\n\n')).toBe(false);
  });

  it('returns true for a string with surrounding whitespace (non-empty after trim)', () => {
    expect(validateTaskTitle('  Design review  ')).toBe(true);
    expect(validateTaskTitle('\tDeploy v2.0\n')).toBe(true);
  });
});
