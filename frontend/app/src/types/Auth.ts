export interface Token {
  token_access: string
  token_refresh: string
  token_type: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface RefreshRequest {
  token_refresh: string
}
