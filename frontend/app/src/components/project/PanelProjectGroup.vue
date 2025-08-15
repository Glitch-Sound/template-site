<script setup lang="ts">
import type { ProjectList } from '@/types/Project'

const props = defineProps<{
  project_group: ProjectList
}>()
</script>

<template>
  <v-sheet class="mb-2 d-flex align-center">
    <v-chip class="mr-3 text-overline font-weight-bold">
      <v-icon icon="mdi-label" size="small" class="ml-0 mr-2" color="primary" start />
      {{ props.project_group.company.name }}
    </v-chip>

    <span class="group font-weight-bold">
      {{ props.project_group.name }}
    </span>
  </v-sheet>
</template>

<style scoped>
@import '@/assets/main.css';

.group {
  color: #c0c0c0;
}
</style>
