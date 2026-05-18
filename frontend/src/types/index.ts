/**
 * Core TypeScript types for the Customer Ordering System frontend
 * Aligned with backend API swagger contracts
 */

// User types
export interface User {
  id: string;
  email: string;
  username: string;
  full_name: string | null;
  role: 'customer' | 'admin' | 'support';
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  username: string;
  full_name?: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

// Product types
export interface Product {
  id: string;
  name: string;
  description: string;
  category: string;
  price: string;
  stock_quantity: number;
  image_url?: string;
  created_at: string;
  updated_at: string;
}

export interface ProductListResponse {
  data: Product[];
  total: number;
  page: number;
  limit: number;
  total_pages: number;
  has_next: boolean;
  has_previous: boolean;
}

// Cart types
export interface CartItem {
  product_id: string;
  quantity: number;
  product?: Product;
}

export interface Cart {
  items: CartItem[];
  subtotal: string;
  tax: string;
  total: string;
}

export interface AddToCartRequest {
  product_id: string;
  quantity: number;
}

// Order types
export enum OrderStatus {
  PENDING = 'pending',
  PROCESSING = 'processing',
  COMPLETED = 'completed',
  CANCELLED = 'cancelled',
}

export interface OrderItem {
  product_id: string;
  quantity: number;
  unit_price: string;
  line_total: string;
}

export interface Order {
  id: string;
  user_id: string;
  items: OrderItem[];
  status: OrderStatus;
  total_amount: string;
  shipping_address: string;
  billing_address: string;
  created_at: string;
  updated_at: string;
}

export interface CheckoutRequest {
  items: OrderItem[];
  shipping_address: string;
  billing_address: string;
  payment_method: string;
}

// Review types
export interface Review {
  id: string;
  product_id: string;
  user_id: string;
  rating: number;
  comment: string;
  created_at: string;
  updated_at: string;
}

export interface ReviewRequest {
  rating: number;
  comment: string;
}

// Profile types
export interface UserProfile {
  id: string;
  email: string;
  username: string;
  full_name: string | null;
  role: 'customer' | 'admin' | 'support';
  is_active: boolean;
  phone?: string;
  created_at: string;
  updated_at: string;
}

// API error type
export interface ApiError {
  detail: string;
  status_code?: number;
}

// API response wrapper
export interface ApiResponse<T> {
  data?: T;
  error?: ApiError;
  status: number;
}
