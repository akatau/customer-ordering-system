/**
 * Zustand store for orders state
 */

import { create } from 'zustand';
import { Order, CheckoutRequest } from '@/types';
import { orderApi } from '@api/orders';

interface OrdersState {
  orders: Order[];
  currentOrder: Order | null;
  totalOrders: number;
  currentPage: number;
  isLoading: boolean;
  error: string | null;

  // Actions
  fetchOrders: (page?: number) => Promise<void>;
  fetchOrderDetail: (orderId: string) => Promise<void>;
  fetchOrderTracking: (orderId: string) => Promise<any>;
  createOrder: (checkoutData: CheckoutRequest) => Promise<boolean>;
  clearError: () => void;
}

export const useOrdersStore = create<OrdersState>((set) => ({
  orders: [],
  currentOrder: null,
  totalOrders: 0,
  currentPage: 1,
  isLoading: false,
  error: null,

  fetchOrders: async (page = 1) => {
    set({ isLoading: true, error: null });
    const response = await orderApi.listOrders(page);

    if (response.error) {
      set({ isLoading: false, error: response.error.detail });
      return;
    }

    if (response.data) {
      set({
        orders: response.data.orders,
        totalOrders: response.data.total,
        currentPage: page,
        isLoading: false,
      });
    }
  },

  fetchOrderDetail: async (orderId: string) => {
    set({ isLoading: true, error: null });
    const response = await orderApi.getOrder(orderId);

    if (response.error) {
      set({ isLoading: false, error: response.error.detail });
      return;
    }

    if (response.data) {
      set({ currentOrder: response.data, isLoading: false });
    }
  },

  fetchOrderTracking: async (orderId: string) => {
    set({ isLoading: true, error: null });
    const response = await orderApi.getOrderTracking(orderId);

    if (response.error) {
      set({ isLoading: false, error: response.error.detail });
      return {};
    }

    set({ isLoading: false });
    return response.data;
  },

  createOrder: async (checkoutData: CheckoutRequest) => {
    set({ isLoading: true, error: null });
    const response = await orderApi.createOrder(checkoutData);

    if (response.error) {
      set({ isLoading: false, error: response.error.detail });
      return false;
    }

    if (response.data) {
      set({ currentOrder: response.data, isLoading: false });
      return true;
    }

    return false;
  },

  clearError: () => set({ error: null }),
}));
