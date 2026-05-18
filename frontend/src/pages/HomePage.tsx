/**
 * Homepage component
 */

import React from 'react';
import { Box, Button, Typography, Container, Grid, Paper } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import ShoppingBagIcon from '@mui/icons-material/ShoppingBag';
import LocalShippingIcon from '@mui/icons-material/LocalShipping';
import VerifiedIcon from '@mui/icons-material/Verified';

const HomePage: React.FC = () => {
  return (
    <Box>
      {/* Hero Section */}
      <Box
        sx={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white',
          py: 8,
          textAlign: 'center',
          borderRadius: 2,
          mb: 6,
        }}
      >
        <Typography variant="h3" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
          Welcome to OrderHub
        </Typography>
        <Typography variant="h6" gutterBottom sx={{ mb: 4 }}>
          Your destination for quality products at unbeatable prices
        </Typography>
        <Button
          component={RouterLink}
          to="/products"
          variant="contained"
          sx={{ backgroundColor: 'white', color: '#667eea' }}
          size="large"
        >
          Start Shopping
        </Button>
      </Box>

      {/* Features Section */}
      <Container maxWidth="lg">
        <Grid container spacing={3} sx={{ mb: 6 }}>
          <Grid item xs={12} sm={6} md={4}>
            <Paper sx={{ p: 3, textAlign: 'center' }}>
              <ShoppingBagIcon sx={{ fontSize: 48, color: '#667eea', mb: 2 }} />
              <Typography variant="h6" gutterBottom>
                Wide Selection
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Browse thousands of products across multiple categories
              </Typography>
            </Paper>
          </Grid>

          <Grid item xs={12} sm={6} md={4}>
            <Paper sx={{ p: 3, textAlign: 'center' }}>
              <LocalShippingIcon sx={{ fontSize: 48, color: '#667eea', mb: 2 }} />
              <Typography variant="h6" gutterBottom>
                Fast Delivery
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Track your orders in real-time with our advanced tracking system
              </Typography>
            </Paper>
          </Grid>

          <Grid item xs={12} sm={6} md={4}>
            <Paper sx={{ p: 3, textAlign: 'center' }}>
              <VerifiedIcon sx={{ fontSize: 48, color: '#667eea', mb: 2 }} />
              <Typography variant="h6" gutterBottom>
                100% Secure
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Your data is protected with advanced encryption and security
              </Typography>
            </Paper>
          </Grid>
        </Grid>

        {/* Call to Action */}
        <Box sx={{ textAlign: 'center', py: 4 }}>
          <Typography variant="h5" gutterBottom sx={{ mb: 2 }}>
            Ready to shop?
          </Typography>
          <Button
            component={RouterLink}
            to="/products"
            variant="contained"
            color="primary"
            size="large"
          >
            Browse Products
          </Button>
        </Box>
      </Container>
    </Box>
  );
};

export default HomePage;
