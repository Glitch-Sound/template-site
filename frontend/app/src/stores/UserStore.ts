import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

import type { User, UserCreate, UserUpdate } from '@/types/User'
import service_user from '@/services/UserService'

export const useUserStore = defineStore('user', () => {
  const users = ref<User[]>([])
  const is_loading = ref(false)

  let inflight: Promise<void> | null = null

  // getters / helpers.
  const by_rid = computed(() => new Map(users.value.map((u) => [u.rid, u])))

  function getByRid(rid: number): User | undefined {
    return by_rid.value.get(rid)
  }

  function upsert_user(u: User) {
    const i = users.value.findIndex((x) => x.rid === u.rid)
    if (i >= 0) users.value[i] = u
    else users.value.push(u)
  }

  // actions.
  async function fetchUsers(): Promise<void> {
    if (inflight) return inflight
    is_loading.value = true
    inflight = (async () => {
      try {
        users.value = await service_user.fetchUsers()
      } finally {
        is_loading.value = false
        inflight = null
      }
    })()
    return inflight
  }

  async function createUser(payload: UserCreate): Promise<User> {
    const created = await service_user.createUser(payload)
    upsert_user(created)
    return created
  }

  async function updateUser(payload: UserUpdate): Promise<User> {
    const updated = await service_user.updateUser(payload)
    upsert_user(updated)
    return updated
  }

  async function deleteUser(rid: number): Promise<void> {
    await service_user.deleteUser(rid)
    const i = users.value.findIndex((x) => x.rid === rid)
    if (i >= 0) users.value.splice(i, 1)
  }

  function reset(): void {
    users.value = []
  }

  return {
    // state
    users,
    is_loading,

    // getters
    by_rid,
    getByRid,

    // actions
    fetchUsers,
    createUser,
    updateUser,
    deleteUser,
    reset,
  }
})
