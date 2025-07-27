import { defineStore } from 'pinia'

import type { Status, Login } from '@/types/Auth'
import type { User, UserCreate } from '@/types/User'

import service_auth from '@/services/AuthService'
import service_user from '@/services/UserService'

const useAuthStore = defineStore('auth', {
  state: () => ({
    user_login: null as User | null,
  }),
  actions: {
    async fetchStatus(): Promise<Status> {
      return await service_auth.fetchStatus()
    },
    async createAdmin(user: UserCreate): Promise<User> {
      return await service_auth.createAdmin(user)
    },
    async login(login: Login): Promise<void> {
      const result = await service_auth.login(login)
      this.user_login = await service_user.fetchUserByRID(result.rid)
    },
    isLogined(): boolean {
      return this.user_login !== null
    },
  },
})

export default useAuthStore
