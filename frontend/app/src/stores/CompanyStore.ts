import { defineStore } from 'pinia'

import type { Company, CompanyCreate, CompanyUpdate } from '@/types/Company'

import service_company from '@/services/CompanyService'

const useCompanyStore = defineStore('company', {
  state: () => ({
    companies: [] as Array<Company>,
  }),
  actions: {
    async fetchCompanies() {
      this.companies = await service_company.fetchCompanies()
    },
    async createCompany(user: CompanyCreate): Promise<Company> {
      const result = await service_company.createCompany(user)
      await this.fetchCompanies()
      return result
    },
    async updateCompany(user: CompanyUpdate): Promise<Company> {
      const result = await service_company.updateCompany(user)
      await this.fetchCompanies()
      return result
    },
    async deleteCompany(rid: number): Promise<void> {
      const result = await service_company.deleteCompany(rid)
      await this.fetchCompanies()
      return result
    },
  },
})

export default useCompanyStore
