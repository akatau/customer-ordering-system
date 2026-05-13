import Typography from '@mui/material/Typography'
import Paper from '@mui/material/Paper'
import Grid from '@mui/material/Grid'
import { PageContainer } from '@components/PageContainer'

export function SupportDashboardPage() {
  return (
    <PageContainer>
      <Typography variant="h4" gutterBottom>
        Support Dashboard
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6">Customer Tickets</Typography>
            <Typography variant="body2" sx={{ mt: 1 }}>
              Review and respond to customer orders and support requests.
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6">Order Tracking</Typography>
            <Typography variant="body2" sx={{ mt: 1 }}>
              Monitor shipping status and help resolve delivery issues.
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6">Support Metrics</Typography>
            <Typography variant="body2" sx={{ mt: 1 }}>
              Track response times and case resolution progress.
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </PageContainer>
  )
}
