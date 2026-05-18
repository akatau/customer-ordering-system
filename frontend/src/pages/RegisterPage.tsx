import { useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import Typography from '@mui/material/Typography'
import TextField from '@mui/material/TextField'
import Button from '@mui/material/Button'
import Alert from '@mui/material/Alert'
import Box from '@mui/material/Box'
import { useAuthStore } from '@store/auth'
import { PageContainer } from '@components/PageContainer'

interface RegisterForm {
  username: string
  fullName?: string
  email: string
  password: string
}

export function RegisterPage() {
  const navigate = useNavigate()
  const { register: signup, error, isLoading, clearError } = useAuthStore()
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterForm>()

  const onSubmit = async (data: RegisterForm) => {
    await signup(data.email, data.password, data.username, data.fullName)
    clearError()
    navigate('/login')
  }

  return (
    <PageContainer>
      <Typography variant="h4" gutterBottom>
        Register
      </Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      <Box component="form" onSubmit={handleSubmit(onSubmit)} sx={{ display: 'grid', gap: 2, maxWidth: 480 }}>
        <TextField label="Username" fullWidth {...register('username', { required: true })} error={Boolean(errors.username)} helperText={errors.username && 'Username is required'} />
        <TextField label="Full Name" fullWidth {...register('fullName')} />
        <TextField label="Email" type="email" fullWidth {...register('email', { required: true })} error={Boolean(errors.email)} helperText={errors.email && 'Email is required'} />
        <TextField label="Password" type="password" fullWidth {...register('password', { required: true, minLength: 8 })} error={Boolean(errors.password)} helperText={errors.password ? 'Password is required and must be at least 8 characters' : ''} />
        <Button type="submit" variant="contained" disabled={isLoading}>
          Create Account
        </Button>
      </Box>
    </PageContainer>
  )
}
