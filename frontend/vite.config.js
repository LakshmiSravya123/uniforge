import { defineConfig } from 'vite';

export default defineConfig({
  server: {
    port: 5174,
    host: '0.0.0.0',
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5001',
        changeOrigin: true,
        rewrite: (path) => path
      },
      '/data': {
        target: 'http://127.0.0.1:5001',
        changeOrigin: true
      },
      '/save': {
        target: 'http://127.0.0.1:5001',
        changeOrigin: true
      },
      '/record': {
        target: 'http://127.0.0.1:5001',
        changeOrigin: true
      },
      '/replay': {
        target: 'http://127.0.0.1:5001',
        changeOrigin: true
      }
    }
  }
});
