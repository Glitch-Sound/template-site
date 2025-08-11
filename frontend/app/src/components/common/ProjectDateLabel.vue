<script setup lang="ts">
import type { Project } from '@/types/Project'

const props = defineProps<{
  project: Project
}>()
</script>

<template>
  <span class="text-caption gray-dark">
    {{ props.project.date_start }}
    <v-icon size="x-small" class="mx-1">mdi-chevron-triple-right</v-icon>
    {{ props.project.date_delivery }}
    <v-icon size="x-small" class="mx-1">mdi-chevron-right</v-icon>
    {{ props.project.date_end }}
  </span>
</template>

<style scoped>
@import '@/assets/main.css';
</style>
