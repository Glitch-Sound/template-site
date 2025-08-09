<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { storeToRefs } from 'pinia'

import type { ProjectCreate } from '@/types/Project'
import ProjectEvent from '@/views/project/ProjectEvent'
import { useProjectStore } from '@/stores/ProjectStore'

import PanelProject from '@/components/project/PanelProject.vue'
import PanelProjectGroup from '@/components/project/PanelProjectGroup.vue'
import CreateProjectDialog from '@/components/dialog/CreateProjectDialog.vue'

const store_project = useProjectStore()
const { projects, is_loading_projects } = storeToRefs(store_project)
const { fetchProjects, createProject } = store_project

const dialog_project_create = ref()

ProjectEvent.on('openCreateProjectDialog', () => {
  dialog_project_create.value?.open()
})

onMounted(async () => {
  try {
    await fetchProjects()
  } catch (e) {
    console.error(e)
  }
})

async function handleCreate(data: ProjectCreate) {
  try {
    await createProject(data)
    dialog_project_create.value?.close()
  } catch (e) {
    console.error(e)
  }
}
</script>

<template>
  <v-main>
    <v-sheet class="main">
      <v-skeleton-loader
        v-if="is_loading_projects"
        type="list-item-two-line, list-item-two-line, list-item-two-line"
        class="mb-4"
      />

      <template v-else>
        <template v-for="project_group in projects" :key="project_group.rid">
          <PanelProjectGroup :project_group="project_group" />
          <template v-for="project in project_group.projects" :key="project.rid">
            <PanelProject :project="project" />
          </template>
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

<style scoped></style>
