import CircularProgress from '@mui/material/CircularProgress'
import Box from '@mui/material/Box'

export function LoadingIndicator() {
  return (
    <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', py: 6 }}>
      <CircularProgress />
    </Box>
  )
}
