import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    rollupOptions: {
      input: './index.html'
    }
  },
  server: {
    port: 3000,
    host: '0.0.0.0',
    proxy: {
      '/solve': 'http://localhost:8000',
      '/anagrams': 'http://localhost:8000',
      '/health': 'http://localhost:8000'
    }
  }
}) 