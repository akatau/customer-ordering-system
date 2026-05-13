import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import Table from '@mui/material/Table'
import TableBody from '@mui/material/TableBody'
import TableCell from '@mui/material/TableCell'
import TableContainer from '@mui/material/TableContainer'
import TableHead from '@mui/material/TableHead'
import TableRow from '@mui/material/TableRow'
import Paper from '@mui/material/Paper'
import Typography from '@mui/material/Typography'
import IconButton from '@mui/material/IconButton'
import Button from '@mui/material/Button'
import TextField from '@mui/material/TextField'
import Box from '@mui/material/Box'
import DeleteIcon from '@mui/icons-material/Delete'
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
          <TableContainer component={Paper} sx={{ mb: 3 }}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Product</TableCell>
                  <TableCell>Price</TableCell>
                  <TableCell>Quantity</TableCell>
                  <TableCell>Subtotal</TableCell>
                  <TableCell align="right">Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {cart.items.map((item) => (
                  <TableRow key={item.product_id}>
                    <TableCell>{item.name}</TableCell>
                    <TableCell>{formatPrice(item.price)}</TableCell>
                    <TableCell>
                      <TextField
                        type="number"
                        value={item.quantity}
                        onChange={(event) => updateItem(item.product_id, Number(event.target.value))}
                        inputProps={{ min: 1 }}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>{formatPrice(item.subtotal)}</TableCell>
                    <TableCell align="right">
                      <IconButton onClick={() => removeItem(item.product_id)}>
                        <DeleteIcon />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>

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
              <Button variant="outlined" color="secondary" onClick={() => clearCart()}>
                Clear Cart
              </Button>
              <Button variant="contained" onClick={() => navigate('/checkout')}>
                Proceed to Checkout
              </Button>
            </Box>
          </Box>
        </>
      )}
    </PageContainer>
  )
}
