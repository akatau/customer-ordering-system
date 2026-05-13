import { apiClient } from './api'
import type { CartSummary, CartItem } from '@/types'

export const cartService = {
  async getCart(): Promise<CartSummary> {
    const response = await apiClient.getInstance().get('/cart')
    return response.data
  },

  async addItem(productId: string, quantity: number): Promise<CartSummary> {
    const response = await apiClient.getInstance().post('/cart/items', {
      product_id: productId,
      quantity,
    })
    return response.data
  },

  async updateItem(productId: string, quantity: number): Promise<CartSummary> {
    const response = await apiClient
      .getInstance()
      .put(`/cart/items/${productId}`, { quantity })
    return response.data
  },

  async removeItem(productId: string): Promise<CartSummary> {
    const response = await apiClient.getInstance().delete(`/cart/items/${productId}`)
    return response.data
  },

  async clearCart(): Promise<{ message: string }> {
    const response = await apiClient.getInstance().delete('/cart')
    return response.data
  },

  async applyDiscount(code: string): Promise<CartSummary> {
    const response = await apiClient.getInstance().post('/cart/discount', { code })
    return response.data
  },

  async removeDiscount(): Promise<CartSummary> {
    const response = await apiClient.getInstance().delete('/cart/discount')
    return response.data
  },
}
