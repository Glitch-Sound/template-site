<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { storeToRefs } from 'pinia'

import type { Target, TargetCreate, TargetUpdate } from '@/types/Target'
import { useTargetStore } from '@/stores/TargetStore'
import SettingEvent from '@/views/setting/SettingEvent'
import CreateTargetDialog from '@/components/dialog/CreateTargetDialog.vue'
import UpdateTargetDialog from '@/components/dialog/UpdateTargetDialog.vue'

const headers = [
  { title: 'RID', width: '50px' },
  { title: 'YEAR', width: '50px' },
  { title: 'QUARTER 1', width: '100px' },
  { title: 'QUARTER 2', width: '100px' },
  { title: 'QUARTER 3', width: '100px' },
  { title: 'QUARTER 4', width: '100px' },
  { title: '', width: '140px' },
]

const store_target = useTargetStore()
const { targets, is_loading } = storeToRefs(store_target)
const { fetchTargets, createTarget, updateTarget, deleteTarget } = store_target

const dialog_target_create = ref()
const dialog_target_update = ref()

onMounted(async () => {
  try {
    await fetchTargets()
  } catch (e) {
    console.error(e)
  }
})

const formatCurrency = (value: number) => {
  if (value === null || value === undefined) return ''
  return value.toLocaleString()
}

SettingEvent.on('openCreateTargetDialog', () => {
  dialog_target_create.value?.open()
})

const openUpdateTargetDialog = (data: Target) => {
  dialog_target_update.value?.open(data)
}

const handleCreate = async (data: TargetCreate) => {
  try {
    await createTarget(data)
    dialog_target_create.value?.close()
  } catch (e) {
    console.error(e)
  }
}

const handleUpdate = async (data: TargetUpdate) => {
  try {
    await updateTarget(data)
    dialog_target_update.value?.close()
  } catch (e) {
    console.error(e)
  }
}

const handleDelete = async (data: TargetUpdate) => {
  try {
    await deleteTarget(data.rid)
    dialog_target_update.value?.close()
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
        :items="targets"
        :headers="headers"
        :loading="is_loading"
        loading-text="Loading targets..."
      >
        <template #item="{ item }">
          <tr>
            <td>{{ item.rid }}</td>
            <td>{{ item.year }}</td>
            <td class="text-right">{{ formatCurrency(item.quarter1) }}</td>
            <td class="text-right">{{ formatCurrency(item.quarter2) }}</td>
            <td class="text-right">{{ formatCurrency(item.quarter3) }}</td>
            <td class="text-right">{{ formatCurrency(item.quarter4) }}</td>
            <td>
              <v-btn
                size="small"
                prepend-icon="mdi-pencil"
                variant="outlined"
                :disabled="is_loading"
                @click="openUpdateTargetDialog(item)"
              >
                UPDATE
              </v-btn>
            </td>
          </tr>
        </template>
      </v-data-table>
    </v-sheet>
  </v-main>

  <CreateTargetDialog ref="dialog_target_create" @submit="handleCreate" />
  <UpdateTargetDialog ref="dialog_target_update" @submit="handleUpdate" @delete="handleDelete" />
</template>

<style scoped>
@import '@/assets/main.css';

.text-right {
  text-align: right;
}
</style>
