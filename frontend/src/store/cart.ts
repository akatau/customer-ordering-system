import { create } from 'zustand'
import type { CartSummary, CartItem } from '@/types'
import { cartService } from '@services/cart'

interface CartState {
  cart: CartSummary | null
  isLoading: boolean
  error: string | null
  fetchCart: () => Promise<void>
  addItem: (productId: string, quantity: number) => Promise<void>
  updateItem: (productId: string, quantity: number) => Promise<void>
  removeItem: (productId: string) => Promise<void>
  clearCart: () => Promise<void>
  applyDiscount: (code: string) => Promise<void>
  removeDiscount: () => Promise<void>
  getItemCount: () => number
  getTotal: () => number
}

export const useCartStore = create<CartState>((set, get) => ({
  cart: null,
  isLoading: false,
  error: null,

  fetchCart: async () => {
    set({ isLoading: true, error: null })
    try {
      const cart = await cartService.getCart()
      set({ cart, isLoading: false })
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to fetch cart',
        isLoading: false,
      })
    }
  },

  addItem: async (productId: string, quantity: number) => {
    set({ isLoading: true, error: null })
    try {
      const cart = await cartService.addItem(productId, quantity)
      set({ cart, isLoading: false })
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to add item',
        isLoading: false,
      })
      throw error
    }
  },

  updateItem: async (productId: string, quantity: number) => {
    set({ isLoading: true })
    try {
      const cart = await cartService.updateItem(productId, quantity)
      set({ cart, isLoading: false })
    } catch (error) {
      set({ error: error instanceof Error ? error.message : 'Failed to update item' })
      throw error
    }
  },

  removeItem: async (productId: string) => {
    set({ isLoading: true })
    try {
      const cart = await cartService.removeItem(productId)
      set({ cart, isLoading: false })
    } catch (error) {
      set({ error: error instanceof Error ? error.message : 'Failed to remove item' })
      throw error
    }
  },

  clearCart: async () => {
    set({ isLoading: true })
    try {
      await cartService.clearCart()
      set({ cart: null, isLoading: false })
    } catch (error) {
      set({ error: error instanceof Error ? error.message : 'Failed to clear cart' })
      throw error
    }
  },

  applyDiscount: async (code: string) => {
    set({ isLoading: true })
    try {
      const cart = await cartService.applyDiscount(code)
      set({ cart, isLoading: false })
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to apply discount',
      })
      throw error
    }
  },

  removeDiscount: async () => {
    set({ isLoading: true })
    try {
      const cart = await cartService.removeDiscount()
      set({ cart, isLoading: false })
    } catch (error) {
      set({ error: error instanceof Error ? error.message : 'Failed to remove discount' })
      throw error
    }
  },

  getItemCount: () => {
    const { cart } = get()
    return cart?.items.reduce((acc, item) => acc + item.quantity, 0) || 0
  },

  getTotal: () => {
    const { cart } = get()
    return cart?.total || 0
  },
}))
