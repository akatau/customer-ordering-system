import Box from '@mui/material/Box'
import { ReactNode } from 'react'

interface Props {
  children: ReactNode
}

export function PageContainer({ children }: Props) {
  return (
    <Box sx={{ backgroundColor: '#fff', borderRadius: 2, boxShadow: 1, p: 3, minHeight: '70vh' }}>
      {children}
    </Box>
  )
}
