/**
 * User Profile API endpoints
 */

import { apiClient } from './client';
import { UserProfile, ApiResponse } from '@/types';

export const userApi = {
  async getProfile(): Promise<ApiResponse<UserProfile>> {
    return apiClient.get<UserProfile>('/users/me');
  },

  async updateProfile(data: Partial<UserProfile>): Promise<ApiResponse<UserProfile>> {
    return apiClient.put<UserProfile>('/users/me', data);
  },

  async changePassword(currentPassword: string, newPassword: string): Promise<ApiResponse<{ message: string }>> {
    return apiClient.post<{ message: string }>('/users/me/change-password', {
      current_password: currentPassword,
      new_password: newPassword,
    });
  },
};
