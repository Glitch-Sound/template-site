<script setup lang="ts">
import { defineProps } from 'vue'

import { type Project } from '@/types/Project'

const props = defineProps<{
  project: Project
}>()

function formatYen(amount?: number | null): string {
  if (typeof amount !== 'number') return '-'
  return `¥${amount.toLocaleString('ja-JP')}`
}
</script>

<template>
  <v-card>
    <span class="text-caption gray-dark text-end d-block">
      {{ formatYen(props.project.amount_expected) }}
    </span>
  </v-card>
  <v-card>
    <span class="text-subtitle-1 font-weight-bold text-end d-block">
      {{ formatYen(props.project.amount_order) }}
    </span>
  </v-card>
</template>

<style scoped>
@import '@/assets/main.css';
</style>
