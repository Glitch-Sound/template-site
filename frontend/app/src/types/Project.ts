import type { Company } from '@/types/Company'

import type { User } from '@/types/User'

// prettier-ignore
export enum TypeRank {
  NONE = 0,
  A    = 1,
  B    = 2,
  C    = 3,
  D    = 4,
  E    = 5
}

// prettier-ignore
export enum TypeNumber {
  NONE = 0,
  M    = 1,
  S    = 2,
  O    = 3
}

// prettier-ignore
export enum TypeQuarter {
  NONE = 0,
  Q1   = 1,
  Q2   = 2,
  Q3   = 3,
  Q4   = 4,
}

export interface ProjectGroup {
  rid: number
  name: string
  detail: string
  company: Company
}

export interface ProjectGroupCreate {
  rid_companies: number
  name: string
  detail: string
}

export interface ProjectGroupUpdate {
  rid: number
  rid_companies: number
  name: string
  detail: string
}

export interface ProjectNumber {
  rid: number
  type: TypeNumber
  number: string
  date_start: string
  date_end: string
}

export interface ProjectNumberCreate {
  rid_projects: number
  type: TypeNumber
  number: string
  date_start: string
  date_end: string
}

export interface ProjectNumberUpdate {
  rid: number
  rid_projects: number
  type: TypeNumber
  number: string
  date_start: string
  date_end: string
}

export interface Project {
  rid: number
  project_group: ProjectGroup
  user_pm: User
  user_pl: User
  rank: TypeRank
  pre_approval: string
  name: string
  number_parent: string
  numbers: ProjectNumber[]
  number_m: boolean
  number_s: boolean
  number_o: boolean
  amount_expected: number
  amount_order: number
  date_start: string
  date_delivery: string
  date_end: string
  karte_plan: boolean
  karte_report: boolean
  checklist: boolean
}

export interface ProjectCreate {
  rid_project_groups: number
  rid_users_pm: number
  rid_users_pl: number
  rank: TypeRank
  pre_approval: string
  name: string
  number_parent: string
  amount_expected: number
  amount_order: number
  date_start: string
  date_delivery: string
  date_end: string
}

export interface ProjectUpdate {
  rid: number
  rid_project_groups: number
  rid_users_pm: number
  rid_users_pl: number
  rank: TypeRank
  pre_approval: string
  name: string
  number_parent: string
  amount_expected: number
  amount_order: number
  date_start: string
  date_delivery: string
  date_end: string
}

export interface ProjectList {
  rid: number
  name: string
  company: Company
  projects: Project[]
}

export interface FilterQuarter {
  year: number
  quarter: TypeQuarter
}
