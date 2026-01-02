import { ref } from 'vue'
import { defineStore } from 'pinia'

import type { SummaryAmount, SummaryCompany } from '@/types/Summary'
import service_summary from '@/services/SummaryService'

export const useSummaryStore = defineStore('summary', () => {
  const summaries_amount_latest = ref<SummaryAmount[]>([])
  const summaries_amount_year = ref<SummaryAmount[]>([])
  const summaries_company_latest = ref<SummaryCompany[]>([])
  const summaries_company_year = ref<SummaryCompany[]>([])

  const amount_year = ref<number | null>(null)
  const company_year = ref<number | null>(null)

  const is_loading_amount_latest = ref(false)
  const is_loading_amount_year = ref(false)
  const is_loading_company_latest = ref(false)
  const is_loading_company_year = ref(false)

  let inflight_amount_latest: Promise<void> | null = null
  let inflight_amount_year: Promise<void> | null = null
  let inflight_company_latest: Promise<void> | null = null
  let inflight_company_year: Promise<void> | null = null

  async function fetchSummariesAmountLatest(): Promise<void> {
    if (inflight_amount_latest) return inflight_amount_latest
    is_loading_amount_latest.value = true
    inflight_amount_latest = (async () => {
      try {
        summaries_amount_latest.value = await service_summary.fetchSummariesAmountLatest()
      } finally {
        is_loading_amount_latest.value = false
        inflight_amount_latest = null
      }
    })()
    return inflight_amount_latest
  }

  async function fetchSummariesAmount(year: number): Promise<void> {
    if (inflight_amount_year) return inflight_amount_year
    is_loading_amount_year.value = true
    inflight_amount_year = (async () => {
      try {
        summaries_amount_year.value = await service_summary.fetchSummariesAmount(year)
        amount_year.value = year
      } finally {
        is_loading_amount_year.value = false
        inflight_amount_year = null
      }
    })()
    return inflight_amount_year
  }

  async function fetchSummariesCompanyLatest(): Promise<void> {
    if (inflight_company_latest) return inflight_company_latest
    is_loading_company_latest.value = true
    inflight_company_latest = (async () => {
      try {
        summaries_company_latest.value = await service_summary.fetchSummariesCompanyLatest()
      } finally {
        is_loading_company_latest.value = false
        inflight_company_latest = null
      }
    })()
    return inflight_company_latest
  }

  async function fetchSummariesCompany(year: number): Promise<void> {
    if (inflight_company_year) return inflight_company_year
    is_loading_company_year.value = true
    inflight_company_year = (async () => {
      try {
        summaries_company_year.value = await service_summary.fetchSummariesCompany(year)
        company_year.value = year
      } finally {
        is_loading_company_year.value = false
        inflight_company_year = null
      }
    })()
    return inflight_company_year
  }

  function reset(): void {
    summaries_amount_latest.value = []
    summaries_amount_year.value = []
    summaries_company_latest.value = []
    summaries_company_year.value = []
    amount_year.value = null
    company_year.value = null
  }

  return {
    // state
    summaries_amount_latest,
    summaries_amount_year,
    summaries_company_latest,
    summaries_company_year,
    amount_year,
    company_year,
    is_loading_amount_latest,
    is_loading_amount_year,
    is_loading_company_latest,
    is_loading_company_year,

    // actions
    fetchSummariesAmountLatest,
    fetchSummariesAmount,
    fetchSummariesCompanyLatest,
    fetchSummariesCompany,
    reset,
  }
})
