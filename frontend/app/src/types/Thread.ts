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
  user: User
  state: TypeThreadState
  note: string
}

export interface ThreadCreate {
  rid_projects: number
  rid_parent: number
  state: TypeThreadState
  note: string
}

export interface ThreadUpdate {
  rid: number
  state: TypeThreadState
  note: string
}
