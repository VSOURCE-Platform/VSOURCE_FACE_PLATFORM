import { defineConfig } from 'vite'
import reactRefresh from '@vitejs/plugin-react-refresh'

// https://vitejs.dev/config/
//export default defineConfig({
//  plugins: [reactRefresh()]
//})

export default defineConfig({
server: {
    proxy: {
      '/app': {
        target: 'http://localhost:12349',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/app/, '')
      }
    },
    plugins: [reactRefresh()]
  }
})