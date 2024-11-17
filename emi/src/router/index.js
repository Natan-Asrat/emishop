import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomeView.vue')
    },
    {
      path: '/signup',
      name: 'signup',
      component: () => import('@/views/AuthView.vue')
    },
    {
      path: '/new',
      name: 'new',
      component: () => import('@/views/NewPostView.vue')
    },
    {
      path: '/transactions',
      name: 'transactions',
      component: () => import('@/views/TransactionsView.vue')
    },
    {
      path: '/favourites',
      name: 'favourites',
      component: () => import('@/views/FavouritesView.vue')
    },
    {
      path: '/chat',
      name: 'chat',
      component: () => import('@/views/ChatVIew.vue')
    }

  ],
})

export default router
