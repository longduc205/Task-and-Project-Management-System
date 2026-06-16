import { createContext, useContext, useState, useEffect, useCallback } from 'react';
import type { User } from './types';
import { loginUser as apiLogin } from './api';

type AuthState = {
  user: User | null;
  isLoading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => void;
};

const AuthContext = createContext<AuthState | null>(null);

const SESSION_KEY = 'task-studio-session';

// TODO(security): Replace sessionStorage with HttpOnly cookie-based session management for production.
// TODO(security): Add OAuth provider support and MFA for production.

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Restore session on mount
  useEffect(() => {
    try {
      const stored = sessionStorage.getItem(SESSION_KEY);
      if (stored) {
        setUser(JSON.parse(stored) as User);
      }
    } catch {
      sessionStorage.removeItem(SESSION_KEY);
    }
    setIsLoading(false);
  }, []);

  const login = useCallback(async (email: string, password: string): Promise<boolean> => {
    setError(null);
    setIsLoading(true);
    try {
      const result = await apiLogin(email, password);
      if (result) {
        setUser(result);
        sessionStorage.setItem(SESSION_KEY, JSON.stringify(result));
        setIsLoading(false);
        return true;
      }
      setError('Invalid email or password');
      setIsLoading(false);
      return false;
    } catch {
      setError('Unable to connect to server. Is the API running?');
      setIsLoading(false);
      return false;
    }
  }, []);

  const logout = useCallback(() => {
    setUser(null);
    setError(null);
    sessionStorage.removeItem(SESSION_KEY);
  }, []);

  return (
    <AuthContext.Provider value={{ user, isLoading, error, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthState {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}
