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
        <CardMedia component="img" height="180" image={product.image_url} alt={product.name} />
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
