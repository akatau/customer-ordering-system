export const createEnv = (): Record<string, string> => {
  return {
    API_URL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
    NODE_ENV: import.meta.env.MODE,
  }
}

export const isDevelopment = (): boolean => import.meta.env.DEV

export const isProduction = (): boolean => import.meta.env.PROD
