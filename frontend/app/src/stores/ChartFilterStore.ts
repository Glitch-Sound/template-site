import { ref } from 'vue'
import { defineStore } from 'pinia'

import { TypeRank } from '@/types/Project'

export const useChartFilterStore = defineStore('chartFilter', () => {
  const selectedRanks = ref<TypeRank[]>([TypeRank.A])
  const amountMode = ref<'order' | 'expected'>('order')

  return {
    selectedRanks,
    amountMode,
  }
})
