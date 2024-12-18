import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
    VitePWA({
      registerType: 'prompt',
      injectRegister: 'script',
      strategies: 'generateSW',
      filename: 'sw.js',
      manifestFilename: 'manifest.webmanifest',
      registerSWFilename: 'registerSW.js',
      includeAssets: [
        'logo_padded.png',
        'appstore.png',
        'playstore.png'
      ],
      manifest: {
        name: 'Emi Shop',
        short_name: 'Emi Shop',
        description: 'Emi Shop',
        theme_color: '#036c84',
        background_color: '#036c84',
        icons: [
          {
            src: 'logo_padded.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: 'logo_padded.png',
            sizes: '512x512',
            type: 'image/png'
          },
          {
            src: 'logo_padded.png',
            sizes: '192x192',
            type: 'image/png',
            purpose: 'maskable'
          },
          {
            src: 'logo_padded.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'maskable'
          }
        ],
        display: 'standalone',
        start_url: '/',
        scope: '/',
        shortcuts: [],
        screenshots: [],
        orientation: "portrait",
        categories: ["shopping", "lifestyle"],
        prefer_related_applications: false
      },
      workbox: {
        skipWaiting: false,
        clientsClaim: true,
        cleanupOutdatedCaches: true,
        globPatterns: [],
        navigateFallback: null,
        runtimeCaching: [
          {
            urlPattern: /^https:\/\/emishoplive\.onrender\.com\/api\/.*/i,
            handler: 'NetworkFirst',
            options: {
              cacheName: 'api-cache',
              networkTimeoutSeconds: 10,
              expiration: {
                maxEntries: 32,
                maxAgeSeconds: 24 * 60 * 60
              }
            }
          },
          {
            urlPattern: /\.(png|jpg|jpeg|svg|gif|webp)$/i,
            handler: 'NetworkFirst',
            options: {
              cacheName: 'image-cache',
              expiration: {
                maxEntries: 50,
                maxAgeSeconds: 24 * 60 * 60
              }
            }
          },
          {
            urlPattern: /\.(js|css|ico)$/,
            handler: 'NetworkFirst',
            options: {
              cacheName: 'static-cache',
              expiration: {
                maxEntries: 32,
                maxAgeSeconds: 24 * 60 * 60
              }
            }
          }
        ]
      }
    })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  base: process.env.NODE_ENV === 'production' ? '/' : '/'
})
