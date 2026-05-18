/**
 * Footer component
 */

import React from 'react';
import { Box, Container, Typography, Link, Grid } from '@mui/material';

const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();

  return (
    <Box component="footer" sx={{ backgroundColor: '#f5f5f5', py: 4, mt: 8 }}>
      <Container maxWidth="lg">
        <Grid container spacing={3}>
          <Grid item xs={12} sm={6} md={3}>
            <Typography variant="h6" gutterBottom>
              About
            </Typography>
            <Typography variant="body2" color="textSecondary">
              OrderHub is your premier online shopping destination with thousands of products at
              great prices.
            </Typography>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Typography variant="h6" gutterBottom>
              Support
            </Typography>
            <Link href="#" display="block" variant="body2" color="inherit">
              Contact Us
            </Link>
            <Link href="#" display="block" variant="body2" color="inherit">
              FAQ
            </Link>
            <Link href="#" display="block" variant="body2" color="inherit">
              Track Order
            </Link>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Typography variant="h6" gutterBottom>
              Legal
            </Typography>
            <Link href="#" display="block" variant="body2" color="inherit">
              Privacy Policy
            </Link>
            <Link href="#" display="block" variant="body2" color="inherit">
              Terms of Service
            </Link>
            <Link href="#" display="block" variant="body2" color="inherit">
              Cookie Policy
            </Link>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Typography variant="h6" gutterBottom>
              Follow Us
            </Typography>
            <Link href="#" display="block" variant="body2" color="inherit">
              Twitter
            </Link>
            <Link href="#" display="block" variant="body2" color="inherit">
              Facebook
            </Link>
            <Link href="#" display="block" variant="body2" color="inherit">
              Instagram
            </Link>
          </Grid>
        </Grid>

        <Box sx={{ textAlign: 'center', mt: 4, borderTop: '1px solid #ddd', pt: 2 }}>
          <Typography variant="body2" color="textSecondary">
            © {currentYear} OrderHub. All rights reserved.
          </Typography>
        </Box>
      </Container>
    </Box>
  );
};

export default Footer;
