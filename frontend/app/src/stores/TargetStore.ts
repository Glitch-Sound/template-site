import { ref } from 'vue'
import { defineStore } from 'pinia'

import type { Target, TargetCreate, TargetUpdate } from '@/types/Target'
import service_target from '@/services/TargetService'

export const useTargetStore = defineStore('target', () => {
  const targets = ref<Target[]>([])
  const is_loading = ref(false)

  let inflight: Promise<void> | null = null

  // actions.
  async function fetchTargets(): Promise<void> {
    if (inflight) return inflight
    is_loading.value = true
    inflight = (async () => {
      try {
        targets.value = await service_target.fetchTargets()
      } finally {
        is_loading.value = false
        inflight = null
      }
    })()
    return inflight
  }

  async function createTarget(payload: TargetCreate): Promise<Target> {
    const created = await service_target.createTarget(payload)
    await fetchTargets()
    return created
  }

  async function updateTarget(payload: TargetUpdate): Promise<Target> {
    const updated = await service_target.updateTarget(payload)
    const index = targets.value.findIndex((target) => target.rid === updated.rid)
    if (index >= 0) {
      targets.value.splice(index, 1, updated)
    } else {
      targets.value.push(updated)
    }
    return updated
  }

  async function deleteTarget(rid: number): Promise<void> {
    await service_target.deleteTarget(rid)
    await fetchTargets()
  }

  function reset(): void {
    targets.value = []
  }

  return {
    // state
    targets,
    is_loading,

    // actions
    fetchTargets,
    createTarget,
    updateTarget,
    deleteTarget,
    reset,
  }
})
