import apiClient, { setTokens } from '@/services/ApiClient'

import type { Status, Token, Login } from '@/types/Auth'
import type { User, UserCreate } from '@/types/User'

class AuthService {
  public async fetchStatus(): Promise<Status> {
    try {
      const response = await apiClient.get<Status>('/setup/status')
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(`fetchStatus: ${error instanceof Error ? error.message : String(error)}`)
    }
  }

  public async createAdmin(user: UserCreate): Promise<User> {
    try {
      const response = await apiClient.post<User>('/setup/admin', user)
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(`createUser: ${error instanceof Error ? error.message : String(error)}`)
    }
  }

  public async login(login: Login): Promise<Token> {
    try {
      const response = await apiClient.post<Token>('/login', login)
      setTokens(response.data.token_access, response.data.token_refresh)
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(`login: ${error instanceof Error ? error.message : String(error)}`)
    }
  }
}

const service_auth = new AuthService()
export default service_auth
