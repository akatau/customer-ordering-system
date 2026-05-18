import { apiClient } from './api'
import type { LoginRequest, RegisterRequest, AuthResponse, User } from '@/types'

type BackendProfile = {
  id: string
  email: string
  username: string
  full_name: string | null
  role: string
  is_active: boolean
  created_at: string
  updated_at: string
}

function mapBackendProfile(profile: BackendProfile): User {
  return {
    id: profile.id,
    email: profile.email,
    name: profile.full_name || profile.username,
    role: profile.role as User['role'],
    created_at: profile.created_at,
  }
}

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
    const response = await apiClient.getInstance().get<BackendProfile>('/users/me')
    return mapBackendProfile(response.data)
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
