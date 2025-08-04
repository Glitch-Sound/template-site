<script setup lang="ts">
import { onMounted } from 'vue'

import useProjectStore from '@/stores/ProjectStore'
import ProjectMenuView from '@/views/project/ProjectMenuView.vue'
import ProjectContentMainView from '@/views/project/ProjectContentView.vue'

const store_project = useProjectStore()

onMounted(() => {
  store_project.fetchProjects()
})
</script>

<template>
  <ProjectMenuView />
  <ProjectContentMainView />
</template>

<style scoped></style>
