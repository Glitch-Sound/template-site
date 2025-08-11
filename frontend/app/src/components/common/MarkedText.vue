<script setup lang="ts">
import { marked } from 'marked'

import { defineProps } from 'vue'

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
