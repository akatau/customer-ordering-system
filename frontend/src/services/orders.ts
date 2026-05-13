import { apiClient } from './api'
import type { Order, PaginatedResponse, Address } from '@/types'

interface CreateOrderRequest {
  items: Array<{ product_id: string; quantity: number }>
  shipping_address: Address
  payment_method_id: string
}

interface OrdersParams {
  page?: number
  limit?: number
  status?: string
}

export const orderService = {
  async createOrder(data: CreateOrderRequest): Promise<Order> {
    const response = await apiClient.getInstance().post('/orders', data)
    return response.data
  },

  async getOrders(params?: OrdersParams): Promise<PaginatedResponse<Order>> {
    const response = await apiClient.getInstance().get('/orders', { params })
    return response.data
  },

  async getOrderById(id: string): Promise<Order> {
    const response = await apiClient.getInstance().get(`/orders/${id}`)
    return response.data
  },

  async cancelOrder(id: string): Promise<Order> {
    const response = await apiClient.getInstance().post(`/orders/${id}/cancel`)
    return response.data
  },

  async getOrderTracking(id: string): Promise<{
    status: string
    tracking_number?: string
    estimated_delivery?: string
    updates: Array<{ date: string; status: string; message: string }>
  }> {
    const response = await apiClient.getInstance().get(`/orders/${id}/tracking`)
    return response.data
  },
}
