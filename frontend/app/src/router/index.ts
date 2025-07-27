import { createRouter, createWebHistory } from 'vue-router'

import useAuthStore from '@/stores/AuthStore'

import MainView from '@/views/main/MainView.vue'
import ProjectView from '@/views/project/ProjectView.vue'
import AccountView from '@/views/account/AccountView.vue'
import VizView from '@/views/viz/VizView.vue'

import SettingMainView from '@/views/setting/SettingMainView.vue'
import SettingUserView from '@/views/setting/SettingUserView.vue'
import SettingProjectView from '@/views/setting/SettingProjectView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'main',
      component: MainView,
    },
    {
      path: '/project',
      component: ProjectView,
      meta: { requiresAuth: true },
    },
    {
      path: '/account',
      component: AccountView,
      meta: { requiresAuth: true },
    },
    {
      path: '/viz',
      component: VizView,
      meta: { requiresAuth: true },
    },
    {
      path: '/setting',
      children: [
        {
          path: 'main',
          component: SettingMainView,
        },
        {
          path: 'user',
          component: SettingUserView,
        },
        {
          path: 'project',
          component: SettingProjectView,
        },
      ],
      meta: { requiresAuth: true },
    },
  ],
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth)

  if (requiresAuth && !authStore.user_login) {
    next('/')
  } else {
    next()
  }
})

export default router
