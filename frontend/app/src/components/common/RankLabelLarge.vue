<script setup lang="ts">
import { TypeRank, type Project } from '@/types/Project'

const props = defineProps<{
  project: Project
}>()
</script>

<template>
  <v-icon size="x-large" color="#2196f3" v-if="props.project.rank == TypeRank.A">
    mdi-alpha-a-box
  </v-icon>
  <v-icon size="x-large" color="#528edb" v-if="props.project.rank == TypeRank.B">
    mdi-alpha-b-box
  </v-icon>
  <v-icon size="x-large" color="#857fc3" v-if="props.project.rank == TypeRank.C">
    mdi-alpha-c-box
  </v-icon>
  <v-icon size="x-large" color="#b06fab" v-if="props.project.rank == TypeRank.D">
    mdi-alpha-d-box
  </v-icon>
  <v-icon size="x-large" color="#808080" v-if="props.project.rank == TypeRank.E">
    mdi-alpha-e-box
  </v-icon>
</template>

<style scoped>
@import '@/assets/main.css';
</style>
