/**
 * Zustand store for products state
 */

import { create } from 'zustand';
import { Product } from '@/types';
import { productApi } from '@api/products';

interface ProductsState {
  products: Product[];
  currentProduct: Product | null;
  totalProducts: number;
  currentPage: number;
  totalPages: number;
  isLoading: boolean;
  error: string | null;
  searchQuery: string;
  selectedCategory: string | null;

  // Actions
  fetchProducts: (
    page?: number,
    search?: string,
    category?: string,
    minPrice?: number,
    maxPrice?: number
  ) => Promise<void>;
  fetchProductDetail: (productId: string) => Promise<void>;
  setSearchQuery: (query: string) => void;
  setSelectedCategory: (category: string | null) => void;
  clearError: () => void;
}

export const useProductsStore = create<ProductsState>((set) => ({
  products: [],
  currentProduct: null,
  totalProducts: 0,
  currentPage: 1,
  totalPages: 1,
  isLoading: false,
  error: null,
  searchQuery: '',
  selectedCategory: null,

  fetchProducts: async (page = 1, search = '', category = '', minPrice = 0, maxPrice = 99999) => {
    set({ isLoading: true, error: null });
    const response = await productApi.listProducts(page, 20, search, category, minPrice, maxPrice);

    if (response.error) {
      set({ isLoading: false, error: response.error.detail });
      return;
    }

    if (response.data) {
      set({
        products: response.data.data,
        totalProducts: response.data.total,
        currentPage: response.data.page,
        totalPages: response.data.total_pages,
        isLoading: false,
      });
    }
  },

  fetchProductDetail: async (productId: string) => {
    set({ isLoading: true, error: null });
    const response = await productApi.getProduct(productId);

    if (response.error) {
      set({ isLoading: false, error: response.error.detail });
      return;
    }

    if (response.data) {
      set({ currentProduct: response.data, isLoading: false });
    }
  },

  setSearchQuery: (query: string) => set({ searchQuery: query }),

  setSelectedCategory: (category: string | null) => set({ selectedCategory: category }),

  clearError: () => set({ error: null }),
}));
