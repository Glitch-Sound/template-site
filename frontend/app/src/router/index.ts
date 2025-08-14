import { createRouter, createWebHistory } from 'vue-router'

import { useAuthStore } from '@/stores/AuthStore'

import MainView from '@/views/main/MainView.vue'
import ProjectView from '@/views/project/ProjectView.vue'
import MemberMainView from '@/views/member/MemberMainView.vue'
import VizMainView from '@/views/viz/VizMainView.vue'
import SettingMainView from '@/views/setting/SettingMainView.vue'
import SettingUserView from '@/views/setting/SettingUserView.vue'
import SettingCompanyView from '@/views/setting/SettingCompanyView.vue'
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
      path: '/member',
      children: [
        {
          path: 'main',
          component: MemberMainView,
        },
      ],
      meta: { requiresAuth: true },
    },
    {
      path: '/viz',
      children: [
        {
          path: 'main',
          component: VizMainView,
        },
      ],
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
          path: 'company',
          component: SettingCompanyView,
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

router.beforeEach((to) => {
  const store_auth = useAuthStore()
  const requiresAuth = to.matched.some((r) => r.meta.requiresAuth)
  if (requiresAuth && !store_auth.is_logined) {
    return { path: '/' }
  }
})

export default router
