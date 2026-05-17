import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import Typography from '@mui/material/Typography'
import Box from '@mui/material/Box'
import { LoadingIndicator } from '@components/LoadingIndicator'
import { PageContainer } from '@components/PageContainer'
import { useCartStore } from '@store/cart'
import { formatPrice } from '@utils/helpers'

export function CartPage() {
  const navigate = useNavigate()
  const { cart, isLoading, error, fetchCart, updateItem, removeItem, clearCart } = useCartStore()

  useEffect(() => {
    fetchCart()
  }, [])

  if (isLoading) {
    return <LoadingIndicator />
  }

  return (
    <PageContainer>
      <Typography variant="h4" gutterBottom>
        Shopping Cart
      </Typography>

      {error && <Typography color="error">{error}</Typography>}
      {!cart || cart.items.length === 0 ? (
        <Typography>Your cart is empty.</Typography>
      ) : (
        <>
          <Box sx={{ mb: 3, border: '1px solid #ddd', borderRadius: 2, overflow: 'hidden' }}>
            <Box sx={{ display: 'grid', gridTemplateColumns: '2fr 1fr 1fr 1fr auto', gap: 2, p: 2, background: '#f7f7f7', fontWeight: 700 }}>
              <div>Product</div>
              <div>Price</div>
              <div>Quantity</div>
              <div>Subtotal</div>
              <div>Actions</div>
            </Box>
            {cart.items.map((item) => (
              <Box key={item.product_id} sx={{ display: 'grid', gridTemplateColumns: '2fr 1fr 1fr 1fr auto', gap: 2, p: 2, borderTop: '1px solid #eee', alignItems: 'center' }}>
                <div>{item.name}</div>
                <div>{formatPrice(item.price)}</div>
                <input
                  type="number"
                  value={item.quantity}
                  min={1}
                  onChange={(event) => updateItem(item.product_id, Number(event.target.value))}
                  style={{ width: 80, padding: '6px 8px' }}
                />
                <div>{formatPrice(item.subtotal)}</div>
                <button
                  type="button"
                  onClick={() => removeItem(item.product_id)}
                  style={{ border: '1px solid #ccc', borderRadius: 6, padding: '6px 10px', background: 'white', cursor: 'pointer' }}
                >
                  Remove
                </button>
              </Box>
            ))}
          </Box>

          <Box sx={{ display: 'flex', justifyContent: 'space-between', flexWrap: 'wrap', gap: 2 }}>
            <Box>
              <Typography>Subtotal: {formatPrice(cart.subtotal)}</Typography>
              <Typography>Tax: {formatPrice(cart.tax)}</Typography>
              <Typography>Shipping: {formatPrice(cart.shipping)}</Typography>
              {cart.discount != null && <Typography>Discount: -{formatPrice(cart.discount)}</Typography>}
              <Typography variant="h6" sx={{ mt: 1 }}>
                Total: {formatPrice(cart.total)}
              </Typography>
            </Box>
            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
              <button
                type="button"
                onClick={() => clearCart()}
                style={{ border: '1px solid #b71c1c', color: '#b71c1c', background: 'white', borderRadius: 6, padding: '10px 14px', cursor: 'pointer' }}
              >
                Clear Cart
              </button>
              <button
                type="button"
                onClick={() => navigate('/checkout')}
                style={{ border: 'none', color: 'white', background: '#1976d2', borderRadius: 6, padding: '10px 14px', cursor: 'pointer' }}
              >
                Proceed to Checkout
              </button>
            </Box>
          </Box>
        </>
      )}
    </PageContainer>
  )
}
