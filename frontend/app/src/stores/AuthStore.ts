import { ref, computed, watch } from 'vue'
import { defineStore } from 'pinia'

import type { Status, Login } from '@/types/Auth'
import type { User, UserCreate } from '@/types/User'
import { saveLoginUser, loadLoginUser } from '@/stores/LocalStorage'
import { setAuthErrorCallback } from '@/services/ApiClient'
import service_auth from '@/services/AuthService'
import service_user from '@/services/UserService'

export const useAuthStore = defineStore('auth', () => {
  // state.
  const user_initial = ref<User | null>(null)
  try {
    user_initial.value = loadLoginUser() as User | null
  } catch {
    user_initial.value = null
    saveLoginUser(null)
  }
  const user_logined = ref<User | null>(user_initial.value)

  // getters.
  const is_logined = computed(() => user_logined.value !== null)

  // effects.
  watch(
    user_logined,
    (val) => {
      saveLoginUser(val)
      user_initial.value = val
    },
    { deep: true },
  )

  setAuthErrorCallback(() => {
    user_logined.value = null
    saveLoginUser(null)
  })

  // actions.
  async function fetchStatus(): Promise<Status> {
    try {
      return await service_auth.fetchStatus()
    } catch (err) {
      throw err
    }
  }

  async function createAdmin(user: UserCreate): Promise<User> {
    try {
      return await service_auth.createAdmin(user)
    } catch (err) {
      throw err
    }
  }

  async function login(login: Login): Promise<void> {
    try {
      const result = await service_auth.login(login)
      user_logined.value = await service_user.fetchUserByRID(result.rid)
      saveLoginUser(user_logined.value)
    } catch (err) {
      user_logined.value = null
      saveLoginUser(null)
      throw err
    }
  }

  async function logout(): Promise<void> {
    try {
      // TODO
    } finally {
      user_logined.value = null
      saveLoginUser(null)
    }
  }

  function reset(): void {
    user_logined.value = null
    saveLoginUser(null)
  }

  return {
    user_initial,
    user_logined,
    is_logined,
    fetchStatus,
    createAdmin,
    login,
    logout,
    reset,
  }
})
