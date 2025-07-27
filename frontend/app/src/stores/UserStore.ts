import { defineStore } from 'pinia'

import type { User, UserCreate, UserUpdate } from '@/types/User'

import service_user from '@/services/UserService'

const useUserStore = defineStore('user', {
  state: () => ({
    users: [] as Array<User>,
  }),
  actions: {
    async fetchUsers() {
      this.users = await service_user.fetchUsers()
    },
    async createUser(user: UserCreate): Promise<User> {
      const result = await service_user.createUser(user)
      await this.fetchUsers()
      return result
    },
    async updateUser(user: UserUpdate): Promise<User> {
      const result = await service_user.updateUser(user)
      await this.fetchUsers()
      return result
    },
    async deleteUser(rid: number): Promise<void> {
      const result = await service_user.deleteUser(rid)
      await this.fetchUsers()
      return result
    },
  },
})

export default useUserStore
