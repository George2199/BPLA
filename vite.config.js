import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import topLevelAwait from 'vite-plugin-top-level-await'

export default defineConfig({
  define: {
    'process.env': {}, // чтобы не падали node-зависимости
  },
  optimizeDeps: {
    exclude: ['pyodide'], // отключаем оптимизацию для pyodide
  },
  plugins: [
    vue(),
    vueDevTools(),
    topLevelAwait({
      promiseExportName: '__tla', // нужно для ESM
      promiseImportName: i => `__tla_${i}`, // безопасный импорт
    }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    headers: {
      'Access-Control-Allow-Origin': '*',
    },
  },
})
