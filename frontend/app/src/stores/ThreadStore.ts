import { ref } from 'vue'
import { defineStore } from 'pinia'

import type { Thread, ThreadReport, ThreadStatus, ThreadCreate, ThreadUpdate } from '@/types/Thread'
import service_thread from '@/services/ThreadService'

export const useThreadStore = defineStore('thread', () => {
  const threads = ref<Thread[]>([])
  const threads_report = ref<ThreadReport[]>([])
  const threads_status = ref<ThreadStatus[]>([])
  const is_loading = ref(false)
  const is_loading_report = ref(false)
  const is_loading_status = ref(false)

  let inflight: Promise<void> | null = null
  let inflight_report: Promise<void> | null = null
  let inflight_status: Promise<void> | null = null

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

  async function fetchThreadsStatus(): Promise<void> {
    if (inflight_status) return inflight_status
    is_loading_status.value = true
    inflight_status = (async () => {
      try {
        threads_status.value = await service_thread.fetchThreadsStatus()
      } finally {
        is_loading_status.value = false
        inflight_status = null
      }
    })()
    return inflight_status
  }

  async function fetchThreadsByUser(rid_users: number): Promise<void> {
    if (inflight_report) return inflight_report
    is_loading_report.value = true
    inflight_report = (async () => {
      try {
        threads_report.value = await service_thread.fetchThreadsByUser(rid_users)
      } finally {
        is_loading_report.value = false
        inflight_report = null
      }
    })()
    return inflight_report
  }

  async function createThread(payload: ThreadCreate): Promise<Thread> {
    const created = await service_thread.createThread(payload)
    await fetchThreadsByRID(payload.rid_projects)
    return created
  }

  async function updateThread(payload: ThreadUpdate): Promise<Thread> {
    const updated = await service_thread.updateThread(payload)
    await fetchThreadsByRID(payload.rid_projects)
    return updated
  }

  async function deleteThread(rid_projects: number, rid: number): Promise<void> {
    await service_thread.deleteThread(rid)
    await fetchThreadsByRID(rid_projects)
  }

  function reset(): void {
    threads.value = []
    threads_report.value = []
    threads_status.value = []
  }

  return {
    // state
    threads,
    threads_report,
    threads_status,
    is_loading,
    is_loading_report,
    is_loading_status,

    // actions
    fetchThreadsByRID,
    fetchThreadsByUser,
    fetchThreadsStatus,
    createThread,
    updateThread,
    deleteThread,
    reset,
  }
})
