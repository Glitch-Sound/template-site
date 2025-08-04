<script setup lang="ts">
import ProjectgEvent from '@/views/project/ProjectEvent'

const handleAddProject = () => {
  ProjectgEvent.emit('openCreateProjectDialog')
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

      <v-list-item> FILTER 1 </v-list-item>
      <v-list-item> FILTER 2 </v-list-item>
      <v-list-item> FILTER 3 </v-list-item>
    </v-sheet>
  </v-navigation-drawer>
</template>

<style scoped>
@import '@/assets/main.css';
</style>
