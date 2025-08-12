<script setup lang="ts">
import { ref, computed } from 'vue'
import { storeToRefs } from 'pinia'

import { TypeNumber, type Project } from '@/types/Project'
import { useDisplayDialog } from '@/components/dialog/BaseDialog'
import { useProjectStore } from '@/stores/ProjectStore'

const headers = [
  { title: 'RID', width: '50px' },
  { title: 'TYPE', width: '20px' },
  { title: 'NUMBER', width: '100px' },
  { title: 'NOTE', width: '330px' },
  { title: 'START', width: '100px' },
  { title: 'END', width: '100px' },
]

const store_project = useProjectStore()
const { project_numbers, is_loading_numbers } = storeToRefs(store_project)
const { fetchProjectNumbers } = store_project

const emit = defineEmits(['submit'])
const { dialog, onClose } = useDisplayDialog(emit)

const project = ref<Project | null>(null)
const title = computed(() => project.value?.name ?? '')

defineExpose({
  async open(data: Project) {
    dialog.value = true
    project.value = data

    await fetchProjectNumbers(data.rid)
  },
  close() {
    dialog.value = false
    project.value = null
  },
})
</script>

<template>
  <v-dialog v-model="dialog" max-width="1500px" min-height="500px">
    <v-card class="d-flex flex-column" style="max-height: 80vh">
      <v-card-title>
        <span class="dialog-title">{{ title }}</span>
      </v-card-title>

      <v-data-table
        class="bg-black"
        :items="project_numbers"
        :headers="headers"
        :loading="is_loading_numbers"
        loading-text="Loading project numbers..."
      >
        <template #item="{ item }">
          <tr>
            <td>{{ item.rid }}</td>
            <td>
              <template v-if="item.type == TypeNumber.M"> M </template>
              <template v-if="item.type == TypeNumber.S"> S </template>
              <template v-if="item.type == TypeNumber.O"> O </template>
            </td>
            <td>{{ item.number }}</td>
            <td>{{ item.note }}</td>
            <td>{{ item.date_start }}</td>
            <td>{{ item.date_end }}</td>
          </tr>
        </template>
      </v-data-table>

      <v-card-actions>
        <v-spacer />
        <v-btn color="primary" @click="onClose">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped>
@import '@/assets/main.css';
</style>
