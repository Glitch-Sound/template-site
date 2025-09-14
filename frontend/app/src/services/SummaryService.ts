import apiClient from '@/services/ApiClient'
import type {
  SummaryTotalCompany,
  SummaryTotalProject,
  SummaryTotalPM,
  SummaryTotalPL,
  SummaryCountCompany,
  SummaryCountProject,
  SummaryCountPM,
  SummaryCountPL,
} from '@/types/Summary'

class SummaryService {
  public async fetchSummariesTotalCompany(): Promise<SummaryTotalCompany[]> {
    try {
      const response = await apiClient.get<SummaryTotalCompany[]>('/summaries/latest/company/total')
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(
        `fetchSummariesTotalCompany: ${error instanceof Error ? error.message : String(error)}`,
      )
    }
  }

  public async fetchSummariesTotalProject(): Promise<SummaryTotalProject[]> {
    try {
      const response = await apiClient.get<SummaryTotalProject[]>('/summaries/latest/project/total')
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(
        `fetchSummariesTotalProject: ${error instanceof Error ? error.message : String(error)}`,
      )
    }
  }

  public async fetchSummariesTotalPM(): Promise<SummaryTotalPM[]> {
    try {
      const response = await apiClient.get<SummaryTotalPM[]>('/summaries/latest/pm/total')
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(
        `fetchSummariesTotalPM: ${error instanceof Error ? error.message : String(error)}`,
      )
    }
  }

  public async fetchSummariesTotalPL(): Promise<SummaryTotalPL[]> {
    try {
      const response = await apiClient.get<SummaryTotalPL[]>('/summaries/latest/pl/total')
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(
        `fetchSummariesTotalPL: ${error instanceof Error ? error.message : String(error)}`,
      )
    }
  }

  public async fetchSummariesCountCompany(): Promise<SummaryCountCompany[]> {
    try {
      const response = await apiClient.get<SummaryCountCompany[]>('/summaries/latest/company/count')
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(
        `fetchSummariesCountCompany: ${error instanceof Error ? error.message : String(error)}`,
      )
    }
  }

  public async fetchSummariesCountProject(): Promise<SummaryCountProject[]> {
    try {
      const response = await apiClient.get<SummaryCountProject[]>('/summaries/latest/project/count')
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(
        `fetchSummariesCountProject: ${error instanceof Error ? error.message : String(error)}`,
      )
    }
  }

  public async fetchSummariesCountPM(): Promise<SummaryCountPM[]> {
    try {
      const response = await apiClient.get<SummaryCountPM[]>('/summaries/latest/pm/count')
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(
        `fetchSummariesCountPM: ${error instanceof Error ? error.message : String(error)}`,
      )
    }
  }

  public async fetchSummariesCountPL(): Promise<SummaryCountPL[]> {
    try {
      const response = await apiClient.get<SummaryCountPL[]>('/summaries/latest/pl/count')
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(
        `fetchSummariesCountPL: ${error instanceof Error ? error.message : String(error)}`,
      )
    }
  }

  public async fetchSummariesTotalCompanyByPeriod(year: number): Promise<SummaryTotalCompany[]> {
    try {
      const response = await apiClient.get<SummaryTotalCompany[]>(
        `/summaries/latest/company/total/${year}`,
      )
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(
        `fetchSummariesTotalCompany: ${error instanceof Error ? error.message : String(error)}`,
      )
    }
  }

  public async fetchSummariesTotalProjectByPeriod(year: number): Promise<SummaryTotalProject[]> {
    try {
      const response = await apiClient.get<SummaryTotalProject[]>(
        `/summaries/latest/project/tota/${year}`,
      )
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(
        `fetchSummariesTotalProject: ${error instanceof Error ? error.message : String(error)}`,
      )
    }
  }

  public async fetchSummariesTotalPMByPeriod(year: number): Promise<SummaryTotalPM[]> {
    try {
      const response = await apiClient.get<SummaryTotalPM[]>(`/summaries/latest/pm/total/${year}`)
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(
        `fetchSummariesTotalPM: ${error instanceof Error ? error.message : String(error)}`,
      )
    }
  }

  public async fetchSummariesTotalPLByPeriod(year: number): Promise<SummaryTotalPL[]> {
    try {
      const response = await apiClient.get<SummaryTotalPL[]>(`/summaries/latest/pl/total/${year}`)
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(
        `fetchSummariesTotalPL: ${error instanceof Error ? error.message : String(error)}`,
      )
    }
  }

  public async fetchSummariesCountCompanyByPeriod(year: number): Promise<SummaryCountCompany[]> {
    try {
      const response = await apiClient.get<SummaryCountCompany[]>(
        `/summaries/latest/company/count/${year}`,
      )
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(
        `fetchSummariesCountCompany: ${error instanceof Error ? error.message : String(error)}`,
      )
    }
  }

  public async fetchSummariesCountProjectByPeriod(year: number): Promise<SummaryCountProject[]> {
    try {
      const response = await apiClient.get<SummaryCountProject[]>(
        `/summaries/latest/project/count/${year}`,
      )
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(
        `fetchSummariesCountProject: ${error instanceof Error ? error.message : String(error)}`,
      )
    }
  }

  public async fetchSummariesCountPMByPeriod(year: number): Promise<SummaryCountPM[]> {
    try {
      const response = await apiClient.get<SummaryCountPM[]>(`/summaries/latest/pm/count/${year}`)
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(
        `fetchSummariesCountPM: ${error instanceof Error ? error.message : String(error)}`,
      )
    }
  }

  public async fetchSummariesCountPLByPeriod(year: number): Promise<SummaryCountPL[]> {
    try {
      const response = await apiClient.get<SummaryCountPL[]>(`/summaries/latest/pl/count/${year}`)
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(
        `fetchSummariesCountPL: ${error instanceof Error ? error.message : String(error)}`,
      )
    }
  }
}

const service_summary = new SummaryService()
export default service_summary
