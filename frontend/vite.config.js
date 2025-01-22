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
    // Asegúrate de que la variable de entorno esté accesible en el código de frontend
    'process.env': {
      VITE_BACKEND_URL: process.env.VITE_BACKEND_URL || 'http://localhost:8000', // Valor por defecto para desarrollo local
    },
  },
  build: {
    sourcemap: false, // Deshabilitar mapas de fuentes en producción
  }
})