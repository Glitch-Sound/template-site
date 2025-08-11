<script setup lang="ts">
import { type Project } from '@/types/Project'

const props = defineProps<{
  project: Project
}>()
</script>

<template>
  <v-row>
    <v-col cols="auto">
      <span class="text-body-2 gray-light"> Number : </span>

      <template v-if="props.project.number_parent !== ''">
        <span class="text-body-2 primary-light"> {{ props.project.number_parent }} </span>
      </template>
      <template v-else>
        <span class="text-body-2 red-light"> XXXXXX </span>
      </template>
    </v-col>

    <v-col cols="auto">
      <template v-if="props.project.pre_approval !== ''">
        <span class="text-caption gray-dark">
          {{ props.project.pre_approval }}
        </span>
      </template>
      <template v-else>
        <span class="text-caption black"> 0000-00-00 </span>
      </template>
    </v-col>

    <v-col cols="auto">
      <template v-if="props.project.number_m">
        <v-chip size="small" color="#198b48" class="font-weight-bold"> M </v-chip>
      </template>
      <template v-else>
        <v-chip size="small" disabled> M </v-chip>
      </template>
    </v-col>
    <v-col cols="auto">
      <template v-if="props.project.number_s">
        <v-chip size="small" color="#198b48" class="font-weight-bold"> S </v-chip>
      </template>
      <template v-else>
        <v-chip size="small" disabled> S </v-chip>
      </template>
    </v-col>
    <v-col cols="auto">
      <template v-if="props.project.number_o">
        <v-chip size="small" color="#198b48" class="font-weight-bold"> 0 </v-chip>
      </template>
      <template v-else>
        <v-chip size="small" disabled> 0 </v-chip>
      </template>
    </v-col>
  </v-row>
</template>

<style scoped>
@import '@/assets/main.css';
</style>
