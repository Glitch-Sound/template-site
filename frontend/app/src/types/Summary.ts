import type { Company } from '@/types/Company'
import { TypeRank, type ProjectGroup } from '@/types/Project'
import type { User } from '@/types/User'

export interface SummaryTotalCompany {
  rid: number
  date_snap: string
  company: Company
  total_expected: number
  total_order: number
}

export interface SummaryTotalProject {
  rid: number
  date_snap: string
  project_group: ProjectGroup
  total_expected: number
  total_order: number
}

export interface SummaryTotalPM {
  rid: number
  date_snap: string
  user_pm: User
  total_expected: number
  total_order: number
}

export interface SummaryTotalPL {
  rid: number
  date_snap: string
  user_pl: User
  total_expected: number
  total_order: number
}

export interface SummaryCountCompany {
  rid: number
  date_snap: string
  company: Company
  rank: TypeRank
  count: number
}

export interface SummaryCountProject {
  rid: number
  date_snap: string
  project_group: ProjectGroup
  rank: TypeRank
  count: number
}

export interface SummaryCountPM {
  rid: number
  date_snap: string
  user_pm: User
  rank: TypeRank
  count: number
}

export interface SummaryCountPL {
  rid: number
  date_snap: string
  user_pl: User
  rank: TypeRank
  count: number
}
