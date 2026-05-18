/**
 * Cart API endpoints
 */

import { apiClient } from './client';
import { Cart, AddToCartRequest, ApiResponse } from '@/types';

export const cartApi = {
  async getCart(): Promise<ApiResponse<Cart>> {
    return apiClient.get<Cart>('/cart');
  },

  async addToCart(item: AddToCartRequest): Promise<ApiResponse<Cart>> {
    return apiClient.post<Cart>('/cart/items', item);
  },

  async updateCartItem(productId: string, quantity: number): Promise<ApiResponse<Cart>> {
    return apiClient.put<Cart>(`/cart/items/${productId}`, { quantity });
  },

  async removeFromCart(productId: string): Promise<ApiResponse<Cart>> {
    return apiClient.delete<Cart>(`/cart/items/${productId}`);
  },

  async clearCart(): Promise<ApiResponse<{ message: string }>> {
    return apiClient.post<{ message: string }>('/cart/clear');
  },
};
