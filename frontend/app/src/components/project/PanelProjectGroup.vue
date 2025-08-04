<script setup lang="ts">
import { defineProps } from 'vue'

import type { ProjectGroup } from '@/types/Project'

const props = defineProps<{
  project_group: ProjectGroup
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

<style scoped></style>
