import apiClient from '@/services/ApiClient'
import type { SummaryAmount, SummaryCompany } from '@/types/Summary'
import type { Project } from '@/types/Project'

class SummaryService {
  public async fetchSummariesAmountLatest(): Promise<SummaryAmount[]> {
    try {
      const response = await apiClient.get<SummaryAmount[]>('/summaries/amount/latest')
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(
        `fetchSummariesAmountLatest: ${error instanceof Error ? error.message : String(error)}`,
      )
    }
  }

  public async fetchSummariesAmount(year: number): Promise<SummaryAmount[]> {
    try {
      const response = await apiClient.get<SummaryAmount[]>(`/summaries/amount/${year}`)
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(
        `fetchSummariesAmount: ${error instanceof Error ? error.message : String(error)}`,
      )
    }
  }

  public async fetchSummariesCompanyLatest(): Promise<SummaryCompany[]> {
    try {
      const response = await apiClient.get<SummaryCompany[]>('/summaries/company/latest')
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(
        `fetchSummariesCompanyLatest: ${error instanceof Error ? error.message : String(error)}`,
      )
    }
  }

  public async fetchSummariesCompany(year: number): Promise<SummaryCompany[]> {
    try {
      const response = await apiClient.get<SummaryCompany[]>(`/summaries/company/${year}`)
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(
        `fetchSummariesCompany: ${error instanceof Error ? error.message : String(error)}`,
      )
    }
  }

  public async fetchSummariesDeadline(): Promise<Project[]> {
    try {
      const response = await apiClient.get<Project[]>('/summaries/deadline')
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(
        `fetchSummariesDeadline: ${error instanceof Error ? error.message : String(error)}`,
      )
    }
  }

  public async fetchSummariesIncomplete(): Promise<Project[]> {
    try {
      const response = await apiClient.get<Project[]>('/summaries/incomplete')
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(
        `fetchSummariesIncomplete: ${error instanceof Error ? error.message : String(error)}`,
      )
    }
  }

  public async fetchSummariesAlert(): Promise<Project[]> {
    try {
      const response = await apiClient.get<Project[]>('/summaries/alert')
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(
        `fetchSummariesAlert: ${error instanceof Error ? error.message : String(error)}`,
      )
    }
  }
}

const service_summary = new SummaryService()
export default service_summary
