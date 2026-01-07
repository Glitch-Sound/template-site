<script setup lang="ts">
import { computed } from 'vue'

import type { Project } from '@/types/Project'
import { TypeThreadState, type ThreadCreate } from '@/types/Thread'
import { useFormDialog } from '@/components/dialog/BaseDialog'

const emit = defineEmits(['submit'])
const { dialog, valid, form_data, form_ref, onSubmit } = useFormDialog<ThreadCreate>(emit)

defineExpose({
  open(data: Project, rid_parent: number | null) {
    dialog.value = true
    form_data.value = {
      rid_projects: data.rid,
      rid_parent: rid_parent == null ? null : Number(rid_parent),
      state: TypeThreadState.RUN,
      note: '',
    }
  },
  close() {
    dialog.value = false
  },
})

const canSubmit = computed(() => form_data.value.note !== '')
</script>

<template>
  <v-dialog v-model="dialog" max-width="1000px" min-height="500px">
    <v-card class="d-flex flex-column" style="max-height: 80vh">
      <v-card-title>
        <span class="dialog-title">Add Thread</span>
      </v-card-title>

      <v-card-text class="flex-grow-1 d-flex">
        <v-form
          ref="form_ref"
          v-model="valid"
          lazy-validation
          class="d-flex flex-column flex-grow-1"
        >
          <v-textarea
            v-model="form_data.note"
            label="Note"
            class="thread-note-textarea flex-grow-1"
          />
        </v-form>
      </v-card-text>

      <v-card-actions>
        <v-spacer />
        <v-btn @click="dialog = false">Cancel</v-btn>
        <v-btn color="primary" :disabled="!canSubmit" @click="onSubmit">Submit</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped>
.thread-note-textarea {
  flex: 1 1 auto;
}

.thread-note-textarea :deep(.v-field__input) {
  height: 100%;
}

.thread-note-textarea :deep(textarea) {
  height: 100%;
}
</style>
