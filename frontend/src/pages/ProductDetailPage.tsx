/**
 * Product detail page component
 */

import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Grid,
  Typography,
  Button,
  TextField,
  Rating,
  CircularProgress,
  Alert,
  Paper,
  Divider,
} from '@mui/material';
import AddShoppingCartIcon from '@mui/icons-material/AddShoppingCart';
import { useProductsStore } from '@stores/productsStore';
import { useCartStore } from '@stores/cartStore';
import { useAuthStore } from '@stores/authStore';
import ProductReviewSection from '@components/ProductReviewSection';

const ProductDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { currentProduct, isLoading, error, fetchProductDetail } = useProductsStore();
  const { addToCart, isLoading: isAddingToCart } = useCartStore();
  const { user } = useAuthStore();
  const [quantity, setQuantity] = useState('1');

  useEffect(() => {
    if (id) {
      fetchProductDetail(id);
    }
  }, [id, fetchProductDetail]);

  const handleAddToCart = async () => {
    if (!user) {
      navigate('/login');
      return;
    }

    const qty = parseInt(quantity);
    if (qty < 1 || qty > (currentProduct?.stock_quantity || 0)) {
      alert('Invalid quantity');
      return;
    }

    const success = await addToCart(id!, qty);
    if (success) {
      alert('Added to cart successfully!');
      navigate('/cart');
    }
  };

  if (isLoading) {
    return <CircularProgress sx={{ display: 'block', mx: 'auto' }} />;
  }

  if (error || !currentProduct) {
    return <Alert severity="error">Product not found</Alert>;
  }

  return (
    <Grid container spacing={4}>
      {/* Product Image */}
      <Grid item xs={12} sm={6}>
        <Box
          sx={{
            bgcolor: '#f0f0f0',
            height: 400,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            borderRadius: 1,
          }}
        >
          <img
            src={currentProduct.image_url || 'https://via.placeholder.com/400'}
            alt={currentProduct.name}
            style={{ maxHeight: '100%', maxWidth: '100%' }}
          />
        </Box>
      </Grid>

      {/* Product Details */}
      <Grid item xs={12} sm={6}>
        <Box>
          <Typography variant="h4" gutterBottom>
            {currentProduct.name}
          </Typography>

          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
            <Rating value={4} readOnly size="small" />
            <Typography variant="body2" color="textSecondary">
              (48 reviews)
            </Typography>
          </Box>

          <Typography variant="h5" color="primary" sx={{ mb: 2 }}>
            ${parseFloat(currentProduct.price).toFixed(2)}
          </Typography>

          <Typography variant="body1" sx={{ mb: 2 }}>
            {currentProduct.description}
          </Typography>

          <Divider sx={{ my: 2 }} />

          <Box sx={{ mb: 2 }}>
            <Typography variant="body2" color="textSecondary">
              Category: {currentProduct.category}
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Stock:{' '}
              <span style={{ color: currentProduct.stock_quantity > 0 ? '#4caf50' : '#f44336' }}>
                {currentProduct.stock_quantity > 0
                  ? `${currentProduct.stock_quantity} available`
                  : 'Out of stock'}
              </span>
            </Typography>
          </Box>

          <Box sx={{ display: 'flex', gap: 2, mb: 3, alignItems: 'center' }}>
            <TextField
              label="Quantity"
              type="number"
              value={quantity}
              onChange={(e) => setQuantity(e.target.value)}
              inputProps={{ min: 1, max: currentProduct.stock_quantity }}
              sx={{ width: 100 }}
            />
            <Button
              variant="contained"
              color="primary"
              size="large"
              startIcon={<AddShoppingCartIcon />}
              onClick={handleAddToCart}
              disabled={currentProduct.stock_quantity === 0 || isAddingToCart}
            >
              {isAddingToCart ? 'Adding...' : 'Add to Cart'}
            </Button>
          </Box>

          <Paper sx={{ p: 2, bgcolor: '#f9f9f9' }}>
            <Typography variant="body2">
              <strong>✓</strong> Free shipping on orders over $50
            </Typography>
            <Typography variant="body2">
              <strong>✓</strong> 30-day money-back guarantee
            </Typography>
            <Typography variant="body2">
              <strong>✓</strong> Secure checkout
            </Typography>
          </Paper>
        </Box>
      </Grid>

      {/* Reviews Section */}
      <Grid item xs={12}>
        <Divider sx={{ my: 4 }} />
        <ProductReviewSection productId={id ?? ''} />
      </Grid>
    </Grid>
  );
};

export default ProductDetailPage;
