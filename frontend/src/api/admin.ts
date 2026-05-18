import { apiClient } from './client';
import {
  AdminLogListResponse,
  AdminOrderListResponse,
  AdminUserListResponse,
  ApiResponse,
} from '@/types';

export const adminApi = {
  async listUsers(limit = 5, skip = 0): Promise<ApiResponse<AdminUserListResponse>> {
    return apiClient.get<AdminUserListResponse>('/admin/users', { limit, skip });
  },

  async listOrders(limit = 5, skip = 0): Promise<ApiResponse<AdminOrderListResponse>> {
    return apiClient.get<AdminOrderListResponse>('/admin/orders', { limit, skip });
  },

  async listActivityLogs(limit = 5, skip = 0): Promise<ApiResponse<AdminLogListResponse>> {
    return apiClient.get<AdminLogListResponse>('/admin/activity-logs', { limit, skip });
  },
};