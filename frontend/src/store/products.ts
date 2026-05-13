import { create } from 'zustand'
import type { Product, ProductDetail } from '@/types'
import { productService } from '@services/products'

interface ProductsState {
  products: Product[]
  selectedProduct: ProductDetail | null
  categories: string[]
  isLoading: boolean
  error: string | null
  totalPages: number
  currentPage: number
  fetchProducts: (
    page?: number,
    category?: string,
    search?: string,
    sort?: string
  ) => Promise<void>
  fetchProductById: (id: string) => Promise<void>
  fetchCategories: () => Promise<void>
  searchProducts: (query: string) => Promise<void>
  setProducts: (products: Product[]) => void
}

export const useProductsStore = create<ProductsState>((set) => ({
  products: [],
  selectedProduct: null,
  categories: [],
  isLoading: false,
  error: null,
  totalPages: 0,
  currentPage: 1,

  fetchProducts: async (page = 1, category?: string, search?: string, sort?: string) => {
    set({ isLoading: true, error: null })
    try {
      const response = await productService.getProducts({
        page,
        category,
        search,
        sort,
      })
      set({
        products: response.data,
        totalPages: response.pagination.total_pages,
        currentPage: page,
        isLoading: false,
      })
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to fetch products',
        isLoading: false,
      })
    }
  },

  fetchProductById: async (id: string) => {
    set({ isLoading: true, error: null })
    try {
      const product = await productService.getProductById(id)
      set({ selectedProduct: product, isLoading: false })
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to fetch product',
        isLoading: false,
      })
    }
  },

  fetchCategories: async () => {
    try {
      const categories = await productService.getCategories()
      set({ categories })
    } catch (error) {
      console.error('Failed to fetch categories:', error)
    }
  },

  searchProducts: async (query: string) => {
    set({ isLoading: true, error: null })
    try {
      const results = await productService.searchProducts(query)
      set({ products: results, isLoading: false })
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Search failed',
        isLoading: false,
      })
    }
  },

  setProducts: (products: Product[]) => set({ products }),
}))
