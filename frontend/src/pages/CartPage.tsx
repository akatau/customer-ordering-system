/**
 * Shopping cart page component
 */

import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  Paper,
  Alert,
  CircularProgress,
  TextField,
  Grid,
  Card,
  CardContent,
  IconButton,
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import { useCartStore } from '@stores/cartStore';
import { useAuthStore } from '@stores/authStore';

const CartPage: React.FC = () => {
  const navigate = useNavigate();
  const { cart, isLoading, error, loadCart, removeFromCart, updateCartItem } = useCartStore();
  const { user } = useAuthStore();

  useEffect(() => {
    loadCart();
  }, [loadCart]);

  if (!user) {
    return <Alert severity="warning">Please log in to view your cart</Alert>;
  }

  if (isLoading && !cart) {
    return <CircularProgress sx={{ display: 'block', mx: 'auto' }} />;
  }

  const handleRemoveItem = async (productId: string) => {
    await removeFromCart(productId);
  };

  const handleQuantityChange = async (productId: string, newQuantity: number) => {
    if (newQuantity < 1) {
      await removeFromCart(productId);
    } else {
      await updateCartItem(productId, newQuantity);
    }
  };

  const handleCheckout = () => {
    if (cart && cart.items.length > 0) {
      navigate('/checkout');
    } else {
      alert('Your cart is empty');
    }
  };

  if (!cart || cart.items.length === 0) {
    return (
      <Box sx={{ textAlign: 'center', py: 8 }}>
        <Typography variant="h5" gutterBottom>
          Your cart is empty
        </Typography>
        <Button variant="contained" color="primary" onClick={() => navigate('/products')}>
          Continue Shopping
        </Button>
      </Box>
    );
  }

  return (
    <Box>
      <Button
        startIcon={<ArrowBackIcon />}
        onClick={() => navigate('/products')}
        sx={{ mb: 2 }}
      >
        Continue Shopping
      </Button>

      <Typography variant="h4" gutterBottom sx={{ mb: 3 }}>
        Shopping Cart
      </Typography>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      <Grid container spacing={3}>
        {/* Cart Items */}
        <Grid item xs={12} md={8}>
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Product</TableCell>
                  <TableCell align="center">Quantity</TableCell>
                  <TableCell align="right">Price</TableCell>
                  <TableCell align="right">Total</TableCell>
                  <TableCell align="center">Action</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {cart.items.map((item) => (
                  <TableRow key={item.product_id}>
                    <TableCell>{item.product?.name || 'Product'}</TableCell>
                    <TableCell align="center">
                      <TextField
                        type="number"
                        value={item.quantity}
                        onChange={(e) =>
                          handleQuantityChange(item.product_id, parseInt(e.target.value))
                        }
                        inputProps={{ min: 1 }}
                        sx={{ width: 60 }}
                      />
                    </TableCell>
                    <TableCell align="right">
                      ${parseFloat(item.product?.price || '0').toFixed(2)}
                    </TableCell>
                    <TableCell align="right">
                      $
                      {(
                        parseFloat(item.product?.price || '0') * item.quantity
                      ).toFixed(2)}
                    </TableCell>
                    <TableCell align="center">
                      <IconButton
                        size="small"
                        onClick={() => handleRemoveItem(item.product_id)}
                      >
                        <DeleteIcon />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Grid>

        {/* Order Summary */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Order Summary
              </Typography>

              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                <Typography>Subtotal:</Typography>
                <Typography>${parseFloat(cart.subtotal).toFixed(2)}</Typography>
              </Box>

              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                <Typography>Tax:</Typography>
                <Typography>${parseFloat(cart.tax).toFixed(2)}</Typography>
              </Box>

              <Box
                sx={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  fontSize: '1.2em',
                  fontWeight: 'bold',
                  mb: 2,
                  borderTop: '1px solid #ddd',
                  pt: 1,
                }}
              >
                <Typography>Total:</Typography>
                <Typography>${parseFloat(cart.total).toFixed(2)}</Typography>
              </Box>

              <Button
                fullWidth
                variant="contained"
                color="primary"
                size="large"
                onClick={handleCheckout}
                disabled={isLoading}
              >
                {isLoading ? 'Processing...' : 'Proceed to Checkout'}
              </Button>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default CartPage;
