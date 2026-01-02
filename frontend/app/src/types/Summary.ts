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
