<script setup lang="ts">
import { defineProps } from 'vue'

const props = defineProps<{
  start: string
  delivery: string
  end: string
}>()
</script>

<template>
  <span class="text-caption gray-dark">
    {{ props.start }}
    <v-icon size="x-small" class="mx-1">mdi-chevron-triple-right</v-icon>
    {{ props.delivery }}
    <v-icon size="x-small" class="mx-1">mdi-chevron-right</v-icon>
    {{ props.end }}
  </span>
</template>

<style scoped>
@import '@/assets/main.css';
</style>
