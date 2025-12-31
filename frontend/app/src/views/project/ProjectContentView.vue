<script setup lang="ts">
import { ref } from 'vue'
import { storeToRefs } from 'pinia'

import type { ProjectCreate } from '@/types/Project'
import ProjectEvent from '@/views/project/ProjectEvent'
import { useProjectStore } from '@/stores/ProjectStore'
import PanelProject from '@/components/project/PanelProject.vue'
import PanelProjectGroup from '@/components/project/PanelProjectGroup.vue'
import CreateProjectDialog from '@/components/dialog/CreateProjectDialog.vue'

const store_project = useProjectStore()
const { projects, is_loading_projects } = storeToRefs(store_project)
const { createProject } = store_project

const dialog_project_create = ref()

ProjectEvent.on('openCreateProjectDialog', () => {
  dialog_project_create.value?.open()
})

async function handleCreate(data: ProjectCreate) {
  await createProject(data)
  dialog_project_create.value?.close()
}
</script>

<template>
  <v-main>
    <v-sheet class="main">
      <v-overlay
        :model-value="is_loading_projects"
        contained
        scrim="transparent"
        class="align-center justify-center"
      >
        <v-progress-circular indeterminate color="primary" />
      </v-overlay>

      <template v-for="(project_group, i) in projects" :key="project_group.rid">
        <PanelProjectGroup :project_group="project_group" :class="{ 'mt-10': 0 < i }" />
        <template v-for="project in project_group.projects" :key="project.rid">
          <PanelProject :project="project" />
        </template>
      </template>
    </v-sheet>
  </v-main>

  <CreateProjectDialog
    ref="dialog_project_create"
    :loading="is_loading_projects"
    @submit="handleCreate"
  />
</template>

<style scoped>
@import '@/assets/main.css';
</style>
