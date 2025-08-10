<script setup lang="ts">
import { onMounted } from 'vue'

import { useProjectStore } from '@/stores/ProjectStore'
import ProjectMenuView from '@/views/project/ProjectMenuView.vue'
import ProjectContentMainView from '@/views/project/ProjectContentView.vue'

const store_project = useProjectStore()
const { initSearchCondition, fetchProjects } = store_project

onMounted(async () => {
  try {
    await initSearchCondition()
    await fetchProjects()
  } catch (e) {
    console.error(e)
  }
})
</script>

<template>
  <ProjectMenuView />
  <ProjectContentMainView />
</template>

<style scoped>
@import '@/assets/main.css';
</style>
