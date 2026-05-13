import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import Grid from '@mui/material/Grid'
import Typography from '@mui/material/Typography'
import TextField from '@mui/material/TextField'
import Button from '@mui/material/Button'
import MenuItem from '@mui/material/MenuItem'
import Alert from '@mui/material/Alert'
import Box from '@mui/material/Box'
import { LoadingIndicator } from '@components/LoadingIndicator'
import { PageContainer } from '@components/PageContainer'
import { useCartStore } from '@store/cart'
import { orderService } from '@services/orders'
import { useAuthStore } from '@store/auth'

interface CheckoutForm {
  firstName: string
  lastName: string
  street: string
  city: string
  state: string
  zipCode: string
  country: string
  paymentMethod: 'credit_card' | 'paypal'
}

export function CheckoutPage() {
  const navigate = useNavigate()
  const { cart, isLoading, error, fetchCart } = useCartStore()
  const { user } = useAuthStore()
  const [orderError, setOrderError] = useState<string | null>(null)
  const [successMessage, setSuccessMessage] = useState<string | null>(null)
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<CheckoutForm>({
    defaultValues: {
      firstName: user?.name || '',
      lastName: '',
      street: '',
      city: '',
      state: '',
      zipCode: '',
      country: 'USA',
      paymentMethod: 'credit_card',
    },
  })

  useEffect(() => {
    fetchCart()
  }, [])

  const onSubmit = async (data: CheckoutForm) => {
    if (!cart || cart.items.length === 0) {
      setOrderError('Your cart is empty.')
      return
    }

    try {
      const order = await orderService.createOrder({
        items: cart.items.map((item) => ({ product_id: item.product_id, quantity: item.quantity })),
        shipping_address: {
          street: data.street,
          city: data.city,
          state: data.state,
          zip_code: data.zipCode,
          country: data.country,
        },
        payment_method_id: data.paymentMethod,
      })
      setSuccessMessage(`Order ${order.order_number} created successfully.`)
      navigate('/orders')
    } catch (error) {
      setOrderError(error instanceof Error ? error.message : 'Order checkout failed.')
    }
  }

  if (isLoading) {
    return <LoadingIndicator />
  }

  return (
    <PageContainer>
      <Typography variant="h4" gutterBottom>
        Checkout
      </Typography>

      {error && <Alert severity="error">{error}</Alert>}
      {orderError && <Alert severity="error">{orderError}</Alert>}
      {successMessage && <Alert severity="success">{successMessage}</Alert>}

      <Box component="form" onSubmit={handleSubmit(onSubmit)} sx={{ mt: 3 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
            <TextField label="First Name" fullWidth {...register('firstName', { required: true })} error={Boolean(errors.firstName)} helperText={errors.firstName && 'Required'} />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField label="Last Name" fullWidth {...register('lastName', { required: true })} error={Boolean(errors.lastName)} helperText={errors.lastName && 'Required'} />
          </Grid>
          <Grid item xs={12}>
            <TextField label="Street Address" fullWidth {...register('street', { required: true })} error={Boolean(errors.street)} helperText={errors.street && 'Required'} />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField label="City" fullWidth {...register('city', { required: true })} error={Boolean(errors.city)} helperText={errors.city && 'Required'} />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField label="State" fullWidth {...register('state', { required: true })} error={Boolean(errors.state)} helperText={errors.state && 'Required'} />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField label="ZIP Code" fullWidth {...register('zipCode', { required: true })} error={Boolean(errors.zipCode)} helperText={errors.zipCode && 'Required'} />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField label="Country" fullWidth {...register('country', { required: true })} error={Boolean(errors.country)} helperText={errors.country && 'Required'} />
          </Grid>
          <Grid item xs={12}>
            <TextField select label="Payment Method" fullWidth {...register('paymentMethod')}>
              <MenuItem value="credit_card">Credit Card</MenuItem>
              <MenuItem value="paypal">PayPal</MenuItem>
            </TextField>
          </Grid>
        </Grid>

        <Button type="submit" variant="contained" size="large" sx={{ mt: 3 }}>
          Confirm Order
        </Button>
      </Box>
    </PageContainer>
  )
}
