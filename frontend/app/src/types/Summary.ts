import type { Company } from '@/types/Company'
import { TypeRank } from '@/types/Project'

export interface SummaryAmount {
  rid: number
  date_snap: string
  rank: TypeRank
  quarter1_expected: number
  quarter1_order: number
  quarter2_expected: number
  quarter2_order: number
  quarter3_expected: number
  quarter3_order: number
  quarter4_expected: number
  quarter4_order: number
  half_first_expected: number
  half_first_order: number
  half_second_expected: number
  half_second_order: number
  all_expected: number
  all_order: number
}

export interface SummaryCompany {
  rid: number
  date_snap: string
  company: Company
  rank: number
  quarter1_expected: number
  quarter1_order: number
  quarter2_expected: number
  quarter2_order: number
  quarter3_expected: number
  quarter3_order: number
  quarter4_expected: number
  quarter4_order: number
  half_first_expected: number
  half_first_order: number
  half_second_expected: number
  half_second_order: number
  all_expected: number
  all_order: number
}

export interface SankeyCompany {
  rid: number
  name: string
  amount: number
}

export interface SankeyProjectGroup {
  rid: number
  name: string
  company_rid: number
  company_name: string
  amount: number
  project_count: number
}

export interface SankeyProjectCount {
  rid: number
  project_count: number
}

export interface SankeyCompanyPm {
  company_rid: number
  company_name: string
  project_group_rid: number
  project_group_name: string
  pm_rid: number
  pm_name: string
  amount: number
}

export interface SankeyPmPl {
  pm_rid: number
  pm_name: string
  pl_rid: number
  pl_name: string
  project_rid: number
  project_name: string
  project_group_rid: number
  amount: number
}

export interface SankeySummary {
  year: number
  total_amount: number
  companies: SankeyCompany[]
  project_groups: SankeyProjectGroup[]
  company_project_counts: SankeyProjectCount[]
  pm_project_counts: SankeyProjectCount[]
  pl_project_counts: SankeyProjectCount[]
  company_pm: SankeyCompanyPm[]
  pm_pl: SankeyPmPl[]
}
