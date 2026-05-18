import React, { useEffect, useState } from 'react';
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Grid,
  Skeleton,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
} from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import { adminApi } from '@api/admin';
import { AdminLog, AdminOrder, AdminUser } from '@/types';

const DashboardCard = ({ title, children }: { title: string; children: React.ReactNode }) => (
  <Card sx={{ height: '100%' }}>
    <CardContent>
      <Typography variant="h6" gutterBottom>
        {title}
      </Typography>
      {children}
    </CardContent>
  </Card>
);

const AdminDashboardPage: React.FC = () => {
  const [users, setUsers] = useState<AdminUser[]>([]);
  const [orders, setOrders] = useState<AdminOrder[]>([]);
  const [activityLogs, setActivityLogs] = useState<AdminLog[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadDashboard = async () => {
      setIsLoading(true);
      setError(null);

      const [usersResponse, ordersResponse, logsResponse] = await Promise.all([
        adminApi.listUsers(5),
        adminApi.listOrders(5),
        adminApi.listActivityLogs(5),
      ]);

      const firstError = usersResponse.error || ordersResponse.error || logsResponse.error;
      if (firstError) {
        setError(firstError.detail);
        setIsLoading(false);
        return;
      }

      setUsers(usersResponse.data?.users || []);
      setOrders(ordersResponse.data?.orders || []);
      setActivityLogs(logsResponse.data?.logs || []);
      setIsLoading(false);
    };

    loadDashboard();
  }, []);

  if (isLoading) {
    return (
      <Stack spacing={3}>
        <Skeleton variant="text" width="30%" height={48} />
        <Grid container spacing={3}>
          {Array.from({ length: 3 }).map((_, index) => (
            <Grid key={index} item xs={12} md={4}>
              <Skeleton variant="rounded" height={220} />
            </Grid>
          ))}
        </Grid>
      </Stack>
    );
  }

  return (
    <Stack spacing={3}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', gap: 2, flexWrap: 'wrap' }}>
        <Box>
          <Typography variant="h4" component="h1" gutterBottom>
            Admin Dashboard
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Operational view backed by the backend admin endpoints.
          </Typography>
        </Box>
        <Button component={RouterLink} to="/products" variant="outlined">
          Back to catalog
        </Button>
      </Box>

      {error && <Alert severity="error">{error}</Alert>}

      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <DashboardCard title="Recent Users">
            <Table size="small" aria-label="recent users">
              <TableHead>
                <TableRow>
                  <TableCell>User</TableCell>
                  <TableCell>Status</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {users.map((user) => (
                  <TableRow key={user.id}>
                    <TableCell>
                      <Typography variant="body2" fontWeight={600}>
                        {user.full_name || user.username}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {user.email}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Chip
                        size="small"
                        label={user.is_active ? user.role : 'inactive'}
                        color={user.is_active ? 'success' : 'default'}
                      />
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </DashboardCard>
        </Grid>

        <Grid item xs={12} md={4}>
          <DashboardCard title="Recent Orders">
            <Table size="small" aria-label="recent orders">
              <TableHead>
                <TableRow>
                  <TableCell>Order</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell align="right">Total</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {orders.map((order) => (
                  <TableRow key={order.id}>
                    <TableCell>
                      <Typography variant="body2" fontWeight={600}>
                        {order.id.slice(0, 8)}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {new Date(order.created_at).toLocaleDateString()}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Chip size="small" label={order.status} />
                    </TableCell>
                    <TableCell align="right">${order.total_amount.toFixed(2)}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </DashboardCard>
        </Grid>

        <Grid item xs={12} md={4}>
          <DashboardCard title="Recent Activity">
            <Table size="small" aria-label="recent activity logs">
              <TableHead>
                <TableRow>
                  <TableCell>Action</TableCell>
                  <TableCell>Resource</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {activityLogs.map((log) => (
                  <TableRow key={log.id}>
                    <TableCell>
                      <Typography variant="body2" fontWeight={600}>
                        {log.action}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {new Date(log.timestamp).toLocaleTimeString()}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2">{log.resource_type}</Typography>
                      <Typography variant="caption" color="text.secondary">
                        {log.resource_id || 'n/a'}
                      </Typography>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </DashboardCard>
        </Grid>
      </Grid>
    </Stack>
  );
};

export default AdminDashboardPage;