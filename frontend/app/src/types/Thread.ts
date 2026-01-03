import type { User } from '@/types/User'

// prettier-ignore
export enum TypeThreadState {
    NONE      = 0,
    RUN       = 1,
    IMPORTANT = 2,
    COMPLETED = 3,
  }

export interface Thread {
  rid: number
  depth: number
  user: User
  state: TypeThreadState
  note: string
  created_at: string
}

export interface ThreadStatus {
  rid_projects: number
  count: number
  is_updated: boolean
}

export interface ThreadCreate {
  rid_projects: number
  rid_parent: number | null
  state: TypeThreadState
  note: string
}

export interface ThreadUpdate {
  rid: number
  rid_projects: number
  state: TypeThreadState
  note: string
}
