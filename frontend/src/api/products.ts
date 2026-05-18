/**
 * Product API endpoints
 */

import { apiClient } from './client';
import { Product, ProductListResponse, Review, ReviewRequest, ApiResponse } from '@/types';

export const productApi = {
  async listProducts(
    page: number = 1,
    limit: number = 20,
    search?: string,
    category?: string,
    minPrice?: number,
    maxPrice?: number,
    sortBy?: string
  ): Promise<ApiResponse<ProductListResponse>> {
    return apiClient.get<ProductListResponse>('/products', {
      page,
      limit,
      q: search,
      category,
      min_price: minPrice,
      max_price: maxPrice,
      sort_by: sortBy,
    });
  },

  async getProduct(productId: string): Promise<ApiResponse<Product>> {
    return apiClient.get<Product>(`/products/${productId}`);
  },

  async getProductReviews(productId: string, page: number = 1): Promise<ApiResponse<any>> {
    return apiClient.get(`/reviews/products/${productId}`, { page });
  },

  async submitReview(productId: string, review: ReviewRequest): Promise<ApiResponse<Review>> {
    return apiClient.post<Review>(`/reviews/products/${productId}`, review);
  },

  async updateReview(reviewId: string, review: ReviewRequest): Promise<ApiResponse<Review>> {
    return apiClient.put<Review>(`/reviews/${reviewId}`, review);
  },

  async deleteReview(reviewId: string): Promise<ApiResponse<{ message: string }>> {
    return apiClient.delete<{ message: string }>(`/reviews/${reviewId}`);
  },
};
