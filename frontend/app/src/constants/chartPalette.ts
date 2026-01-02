import { TypeRank } from '@/types/Project'

export const chartPalette = [
  '#ffffff',
  '#00948B',
  '#90f1ef',
  '#9f9f9f',
  '#ffd93d',
  '#9b5de5',
  '#f67280',
  '#90f1c4',
  '#60d394',
  '#ffd4a5',
  '#b067ff',
  '#99c1de',
  '#ff6b6b',
  '#f4b6c2',
  '#ff9a8b',
  '#f47c7c',
]

export const rankPalette: Record<TypeRank, string> = {
  [TypeRank.NONE]: '#000000',
  [TypeRank.A]: '#2196f3',
  [TypeRank.B]: '#4caf8a',
  [TypeRank.C]: '#b06fab',
  [TypeRank.D]: '#c3bf7f',
  [TypeRank.E]: '#808080',
}
