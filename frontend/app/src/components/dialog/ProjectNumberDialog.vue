<script setup lang="ts">
import { ref, computed } from 'vue'

import { useDisplayDialog } from '@/components/dialog/BaseDialog'
import type { Project } from '@/types/Project'

const emit = defineEmits(['submit'])
const { dialog, onClose } = useDisplayDialog(emit)

const project = ref<Project | null>(null)
const title = computed(() => project.value?.name ?? '')

defineExpose({
  async open(data: Project) {
    dialog.value = true
    project.value = data
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

      <v-card-text class="flex-grow-1 overflow-y-auto"> aaa </v-card-text>

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
