/**
 * API client for communicating with backend services
 * Handles authentication, error handling, and request/response formatting
 */

import axios, { AxiosInstance, AxiosError } from 'axios';
import { ApiError, ApiResponse } from '@/types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const API_TIMEOUT = import.meta.env.VITE_API_TIMEOUT ? Number(import.meta.env.VITE_API_TIMEOUT) : 30000;

class ApiClient {
  private client: AxiosInstance;
  private token: string | null = null;

  constructor() {
    this.client = axios.create({
      baseURL: `${API_BASE_URL}/api/v1`,
      timeout: API_TIMEOUT,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add request interceptor for authentication
    this.client.interceptors.request.use((config) => {
      if (this.token) {
        config.headers.Authorization = `Bearer ${this.token}`;
      }
      return config;
    });

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response?.status === 401) {
          // Token expired or invalid - clear and redirect to login
          this.clearToken();
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );

    // Load token from localStorage on initialization
    this.loadToken();
  }

  setToken(token: string): void {
    this.token = token;
    localStorage.setItem('auth_token', token);
  }

  getToken(): string | null {
    return this.token;
  }

  clearToken(): void {
    this.token = null;
    localStorage.removeItem('auth_token');
  }

  private loadToken(): void {
    this.token = localStorage.getItem('auth_token');
  }

  async get<T>(url: string, params?: Record<string, any>): Promise<ApiResponse<T>> {
    try {
      const response = await this.client.get<T>(url, { params });
      return {
        data: response.data,
        status: response.status,
      };
    } catch (error) {
      return this.handleError(error);
    }
  }

  async post<T>(url: string, data?: Record<string, any>): Promise<ApiResponse<T>> {
    try {
      const response = await this.client.post<T>(url, data);
      return {
        data: response.data,
        status: response.status,
      };
    } catch (error) {
      return this.handleError(error);
    }
  }

  async put<T>(url: string, data?: Record<string, any>): Promise<ApiResponse<T>> {
    try {
      const response = await this.client.put<T>(url, data);
      return {
        data: response.data,
        status: response.status,
      };
    } catch (error) {
      return this.handleError(error);
    }
  }

  async delete<T>(url: string): Promise<ApiResponse<T>> {
    try {
      const response = await this.client.delete<T>(url);
      return {
        data: response.data,
        status: response.status,
      };
    } catch (error) {
      return this.handleError(error);
    }
  }

  private handleError(error: any): ApiResponse<any> {
    if (axios.isAxiosError(error)) {
      const apiError: ApiError = {
        detail: error.response?.data?.detail || error.message || 'Unknown error occurred',
        status_code: error.response?.status,
      };
      return {
        error: apiError,
        status: error.response?.status || 500,
      };
    }

    return {
      error: {
        detail: 'An unexpected error occurred',
      },
      status: 500,
    };
  }
}

export const apiClient = new ApiClient();
