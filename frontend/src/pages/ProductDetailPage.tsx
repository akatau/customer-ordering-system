import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import Grid from '@mui/material/Grid'
import Typography from '@mui/material/Typography'
import TextField from '@mui/material/TextField'
import Button from '@mui/material/Button'
import Box from '@mui/material/Box'
import Card from '@mui/material/Card'
import CardMedia from '@mui/material/CardMedia'
import CardContent from '@mui/material/CardContent'
import { LoadingIndicator } from '@components/LoadingIndicator'
import { PageContainer } from '@components/PageContainer'
import { useProductsStore } from '@store/products'
import { useCartStore } from '@store/cart'
import { formatPrice } from '@utils/helpers'

export function ProductDetailPage() {
  const { productId } = useParams()
  const navigate = useNavigate()
  const [quantity, setQuantity] = useState(1)
  const { selectedProduct, fetchProductById, isLoading, error } = useProductsStore()
  const { addItem } = useCartStore()

  useEffect(() => {
    if (productId) {
      fetchProductById(productId)
    }
  }, [productId])

  const handleAddToCart = async () => {
    if (!selectedProduct) return
    await addItem(selectedProduct.id, quantity)
    navigate('/cart')
  }

  const isInStock = (selectedProduct?.stock_quantity ?? 0) > 0

  if (isLoading) {
    return <LoadingIndicator />
  }

  if (error) {
    return (
      <PageContainer>
        <Typography color="error">{error}</Typography>
      </PageContainer>
    )
  }

  if (!selectedProduct) {
    return (
      <PageContainer>
        <Typography>Product not found.</Typography>
      </PageContainer>
    )
  }

  return (
    <PageContainer>
      <Grid container spacing={4}>
        <Grid item xs={12} md={6}>
          <Card>
            <img
              src={selectedProduct.image_url || ''}
              alt={selectedProduct.name}
              onError={(e) => {
                const t = e.currentTarget as HTMLImageElement
                t.onerror = null
                const slug = selectedProduct.name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '')
                t.src = `/images/${slug}.svg`
                setTimeout(() => {
                  if (!t.naturalWidth || t.naturalWidth === 0) {
                    t.src = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="800" height="400"><rect width="100%" height="100%" fill="%23f3f4f6"/><text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="24" fill="%23888">Image unavailable</text></svg>'
                  }
                }, 200)
              }}
              style={{ width: '100%', height: 360, objectFit: 'cover', display: 'block' }}
            />
            <CardContent>
              <Typography variant="h4" gutterBottom>
                {selectedProduct.name}
              </Typography>
              <Typography variant="body1" color="text.secondary" paragraph>
                {selectedProduct.description}
              </Typography>
              <Typography variant="h5" fontWeight={700} sx={{ mt: 2 }}>
                {formatPrice(selectedProduct.price)}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <Typography variant="subtitle1">Category: {selectedProduct.category}</Typography>
            <Typography>Stock: {isInStock ? 'Available' : 'Out of stock'}</Typography>
            <TextField
              label="Quantity"
              type="number"
              value={quantity}
              onChange={(event) => setQuantity(Number(event.target.value))}
              inputProps={{ min: 1, max: selectedProduct.stock_quantity }}
              fullWidth
            />
            <Button variant="contained" size="large" onClick={handleAddToCart} disabled={!isInStock}>
              Add to Cart
            </Button>
          </Box>
        </Grid>
      </Grid>
    </PageContainer>
  )
}
