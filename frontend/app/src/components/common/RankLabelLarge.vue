<script setup lang="ts">
import { TypeRank, type Project } from '@/types/Project'
import { rankPalette } from '@/constants/chartPalette'

const props = defineProps<{
  project: Project
}>()
</script>

<template>
  <v-icon size="x-large" :color="rankPalette[TypeRank.A]" v-if="props.project.rank == TypeRank.A">
    mdi-alpha-a-box
  </v-icon>
  <v-icon size="x-large" :color="rankPalette[TypeRank.B]" v-if="props.project.rank == TypeRank.B">
    mdi-alpha-b-box
  </v-icon>
  <v-icon size="x-large" :color="rankPalette[TypeRank.C]" v-if="props.project.rank == TypeRank.C">
    mdi-alpha-c-box
  </v-icon>
  <v-icon size="x-large" :color="rankPalette[TypeRank.D]" v-if="props.project.rank == TypeRank.D">
    mdi-alpha-d-box
  </v-icon>
  <v-icon size="x-large" :color="rankPalette[TypeRank.E]" v-if="props.project.rank == TypeRank.E">
    mdi-alpha-e-box
  </v-icon>
  <v-icon size="x-large" :color="rankPalette[TypeRank.X]" v-if="props.project.rank == TypeRank.X">
    mdi-alpha-x-box
  </v-icon>
</template>

<style scoped>
@import '@/assets/main.css';
</style>
