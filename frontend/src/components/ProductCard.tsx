import { Link as RouterLink } from 'react-router-dom'
import Card from '@mui/material/Card'
import CardActionArea from '@mui/material/CardActionArea'
import CardContent from '@mui/material/CardContent'
import CardMedia from '@mui/material/CardMedia'
import Typography from '@mui/material/Typography'
import Button from '@mui/material/Button'
import Box from '@mui/material/Box'
import type { Product } from '@/types'
import { formatPrice, truncateText } from '@utils/helpers'
import { useCartStore } from '@store/cart'
import { useState } from 'react'

interface Props {
  product: Product
}

export function ProductCard({ product }: Props) {
  const [isAdding, setIsAdding] = useState(false)
  const addItem = useCartStore((state) => state.addItem)
  const isInStock = product.stock_quantity > 0

  const handleAddToCart = async () => {
    setIsAdding(true)
    try {
      await addItem(product.id, 1)
    } finally {
      setIsAdding(false)
    }
  }

  return (
    <Card>
      <CardActionArea component={RouterLink} to={`/products/${product.id}`}>
        <Box sx={{ position: 'relative' }}>
          <img
            src={product.image_url || ''}
            alt={product.name}
            onError={(e) => {
              const target = e.currentTarget as HTMLImageElement
              target.onerror = null
              const slug = product.name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '')
              // try local public image first
              target.src = `/images/${slug}.svg`
              // later, if that also fails, fallback to inline SVG
              setTimeout(() => {
                if (!target.naturalWidth || target.naturalWidth === 0) {
                  target.src = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400"><rect width="100%" height="100%" fill="%23f3f4f6"/><text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="20" fill="%23888">Image unavailable</text></svg>'
                }
              }, 200)
            }}
            style={{ width: '100%', height: 180, objectFit: 'cover', display: 'block', borderTopLeftRadius: 4, borderTopRightRadius: 4 }}
          />
          <Box
            sx={{
              position: 'absolute',
              left: 0,
              right: 0,
              bottom: 0,
              bgcolor: 'rgba(0,0,0,0.45)',
              color: 'common.white',
              py: 1,
              px: 2,
            }}
          >
            <Typography variant="subtitle1" sx={{ color: 'common.white' }}>
              {product.name}
            </Typography>
          </Box>
        </Box>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            {product.name}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {truncateText(product.description, 100)}
          </Typography>
        </CardContent>
      </CardActionArea>
      <Box sx={{ p: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 1 }}>
        <Typography variant="subtitle1" fontWeight={700}>
          {formatPrice(product.price)}
        </Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button size="small" variant="outlined" component={RouterLink} to={`/products/${product.id}`}>
            View
          </Button>
          <Button size="small" variant="contained" onClick={handleAddToCart} disabled={isAdding || !isInStock}>
            {isAdding ? 'Adding...' : 'Add to Cart'}
          </Button>
        </Box>
      </Box>
    </Card>
  )
}
