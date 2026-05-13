import { useEffect } from 'react'
import { useForm } from 'react-hook-form'
import Typography from '@mui/material/Typography'
import TextField from '@mui/material/TextField'
import Button from '@mui/material/Button'
import Alert from '@mui/material/Alert'
import Box from '@mui/material/Box'
import { useAuthStore } from '@store/auth'
import { useUserStore } from '@store/user'
import { PageContainer } from '@components/PageContainer'

interface ProfileForm {
  name: string
  phone?: string
}

interface PasswordForm {
  currentPassword: string
  newPassword: string
}

export function ProfilePage() {
  const { user, setUser } = useAuthStore()
  const { profile, fetchProfile, updateProfile, changePassword, isLoading, error } = useUserStore()
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<ProfileForm>()
  const {
    register: registerPassword,
    handleSubmit: handleSubmitPassword,
    reset: resetPassword,
    formState: { errors: passwordErrors },
  } = useForm<PasswordForm>()

  useEffect(() => {
    fetchProfile()
  }, [])

  useEffect(() => {
    if (profile) {
      reset({ name: profile.name, phone: profile.phone || '' })
    }
  }, [profile])

  const onProfileSubmit = async (data: ProfileForm) => {
    const updated = await updateProfile({ name: data.name, phone: data.phone })
    if (user) {
      setUser({ ...user, name: updated.name, phone: updated.phone })
    }
  }

  const onPasswordSubmit = async (data: PasswordForm) => {
    await changePassword(data.currentPassword, data.newPassword)
    resetPassword()
  }

  return (
    <PageContainer>
      <Typography variant="h4" gutterBottom>
        Profile
      </Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      <Box component="form" onSubmit={handleSubmit(onProfileSubmit)} sx={{ display: 'grid', gap: 2, maxWidth: 520, mb: 4 }}>
        <TextField label="Name" fullWidth {...register('name', { required: true })} error={Boolean(errors.name)} helperText={errors.name && 'Name is required'} />
        <TextField label="Phone" fullWidth {...register('phone')} />
        <Button variant="contained" type="submit" disabled={isLoading}>
          Update Profile
        </Button>
      </Box>

      <Typography variant="h5" gutterBottom>
        Change Password
      </Typography>
      <Box component="form" onSubmit={handleSubmitPassword(onPasswordSubmit)} sx={{ display: 'grid', gap: 2, maxWidth: 520 }}>
        <TextField label="Current Password" type="password" fullWidth {...registerPassword('currentPassword', { required: true })} error={Boolean(passwordErrors.currentPassword)} helperText={passwordErrors.currentPassword && 'Current password is required'} />
        <TextField label="New Password" type="password" fullWidth {...registerPassword('newPassword', { required: true, minLength: 8 })} error={Boolean(passwordErrors.newPassword)} helperText={passwordErrors.newPassword ? 'New password is required and should be at least 8 characters' : ''} />
        <Button variant="contained" type="submit" disabled={isLoading}>
          Change Password
        </Button>
      </Box>
    </PageContainer>
  )
}
