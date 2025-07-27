import { defineStore } from 'pinia'

import type { Login } from '@/types/Auth'
import type { User } from '@/types/User'

import service_auth from '@/services/AuthService'
import service_user from '@/services/UserService'

const useAuthStore = defineStore('auth', {
  state: () => ({
    user_login: null as User | null,
  }),
  actions: {
    async login(login: Login): Promise<void> {
      const result = await service_auth.login(login)
      this.user_login = await service_user.fetchUserByRID(result.rid)
    },

    isLogined(): boolean {
      return service_auth.isLogined()
    },
  },
})

export default useAuthStore
