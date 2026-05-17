import { apiClient } from './api'
import type { Order, PaginatedResponse, Address } from '@/types'

interface CreateOrderRequest {
  items: Array<{ product_id: string; quantity: number }>
  shipping_address: string
  billing_address?: string
  payment_method: string
}

interface OrdersParams {
  page?: number
  limit?: number
  status?: string
}

type BackendOrderItem = {
  product_id: string
  product_name: string
  quantity: number
  unit_price: string | number
  total_price: string | number
}

type BackendOrder = {
  id: string
  user_id: string
  shipping_address: string
  billing_address?: string | null
  status: string
  total_amount: string | number
  items: BackendOrderItem[]
  created_at: string
  updated_at: string
}

function normalizeAddress(address: string): Address {
  return {
    street: address,
    city: '',
    state: '',
    zip_code: '',
    country: '',
  }
}

function normalizeOrder(order: BackendOrder): Order {
  return {
    id: order.id,
    order_number: order.id.slice(0, 8).toUpperCase(),
    user_id: order.user_id,
    status: order.status as Order['status'],
    items: order.items.map((item) => ({
      product_id: item.product_id,
      name: item.product_name,
      price: Number(item.unit_price),
      quantity: Number(item.quantity),
      image_url: '',
      subtotal: Number(item.total_price),
    })),
    total: Number(order.total_amount),
    shipping_address: normalizeAddress(order.shipping_address),
    created_at: order.created_at,
    updated_at: order.updated_at,
  }
}

export const orderService = {
  async createOrder(data: CreateOrderRequest): Promise<Order> {
    const response = await apiClient.getInstance().post('/orders/', data)
    return normalizeOrder(response.data)
  },

  async getOrders(params?: OrdersParams): Promise<{ data: Order[] }> {
    const response = await apiClient.getInstance().get('/orders/', { params })
    const orders = Array.isArray(response.data) ? response.data.map(normalizeOrder) : []
    return { data: orders }
  },

  async getOrderById(id: string): Promise<Order> {
    const response = await apiClient.getInstance().get(`/orders/${id}`)
    return normalizeOrder(response.data)
  },

  async cancelOrder(id: string): Promise<Order> {
    const response = await apiClient.getInstance().post(`/orders/${id}/cancel`)
    return normalizeOrder(response.data)
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
