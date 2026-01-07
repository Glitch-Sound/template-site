<script setup lang="ts">
import { marked } from 'marked'

marked.setOptions({
  breaks: true,
})

const props = defineProps<{
  src: string
}>()
</script>

<template>
  <div class="markdown-body" v-html="marked(props.src)" />
</template>

<style scoped>
.markdown-body :deep(ul),
.markdown-body :deep(ol) {
  padding-left: 1.25rem;
  margin: 0.25rem 0;
}

.markdown-body :deep(ul) {
  list-style: disc;
}

.markdown-body :deep(ol) {
  list-style: decimal;
}

.markdown-body :deep(h1),
.markdown-body :deep(h2),
.markdown-body :deep(h3),
.markdown-body :deep(h4),
.markdown-body :deep(h5),
.markdown-body :deep(h6) {
  margin: 0.6rem 0 0.35rem;
  font-weight: 600;
}

.markdown-body :deep(h1) {
  font-size: 1.5rem;
}

.markdown-body :deep(h2) {
  font-size: 1.3rem;
}

.markdown-body :deep(h3) {
  font-size: 1.15rem;
}

.markdown-body :deep(p) {
  margin: 0.35rem 0;
}

.markdown-body :deep(a) {
  color: #8fbaff;
  text-decoration: underline;
}

.markdown-body :deep(strong) {
  color: #f0f0f0;
  font-weight: 700;
}

.markdown-body :deep(em) {
  color: #d6d6d6;
  font-style: italic;
}

.markdown-body :deep(blockquote) {
  margin: 0.5rem 0;
  padding: 0.5rem 0.75rem;
  border-left: 2px solid #9f9f9f;
  background: #1a1a1a;
  color: #d0d0d0;
}

.markdown-body :deep(pre) {
  margin: 0.5rem 0;
  padding: 0.6rem 0.75rem;
  background: #0f0f0f;
  border: 1px solid #2a2a2a;
  border-radius: 6px;
  overflow-x: auto;
}

.markdown-body :deep(code) {
  padding: 0.1rem 0.3rem;
  background: #141414;
  border: 1px solid #2a2a2a;
  border-radius: 4px;
  font-family: 'DM Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono',
    'Courier New', monospace;
  font-size: 0.92em;
}

.markdown-body :deep(pre code) {
  padding: 0;
  border: 0;
  background: transparent;
}

.markdown-body :deep(hr) {
  margin: 0.75rem 0;
  border: 0;
  border-top: 1px solid #2a2a2a;
}

.markdown-body :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 0.5rem 0;
}

.markdown-body :deep(th),
.markdown-body :deep(td) {
  border: 1px solid #2a2a2a;
  padding: 0.35rem 0.5rem;
}

.markdown-body :deep(th) {
  background: #141414;
  font-weight: 600;
}
</style>
