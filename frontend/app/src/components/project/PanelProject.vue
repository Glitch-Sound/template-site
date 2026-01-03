<script setup lang="ts">
import { ref, computed } from 'vue'
import { storeToRefs } from 'pinia'

import type { Project, ProjectUpdate } from '@/types/Project'
import { useProjectStore } from '@/stores/ProjectStore'
import { useThreadStore } from '@/stores/ThreadStore'
import QuarterLabel from '@/components/common/QuarterLabel.vue'
import RankLabelLarge from '@/components/common/RankLabelLarge.vue'
import ProjectDateLabel from '@/components/common/ProjectDateLabel.vue'
import AmountLabel from '@/components/common/AmountLabel.vue'
import UserLabel from '@/components/common/UserLabel.vue'
import NumberLabel from '@/components/common/NumberLabel.vue'
import KarteLabel from '@/components/common/KarteLabel.vue'
import UpdateProjectDialog from '@/components/dialog/UpdateProjectDialog.vue'
import ThreadDialog from '@/components/dialog/ThreadDialog.vue'
import ProjectNumberDialog from '@/components/dialog/ProjectNumberDialog.vue'

const props = defineProps<{
  project: Project
}>()

const store_project = useProjectStore()
const { updateProject, deleteProject } = store_project

const store_thread = useThreadStore()
const { threads_status } = storeToRefs(store_thread)

const has_thread_update = computed(() => {
  const status = threads_status.value.find((item) => item.rid_projects === props.project.rid)
  return status?.is_important ?? false
})

const dialog_project_update = ref()
const dialog_thread = ref()
const dialog_project_number = ref()

function openUpdateProjectDialog() {
  dialog_project_update.value?.open(props.project)
}

function openThreadDialog() {
  dialog_thread.value?.open(props.project)
}

function openProjectNumberDialog() {
  dialog_project_number.value?.open(props.project)
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
  <v-sheet class="mb-1 mr-5">
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
          <NumberLabel
            :project="props.project"
            class="cursor-pointer"
            @click="openProjectNumberDialog()"
          />
        </v-card>

        <v-card>
          <KarteLabel :project="props.project" />
        </v-card>
      </v-col>

      <v-col cols="auto" class="mr-2 user">
        <UserLabel :user="props.project.user_pm" class="mb-1" />
        <UserLabel :user="props.project.user_pl" />
      </v-col>

      <v-col cols="auto" class="d-flex align-center justify-center ga-5">
        <v-icon :color="has_thread_update ? '#f5c542' : '#c0c0c0'" @click="openThreadDialog()">
          mdi-message-bulleted
        </v-icon>
        <v-icon color="#c0c0c0" @click="openUpdateProjectDialog()"> mdi-pencil </v-icon>
      </v-col>
    </v-row>
  </v-sheet>

  <UpdateProjectDialog ref="dialog_project_update" @submit="handleUpdate" @delete="handleDelete" />
  <ThreadDialog ref="dialog_thread" />
  <ProjectNumberDialog ref="dialog_project_number" />
</template>

<style scoped>
@import '@/assets/main.css';

.user {
  min-width: 150px;
  max-width: 150px;
}

.cursor-pointer {
  cursor: pointer;
}
.opacity-50 {
  opacity: 0.5;
}
</style>
