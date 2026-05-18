/**
 * Zustand store for authentication state
 */

import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { User, LoginRequest, RegisterRequest } from '@/types';
import { authApi } from '@api/auth';

interface AuthState {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  error: string | null;

  // Actions
  login: (credentials: LoginRequest) => Promise<boolean>;
  register: (data: RegisterRequest) => Promise<boolean>;
  logout: () => void;
  clearError: () => void;
  setToken: (token: string) => void;
  loadStoredAuth: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isLoading: false,
      error: null,

      login: async (credentials: LoginRequest) => {
        set({ isLoading: true, error: null });
        const response = await authApi.login(credentials);

        if (response.error) {
          set({ isLoading: false, error: response.error.detail });
          return false;
        }

        if (response.data) {
          set({
            user: response.data.user,
            token: response.data.access_token,
            isLoading: false,
            error: null,
          });
          localStorage.setItem('auth_token', response.data.access_token);
          return true;
        }

        set({ isLoading: false, error: 'Login failed' });
        return false;
      },

      register: async (data: RegisterRequest) => {
        set({ isLoading: true, error: null });
        const response = await authApi.register(data);

        if (response.error) {
          set({ isLoading: false, error: response.error.detail });
          return false;
        }

        if (response.data) {
          set({
            user: response.data.user,
            token: response.data.access_token,
            isLoading: false,
            error: null,
          });
          localStorage.setItem('auth_token', response.data.access_token);
          return true;
        }

        set({ isLoading: false, error: 'Registration failed' });
        return false;
      },

      logout: () => {
        authApi.logout();
        set({ user: null, token: null, error: null });
        localStorage.removeItem('auth_token');
      },

      clearError: () => set({ error: null }),

      setToken: (token: string) => {
        set({ token });
        localStorage.setItem('auth_token', token);
      },

      loadStoredAuth: () => {
        const token = localStorage.getItem('auth_token');
        if (token) {
          set({ token });
        }
      },
    }),
    {
      name: 'auth-store',
      partialize: (state) => ({
        token: state.token,
        user: state.user,
      }),
    }
  )
);
