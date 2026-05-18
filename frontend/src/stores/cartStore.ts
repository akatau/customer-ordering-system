/**
 * Zustand store for shopping cart state
 */

import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { Cart } from '@/types';
import { cartApi } from '@api/cart';

interface CartState {
  cart: Cart | null;
  isLoading: boolean;
  error: string | null;

  // Actions
  loadCart: () => Promise<void>;
  addToCart: (productId: string, quantity: number) => Promise<boolean>;
  updateCartItem: (productId: string, quantity: number) => Promise<boolean>;
  removeFromCart: (productId: string) => Promise<boolean>;
  clearCart: () => Promise<boolean>;
  clearError: () => void;
}

export const useCartStore = create<CartState>()(
  persist(
    (set) => ({
      cart: null,
      isLoading: false,
      error: null,

      loadCart: async () => {
        set({ isLoading: true, error: null });
        const response = await cartApi.getCart();

        if (response.error) {
          set({ isLoading: false, error: response.error.detail });
          return;
        }

        if (response.data) {
          set({ cart: response.data, isLoading: false });
        }
      },

      addToCart: async (productId: string, quantity: number) => {
        set({ isLoading: true, error: null });
        const response = await cartApi.addToCart({ product_id: productId, quantity });

        if (response.error) {
          set({ isLoading: false, error: response.error.detail });
          return false;
        }

        if (response.data) {
          set({ cart: response.data, isLoading: false });
          return true;
        }

        return false;
      },

      updateCartItem: async (productId: string, quantity: number) => {
        set({ isLoading: true, error: null });
        const response = await cartApi.updateCartItem(productId, quantity);

        if (response.error) {
          set({ isLoading: false, error: response.error.detail });
          return false;
        }

        if (response.data) {
          set({ cart: response.data, isLoading: false });
          return true;
        }

        return false;
      },

      removeFromCart: async (productId: string) => {
        set({ isLoading: true, error: null });
        const response = await cartApi.removeFromCart(productId);

        if (response.error) {
          set({ isLoading: false, error: response.error.detail });
          return false;
        }

        if (response.data) {
          set({ cart: response.data, isLoading: false });
          return true;
        }

        return false;
      },

      clearCart: async () => {
        set({ isLoading: true, error: null });
        const response = await cartApi.clearCart();

        if (response.error) {
          set({ isLoading: false, error: response.error.detail });
          return false;
        }

        set({ cart: null, isLoading: false });
        return true;
      },

      clearError: () => set({ error: null }),
    }),
    {
      name: 'cart-store',
      partialize: (state) => ({
        cart: state.cart,
      }),
    }
  )
);
