import { Route, Routes } from 'react-router-dom'
import Container from '@mui/material/Container'
import { Header } from '@components/Header'
import { ProtectedRoute } from '@components/ProtectedRoute'
import { HomePage } from '@pages/HomePage'
import { ProductDetailPage } from '@pages/ProductDetailPage'
import { CartPage } from '@pages/CartPage'
import { CheckoutPage } from '@pages/CheckoutPage'
import { LoginPage } from '@pages/LoginPage'
import { RegisterPage } from '@pages/RegisterPage'
import { ProfilePage } from '@pages/ProfilePage'
import { OrdersPage } from '@pages/OrdersPage'
import { OrderDetailPage } from '@pages/OrderDetailPage'
import { AdminDashboardPage } from '@pages/AdminDashboardPage'
import { SupportDashboardPage } from '@pages/SupportDashboardPage'
import { NotFoundPage } from '@pages/NotFoundPage'

function App() {
  return (
    <>
      <Header />
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/products" element={<HomePage />} />
          <Route path="/products/:productId" element={<ProductDetailPage />} />
          <Route path="/cart" element={<CartPage />} />
          <Route path="/checkout" element={<ProtectedRoute><CheckoutPage /></ProtectedRoute>} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/profile" element={<ProtectedRoute><ProfilePage /></ProtectedRoute>} />
          <Route path="/orders" element={<ProtectedRoute><OrdersPage /></ProtectedRoute>} />
          <Route path="/orders/:orderId" element={<ProtectedRoute><OrderDetailPage /></ProtectedRoute>} />
          <Route path="/admin" element={<ProtectedRoute requireRole="admin"><AdminDashboardPage /></ProtectedRoute>} />
          <Route path="/support" element={<ProtectedRoute requireRole="support"><SupportDashboardPage /></ProtectedRoute>} />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </Container>
    </>
  )
}

export default App
