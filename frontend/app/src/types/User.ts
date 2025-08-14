// prettier-ignore
export enum TypePost {
  NONE = 0,
  K    = 1,
  C    = 2,
  L    = 3,
  T    = 4,
  BP   = 5,
}

// prettier-ignore
export enum TypeContract {
  NONE      = 0,
  PROPER    = 1,
  TEMP      = 2,
  CONSIGN_C = 3,
  CONSIGN_M = 4,
}

export interface User {
  rid: number
  eid: string
  username: string
  name: string
  company: string
  post: TypePost
  contract: TypeContract
  is_admin: boolean
}

export interface UserCreate {
  eid: string
  username: string
  password: string
  name: string
  company: string
  post: TypePost
  contract: TypeContract
  is_admin: boolean
}

export interface UserUpdate {
  rid: number
  eid: string
  username: string
  password: string
  name: string
  company: string
  post: TypePost
  contract: TypeContract
  is_admin: boolean
}
