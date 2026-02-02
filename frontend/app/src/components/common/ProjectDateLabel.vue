<script setup lang="ts">
import { TypeRank } from '@/types/Project'
import type { Project } from '@/types/Project'

const props = defineProps<{
  project: Project
}>()
</script>

<template>
  <span class="text-caption gray-dark">
    <template v-if="props.project.rank === TypeRank.E">-</template>
    <template v-else>
      {{ props.project.date_start || '-' }}
      <v-icon size="x-small" class="mx-1">mdi-chevron-triple-right</v-icon>
      {{ props.project.date_delivery || '-' }}
      <v-icon size="x-small" class="mx-1">mdi-chevron-right</v-icon>
      {{ props.project.date_end || '-' }}
    </template>
  </span>
</template>

<style scoped>
</style>
