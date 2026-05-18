/**
 * Product catalog page component
 */

import React, { useEffect, useRef, useState } from 'react';
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
  Alert,
  Pagination,
  Skeleton,
  Stack,
} from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import AddShoppingCartIcon from '@mui/icons-material/AddShoppingCart';
import { useProductsStore } from '@stores/productsStore';
import { useCartStore } from '@stores/cartStore';
import { useAuthStore } from '@stores/authStore';
import useDebouncedValue from '@hooks/useDebouncedValue';

const CatalogSkeleton = () => (
  <Grid container spacing={3} sx={{ mb: 4 }}>
    {Array.from({ length: 8 }).map((_, index) => (
      <Grid item xs={12} sm={6} md={4} lg={3} key={index}>
        <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
          <Skeleton variant="rectangular" height={200} />
          <CardContent sx={{ flexGrow: 1 }}>
            <Stack spacing={1}>
              <Skeleton variant="text" height={36} width="80%" />
              <Skeleton variant="text" height={22} width="95%" />
              <Skeleton variant="text" height={28} width="40%" />
              <Skeleton variant="text" height={20} width="50%" />
            </Stack>
          </CardContent>
          <CardActions>
            <Skeleton variant="rounded" width={96} height={36} />
            <Skeleton variant="rounded" width={96} height={36} />
          </CardActions>
        </Card>
      </Grid>
    ))}
  </Grid>
);

const ProductCatalogPage: React.FC = () => {
  const {
    products,
    isLoading,
    error,
    totalPages,
    currentPage,
    fetchProducts,
    setSearchQuery,
    setSelectedCategory,
  } = useProductsStore();

  const { addToCart } = useCartStore();
  const { user } = useAuthStore();
  const [quantity, setQuantity] = useState<Record<string, number>>({});
  const [addingToCart, setAddingToCart] = useState<string | null>(null);
  const [categoryFilter, setCategoryFilter] = useState('');
  const [searchInput, setSearchInput] = useState('');
  const debouncedSearch = useDebouncedValue(searchInput, 300);
  const hasHandledDebouncedSearch = useRef(false);

  useEffect(() => {
    fetchProducts(1, '', '');
  }, [fetchProducts]);

  useEffect(() => {
    if (!hasHandledDebouncedSearch.current) {
      hasHandledDebouncedSearch.current = true;
      return;
    }

    setSearchQuery(debouncedSearch);
    fetchProducts(1, debouncedSearch, categoryFilter);
  }, [categoryFilter, debouncedSearch, fetchProducts, setSearchQuery]);

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchInput(e.target.value);
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
    return <CatalogSkeleton />;
  }

  return (
    <Box>
      {/* Filters */}
      <Box sx={{ display: 'flex', gap: 2, mb: 4, flexWrap: 'wrap' }}>
        <TextField
          label="Search products"
          variant="outlined"
          value={searchInput}
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
            fetchProducts(page, debouncedSearch, categoryFilter);
          }}
          disabled={isLoading}
        />
      </Box>
    </Box>
  );
};

export default ProductCatalogPage;
