import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  define: {
    // Esto inyecta la variable en el bundle, tanto en desarrollo como en producción.
    'process.env': {
      VITE_BACKEND_URL: process.env.VITE_BACKEND_URL || 'http://localhost:8000',
    },
  },
  build: {
    sourcemap: false, // Deshabilitar mapas de fuentes en producción
  },
  server: {
    host: '0.0.0.0', // Para que sea accesible en la red
    port: 5173,
  },
})