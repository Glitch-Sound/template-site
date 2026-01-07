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
</style>
