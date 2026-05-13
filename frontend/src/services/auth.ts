import { apiClient } from './api'
import type { LoginRequest, RegisterRequest, AuthResponse, User } from '@/types'

export const authService = {
  async register(data: RegisterRequest): Promise<{ user_id: string; message: string }> {
    const response = await apiClient.getInstance().post('/auth/register', data)
    return response.data
  },

  async login(data: LoginRequest): Promise<AuthResponse> {
    const response = await apiClient.getInstance().post('/auth/login', data)
    return response.data
  },

  async logout(): Promise<void> {
    await apiClient.getInstance().post('/auth/logout')
  },

  async getCurrentUser(): Promise<User> {
    const response = await apiClient.getInstance().get('/auth/me')
    return response.data
  },

  async requestPasswordReset(email: string): Promise<{ message: string }> {
    const response = await apiClient.getInstance().post('/auth/request-reset', { email })
    return response.data
  },

  async resetPassword(token: string, newPassword: string): Promise<{ message: string }> {
    const response = await apiClient.getInstance().post('/auth/reset-password', {
      token,
      new_password: newPassword,
    })
    return response.data
  },

  async refreshToken(): Promise<AuthResponse> {
    const response = await apiClient.getInstance().post('/auth/refresh')
    return response.data
  },
}
