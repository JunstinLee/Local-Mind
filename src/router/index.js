// router/index.js
import { createRouter, createWebHashHistory } from 'vue-router'
import forTradition from '../views/forTradition.vue'

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/traditional',
    },
    {
      path: '/traditional',
      name: 'traditional',
      component: forTradition,
    },
    {
      path: '/search',
      name: 'search',
      component: () => import('../views/forSearch.vue'),
    },
    {
      path: '/qa',
      name: 'qa',
      component: () => import('../views/forQA.vue'),
    },
  ],
})

export default router