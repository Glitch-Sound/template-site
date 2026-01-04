<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { storeToRefs } from 'pinia'

import type { ProjectGroup, ProjectGroupCreate, ProjectGroupUpdate } from '@/types/Project'
import { useProjectStore } from '@/stores/ProjectStore'
import SettingEvent from '@/views/setting/SettingEvent'
import CreateProjectGroupDialog from '@/components/dialog/CreateProjectGroupDialog.vue'
import UpdateProjectGroupDialog from '@/components/dialog/UpdateProjectGroupDialog.vue'

const headers = [
  { title: 'RID', width: '50px' },
  { title: 'COMPANY', width: '150px' },
  { title: 'NAME', width: '200px' },
  { title: 'DETAIL', width: '500px' },
  { title: '', width: '140px' },
]

const store_project = useProjectStore()
const { project_groups, is_loading_groups } = storeToRefs(store_project)
const { fetchProjectGroups, createProjectGroup, updateProjectGroup, deleteProjectGroup } =
  store_project

const dialog_project_group_create = ref()
const dialog_project_group_update = ref()

onMounted(async () => {
  try {
    await fetchProjectGroups()
  } catch (e) {
    console.error(e)
  }
})

SettingEvent.on('openCreateProjectGroupDialog', () => {
  dialog_project_group_create.value?.open()
})

const openUpdateProjectGroupDialog = (data: ProjectGroup) => {
  dialog_project_group_update.value?.open(data)
}

const handleCreate = async (data: ProjectGroupCreate) => {
  try {
    await createProjectGroup(data)
    dialog_project_group_create.value?.close()
  } catch (e) {
    console.error(e)
  }
}

const handleUpdate = async (data: ProjectGroupUpdate) => {
  try {
    await updateProjectGroup(data)
    dialog_project_group_update.value?.close()
  } catch (e) {
    console.error(e)
  }
}

const handleDelete = async (data: ProjectGroupUpdate) => {
  try {
    await deleteProjectGroup(data.rid)
    dialog_project_group_update.value?.close()
  } catch (e) {
    console.error(e)
  }
}
</script>

<template>
  <v-main>
    <v-sheet class="main">
      <v-data-table
        class="bg-black"
        :items="project_groups"
        :headers="headers"
        :loading="is_loading_groups"
        loading-text="Loading project groups..."
      >
        <template #item="{ item }">
          <tr>
            <td>{{ item.rid }}</td>
            <td>{{ item.company.name }}</td>
            <td>{{ item.name }}</td>
            <td>{{ item.detail }}</td>
            <td>
              <v-btn
                size="small"
                prepend-icon="mdi-pencil"
                variant="outlined"
                :disabled="is_loading_groups"
                @click="openUpdateProjectGroupDialog(item)"
              >
                UPDATE
              </v-btn>
            </td>
          </tr>
        </template>
      </v-data-table>
    </v-sheet>
  </v-main>

  <CreateProjectGroupDialog ref="dialog_project_group_create" @submit="handleCreate" />
  <UpdateProjectGroupDialog
    ref="dialog_project_group_update"
    @submit="handleUpdate"
    @delete="handleDelete"
  />
</template>

<style scoped>
</style>
