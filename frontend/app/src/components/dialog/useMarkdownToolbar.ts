import { nextTick, type Ref } from 'vue'

export type MarkdownAction =
  | 'bold'
  | 'italic'
  | 'strike'
  | 'codeblock'
  | 'quote'
  | 'list'
  | 'h1'
  | 'h2'
  | 'h3'
  | 'checkbox'

type TextareaRef = Ref<{ $el?: HTMLElement } | null>

const getTextarea = (textareaRef: TextareaRef) => {
  const root = textareaRef.value?.$el
  return root ? (root.querySelector('textarea') as HTMLTextAreaElement | null) : null
}

const wrapSelection = (note: Ref<string>, textareaRef: TextareaRef, prefix: string, suffix: string, placeholder: string) => {
  const textarea = getTextarea(textareaRef)
  const value = note.value ?? ''

  if (!textarea) {
    note.value = `${value}${prefix}${placeholder}${suffix}`
    return
  }

  const start = textarea.selectionStart ?? 0
  const end = textarea.selectionEnd ?? 0
  const selected = value.slice(start, end) || placeholder
  const nextValue = `${value.slice(0, start)}${prefix}${selected}${suffix}${value.slice(end)}`

  note.value = nextValue
  nextTick(() => {
    textarea.focus()
    const selectionStart = start + prefix.length
    textarea.setSelectionRange(selectionStart, selectionStart + selected.length)
  })
}

const prefixLines = (note: Ref<string>, textareaRef: TextareaRef, prefix: string) => {
  const textarea = getTextarea(textareaRef)
  const value = note.value ?? ''

  if (!textarea) {
    note.value = `${value}${prefix}`
    return
  }

  const start = textarea.selectionStart ?? 0
  const end = textarea.selectionEnd ?? 0
  if (start === end) {
    note.value = `${value.slice(0, start)}${prefix}${value.slice(start)}`
    nextTick(() => {
      textarea.focus()
      const cursor = start + prefix.length
      textarea.setSelectionRange(cursor, cursor)
    })
    return
  }

  const selected = value.slice(start, end)
  const withPrefix = selected
    .split('\n')
    .map((line) => `${prefix}${line}`)
    .join('\n')
  const nextValue = `${value.slice(0, start)}${withPrefix}${value.slice(end)}`

  note.value = nextValue
  nextTick(() => {
    textarea.focus()
    textarea.setSelectionRange(start, start + withPrefix.length)
  })
}

export const useMarkdownToolbar = (note: Ref<string>, textareaRef: TextareaRef) => {
  const applyMarkdown = (action: MarkdownAction) => {
    switch (action) {
      case 'bold':
        wrapSelection(note, textareaRef, '**', '**', 'bold text')
        break
      case 'italic':
        wrapSelection(note, textareaRef, '*', '*', 'italic text')
        break
      case 'strike':
        wrapSelection(note, textareaRef, '~~', '~~', 'strikethrough')
        break
      case 'codeblock':
        wrapSelection(note, textareaRef, '```\n', '\n```', 'code block')
        break
      case 'quote':
        prefixLines(note, textareaRef, '> ')
        break
      case 'list':
        prefixLines(note, textareaRef, '- ')
        break
      case 'h1':
        prefixLines(note, textareaRef, '# ')
        break
      case 'h2':
        prefixLines(note, textareaRef, '## ')
        break
      case 'h3':
        prefixLines(note, textareaRef, '### ')
        break
      case 'checkbox':
        prefixLines(note, textareaRef, '- [ ] ')
        break
    }
  }

  return { applyMarkdown }
}
