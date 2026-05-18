/**
 * Order tracking page component
 */

import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Paper,
  Typography,
  Stepper,
  Step,
  StepLabel,
  Divider,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  CircularProgress,
  Alert,
  Button,
} from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import { useOrdersStore } from '@stores/ordersStore';

interface TrackingInfo {
  status: string;
  estimated_delivery: string;
  tracking_number?: string;
  carrier?: string;
}

const OrderTrackingPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { currentOrder, isLoading, error, fetchOrderDetail, fetchOrderTracking } =
    useOrdersStore();
  const [tracking, setTracking] = useState<TrackingInfo | null>(null);
  const [trackingLoading, setTrackingLoading] = useState(false);

  useEffect(() => {
    if (id) {
      fetchOrderDetail(id);
    }
  }, [id, fetchOrderDetail]);

  useEffect(() => {
    const loadTracking = async () => {
      if (id) {
        setTrackingLoading(true);
        const trackingData = await fetchOrderTracking(id);
        if (trackingData) {
          setTracking(trackingData);
        }
        setTrackingLoading(false);
      }
    };

    loadTracking();
  }, [id, fetchOrderTracking]);

  if (isLoading && !currentOrder) {
    return <CircularProgress sx={{ display: 'block', mx: 'auto' }} />;
  }

  if (error || !currentOrder) {
    return <Alert severity="error">Order not found</Alert>;
  }

  const getStepIndex = (status: string): number => {
    const steps: Record<string, number> = {
      pending: 0,
      processing: 1,
      shipped: 2,
      delivered: 3,
    };
    return steps[status.toLowerCase()] || 0;
  };

  return (
    <Box>
      <Button
        startIcon={<ArrowBackIcon />}
        onClick={() => navigate('/orders')}
        sx={{ mb: 2 }}
      >
        Back to Orders
      </Button>

      <Typography variant="h4" gutterBottom sx={{ mb: 3 }}>
        Order Tracking
      </Typography>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
          <Box>
            <Typography variant="body2" color="textSecondary">
              Order ID
            </Typography>
            <Typography variant="body1" sx={{ fontFamily: 'monospace' }}>
              {currentOrder.id}
            </Typography>
          </Box>
          <Box>
            <Typography variant="body2" color="textSecondary">
              Order Date
            </Typography>
            <Typography variant="body1">
              {new Date(currentOrder.created_at).toLocaleDateString()}
            </Typography>
          </Box>
          <Box>
            <Typography variant="body2" color="textSecondary">
              Total Amount
            </Typography>
            <Typography variant="body1" sx={{ fontWeight: 'bold' }}>
              ${parseFloat(currentOrder.total_amount).toFixed(2)}
            </Typography>
          </Box>
        </Box>
      </Paper>

      {/* Tracking Timeline */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Tracking Timeline
        </Typography>
        <Divider sx={{ mb: 2 }} />

        {trackingLoading ? (
          <CircularProgress />
        ) : tracking ? (
          <Box>
            <Stepper activeStep={getStepIndex(currentOrder.status)} sx={{ mb: 2 }}>
              <Step>
                <StepLabel>Ordered</StepLabel>
              </Step>
              <Step>
                <StepLabel>Processing</StepLabel>
              </Step>
              <Step>
                <StepLabel>Shipped</StepLabel>
              </Step>
              <Step>
                <StepLabel>Delivered</StepLabel>
              </Step>
            </Stepper>

            {tracking.tracking_number && (
              <Box sx={{ mt: 2, p: 2, backgroundColor: '#f5f5f5', borderRadius: 1 }}>
                <Typography variant="body2">
                  <strong>Tracking Number:</strong> {tracking.tracking_number}
                </Typography>
                {tracking.carrier && (
                  <Typography variant="body2">
                    <strong>Carrier:</strong> {tracking.carrier}
                  </Typography>
                )}
              </Box>
            )}

            <Box sx={{ mt: 2 }}>
              <Typography variant="body2" color="textSecondary">
                <strong>Estimated Delivery:</strong> {tracking.estimated_delivery}
              </Typography>
            </Box>
          </Box>
        ) : (
          <Typography variant="body2" color="textSecondary">
            Tracking information not yet available. Please check back soon.
          </Typography>
        )}
      </Paper>

      {/* Order Items */}
      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Order Items
        </Typography>
        <Divider sx={{ mb: 2 }} />

        <TableContainer>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Product</TableCell>
                <TableCell align="center">Quantity</TableCell>
                <TableCell align="right">Unit Price</TableCell>
                <TableCell align="right">Total</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {currentOrder.items.map((item, idx) => (
                <TableRow key={idx}>
                  <TableCell>Product ID: {item.product_id}</TableCell>
                  <TableCell align="center">{item.quantity}</TableCell>
                  <TableCell align="right">
                    ${parseFloat(item.unit_price).toFixed(2)}
                  </TableCell>
                  <TableCell align="right">
                    ${parseFloat(item.line_total).toFixed(2)}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    </Box>
  );
};

export default OrderTrackingPage;
