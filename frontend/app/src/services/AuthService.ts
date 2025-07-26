import apiClient, { setTokens, getAccessToken } from '@/services/ApiClient'
import type { Token, LoginRequest } from '@/types/Auth'

class AuthService {
  public async login(username: string, password: string): Promise<void> {
    const payload: LoginRequest = { username, password }
    const res = await apiClient.post<Token>('/login', payload)
    setTokens(res.data.token_access, res.data.token_refresh)
  }

  public isAuthenticated(): boolean {
    return !!getAccessToken()
  }
}

export default new AuthService()
