/**
 * Header component with navigation and user menu
 */

import React, { useState } from 'react';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Menu,
  MenuItem,
  Badge,
  Box,
  IconButton,
} from '@mui/material';
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import { useAuthStore } from '@stores/authStore';
import { useCartStore } from '@stores/cartStore';

const Header: React.FC = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();
  const { cart } = useCartStore();
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    logout();
    handleMenuClose();
    navigate('/');
  };

  const cartItemCount = cart?.items.reduce((sum, item) => sum + item.quantity, 0) || 0;

  return (
    <AppBar position="static" sx={{ boxShadow: 1 }}>
      <Toolbar sx={{ justifyContent: 'space-between' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 3 }}>
          <RouterLink to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
            <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
              🛒 OrderHub
            </Typography>
          </RouterLink>

          <Box sx={{ display: { xs: 'none', sm: 'flex' }, gap: 2 }}>
            <Button color="inherit" component={RouterLink} to="/products">
              Products
            </Button>
            {user?.role === 'admin' && (
              <Button color="inherit" component={RouterLink} to="/admin">
                Admin
              </Button>
            )}
          </Box>
        </Box>

        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
          {user ? (
            <>
              <IconButton color="inherit" component={RouterLink} to="/cart" title="Shopping Cart">
                <Badge badgeContent={cartItemCount} color="secondary">
                  <ShoppingCartIcon />
                </Badge>
              </IconButton>

              <IconButton
                color="inherit"
                onClick={handleMenuOpen}
                title={`Account: ${user.full_name}`}
              >
                <AccountCircleIcon />
              </IconButton>

              <Menu
                anchorEl={anchorEl}
                open={Boolean(anchorEl)}
                onClose={handleMenuClose}
                anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
              >
                <MenuItem disabled>
                  <Typography variant="body2">{user.full_name}</Typography>
                </MenuItem>
                <MenuItem component={RouterLink} to="/orders" onClick={handleMenuClose}>
                  My Orders
                </MenuItem>
                <MenuItem component={RouterLink} to="/profile" onClick={handleMenuClose}>
                  Profile
                </MenuItem>
                <MenuItem onClick={handleLogout}>Logout</MenuItem>
              </Menu>
            </>
          ) : (
            <>
              <Button
                color="inherit"
                component={RouterLink}
                to="/login"
                variant="outlined"
                sx={{ borderColor: 'inherit' }}
              >
                Login
              </Button>
              <Button
                color="inherit"
                component={RouterLink}
                to="/register"
                variant="contained"
                sx={{ backgroundColor: 'secondary.main' }}
              >
                Sign Up
              </Button>
            </>
          )}
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
