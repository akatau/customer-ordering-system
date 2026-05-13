import Typography from '@mui/material/Typography'
import Paper from '@mui/material/Paper'
import Grid from '@mui/material/Grid'
import { PageContainer } from '@components/PageContainer'

export function AdminDashboardPage() {
  return (
    <PageContainer>
      <Typography variant="h4" gutterBottom>
        Admin Dashboard
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6">Product Management</Typography>
            <Typography variant="body2" sx={{ mt: 1 }}>
              Add, update, or remove catalog items and manage stock.
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6">Order Monitoring</Typography>
            <Typography variant="body2" sx={{ mt: 1 }}>
              Review orders, update fulfillment status, and support customers.
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6">Reports</Typography>
            <Typography variant="body2" sx={{ mt: 1 }}>
              Access sales, stock, and customer data dashboards.
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </PageContainer>
  )
}
