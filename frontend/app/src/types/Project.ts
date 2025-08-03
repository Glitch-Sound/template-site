import type { Company } from '@/types/Company'

export interface ProjectGroup {
  rid: number
  company: Company
  name: string
  detail: string
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
