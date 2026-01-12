export type ThreadIndentOptions = {
  indentStep?: number
  lineColor?: string
  lineGap?: number
  lineWidth?: number
  paddingOffset?: number
}

export const threadIndentStyle = (depth: number, options: ThreadIndentOptions = {}) => {
  const level = Math.max(0, depth)
  const {
    indentStep = 40,
    lineColor = '#2e2e2e',
    lineGap = 8,
    lineWidth = 2,
    paddingOffset = 10,
  } = options

  if (level === 0) {
    return {
      marginLeft: '0',
      paddingLeft: '0',
      backgroundImage: 'none',
      backgroundPosition: '0 0',
      backgroundSize: '0 0',
      backgroundRepeat: 'no-repeat',
    }
  }

  const lines = Array.from({ length: level }, () => `linear-gradient(${lineColor}, ${lineColor})`)
  const positions = Array.from({ length: level }, (_, i) => `${i * lineGap}px 0`)
  const sizes = Array.from({ length: level }, () => `${lineWidth}px 100%`)

  return {
    marginLeft: `${level * indentStep}px`,
    paddingLeft: `${level * lineGap + paddingOffset}px`,
    backgroundImage: lines.join(', '),
    backgroundPosition: positions.join(', '),
    backgroundSize: sizes.join(', '),
    backgroundRepeat: 'no-repeat',
  }
}
