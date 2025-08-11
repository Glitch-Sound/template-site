<script setup lang="ts">
import type { ProjectList } from '@/types/Project'

const props = defineProps<{
  project_group: ProjectList
}>()
</script>

<template>
  <v-sheet>
    <v-chip class="mr-3 text-overline font-weight-bold">
      {{ props.project_group.company.name }}
    </v-chip>

    {{ props.project_group.name }}
  </v-sheet>
</template>

<style scoped>
@import '@/assets/main.css';
</style>
