import { ref } from 'vue'
import { defineStore } from 'pinia'

import type { Thread, ThreadCreate, ThreadUpdate } from '@/types/Thread'
import service_thread from '@/services/ThreadService'

export const useThreadStore = defineStore('thread', () => {
  const threads = ref<Thread[]>([])
  const is_loading = ref(false)

  let inflight: Promise<void> | null = null

  // getters / helpers.
  function upsert_thread(u: Thread) {
    const i = threads.value.findIndex((x) => x.rid === u.rid)
    if (i >= 0) threads.value[i] = u
    else threads.value.push(u)
  }

  // actions.
  async function fetchThreadsByRID(rid: number): Promise<void> {
    if (inflight) return inflight
    is_loading.value = true
    inflight = (async () => {
      try {
        threads.value = await service_thread.fetchThreadsByRID(rid)
      } finally {
        is_loading.value = false
        inflight = null
      }
    })()
    return inflight
  }

  async function createThread(payload: ThreadCreate): Promise<Thread> {
    const created = await service_thread.createThread(payload)
    upsert_thread(created)
    return created
  }

  async function updateThread(payload: ThreadUpdate): Promise<Thread> {
    const updated = await service_thread.updateThread(payload)
    upsert_thread(updated)
    return updated
  }

  async function deleteThread(rid: number): Promise<void> {
    await service_thread.deleteThread(rid)
    const i = threads.value.findIndex((x) => x.rid === rid)
    if (i >= 0) threads.value.splice(i, 1)
  }

  function reset(): void {
    threads.value = []
  }

  return {
    // state
    threads,
    is_loading,

    // actions
    fetchThreadsByRID,
    createThread,
    updateThread,
    deleteThread,
    reset,
  }
})
