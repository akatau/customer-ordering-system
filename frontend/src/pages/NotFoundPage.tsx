import Typography from '@mui/material/Typography'
import Button from '@mui/material/Button'
import Box from '@mui/material/Box'
import { Link as RouterLink } from 'react-router-dom'
import { PageContainer } from '@components/PageContainer'

export function NotFoundPage() {
  return (
    <PageContainer>
      <Box sx={{ textAlign: 'center', py: 6 }}>
        <Typography variant="h4" gutterBottom>
          Page not found
        </Typography>
        <Typography sx={{ mb: 3 }}>We couldn’t find the page you were looking for.</Typography>
        <Button variant="contained" component={RouterLink} to="/">
          Return Home
        </Button>
      </Box>
    </PageContainer>
  )
}
