/**
 * Root App component with routing
 */

import React, { Suspense, lazy, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Container from '@mui/material/Container';
import { Box, Grid, Skeleton, Stack, Typography } from '@mui/material';

import { useAuthStore } from '@stores/authStore';
import Header from '@components/Header';
import Footer from '@components/Footer';
import AppErrorBoundary from '@components/AppErrorBoundary';

const HomePage = lazy(() => import('@pages/HomePage'));
const LoginPage = lazy(() => import('@pages/LoginPage'));
const RegisterPage = lazy(() => import('@pages/RegisterPage'));
const ProductCatalogPage = lazy(() => import('@pages/ProductCatalogPage'));
const ProductDetailPage = lazy(() => import('@pages/ProductDetailPage'));
const CartPage = lazy(() => import('@pages/CartPage'));
const CheckoutPage = lazy(() => import('@pages/CheckoutPage'));
const OrdersPage = lazy(() => import('@pages/OrdersPage'));
const OrderTrackingPage = lazy(() => import('@pages/OrderTrackingPage'));
const ProfilePage = lazy(() => import('@pages/ProfilePage'));
const AdminDashboardPage = lazy(() => import('@pages/AdminDashboardPage'));

const RouteFallback = () => (
  <Stack spacing={3} sx={{ py: 4 }} aria-live="polite" role="status">
    <Box>
      <Skeleton variant="text" width="28%" height={44} />
      <Typography variant="body2" color="text.secondary" sx={{ maxWidth: 640 }}>
        Loading the next view and keeping the shell interactive.
      </Typography>
    </Box>

    <Grid container spacing={3}>
      {Array.from({ length: 6 }).map((_, index) => (
        <Grid key={index} item xs={12} sm={6} md={4}>
          <Skeleton variant="rounded" height={180} />
        </Grid>
      ))}
    </Grid>
  </Stack>
);

// Protected route wrapper
const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const { token } = useAuthStore();
  return token ? <>{children}</> : <Navigate to="/login" replace />;
};

const AdminRoute = ({ children }: { children: React.ReactNode }) => {
  const { token, user } = useAuthStore();

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return user?.role === 'admin' ? <>{children}</> : <Navigate to="/" replace />;
};

// Material-UI theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  const { loadStoredAuth } = useAuthStore();

  useEffect(() => {
    loadStoredAuth();
  }, [loadStoredAuth]);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <AppErrorBoundary>
          <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
            <Header />
            <Container maxWidth="lg" sx={{ flex: 1, py: 4 }}>
              <Suspense fallback={<RouteFallback />}>
                <Routes>
                  <Route path="/" element={<HomePage />} />
                  <Route path="/login" element={<LoginPage />} />
                  <Route path="/register" element={<RegisterPage />} />
                  <Route path="/products" element={<ProductCatalogPage />} />
                  <Route path="/products/:id" element={<ProductDetailPage />} />
                  <Route
                    path="/cart"
                    element={
                      <ProtectedRoute>
                        <CartPage />
                      </ProtectedRoute>
                    }
                  />
                  <Route
                    path="/checkout"
                    element={
                      <ProtectedRoute>
                        <CheckoutPage />
                      </ProtectedRoute>
                    }
                  />
                  <Route
                    path="/orders"
                    element={
                      <ProtectedRoute>
                        <OrdersPage />
                      </ProtectedRoute>
                    }
                  />
                  <Route
                    path="/orders/:id/tracking"
                    element={
                      <ProtectedRoute>
                        <OrderTrackingPage />
                      </ProtectedRoute>
                    }
                  />
                  <Route
                    path="/profile"
                    element={
                      <ProtectedRoute>
                        <ProfilePage />
                      </ProtectedRoute>
                    }
                  />
                  <Route
                    path="/admin"
                    element={
                      <AdminRoute>
                        <AdminDashboardPage />
                      </AdminRoute>
                    }
                  />
                </Routes>
              </Suspense>
            </Container>
            <Footer />
          </div>
        </AppErrorBoundary>
      </Router>
    </ThemeProvider>
  );
}

export default App;
