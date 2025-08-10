import apiClient from '@/services/ApiClient'
import type { Thread, ThreadCreate, ThreadUpdate } from '@/types/Thread'

class ThreadService {
  public async fetchThreadsByRID(rid: number): Promise<Thread[]> {
    try {
      const response = await apiClient.get<Thread[]>(`/threads/${rid}`)
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(
        `fetchThreadsByRID: ${error instanceof Error ? error.message : String(error)}`,
      )
    }
  }

  public async createThread(thread: ThreadCreate): Promise<Thread> {
    try {
      const response = await apiClient.post<Thread>('/threads', thread)
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(`createThread: ${error instanceof Error ? error.message : String(error)}`)
    }
  }

  public async updateThread(thread: ThreadUpdate): Promise<Thread> {
    try {
      const response = await apiClient.put<Thread>('/threads', thread)
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(`updateThread: ${error instanceof Error ? error.message : String(error)}`)
    }
  }

  public async deleteThread(rid: number): Promise<void> {
    try {
      await apiClient.delete(`/threads/${rid}`)
    } catch (error: unknown) {
      console.error(error)
      throw new Error(`deleteThread: ${error instanceof Error ? error.message : String(error)}`)
    }
  }
}

const service_thread = new ThreadService()
export default service_thread
