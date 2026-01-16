import { ref } from 'vue'
import { defineStore } from 'pinia'

import type { SankeySummary, SummaryAmount, SummaryCompany } from '@/types/Summary'
import type { Project } from '@/types/Project'
import service_summary from '@/services/SummaryService'

export const useSummaryStore = defineStore('summary', () => {
  const summaries_amount_latest = ref<SummaryAmount[]>([])
  const summaries_amount_year = ref<SummaryAmount[]>([])
  const summaries_company_latest = ref<SummaryCompany[]>([])
  const summaries_company_year = ref<SummaryCompany[]>([])
  const summaries_deadline = ref<Project[]>([])
  const summaries_incomplete = ref<Project[]>([])
  const summaries_alert = ref<Project[]>([])
  const summaries_sankey = ref<SankeySummary | null>(null)

  const amount_year = ref<number | null>(null)
  const company_year = ref<number | null>(null)

  const is_loading_amount_latest = ref(false)
  const is_loading_amount_year = ref(false)
  const is_loading_company_latest = ref(false)
  const is_loading_company_year = ref(false)
  const is_loading_deadline = ref(false)
  const is_loading_incomplete = ref(false)
  const is_loading_alert = ref(false)
  const is_loading_sankey = ref(false)

  let inflight_amount_latest: Promise<void> | null = null
  let inflight_amount_year: Promise<void> | null = null
  let inflight_company_latest: Promise<void> | null = null
  let inflight_company_year: Promise<void> | null = null
  let inflight_deadline: Promise<void> | null = null
  let inflight_incomplete: Promise<void> | null = null
  let inflight_alert: Promise<void> | null = null
  let inflight_sankey: Promise<void> | null = null

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

  async function fetchSummariesDeadline(): Promise<void> {
    if (inflight_deadline) return inflight_deadline
    is_loading_deadline.value = true
    inflight_deadline = (async () => {
      try {
        summaries_deadline.value = await service_summary.fetchSummariesDeadline()
      } finally {
        is_loading_deadline.value = false
        inflight_deadline = null
      }
    })()
    return inflight_deadline
  }

  async function fetchSummariesIncomplete(): Promise<void> {
    if (inflight_incomplete) return inflight_incomplete
    is_loading_incomplete.value = true
    inflight_incomplete = (async () => {
      try {
        summaries_incomplete.value = await service_summary.fetchSummariesIncomplete()
      } finally {
        is_loading_incomplete.value = false
        inflight_incomplete = null
      }
    })()
    return inflight_incomplete
  }

  async function fetchSummariesAlert(): Promise<void> {
    if (inflight_alert) return inflight_alert
    is_loading_alert.value = true
    inflight_alert = (async () => {
      try {
        summaries_alert.value = await service_summary.fetchSummariesAlert()
      } finally {
        is_loading_alert.value = false
        inflight_alert = null
      }
    })()
    return inflight_alert
  }

  async function fetchSummariesSankey(): Promise<void> {
    if (inflight_sankey) return inflight_sankey
    is_loading_sankey.value = true
    inflight_sankey = (async () => {
      try {
        summaries_sankey.value = await service_summary.fetchSummariesSankey()
      } finally {
        is_loading_sankey.value = false
        inflight_sankey = null
      }
    })()
    return inflight_sankey
  }

  function reset(): void {
    summaries_amount_latest.value = []
    summaries_amount_year.value = []
    summaries_company_latest.value = []
    summaries_company_year.value = []
    summaries_deadline.value = []
    summaries_incomplete.value = []
    summaries_alert.value = []
    summaries_sankey.value = null
    amount_year.value = null
    company_year.value = null
  }

  return {
    // state
    summaries_amount_latest,
    summaries_amount_year,
    summaries_company_latest,
    summaries_company_year,
    summaries_deadline,
    summaries_incomplete,
    summaries_alert,
    summaries_sankey,
    amount_year,
    company_year,
    is_loading_amount_latest,
    is_loading_amount_year,
    is_loading_company_latest,
    is_loading_company_year,
    is_loading_deadline,
    is_loading_incomplete,
    is_loading_alert,
    is_loading_sankey,

    // actions
    fetchSummariesAmountLatest,
    fetchSummariesAmount,
    fetchSummariesCompanyLatest,
    fetchSummariesCompany,
    fetchSummariesDeadline,
    fetchSummariesIncomplete,
    fetchSummariesAlert,
    fetchSummariesSankey,
    reset,
  }
})
