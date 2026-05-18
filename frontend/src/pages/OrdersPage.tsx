/**
 * Orders page component - list all user orders
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
  Paper,
  Button,
  Chip,
  CircularProgress,
  Alert,
} from '@mui/material';
import VisibilityIcon from '@mui/icons-material/Visibility';
import TrackingIcon from '@mui/icons-material/LocalShipping';
import { useOrdersStore } from '@stores/ordersStore';
import { useAuthStore } from '@stores/authStore';
import { OrderStatus } from '@/types';

const OrdersPage: React.FC = () => {
  const navigate = useNavigate();
  const { orders, isLoading, error, fetchOrders } = useOrdersStore();
  const { user } = useAuthStore();

  useEffect(() => {
    fetchOrders();
  }, [fetchOrders]);

  if (!user) {
    return <Alert severity="warning">Please log in to view your orders</Alert>;
  }

  if (isLoading && orders.length === 0) {
    return <CircularProgress sx={{ display: 'block', mx: 'auto' }} />;
  }

  if (orders.length === 0) {
    return (
      <Box sx={{ textAlign: 'center', py: 8 }}>
        <Typography variant="h5" gutterBottom>
          You haven't placed any orders yet
        </Typography>
        <Button
          variant="contained"
          color="primary"
          onClick={() => navigate('/products')}
        >
          Start Shopping
        </Button>
      </Box>
    );
  }

  const getStatusColor = (status: OrderStatus): any => {
    const colors: Record<OrderStatus, any> = {
      [OrderStatus.PENDING]: 'warning',
      [OrderStatus.PROCESSING]: 'info',
      [OrderStatus.COMPLETED]: 'success',
      [OrderStatus.CANCELLED]: 'error',
    };
    return colors[status] || 'default';
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ mb: 3 }}>
        My Orders
      </Typography>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
              <TableCell>Order ID</TableCell>
              <TableCell>Date</TableCell>
              <TableCell align="right">Amount</TableCell>
              <TableCell>Status</TableCell>
              <TableCell align="center">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {orders.map((order) => (
              <TableRow key={order.id}>
                <TableCell>
                  <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
                    {order.id.substring(0, 8)}...
                  </Typography>
                </TableCell>
                <TableCell>
                  {new Date(order.created_at).toLocaleDateString()}
                </TableCell>
                <TableCell align="right">
                  <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                    ${parseFloat(order.total_amount).toFixed(2)}
                  </Typography>
                </TableCell>
                <TableCell>
                  <Chip
                    label={order.status.toUpperCase()}
                    color={getStatusColor(order.status as OrderStatus)}
                    variant="outlined"
                    size="small"
                  />
                </TableCell>
                <TableCell align="center">
                  <Button
                    size="small"
                    startIcon={<VisibilityIcon />}
                    onClick={() => navigate(`/orders/${order.id}`)}
                  >
                    View
                  </Button>
                  {order.status === OrderStatus.PROCESSING ||
                  order.status === OrderStatus.COMPLETED ? (
                    <Button
                      size="small"
                      startIcon={<TrackingIcon />}
                      onClick={() => navigate(`/orders/${order.id}/tracking`)}
                    >
                      Track
                    </Button>
                  ) : null}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default OrdersPage;
