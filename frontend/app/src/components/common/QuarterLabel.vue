<script setup lang="ts">
import { computed } from 'vue'
import { type Project } from '@/types/Project'

const props = defineProps<{
  project: Project
}>()

const year = computed(() => {
  return Math.floor(props.project.target_quarter / 10)
})

const quarter = computed(() => {
  return `${props.project.target_quarter % 10}Q`
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
