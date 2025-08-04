<script setup lang="ts">
import { defineProps, computed } from 'vue'
import { type Project } from '@/types/Project'

const props = defineProps<{ project: Project }>()

const year = computed(() => {
  const dateStr = props.project.date_end
  if (!dateStr) return ''
  return dateStr.slice(2, 4)
})
const quarter = computed(() => {
  const dateStr = props.project.date_end
  if (!dateStr) return ''

  const mm = Number(dateStr.split('-')[1])
  let q = 1
  if (mm >= 1 && mm <= 3) q = 1
  else if (mm >= 4 && mm <= 6) q = 2
  else if (mm >= 7 && mm <= 9) q = 3
  else if (mm >= 10 && mm <= 12) q = 4
  return `${q}Q`
})
</script>

<template>
  <v-row dense class="ma-0 pa-0 flex-column align-center">
    <v-col cols="auto" class="pa-0 text-center">
      <span class="text-subtitle-1 font-weight-black gray-light">
        {{ year }}
      </span>
    </v-col>
    <v-col cols="auto" class="pa-0 text-center gray-dark mt-n1">
      {{ quarter }}
    </v-col>
  </v-row>
</template>

<style scoped>
@import '@/assets/main.css';
</style>
