<script setup lang="ts">
import { ref } from 'vue'

import { FilterQuarter, TypeQuarter } from '@/types/Project'

import ProjectEvent from '@/views/project/ProjectEvent'
import QuarterFilter from '@/components/filter/QuarterFilter.vue'

const filter_quarter = ref<FilterQuarter>()

const handleAddProject = () => {
  console.log(filter_quarter.value)
  ProjectEvent.emit('openCreateProjectDialog')
}
</script>

<template>
  <v-navigation-drawer class="no-border" color="background">
    <v-sheet class="navigation">
      <v-list-item class="mb-2">
        <v-btn
          width="250px"
          color="#940000"
          prepend-icon="mdi-plus-circle"
          @click="handleAddProject"
        >
          Project
        </v-btn>
      </v-list-item>

      <v-list-item>
        <QuarterFilter v-model="filter_quarter" />
      </v-list-item>

      <v-list-item> FILTER 2 </v-list-item>
      <v-list-item> FILTER 3 </v-list-item>
    </v-sheet>
  </v-navigation-drawer>
</template>

<style scoped>
@import '@/assets/main.css';
</style>
