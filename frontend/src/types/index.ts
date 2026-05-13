// User Types
export interface User {
  id: string
  email: string
  name: string
  phone?: string
  role: 'customer' | 'admin' | 'support'
  created_at: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  expires_in: number
  user: User
}

export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest {
  email: string
  password: string
  name: string
}

// Product Types
export interface Product {
  id: string
  name: string
  description: string
  price: number
  category: string
  image_url: string
  images?: string[]
  in_stock: boolean
  stock_quantity: number
  specifications?: Record<string, string>
  rating?: number
  reviews_count?: number
}

export interface ProductDetail extends Product {
  reviews: Review[]
  related_products?: Product[]
}

export interface Review {
  id: string
  rating: number
  comment: string
  user_name: string
  date: string
  user_id?: string
}

// Cart Types
export interface CartItem {
  product_id: string
  name: string
  price: number
  quantity: number
  image_url: string
  subtotal: number
}

export interface CartSummary {
  items: CartItem[]
  subtotal: number
  tax: number
  shipping: number
  total: number
  discount?: number
}

// Order Types
export interface Order {
  id: string
  order_number: string
  user_id: string
  status: 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled'
  items: CartItem[]
  total: number
  shipping_address: Address
  created_at: string
  updated_at: string
  tracking_number?: string
}

export interface Address {
  street: string
  city: string
  state: string
  zip_code: string
  country: string
  is_default?: boolean
}

// Payment Types
export interface PaymentMethod {
  id: string
  type: 'credit_card' | 'paypal' | 'apple_pay'
  last_four?: string
  is_default?: boolean
}

// Pagination
export interface PaginatedResponse<T> {
  data: T[]
  pagination: {
    page: number
    limit: number
    total: number
    total_pages: number
  }
}

// API Error
export interface ApiError {
  error: string
  message: string
  details?: Record<string, unknown>
}
