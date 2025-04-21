import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'login',
    component: () => import('@/views/Autorizatiion.vue'),
    meta: { title: 'Вход' }
  },
  {
    path: '/courses',
    name: 'home',
    component: () => import('@/views/Courses.vue'),
    meta: { title: 'Курсы' }
  },
  {
    path: '/tasks',
    name: 'tasks',
    component: () => import('@/views/Tasks.vue'),
    meta: { title: 'Задания' }
  },
  {
    path: '/courses/:id',
    name: 'course',
    component: () => import('@/views/Tasks.vue') // или твой курс-компонент
    // meta здесь не нужен, так как будет динамически с бэка
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  console.log('Navigating to:', to.name)
  next()
})

export default router
