<script setup lang="ts">
import { ref } from 'vue'
import { storeToRefs } from 'pinia'

import type { ProjectCreate } from '@/types/Project'
import ProjectEvent from '@/views/project/ProjectEvent'
import { TypeThreadState } from '@/types/Thread'
import { useProjectStore } from '@/stores/ProjectStore'
import { useThreadStore } from '@/stores/ThreadStore'
import PanelProject from '@/components/project/PanelProject.vue'
import PanelProjectGroup from '@/components/project/PanelProjectGroup.vue'
import CreateProjectDialog from '@/components/dialog/CreateProjectDialog.vue'

const store_project = useProjectStore()
const store_thread = useThreadStore()
const { projects, is_loading_projects } = storeToRefs(store_project)
const { createProject } = store_project
const { threads } = storeToRefs(store_thread)

const indent_depth = (d: number) => `${Math.max(0, d) * 22}px`

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

      考え中・・・<br />
      課内会議をスムーズに進めるためのUIにしたい<br /><br />

      アイデア募集中 (*´Д`)ﾊｧﾊｧ
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
