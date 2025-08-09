import axios from 'axios'
import type { AxiosInstance, InternalAxiosRequestConfig } from 'axios'

// prettier-ignore
const TOKEN_ACCESS_KEY  = 'token_access'
const TOKEN_REFRESH_KEY = 'token_refresh'

function getAccessToken(): string | null {
  return localStorage.getItem(TOKEN_ACCESS_KEY)
}

function getRefreshToken(): string | null {
  return localStorage.getItem(TOKEN_REFRESH_KEY)
}

function setTokens(token_access: string, token_refresh: string) {
  localStorage.setItem(TOKEN_ACCESS_KEY, token_access)
  localStorage.setItem(TOKEN_REFRESH_KEY, token_refresh)
}

function clearTokens() {
  localStorage.removeItem(TOKEN_ACCESS_KEY)
  localStorage.removeItem(TOKEN_REFRESH_KEY)
}

const API_BASE_URL = import.meta.env.VITE_API_URL + '/api'

const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
  timeout: 10000,
})

apiClient.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const token_access = getAccessToken()
  if (token_access && config.headers) {
    config.headers['Authorization'] = `Bearer ${token_access}`
  }
  return config
})

type AuthErrorCallback = () => void
let onAuthError: AuthErrorCallback | null = null

function setAuthErrorCallback(cb: AuthErrorCallback) {
  onAuthError = cb
}

let isRefreshing = false
let refreshSubscribers: ((token: string) => void)[] = []

function subscribeTokenRefresh(cb: (token: string) => void) {
  refreshSubscribers.push(cb)
}

function onRrefreshed(token: string) {
  refreshSubscribers.forEach((cb) => cb(token))
  refreshSubscribers = []
}

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean }

    if (!error.response) {
      console.error('Network/CORS error:', error)
      return Promise.reject(error)
    }

    if (error.response.status === 401 && !originalRequest._retry && getRefreshToken()) {
      originalRequest._retry = true

      if (isRefreshing) {
        return new Promise((resolve) => {
          subscribeTokenRefresh((newToken: string) => {
            originalRequest.headers = originalRequest.headers || {}
            originalRequest.headers['Authorization'] = `Bearer ${newToken}`
            resolve(apiClient(originalRequest))
          })
        })
      }

      isRefreshing = true
      try {
        const refreshRes = await axios.post('/refresh', {
          token_refresh: getRefreshToken(),
        })

        const { token_access, token_refresh } = refreshRes.data
        setTokens(token_access, token_refresh)

        apiClient.defaults.headers.common['Authorization'] = `Bearer ${token_access}`
        onRrefreshed(token_access) // キューを解放

        originalRequest.headers = originalRequest.headers || {}
        originalRequest.headers['Authorization'] = `Bearer ${token_access}`
        return apiClient(originalRequest)
      } catch (refreshErr) {
        clearTokens()
        onAuthError?.()
        return Promise.reject(refreshErr)
      } finally {
        isRefreshing = false
      }
    }

    return Promise.reject(error)
  },
)

export function isAuthenticated(): boolean {
  return !!getAccessToken()
}

export default apiClient
export { setTokens, clearTokens, getAccessToken, getRefreshToken, setAuthErrorCallback }
