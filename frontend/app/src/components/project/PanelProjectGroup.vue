<script setup lang="ts">
import { computed } from 'vue'
import type { ProjectList } from '@/types/Project'

const props = defineProps<{
  project_group: ProjectList
}>()

const labelColors = [
  '#ffffff',
  '#6bcb77',
  '#c06c84',
  '#4d96ff',
  '#ffd93d',
  '#9b5de5',
  '#f67280',
  '#90f1ef',
  '#60d394',
  '#ffd4a5',
  '#b067ff',
  '#99c1de',
  '#ff6b6b',
  '#f4b6c2',
  '#ff9a8b',
  '#f47c7c',
]

const labelColor = computed(() => {
  const rid = props.project_group.company.rid ?? 0
  const index = Math.abs(rid) % labelColors.length
  return labelColors[index]
})
</script>

<template>
  <v-sheet class="mb-2 d-flex align-center">
    <v-chip class="mr-3 text-overline font-weight-bold">
      <v-icon icon="mdi-label" size="small" class="ml-0 mr-2" :color="labelColor" start />
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

/* check color. */
.color {
  color: #ffffff;
  color: #6bcb77;
  color: #c06c84;
  color: #4d96ff;
  color: #ffd93d;
  color: #9b5de5;
  color: #f67280;
  color: #90f1ef;
  color: #60d394;
  color: #ffd4a5;
  color: #b067ff;
  color: #99c1de;
  color: #ff6b6b;
  color: #f4b6c2;
  color: #ff9a8b;
  color: #f47c7c;
}
</style>
