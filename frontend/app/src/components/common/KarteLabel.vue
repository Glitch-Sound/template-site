<script setup lang="ts">
import { type Project } from '@/types/Project'

const props = defineProps<{
  project: Project
}>()
</script>

<template>
  <v-row>
    <v-col cols="auto">
      <span class="text-body-2 gray-light"> Karte + checklist : </span>
    </v-col>
    <v-col cols="auto">
      <template v-if="props.project.karte_plan">
        <v-chip size="small" color="#a8326d" class="font-weight-bold"> PLAN </v-chip>
      </template>
      <template v-else>
        <v-chip size="small" disabled> PLAN </v-chip>
      </template>
    </v-col>
    <v-col cols="auto">
      <template v-if="props.project.karte_report">
        <v-chip size="small" color="#a8326d" class="font-weight-bold"> REPORT </v-chip>
      </template>
      <template v-else>
        <v-chip size="small" disabled> REPORT </v-chip>
      </template>
    </v-col>
    <v-col cols="auto">
      <template v-if="props.project.checklist">
        <v-chip size="small" color="#a8326d" class="font-weight-bold"> CHECK </v-chip>
      </template>
      <template v-else>
        <v-chip size="small" disabled> CHECK </v-chip>
      </template>
    </v-col>
  </v-row>
</template>

<style scoped></style>
