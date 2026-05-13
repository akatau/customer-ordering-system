import { create } from 'zustand'
import type { User } from '@/types'
import { userService } from '@services/users'

interface UserState {
  profile: User | null
  isLoading: boolean
  error: string | null
  fetchProfile: () => Promise<void>
  updateProfile: (data: { name?: string; phone?: string }) => Promise<User>
  changePassword: (current: string, newPassword: string) => Promise<void>
}

export const useUserStore = create<UserState>((set) => ({
  profile: null,
  isLoading: false,
  error: null,

  fetchProfile: async () => {
    set({ isLoading: true, error: null })
    try {
      const profile = await userService.getProfile()
      set({ profile, isLoading: false })
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to fetch profile',
        isLoading: false,
      })
    }
  },

  updateProfile: async (data) => {
    set({ isLoading: true })
    try {
      const profile = await userService.updateProfile(data)
      set({ profile, isLoading: false })
      return profile
    } catch (error) {
      set({ error: error instanceof Error ? error.message : 'Update failed' })
      throw error
    }
  },

  changePassword: async (current: string, newPassword: string) => {
    set({ isLoading: true })
    try {
      await userService.updatePassword({ current_password: current, new_password: newPassword })
      set({ isLoading: false })
    } catch (error) {
      set({ error: error instanceof Error ? error.message : 'Password change failed' })
      throw error
    }
  },
}))
