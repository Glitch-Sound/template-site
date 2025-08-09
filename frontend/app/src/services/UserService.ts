import apiClient from '@/services/ApiClient'
import type { User, UserCreate, UserUpdate } from '@/types/User'

class UserService {
  public async fetchUsers(): Promise<User[]> {
    try {
      const response = await apiClient.get<User[]>('/users')
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(`fetchUsers: ${error instanceof Error ? error.message : String(error)}`)
    }
  }

  public async fetchUserByRID(rid: number): Promise<User> {
    try {
      const response = await apiClient.get<User>(`/users/${rid}`)
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(`fetchUserByRID: ${error instanceof Error ? error.message : String(error)}`)
    }
  }

  public async createUser(user: UserCreate): Promise<User> {
    try {
      const response = await apiClient.post<User>('/users', user)
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(`createUser: ${error instanceof Error ? error.message : String(error)}`)
    }
  }

  public async updateUser(user: UserUpdate): Promise<User> {
    try {
      const response = await apiClient.put<User>('/users', user)
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(`updateUser: ${error instanceof Error ? error.message : String(error)}`)
    }
  }

  public async deleteUser(rid: number): Promise<void> {
    try {
      await apiClient.delete(`/users/${rid}`)
    } catch (error: unknown) {
      console.error(error)
      throw new Error(`deleteUser: ${error instanceof Error ? error.message : String(error)}`)
    }
  }
}

const service_user = new UserService()
export default service_user
