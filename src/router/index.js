import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'login',
    component: () => import('@/views/Autorizatiion.vue')
  },
  {
    path: '/courses',
    component: () => import('@/views/Courses.vue'),
    name: 'home'
  },
  {
    path: '/tasks',
    component: () => import('@/views/Tasks.vue'),
    name: 'tasks',
    meta: { requiresAuth: false }
  }
  
]


const router = createRouter({
  history: createWebHistory(),
  routes
})

// Добавляем глобальный навигационный хук
router.beforeEach((to, from, next) => {
  console.log('Navigating to:', to.name)
  next()
})

export default router