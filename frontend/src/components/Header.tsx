import { useState, type MouseEvent } from 'react'
import { Link as RouterLink, useNavigate } from 'react-router-dom'
import AppBar from '@mui/material/AppBar'
import Box from '@mui/material/Box'
import Toolbar from '@mui/material/Toolbar'
import Typography from '@mui/material/Typography'
import Button from '@mui/material/Button'
import IconButton from '@mui/material/IconButton'
import Badge from '@mui/material/Badge'
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart'
import AccountCircleIcon from '@mui/icons-material/AccountCircle'
import Menu from '@mui/material/Menu'
import MenuItem from '@mui/material/MenuItem'
import { useAuthStore } from '@store/auth'
import { useCartStore } from '@store/cart'

export function Header() {
  const navigate = useNavigate()
  const { isAuthenticated, user, logout } = useAuthStore()
  const cartCount = useCartStore((state) => state.getItemCount())
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null)

  const handleMenuOpen = (event: MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget)
  }

  const handleMenuClose = () => {
    setAnchorEl(null)
  }

  const handleLogout = async () => {
    await logout()
    navigate('/')
  }

  return (
    <AppBar position="static" color="primary">
      <Toolbar sx={{ justifyContent: 'space-between' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Typography variant="h6" component={RouterLink} to="/" sx={{ color: 'inherit', textDecoration: 'none' }}>
            Customer Ordering
          </Typography>
          <Button color="inherit" component={RouterLink} to="/products">
            Products
          </Button>
        </Box>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <IconButton color="inherit" component={RouterLink} to="/cart" aria-label="Cart">
            <Badge badgeContent={cartCount} color="secondary">
              <ShoppingCartIcon />
            </Badge>
          </IconButton>

          {isAuthenticated ? (
            <>
              <Button color="inherit" startIcon={<AccountCircleIcon />} onClick={handleMenuOpen}>
                {user?.name ?? 'Account'}
              </Button>
              <Menu anchorEl={anchorEl} open={Boolean(anchorEl)} onClose={handleMenuClose}>
                <MenuItem component={RouterLink} to="/profile" onClick={handleMenuClose}>
                  Profile
                </MenuItem>
                <MenuItem component={RouterLink} to="/orders" onClick={handleMenuClose}>
                  Orders
                </MenuItem>
                {user?.role === 'admin' && (
                  <MenuItem component={RouterLink} to="/admin" onClick={handleMenuClose}>
                    Admin Dashboard
                  </MenuItem>
                )}
                {user?.role === 'support' && (
                  <MenuItem component={RouterLink} to="/support" onClick={handleMenuClose}>
                    Support Dashboard
                  </MenuItem>
                )}
                <MenuItem onClick={handleLogout}>Logout</MenuItem>
              </Menu>
            </>
          ) : (
            <Button color="inherit" component={RouterLink} to="/login">
              Login
            </Button>
          )}
        </Box>
      </Toolbar>
    </AppBar>
  )
}
