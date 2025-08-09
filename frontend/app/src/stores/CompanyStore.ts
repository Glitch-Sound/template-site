import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

import type { Company, CompanyCreate, CompanyUpdate } from '@/types/Company'
import service_company from '@/services/CompanyService'

export const useCompanyStore = defineStore('company', () => {
  let inflight: Promise<void> | null = null

  const companies = ref<Company[]>([])
  const is_loading = ref(false)

  const by_rid = computed(() => new Map(companies.value.map((c) => [c.rid, c])))

  // helpers
  function upsertCompany(c: Company) {
    const i = companies.value.findIndex((x) => x.rid === c.rid)
    if (i >= 0) companies.value[i] = c
    else companies.value.push(c)
  }

  function getByRid(rid: number): Company | undefined {
    return by_rid.value.get(rid)
  }

  // actions
  async function fetchCompanies(): Promise<void> {
    if (inflight) return inflight
    is_loading.value = true
    inflight = (async () => {
      try {
        companies.value = await service_company.fetchCompanies()
      } catch (err) {
        throw err
      } finally {
        is_loading.value = false
        inflight = null
      }
    })()
    return inflight
  }

  async function createCompany(payload: CompanyCreate): Promise<Company> {
    const created = await service_company.createCompany(payload)
    upsertCompany(created)
    return created
  }

  async function updateCompany(payload: CompanyUpdate): Promise<Company> {
    const updated = await service_company.updateCompany(payload)
    upsertCompany(updated)
    return updated
  }

  async function deleteCompany(rid: number): Promise<void> {
    await service_company.deleteCompany(rid)
    const i = companies.value.findIndex((x) => x.rid === rid)
    if (i >= 0) companies.value.splice(i, 1)
  }

  function reset(): void {
    companies.value = []
  }

  return {
    // state
    companies,
    is_loading,

    // getters
    by_rid,
    getByRid,

    // actions
    fetchCompanies,
    createCompany,
    updateCompany,
    deleteCompany,
    reset,
  }
})
