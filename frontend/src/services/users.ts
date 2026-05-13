import { apiClient } from './api'
import type { User, Address } from '@/types'

interface UpdateProfileRequest {
  name?: string
  phone?: string
}

interface UpdatePasswordRequest {
  current_password: string
  new_password: string
}

export const userService = {
  async getProfile(): Promise<User> {
    const response = await apiClient.getInstance().get('/users/profile')
    return response.data
  },

  async updateProfile(data: UpdateProfileRequest): Promise<User> {
    const response = await apiClient.getInstance().put('/users/profile', data)
    return response.data
  },

  async updatePassword(data: UpdatePasswordRequest): Promise<{ message: string }> {
    const response = await apiClient.getInstance().post('/users/change-password', data)
    return response.data
  },

  async getAddresses(): Promise<Address[]> {
    const response = await apiClient.getInstance().get('/users/addresses')
    return response.data
  },

  async addAddress(data: Address): Promise<Address> {
    const response = await apiClient.getInstance().post('/users/addresses', data)
    return response.data
  },

  async updateAddress(id: string, data: Address): Promise<Address> {
    const response = await apiClient.getInstance().put(`/users/addresses/${id}`, data)
    return response.data
  },

  async deleteAddress(id: string): Promise<{ message: string }> {
    const response = await apiClient.getInstance().delete(`/users/addresses/${id}`)
    return response.data
  },

  async setDefaultAddress(id: string): Promise<Address> {
    const response = await apiClient.getInstance().post(`/users/addresses/${id}/default`)
    return response.data
  },
}
