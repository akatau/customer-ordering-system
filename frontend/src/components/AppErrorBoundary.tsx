import { Component, type ErrorInfo, type ReactNode } from 'react';
import { Alert, Box, Button, Container, Stack, Typography } from '@mui/material';

interface AppErrorBoundaryProps {
  children: ReactNode;
}

interface AppErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

class AppErrorBoundary extends Component<AppErrorBoundaryProps, AppErrorBoundaryState> {
  state: AppErrorBoundaryState = {
    hasError: false,
    error: null,
  };

  static getDerivedStateFromError(error: Error): AppErrorBoundaryState {
    return {
      hasError: true,
      error,
    };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Application render error:', error, errorInfo);
  }

  handleReload = () => {
    window.location.reload();
  };

  handleGoHome = () => {
    window.location.assign('/');
  };

  render() {
    const { children } = this.props;
    const { hasError, error } = this.state;

    if (hasError) {
      return (
        <Container maxWidth="md" sx={{ py: 8 }}>
          <Box
            sx={{
              borderRadius: 4,
              border: '1px solid',
              borderColor: 'error.main',
              backgroundColor: 'background.paper',
              p: { xs: 3, sm: 4 },
              boxShadow: 2,
            }}
          >
            <Stack spacing={3}>
              <Box>
                <Typography variant="h4" component="h1" gutterBottom>
                  Something stopped the app
                </Typography>
                <Typography variant="body1" color="text.secondary">
                  The shell detected a render-time problem. Reload the app or return to the home
                  page to recover.
                </Typography>
              </Box>

              <Alert severity="error">
                {error?.message || 'An unexpected rendering error occurred.'}
              </Alert>

              <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2}>
                <Button variant="contained" onClick={this.handleReload}>
                  Reload app
                </Button>
                <Button variant="outlined" onClick={this.handleGoHome}>
                  Go to home
                </Button>
              </Stack>
            </Stack>
          </Box>
        </Container>
      );
    }

    return children;
  }
}

export default AppErrorBoundary;