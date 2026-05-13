import { create } from 'zustand'
import type { Order } from '@/types'
import { orderService } from '@services/orders'

interface OrdersState {
  orders: Order[]
  selectedOrder: Order | null
  isLoading: boolean
  error: string | null
  fetchOrders: (page?: number) => Promise<void>
  fetchOrderById: (id: string) => Promise<void>
  cancelOrder: (id: string) => Promise<void>
  getOrderTracking: (id: string) => Promise<any>
}

export const useOrdersStore = create<OrdersState>((set) => ({
  orders: [],
  selectedOrder: null,
  isLoading: false,
  error: null,

  fetchOrders: async (page = 1) => {
    set({ isLoading: true, error: null })
    try {
      const response = await orderService.getOrders({ page })
      set({ orders: response.data, isLoading: false })
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to fetch orders',
        isLoading: false,
      })
    }
  },

  fetchOrderById: async (id: string) => {
    set({ isLoading: true })
    try {
      const order = await orderService.getOrderById(id)
      set({ selectedOrder: order, isLoading: false })
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to fetch order',
        isLoading: false,
      })
    }
  },

  cancelOrder: async (id: string) => {
    set({ isLoading: true })
    try {
      const order = await orderService.cancelOrder(id)
      set({ selectedOrder: order, isLoading: false })
    } catch (error) {
      set({ error: error instanceof Error ? error.message : 'Failed to cancel order' })
      throw error
    }
  },

  getOrderTracking: async (id: string) => {
    try {
      const tracking = await orderService.getOrderTracking(id)
      return tracking
    } catch (error) {
      throw error
    }
  },
}))
