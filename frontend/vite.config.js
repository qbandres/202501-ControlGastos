import { defineConfig, loadEnv } from 'vite'
import vue from '@vite/plugin-vue'
import path from 'path'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  // Cargar las variables de entorno según el modo (development/production)
  const env = loadEnv(mode, process.cwd(), '')
  
  return {
    plugins: [vue()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
      },
    },
    // Ya no es necesario definir 'process.env' manualmente,
    // Vite inyecta las variables que comienzan con VITE_ en import.meta.env
    build: {
      sourcemap: false, // Deshabilitar mapas de fuentes en producción
    },
    server: {
      host: true, // Permite que el servidor de desarrollo sea accesible en la red
    }
  }
})