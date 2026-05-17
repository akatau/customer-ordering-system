import { Link as RouterLink, useNavigate } from 'react-router-dom'
import { useAuthStore } from '@store/auth'

export function Header() {
  const navigate = useNavigate()
  const { isAuthenticated, logout } = useAuthStore()

  const handleLogout = async () => {
    await logout()
    navigate('/login')
  }

  return (
    <header style={{ background: '#1976d2', color: 'white', padding: '12px 20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ fontWeight: 700 }}>Customer Ordering</div>
        <nav style={{ display: 'flex', gap: 12 }}>
          <RouterLink to="/products" style={{ color: 'white', textDecoration: 'none' }}>Products</RouterLink>
          <RouterLink to="/cart" style={{ color: 'white', textDecoration: 'none' }}>Cart</RouterLink>
          {isAuthenticated ? (
            <button
              type="button"
              onClick={handleLogout}
              style={{
                background: 'transparent',
                border: '1px solid rgba(255,255,255,0.8)',
                color: 'white',
                borderRadius: 6,
                padding: '6px 12px',
                cursor: 'pointer',
              }}
            >
              Logout
            </button>
          ) : (
            <RouterLink to="/login" style={{ color: 'white', textDecoration: 'none' }}>Login</RouterLink>
          )}
        </nav>
      </div>
    </header>
  )
}
