/**
 * Product catalog page component
 */

import React, { useEffect, useState } from 'react';
import {
  Grid,
  Card,
  CardMedia,
  CardContent,
  CardActions,
  Button,
  Typography,
  Box,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  CircularProgress,
  Alert,
  Pagination,
} from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import AddShoppingCartIcon from '@mui/icons-material/AddShoppingCart';
import { useProductsStore } from '@stores/productsStore';
import { useCartStore } from '@stores/cartStore';
import { useAuthStore } from '@stores/authStore';

const ProductCatalogPage: React.FC = () => {
  const {
    products,
    isLoading,
    error,
    totalPages,
    currentPage,
    searchQuery,
    fetchProducts,
    setSearchQuery,
    setSelectedCategory,
  } = useProductsStore();

  const { addToCart } = useCartStore();
  const { user } = useAuthStore();
  const [quantity, setQuantity] = useState<Record<string, number>>({});
  const [addingToCart, setAddingToCart] = useState<string | null>(null);
  const [categoryFilter, setCategoryFilter] = useState('');

  useEffect(() => {
    fetchProducts(currentPage, searchQuery, categoryFilter);
  }, [currentPage, searchQuery, categoryFilter, fetchProducts]);

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(e.target.value);
  };

  const handleCategoryChange = (e: any) => {
    setCategoryFilter(e.target.value);
    setSelectedCategory(e.target.value || null);
  };

  const handleAddToCart = async (productId: string) => {
    if (!user) {
      alert('Please login to add items to cart');
      return;
    }

    setAddingToCart(productId);
    const qty = quantity[productId] || 1;
    const success = await addToCart(productId, qty);
    setAddingToCart(null);

    if (success) {
      setQuantity((prev) => ({ ...prev, [productId]: 1 }));
      alert('Added to cart successfully!');
    }
  };

  if (isLoading && products.length === 0) {
    return <CircularProgress sx={{ display: 'block', mx: 'auto' }} />;
  }

  return (
    <Box>
      {/* Filters */}
      <Box sx={{ display: 'flex', gap: 2, mb: 4, flexWrap: 'wrap' }}>
        <TextField
          label="Search products"
          variant="outlined"
          value={searchQuery}
          onChange={handleSearch}
          sx={{ flex: 1, minWidth: 200 }}
        />

        <FormControl sx={{ minWidth: 200 }}>
          <InputLabel>Category</InputLabel>
          <Select value={categoryFilter} onChange={handleCategoryChange} label="Category">
            <MenuItem value="">All Categories</MenuItem>
            <MenuItem value="Electronics">Electronics</MenuItem>
            <MenuItem value="Books">Books</MenuItem>
            <MenuItem value="Clothing">Clothing</MenuItem>
            <MenuItem value="Home">Home & Garden</MenuItem>
            <MenuItem value="Sports">Sports</MenuItem>
          </Select>
        </FormControl>
      </Box>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      {/* Products Grid */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {products.map((product) => (
          <Grid item xs={12} sm={6} md={4} lg={3} key={product.id}>
            <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <CardMedia
                sx={{ height: 200, backgroundColor: '#f0f0f0 ', cursor: 'pointer' }}
                title={product.name}
                image={product.image_url || 'https://via.placeholder.com/200'}
                component={RouterLink}
                to={`/products/${product.id}`}
              />
              <CardContent sx={{ flexGrow: 1 }}>
                <Typography variant="h6" gutterBottom noWrap>
                  {product.name}
                </Typography>
                <Typography variant="body2" color="textSecondary" sx={{ mb: 1 }}>
                  {product.description?.substring(0, 100)}...
                </Typography>
                <Typography variant="h6" color="primary">
                  ${parseFloat(product.price).toFixed(2)}
                </Typography>
                <Typography
                  variant="body2"
                  color={product.stock_quantity > 0 ? 'success.main' : 'error.main'}
                >
                  {product.stock_quantity > 0
                    ? `${product.stock_quantity} in stock`
                    : 'Out of stock'}
                </Typography>
              </CardContent>
              <CardActions>
                <Button
                  component={RouterLink}
                  to={`/products/${product.id}`}
                  size="small"
                  color="primary"
                >
                  View Details
                </Button>
                <Button
                  size="small"
                  color="primary"
                  variant="contained"
                  startIcon={<AddShoppingCartIcon />}
                  onClick={() => handleAddToCart(product.id)}
                  disabled={product.stock_quantity === 0 || addingToCart === product.id}
                >
                  {addingToCart === product.id ? 'Adding...' : 'Add'}
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Pagination */}
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <Pagination
          count={totalPages}
          page={currentPage}
          onChange={(_, page) => {
            fetchProducts(page, searchQuery, categoryFilter);
          }}
        />
      </Box>
    </Box>
  );
};

export default ProductCatalogPage;
