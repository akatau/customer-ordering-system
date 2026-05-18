/**
 * Authentication API endpoints
 */

import { apiClient } from './client';
import { LoginRequest, RegisterRequest, LoginResponse, ApiResponse, User } from '@/types';

export const authApi = {
  async login(credentials: LoginRequest): Promise<ApiResponse<LoginResponse>> {
    return apiClient.post<LoginResponse>('/auth/login', credentials);
  },

  async register(data: RegisterRequest): Promise<ApiResponse<User>> {
    return apiClient.post<User>('/auth/register', data);
  },

  async logout(): Promise<void> {
    apiClient.clearToken();
  },

  async changePassword(currentPassword: string, newPassword: string): Promise<ApiResponse<{ message: string }>> {
    return apiClient.post<{ message: string }>('/users/me/change-password', {
      current_password: currentPassword,
      new_password: newPassword,
    });
  },
};
