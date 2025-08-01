import apiClient from '@/services/ApiClient'
import type { Company, CompanyCreate, CompanyUpdate } from '@/types/Company'

class CompanyService {
  public async fetchCompanies(): Promise<Company[]> {
    try {
      const response = await apiClient.get<Company[]>('/company')
      return response.data
    } catch (error: any) {
      console.error(error)
      throw new Error(`fetchCompanies: ${error?.message || error}`)
    }
  }

  public async createCompany(company: CompanyCreate): Promise<Company> {
    try {
      const response = await apiClient.post<Company>('/company', company)
      return response.data
    } catch (error: any) {
      console.error(error)
      throw new Error(`createCompany: ${error?.message || error}`)
    }
  }

  public async updateCompany(company: CompanyUpdate): Promise<Company> {
    try {
      const response = await apiClient.put<Company>('/company', company)
      return response.data
    } catch (error: any) {
      console.error(error)
      throw new Error(`updateCompany: ${error?.message || error}`)
    }
  }

  public async deleteCompany(rid: number): Promise<void> {
    try {
      await apiClient.delete(`/company/${rid}`)
    } catch (error: any) {
      console.error(error)
      throw new Error(`deleteCompany: ${error?.message || error}`)
    }
  }
}

const service_company = new CompanyService()
export default service_company
