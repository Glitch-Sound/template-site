import apiClient from '@/services/ApiClient'
import type { Target, TargetCreate, TargetUpdate } from '@/types/Target'

class TargetService {
  public async fetchTargets(): Promise<Target[]> {
    try {
      const response = await apiClient.get<Target[]>('/targets')
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(`fetchTargets: ${error instanceof Error ? error.message : String(error)}`)
    }
  }

  public async createTarget(target: TargetCreate): Promise<Target> {
    try {
      const response = await apiClient.post<Target>('/targets', target)
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(`createTarget: ${error instanceof Error ? error.message : String(error)}`)
    }
  }

  public async updateTarget(target: TargetUpdate): Promise<Target> {
    try {
      const response = await apiClient.put<Target>('/targets', target)
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(`updateTarget: ${error instanceof Error ? error.message : String(error)}`)
    }
  }

  public async deleteTarget(rid: number): Promise<void> {
    try {
      await apiClient.delete(`/targets/${rid}`)
    } catch (error: unknown) {
      console.error(error)
      throw new Error(`deleteTarget: ${error instanceof Error ? error.message : String(error)}`)
    }
  }
}

const service_target = new TargetService()
export default service_target
