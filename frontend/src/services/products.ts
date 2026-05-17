import { apiClient } from './api'
import type { Product, ProductDetail, PaginatedResponse, Review } from '@/types'

interface ProductsParams {
  page?: number
  limit?: number
  category?: string
  search?: string
  sort?: string
}

export const productService = {
  async getProducts(params?: ProductsParams): Promise<PaginatedResponse<Product>> {
    const response = await apiClient.getInstance().get('/products/', { params })
    return response.data
  },

  async getProductById(id: string): Promise<ProductDetail> {
    const response = await apiClient.getInstance().get(`/products/${id}`)
    return response.data
  },

  async getCategories(): Promise<string[]> {
    const response = await apiClient.getInstance().get('/products/categories')
    return response.data
  },

  async searchProducts(query: string, limit?: number, sort?: string): Promise<Product[]> {
    try {
      const response = await apiClient.getInstance().get('/products/search', {
        params: { q: query, limit: limit || 10, sort },
      })
      return response.data
    } catch (error) {
      // Fallback for older backends that don't expose /products/search.
      const response = await apiClient.getInstance().get('/products/', {
        params: { q: query, limit: limit || 10, sort },
      })
      return response.data.data ?? response.data ?? []
    }
  },

  async addReview(productId: string, data: { rating: number; comment: string }): Promise<Review> {
    const response = await apiClient.getInstance().post(`/products/${productId}/reviews`, data)
    return response.data
  },

  async updateReview(
    productId: string,
    reviewId: string,
    data: { rating: number; comment: string }
  ): Promise<Review> {
    const response = await apiClient
      .getInstance()
      .patch(`/products/${productId}/reviews/${reviewId}`, data)
    return response.data
  },
}
