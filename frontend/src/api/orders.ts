/**
 * Order API endpoints
 */

import { apiClient } from './client';
import { Order, CheckoutRequest, ApiResponse } from '@/types';

export const orderApi = {
  async listOrders(page: number = 1, limit: number = 10): Promise<ApiResponse<any>> {
    return apiClient.get('/orders', { page, limit });
  },

  async getOrder(orderId: string): Promise<ApiResponse<Order>> {
    return apiClient.get<Order>(`/orders/${orderId}`);
  },

  async createOrder(checkoutData: CheckoutRequest): Promise<ApiResponse<Order>> {
    return apiClient.post<Order>('/orders', checkoutData);
  },

  async getOrderTracking(orderId: string): Promise<ApiResponse<any>> {
    return apiClient.get(`/orders/${orderId}/tracking`);
  },

  async cancelOrder(orderId: string): Promise<ApiResponse<Order>> {
    return apiClient.post<Order>(`/orders/${orderId}/cancel`);
  },
};
