import apiClient, { setTokens, getAccessToken } from '@/services/ApiClient'

import type { Token, Login } from '@/types/Auth'

class AuthService {
  public async login(login: Login): Promise<Token> {
    const response = await apiClient.post<Token>('/login', login)
    setTokens(response.data.token_access, response.data.token_refresh)
    return response.data
  }

  public isLogined(): boolean {
    return !!getAccessToken()
  }
}

const service_auth = new AuthService()
export default service_auth
