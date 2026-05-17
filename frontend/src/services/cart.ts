import { apiClient } from './api'
import type { CartSummary, CartItem } from '@/types'

type CartApiItem = {
  product_id: string
  quantity: number
  name?: string | null
  price?: number | null
}

type CartApiResponse = {
  user_id?: string
  items: CartApiItem[]
  total?: number
  subtotal?: number
  tax?: number
  shipping?: number
  discount?: number
}

function normalizeCart(response: CartApiResponse): CartSummary {
  const items = response.items.map((item) => {
    const price = Number(item.price ?? 0)
    const quantity = Number(item.quantity ?? 0)
    return {
      product_id: item.product_id,
      name: item.name ?? 'Unknown product',
      price,
      quantity,
      image_url: '',
      subtotal: price * quantity,
    }
  })

  const subtotal = response.subtotal ?? items.reduce((sum, item) => sum + item.subtotal, 0)
  const tax = response.tax ?? 0
  const shipping = response.shipping ?? 0
  const total = response.total ?? subtotal + tax + shipping - (response.discount ?? 0)

  return {
    items,
    subtotal,
    tax,
    shipping,
    total,
    ...(response.discount != null ? { discount: response.discount } : {}),
  }
}

export const cartService = {
  async getCart(): Promise<CartSummary> {
    const response = await apiClient.getInstance().get('/cart')
    return normalizeCart(response.data)
  },

  async addItem(productId: string, quantity: number): Promise<CartSummary> {
    const response = await apiClient.getInstance().post('/cart/items', {
      product_id: productId,
      quantity,
    })
    return normalizeCart(response.data)
  },

  async updateItem(productId: string, quantity: number): Promise<CartSummary> {
    const response = await apiClient
      .getInstance()
      .put(`/cart/items/${productId}`, { quantity })
    return normalizeCart(response.data)
  },

  async removeItem(productId: string): Promise<CartSummary> {
    const response = await apiClient.getInstance().delete(`/cart/items/${productId}`)
    return normalizeCart(response.data)
  },

  async clearCart(): Promise<CartSummary> {
    const response = await apiClient.getInstance().post('/cart/clear')
    return normalizeCart(response.data)
  },

  async applyDiscount(code: string): Promise<CartSummary> {
    const response = await apiClient.getInstance().post('/cart/discount', { code })
    return normalizeCart(response.data)
  },

  async removeDiscount(): Promise<CartSummary> {
    const response = await apiClient.getInstance().delete('/cart/discount')
    return normalizeCart(response.data)
  },
}
