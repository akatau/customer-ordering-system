import { useEffect } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import Typography from '@mui/material/Typography'
import TextField from '@mui/material/TextField'
import Button from '@mui/material/Button'
import Alert from '@mui/material/Alert'
import Box from '@mui/material/Box'
import { useAuthStore } from '@store/auth'
import { PageContainer } from '@components/PageContainer'

interface LoginForm {
  email: string
  password: string
}

export function LoginPage() {
  const navigate = useNavigate()
  const location = useLocation()
  const { isAuthenticated, login, error, isLoading, clearError } = useAuthStore()
  const from = (location.state as { from?: Location })?.from?.pathname || '/'

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginForm>()

  useEffect(() => {
    if (isAuthenticated) {
      navigate(from, { replace: true })
    }
  }, [isAuthenticated, from])

  const onSubmit = async (data: LoginForm) => {
    await login(data.email, data.password)
    clearError()
  }

  return (
    <PageContainer>
      <Typography variant="h4" gutterBottom>
        Login
      </Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      <Box component="form" onSubmit={handleSubmit(onSubmit)} sx={{ display: 'grid', gap: 2, maxWidth: 480 }}>
        <TextField label="Email" type="email" fullWidth {...register('email', { required: true })} error={Boolean(errors.email)} helperText={errors.email && 'Email is required'} />
        <TextField label="Password" type="password" fullWidth {...register('password', { required: true })} error={Boolean(errors.password)} helperText={errors.password && 'Password is required'} />
        <Button type="submit" variant="contained" disabled={isLoading}>
          Sign In
        </Button>
      </Box>
    </PageContainer>
  )
}
