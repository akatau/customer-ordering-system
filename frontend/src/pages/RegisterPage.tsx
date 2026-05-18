/**
 * Register page component
 */

import React, { useState } from 'react';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Alert,
  CircularProgress,
} from '@mui/material';
import { useAuthStore } from '@stores/authStore';
import { RegisterRequest } from '@/types';

const RegisterPage: React.FC = () => {
  const navigate = useNavigate();
  const { register, isLoading, error } = useAuthStore();
  const [formData, setFormData] = useState<RegisterRequest>({
    email: '',
    password: '',
    username: '',
    full_name: '',
  });
  const [passwordConfirm, setPasswordConfirm] = useState('');
  const [validationError, setValidationError] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setValidationError('');

    if (formData.password !== passwordConfirm) {
      setValidationError('Passwords do not match');
      return;
    }

    if (formData.password.length < 8) {
      setValidationError('Password must be at least 8 characters');
      return;
    }

    const success = await register(formData);
    if (success) {
      navigate('/login');
    }
  };

  return (
    <Container maxWidth="sm" sx={{ py: 8 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom sx={{ textAlign: 'center', mb: 3 }}>
          Create Account
        </Typography>

        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        {validationError && <Alert severity="error" sx={{ mb: 2 }}>{validationError}</Alert>}

        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            label="Username"
            name="username"
            value={formData.username}
            onChange={handleChange}
            required
            margin="normal"
            disabled={isLoading}
          />

          <TextField
            fullWidth
            label="Full Name"
            name="full_name"
            value={formData.full_name}
            onChange={handleChange}
            margin="normal"
            disabled={isLoading}
          />

          <TextField
            fullWidth
            label="Email"
            name="email"
            type="email"
            value={formData.email}
            onChange={handleChange}
            required
            margin="normal"
            disabled={isLoading}
          />

          <TextField
            fullWidth
            label="Password"
            name="password"
            type="password"
            value={formData.password}
            onChange={handleChange}
            required
            margin="normal"
            disabled={isLoading}
            helperText="At least 8 characters required"
          />

          <TextField
            fullWidth
            label="Confirm Password"
            name="passwordConfirm"
            type="password"
            value={passwordConfirm}
            onChange={(e) => setPasswordConfirm(e.target.value)}
            required
            margin="normal"
            disabled={isLoading}
          />

          <Button
            fullWidth
            variant="contained"
            color="primary"
            type="submit"
            sx={{ mt: 3, mb: 2 }}
            disabled={isLoading}
          >
            {isLoading ? <CircularProgress size={24} /> : 'Create Account'}
          </Button>
        </form>

        <Box sx={{ textAlign: 'center', mt: 2 }}>
          <Typography variant="body2">
            Already have an account?{' '}
            <RouterLink to="/login" style={{ color: '#1976d2' }}>
              Login here
            </RouterLink>
          </Typography>
        </Box>
      </Paper>
    </Container>
  );
};

export default RegisterPage;
