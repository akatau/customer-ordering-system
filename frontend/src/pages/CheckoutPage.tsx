/**
 * Checkout page component
 */

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  TextField,
  Button,
  Paper,
  Step,
  Stepper,
  StepLabel,
  Grid,
  Alert,
  CircularProgress,
} from '@mui/material';
import { useCartStore } from '@stores/cartStore';
import { useOrdersStore } from '@stores/ordersStore';
import { useAuthStore } from '@stores/authStore';
import { CheckoutRequest, OrderItem } from '@/types';

const steps = ['Shipping', 'Payment', 'Review', 'Complete'];

const CheckoutPage: React.FC = () => {
  const navigate = useNavigate();
  const { cart } = useCartStore();
  const { createOrder, isLoading } = useOrdersStore();
  const { user } = useAuthStore();
  const [activeStep, setActiveStep] = useState(0);
  const [error, setError] = useState('');

  const [shippingData, setShippingData] = useState({
    street: '',
    city: '',
    state: '',
    zip: '',
    country: '',
  });

  const [paymentData, setPaymentData] = useState({
    cardNumber: '',
    cardName: '',
    expiryDate: '',
    cvv: '',
  });

  const handleShippingChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setShippingData((prev) => ({ ...prev, [name]: value }));
  };

  const handlePaymentChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setPaymentData((prev) => ({ ...prev, [name]: value }));
  };

  const handleNext = () => {
    if (activeStep === steps.length - 1) {
      handlePlaceOrder();
    } else {
      setActiveStep((prev) => prev + 1);
    }
  };

  const handleBack = () => {
    setActiveStep((prev) => prev - 1);
  };

  const handlePlaceOrder = async () => {
    setError('');

    if (!cart || cart.items.length === 0) {
      setError('Your cart is empty');
      return;
    }

    const shippingAddress = `${shippingData.street}, ${shippingData.city}, ${shippingData.state} ${shippingData.zip}, ${shippingData.country}`;
    const billingAddress = shippingAddress;

    const items: OrderItem[] = cart.items.map((item) => ({
      product_id: item.product_id,
      quantity: item.quantity,
      unit_price: item.product?.price || '0',
      line_total: (
        parseFloat(item.product?.price || '0') * item.quantity
      ).toString(),
    }));

    const checkoutRequest: CheckoutRequest = {
      items,
      shipping_address: shippingAddress,
      billing_address: billingAddress,
      payment_method: 'stripe',
    };

    const success = await createOrder(checkoutRequest);
    if (success) {
      setActiveStep(3);
    } else {
      setError('Failed to place order. Please try again.');
    }
  };

  if (!user) {
    return <Alert severity="warning">Please log in to continue checkout</Alert>;
  }

  if (!cart || cart.items.length === 0) {
    return (
      <Box sx={{ textAlign: 'center', py: 8 }}>
        <Alert severity="warning" sx={{ mb: 2 }}>
          Your cart is empty
        </Alert>
        <Button variant="contained" color="primary" onClick={() => navigate('/products')}>
          Continue Shopping
        </Button>
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ mb: 4 }}>
        Checkout
      </Typography>

      <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
        {steps.map((label) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      <Box sx={{ minHeight: 300, mb: 4 }}>
        {activeStep === 0 && (
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Shipping Address
            </Typography>
            <Grid container spacing={2} sx={{ mb: 3 }}>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Street Address"
                  name="street"
                  value={shippingData.street}
                  onChange={handleShippingChange}
                  required
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="City"
                  name="city"
                  value={shippingData.city}
                  onChange={handleShippingChange}
                  required
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="State/Province"
                  name="state"
                  value={shippingData.state}
                  onChange={handleShippingChange}
                  required
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Zip/Postal Code"
                  name="zip"
                  value={shippingData.zip}
                  onChange={handleShippingChange}
                  required
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Country"
                  name="country"
                  value={shippingData.country}
                  onChange={handleShippingChange}
                  required
                />
              </Grid>
            </Grid>
          </Paper>
        )}

        {activeStep === 1 && (
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Payment Information
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Cardholder Name"
                  name="cardName"
                  value={paymentData.cardName}
                  onChange={handlePaymentChange}
                  required
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Card Number"
                  name="cardNumber"
                  value={paymentData.cardNumber}
                  onChange={handlePaymentChange}
                  placeholder="1234 5678 9012 3456"
                  required
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Expiry Date"
                  name="expiryDate"
                  value={paymentData.expiryDate}
                  onChange={handlePaymentChange}
                  placeholder="MM/YY"
                  required
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="CVV"
                  name="cvv"
                  type="password"
                  value={paymentData.cvv}
                  onChange={handlePaymentChange}
                  placeholder="123"
                  required
                />
              </Grid>
            </Grid>
            <Typography variant="body2" color="textSecondary" sx={{ mt: 2 }}>
              💡 Use test card: 4242 4242 4242 4242 | Any future expiry | Any CVC
            </Typography>
          </Paper>
        )}

        {activeStep === 2 && (
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Order Review
            </Typography>
            <Box sx={{ mb: 3 }}>
              <Typography variant="subtitle1" gutterBottom>
                Items ({cart.items.length})
              </Typography>
              {cart.items.map((item) => (
                <Box
                  key={item.product_id}
                  sx={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    py: 1,
                    borderBottom: '1px solid #eee',
                  }}
                >
                  <Typography>{item.product?.name}</Typography>
                  <Typography>
                    {item.quantity}x ${parseFloat(item.product?.price || '0').toFixed(2)}
                  </Typography>
                </Box>
              ))}
            </Box>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', fontWeight: 'bold' }}>
              <Typography>Total:</Typography>
              <Typography>${parseFloat(cart.total).toFixed(2)}</Typography>
            </Box>
          </Paper>
        )}

        {activeStep === 3 && (
          <Paper sx={{ p: 3, textAlign: 'center' }}>
            <Typography variant="h5" color="success.main" gutterBottom>
              ✓ Order Placed Successfully!
            </Typography>
            <Typography>Thank you for your purchase. You will receive a confirmation email soon.</Typography>
            <Button
              variant="contained"
              color="primary"
              onClick={() => navigate('/orders')}
              sx={{ mt: 2 }}
            >
              View My Orders
            </Button>
          </Paper>
        )}
      </Box>

      <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
        <Button
          disabled={activeStep === 0 || isLoading}
          onClick={handleBack}
        >
          Back
        </Button>
        <Button
          variant="contained"
          color="primary"
          onClick={handleNext}
          disabled={isLoading}
        >
          {isLoading ? (
            <CircularProgress size={24} />
          ) : activeStep === steps.length - 1 ? (
            'Complete'
          ) : (
            'Next'
          )}
        </Button>
      </Box>
    </Box>
  );
};

export default CheckoutPage;
