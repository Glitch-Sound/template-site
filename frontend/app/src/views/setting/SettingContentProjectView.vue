<script setup lang="ts">
import { onMounted, ref } from 'vue'

import type { ProjectGroup, ProjectGroupCreate, ProjectGroupUpdate } from '@/types/ProjectGroup'

import SettingEvent from '@/views/setting/SettingEvent'
import useProjectGroupStore from '@/stores/ProjectGroupStore'
import CreateProjectGroupDialog from '@/components/dialog/CreateProjectGroupDialog.vue'
import UpdateProjectGroupDialog from '@/components/dialog/UpdateProjectGroupDialog.vue'

const headers = [
  { title: 'RID', width: '50px' },
  { title: 'COMPANY', width: '150px' },
  { title: 'NAME', width: '200px' },
  { title: 'DETAIL', width: '500px' },
  { title: '', width: '140px' },
]

const store_project_group = useProjectGroupStore()

const dialog_project_group_create = ref()
const dialog_project_group_update = ref()

onMounted(() => {
  store_project_group.fetchProjectGroups()
})

SettingEvent.on('openCreateProjectGroupDialog', () => {
  dialog_project_group_create.value?.open()
})

const openUpdateProjectGroupDialog = (data: ProjectGroup) => {
  dialog_project_group_update.value?.open(data)
}

const handleCreate = async (data: ProjectGroupCreate) => {
  await store_project_group.createProjectGroup(data)
  dialog_project_group_create.value?.close()
}

const handleUpdate = async (data: ProjectGroupUpdate) => {
  await store_project_group.updateProjectGroup(data)
  dialog_project_group_update.value?.close()
}

const handleDelete = async (data: ProjectGroupUpdate) => {
  await store_project_group.deleteProjectGroup(data.rid)
  dialog_project_group_update.value?.close()
}
</script>

<template>
  <v-main>
    <v-sheet class="main">
      <v-data-table class="bg-black" :items="store_project_group.project_groups" :headers="headers">
        <template v-slot:item="{ item }">
          <tr>
            <td>{{ item.rid }}</td>
            <td>{{ item.company.name }}</td>
            <td>{{ item.name }}</td>
            <td>{{ item.detrail }}</td>
            <td>
              <v-btn
                size="small"
                prepend-icon="mdi-pencil"
                variant="outlined"
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
@import '@/assets/main.css';
</style>
