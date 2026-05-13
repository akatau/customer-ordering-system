import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
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

export function OrdersPage() {
  const navigate = useNavigate()
  const { orders, isLoading, error, fetchOrders } = useOrdersStore()

  useEffect(() => {
    fetchOrders()
  }, [])

  if (isLoading) {
    return <LoadingIndicator />
  }

  return (
    <PageContainer>
      <Typography variant="h4" gutterBottom>
        Your Orders
      </Typography>
      {error && <Typography color="error">{error}</Typography>}
      {orders.length === 0 ? (
        <Typography>No orders found.</Typography>
      ) : (
        <List>
          {orders.map((order) => (
            <Paper key={order.id} sx={{ mb: 2, p: 2 }}>
              <ListItem secondaryAction={<Button onClick={() => navigate(`/orders/${order.id}`)}>View</Button>}>
                <ListItemText
                  primary={`Order ${order.order_number}`}
                  secondary={`Status: ${order.status} • Total: ${formatPrice(order.total)} • ${formatDate(order.created_at)}`}
                />
              </ListItem>
            </Paper>
          ))}
        </List>
      )}
    </PageContainer>
  )
}
