import { TypeRank } from '@/types/Project'

export const chartPalette = [
  '#ffffff',
  '#00948B', // Z
  '#003C88', // G
  '#3e3e3e', // S
  '#00B0D4', // D
  '#C00000', // M
  '#4fa29e', // M4
  '#4955A3', // T
  '#1CA3CE', // T4
  '#ffffff',
  '#ffffff',
  '#ffffff',
  '#ffffff',
  '#ffffff',
  '#ffffff',
  '#ffffff',
]

export const rankPalette: Record<TypeRank, string> = {
  [TypeRank.NONE]: '#000000',
  [TypeRank.A]: '#2196f3',
  [TypeRank.B]: '#4caf8a',
  [TypeRank.C]: '#b06fab',
  [TypeRank.D]: '#c3bf7f',
  [TypeRank.E]: '#808080',
}
