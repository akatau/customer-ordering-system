import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import Typography from '@mui/material/Typography'
import Paper from '@mui/material/Paper'
import List from '@mui/material/List'
import ListItem from '@mui/material/ListItem'
import ListItemText from '@mui/material/ListItemText'
import Button from '@mui/material/Button'
import { LoadingIndicator } from '@components/LoadingIndicator'
import { PageContainer } from '@components/PageContainer'
import { useOrdersStore } from '@store/orders'
import { formatPrice, formatDate } from '@utils/helpers'

export function OrderDetailPage() {
  const navigate = useNavigate()
  const { orderId } = useParams()
  const [tracking, setTracking] = useState<any>(null)
  const { selectedOrder, fetchOrderById, getOrderTracking, isLoading, error } = useOrdersStore()

  useEffect(() => {
    if (orderId) {
      fetchOrderById(orderId)
    }
  }, [orderId])

  useEffect(() => {
    if (orderId) {
      getOrderTracking(orderId).then(setTracking).catch(() => null)
    }
  }, [orderId])

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

  if (!selectedOrder) {
    return (
      <PageContainer>
        <Typography>Order not found.</Typography>
      </PageContainer>
    )
  }

  return (
    <PageContainer>
      <Button variant="text" onClick={() => navigate('/orders')} sx={{ mb: 2 }}>
        Back to orders
      </Button>
      <Typography variant="h4" gutterBottom>
        Order {selectedOrder.order_number}
      </Typography>
      <Typography>Status: {selectedOrder.status}</Typography>
      <Typography>Total: {formatPrice(selectedOrder.total)}</Typography>
      <Typography>Placed: {formatDate(selectedOrder.created_at)}</Typography>
      <Paper sx={{ p: 2, mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          Shipping Address
        </Typography>
        <Typography>{selectedOrder.shipping_address.street}</Typography>
        <Typography>{`${selectedOrder.shipping_address.city}, ${selectedOrder.shipping_address.state} ${selectedOrder.shipping_address.zip_code}`}</Typography>
        <Typography>{selectedOrder.shipping_address.country}</Typography>
      </Paper>

      <Paper sx={{ p: 2, mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          Items
        </Typography>
        <List>
          {selectedOrder.items.map((item) => (
            <ListItem key={item.product_id}>
              <ListItemText primary={item.name} secondary={`Qty: ${item.quantity} • ${formatPrice(item.subtotal)}`} />
            </ListItem>
          ))}
        </List>
      </Paper>

      {tracking && (
        <Paper sx={{ p: 2, mt: 3 }}>
          <Typography variant="h6" gutterBottom>
            Tracking
          </Typography>
          <Typography>Status: {tracking.status}</Typography>
          {tracking.tracking_number && <Typography>Tracking #: {tracking.tracking_number}</Typography>}
          {tracking.estimated_delivery && <Typography>Estimated Delivery: {tracking.estimated_delivery}</Typography>}
        </Paper>
      )}
    </PageContainer>
  )
}
