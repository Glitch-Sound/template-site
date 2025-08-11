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
  <span v-html="marked(props.src)" />
</template>

<style scoped></style>
