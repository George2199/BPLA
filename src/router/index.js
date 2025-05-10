import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'login',
    component: () => import('@/views/Autorizatiion.vue'),
    meta: {
      title: 'Вход',
      hideSidebar: true,
      hasHeader: false
     }
  },
  {
    path: '/courses',
    name: 'home',
    component: () => import('@/views/Courses.vue'),
    meta: { title: 'Курсы',
      hasHeader: true
    }
  },
  {
    path: '/tasks',
    name: 'tasks',
    component: () => import('@/views/Tasks.vue'),
    meta: { title: 'Задания' ,
      hasHeader: true
    }
  },
  {
    path: '/courses/:id',
    name: 'course',
    component: () => import('@/views/Tasks.vue'),
    meta: {
      hasHeader: true
    }
     // или твой курс-компонент
    // meta здесь не нужен, так как будет динамически с бэка
  }
]

const router = createRouter({
  history: createWebHashHistory(), // 👈 вот это изменение
  routes
})

router.beforeEach((to, from, next) => {
  console.log('Navigating to:', to.name)
  next()
})

export default router
