export interface Token {
  rid: number
  token_access: string
  token_refresh: string
  token_type: string
}

export interface Login {
  username: string
  password: string
}

export interface Refresh {
  token_refresh: string
}
