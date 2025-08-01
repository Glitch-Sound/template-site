export interface Company {
  rid: number
  name: string
  detail: string
}

export interface CompanyCreate {
  name: string
  detail: string
}

export interface CompanyUpdate {
  rid: number
  name: string
  detail: string
}
