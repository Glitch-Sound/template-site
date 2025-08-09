import apiClient from '@/services/ApiClient'
import type { Company, CompanyCreate, CompanyUpdate } from '@/types/Company'

class CompanyService {
  public async fetchCompanies(): Promise<Company[]> {
    try {
      const response = await apiClient.get<Company[]>('/companies')
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(`fetchCompanies: ${error instanceof Error ? error.message : String(error)}`)
    }
  }

  public async createCompany(company: CompanyCreate): Promise<Company> {
    try {
      const response = await apiClient.post<Company>('/companies', company)
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(`createCompany: ${error instanceof Error ? error.message : String(error)}`)
    }
  }

  public async updateCompany(company: CompanyUpdate): Promise<Company> {
    try {
      const response = await apiClient.put<Company>('/companies', company)
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(`updateCompany: ${error instanceof Error ? error.message : String(error)}`)
    }
  }

  public async deleteCompany(rid: number): Promise<void> {
    try {
      await apiClient.delete(`/companies/${rid}`)
    } catch (error: unknown) {
      console.error(error)
      throw new Error(`deleteCompany: ${error instanceof Error ? error.message : String(error)}`)
    }
  }
}

const service_company = new CompanyService()
export default service_company
