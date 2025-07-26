import { createRouter, createWebHistory } from 'vue-router'

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
    },
    {
      path: '/account',
      component: AccountView,
    },
    {
      path: '/viz',
      component: VizView,
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

export default router
