import apiClient from '@/services/ApiClient'
import type { User, UserCreate, UserUpdate } from '@/types/User'

class UserService {
  public async fetchUsers(): Promise<User[]> {
    try {
      const response = await apiClient.get<User[]>('/user')
      return response.data
    } catch (error: any) {
      console.error(error)
      throw new Error(`fetchUsers: ${error?.message || error}`)
    }
  }

  public async fetchUserByRID(rid: number): Promise<User> {
    try {
      const response = await apiClient.get<User>(`/user/${rid}`)
      return response.data
    } catch (error: any) {
      console.error(error)
      throw new Error(`fetchUserByRID: ${error?.message || error}`)
    }
  }

  public async createUser(user: UserCreate): Promise<User> {
    try {
      const response = await apiClient.post<User>('/user', user)
      return response.data
    } catch (error: any) {
      console.error(error)
      throw new Error(`createUser: ${error?.message || error}`)
    }
  }

  public async updateUser(user: UserUpdate): Promise<User> {
    try {
      const response = await apiClient.put<User>('/user', user)
      return response.data
    } catch (error: any) {
      console.error(error)
      throw new Error(`updateUser: ${error?.message || error}`)
    }
  }

  public async deleteUser(rid: number): Promise<void> {
    try {
      await apiClient.delete(`/user/${rid}`)
    } catch (error: any) {
      console.error(error)
      throw new Error(`deleteUser: ${error?.message || error}`)
    }
  }
}

const service_user = new UserService()
export default service_user
