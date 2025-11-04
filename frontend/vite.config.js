import { defineConfig } from 'vite';

export default defineConfig({
  server: {
    port: 5174,  // Force your port
    host: '127.0.0.1',  // Force IPv4 (not ::1)
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5001',
        changeOrigin: true
      }
    }
  }
});