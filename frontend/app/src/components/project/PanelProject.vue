<script setup lang="ts">
import { ref } from 'vue'
import { storeToRefs } from 'pinia'

import type { Project, ProjectUpdate } from '@/types/Project'
import { useProjectStore } from '@/stores/ProjectStore'

import QuarterLabel from '@/components/common/QuarterLabel.vue'
import RankLabelLarge from '@/components/common/RankLabelLarge.vue'
import ProjectDateLabel from '@/components/common/ProjectDateLabel.vue'
import AmountLabel from '@/components/common/AmountLabel.vue'
import UserLabel from '@/components/common/UserLabel.vue'
import NumberLabel from '@/components/common/NumberLabel.vue'
import KarteLabel from '@/components/common/KarteLabel.vue'
import UpdateProjectDialog from '@/components/dialog/UpdateProjectDialog.vue'

const props = defineProps<{
  project: Project
}>()

const store_project = useProjectStore()
const { is_loading_projects } = storeToRefs(store_project)
const { updateProject, deleteProject } = store_project

const dialog_project_update = ref()

function openUpdateProjectDialog() {
  if (!is_loading_projects.value) {
    dialog_project_update.value?.open(props.project)
  }
}

async function handleUpdate(data: ProjectUpdate) {
  await updateProject(data)
  dialog_project_update.value?.close()
}

const handleDelete = async (data: ProjectUpdate) => {
  await deleteProject(data.rid)
  dialog_project_update.value?.close()
}
</script>

<template>
  <v-sheet class="mr-5">
    <v-row>
      <v-col cols="auto" class="d-flex align-center justify-center ml-5">
        <QuarterLabel :project="props.project" />
      </v-col>

      <v-col cols="auto" class="d-flex align-center justify-center mx-2 pa-1">
        <RankLabelLarge :project="props.project" />
      </v-col>

      <v-col>
        <v-card>
          <ProjectDateLabel :project="props.project" />
        </v-card>

        <v-card>
          <span class="text-subtitle-1 font-weight-black">{{ props.project.name }}</span>
        </v-card>
      </v-col>

      <v-col cols="auto" class="mr-5">
        <AmountLabel :project="props.project" />
      </v-col>

      <v-col cols="auto" class="mr-5">
        <v-card>
          <NumberLabel :project="props.project" />
        </v-card>

        <v-card>
          <KarteLabel :project="props.project" />
        </v-card>
      </v-col>

      <v-col cols="auto" class="mr-2">
        <UserLabel :user="props.project.user_pm" class="mb-1" />
        <UserLabel :user="props.project.user_pl" />
      </v-col>

      <v-col cols="auto" class="d-flex align-center justify-center ga-5">
        <v-icon color="#c0c0c0">mdi-message-bulleted</v-icon>

        <v-tooltip text="Update Project" location="top">
          <template #activator="{ props: vprops }">
            <v-icon
              v-bind="vprops"
              color="#c0c0c0"
              :class="[
                { 'opacity-50': is_loading_projects, 'cursor-pointer': !is_loading_projects },
              ]"
              :disabled="is_loading_projects"
              @click="openUpdateProjectDialog"
            >
              mdi-pencil
            </v-icon>
          </template>
        </v-tooltip>
      </v-col>
    </v-row>
  </v-sheet>

  <UpdateProjectDialog ref="dialog_project_update" @submit="handleUpdate" @delete="handleDelete" />
</template>

<style scoped>
@import '@/assets/main.css';

.cursor-pointer {
  cursor: pointer;
}
.opacity-50 {
  opacity: 0.5;
}
</style>
