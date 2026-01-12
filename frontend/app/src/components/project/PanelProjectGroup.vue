<script setup lang="ts">
import { computed } from 'vue'
import type { ProjectList } from '@/types/Project'
import { chartPalette } from '@/constants/chartPalette'

const props = defineProps<{
  project_group: ProjectList
}>()

const labelColor = computed(() => {
  const rid = props.project_group.company.rid ?? 0
  const index = Math.abs(rid) % chartPalette.length
  return chartPalette[index]
})
</script>

<template>
  <v-sheet class="mb-2 d-flex align-center">
    <v-chip class="mr-3 text-overline font-weight-bold">
      <v-icon icon="mdi-label" size="small" class="ml-0 mr-2" :color="labelColor" start />
      {{ props.project_group.company.name }}
    </v-chip>

    <span class="group font-weight-black">
      {{ props.project_group.name }}
    </span>
  </v-sheet>
</template>

<style scoped>
.group {
  color: #c0c0c0;
}
</style>
