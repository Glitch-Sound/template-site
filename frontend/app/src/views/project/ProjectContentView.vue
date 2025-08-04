<script setup lang="ts">
import { ref } from 'vue'

import type { Project, ProjectCreate, ProjectUpdate } from '@/types/Project'
import ProjectEvent from '@/views/project/ProjectEvent'
import useProjectStore from '@/stores/ProjectStore'
import PanelProject from '@/components/project/PanelProject.vue'
import PanelProjectGroup from '@/components/project/PanelProjectGroup.vue'
import CreateProjectDialog from '@/components/dialog/CreateProjectDialog.vue'

const store_project = useProjectStore()

const dialog_project_create = ref()

ProjectEvent.on('openCreateProjectDialog', () => {
  dialog_project_create.value?.open()
})

const handleCreate = async (data: ProjectCreate) => {
  await store_project.createProject(data)
  dialog_project_create.value?.close()
}
</script>

<template>
  <v-main>
    <v-sheet class="main">
      <template
        v-for="(project_group, index_project_group) in store_project.projects"
        :key="project_group.rid"
      >
        <PanelProjectGroup :project_group="project_group" />

        <template v-for="(project, index_project) in project_group.projects" :key="project.rid">
          <PanelProject :project="project" />
        </template>
      </template>
    </v-sheet>
  </v-main>

  <CreateProjectDialog ref="dialog_project_create" @submit="handleCreate" />
</template>

<style scoped>
@import '@/assets/main.css';
</style>
