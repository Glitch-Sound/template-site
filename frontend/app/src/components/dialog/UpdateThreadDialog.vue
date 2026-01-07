<script setup lang="ts">
import { computed, ref } from 'vue'
import type { Thread } from '@/types/Thread'
import { type ThreadUpdate } from '@/types/Thread'
import { useFormDialog } from '@/components/dialog/BaseDialog'
import DeleteButton from '@/components/common/DeleteButton.vue'
import { useMarkdownToolbar } from '@/components/dialog/useMarkdownToolbar'

const emit = defineEmits(['submit', 'delete'])
const { dialog, valid, form_data, form_ref, onSubmit, onDelete } = useFormDialog<ThreadUpdate>(emit)
const noteTextarea = ref<{ $el?: HTMLElement } | null>(null)
const noteValue = computed({
  get: () => form_data.value.note ?? '',
  set: (value) => {
    form_data.value.note = value
  },
})
const { applyMarkdown } = useMarkdownToolbar(noteValue, noteTextarea)

defineExpose({
  open(data: Thread, rid_projects: number) {
    dialog.value = true
    form_data.value = {
      rid: data.rid,
      rid_projects: rid_projects,
      state: data.state,
      note: data.note,
    }
  },
  close() {
    dialog.value = false
  },
})
</script>

<template>
  <v-dialog v-model="dialog" max-width="1000px" min-height="500px">
    <v-card class="d-flex flex-column" style="max-height: 80vh">
      <v-card-title>
        <span class="dialog-title">Update Thread</span>
      </v-card-title>

      <v-card-text class="flex-grow-1 d-flex">
        <v-form
          ref="form_ref"
          v-model="valid"
          lazy-validation
          class="d-flex flex-column flex-grow-1"
        >
          <v-form
            ref="form_ref"
            v-model="valid"
            lazy-validation
            class="d-flex flex-column flex-grow-1"
          >
            <div class="markdown-toolbar">
              <v-btn-group density="compact" variant="outlined">
                <v-btn size="small" @click="applyMarkdown('bold')">B</v-btn>
                <v-btn size="small" @click="applyMarkdown('italic')">I</v-btn>
                <v-btn size="small" @click="applyMarkdown('strike')">S</v-btn>
                <v-btn size="small" @click="applyMarkdown('codeblock')">Block</v-btn>
                <v-btn size="small" @click="applyMarkdown('quote')">&gt;</v-btn>
                <v-btn size="small" @click="applyMarkdown('list')">List</v-btn>
                <v-btn size="small" @click="applyMarkdown('h1')">H1</v-btn>
                <v-btn size="small" @click="applyMarkdown('h2')">H2</v-btn>
                <v-btn size="small" @click="applyMarkdown('h3')">H3</v-btn>
                <v-btn size="small" @click="applyMarkdown('checkbox')">Check</v-btn>
              </v-btn-group>
            </div>
            <v-textarea
              v-model="form_data.note"
              label="Note"
              class="thread-note-textarea flex-grow-1"
              ref="noteTextarea"
            />
          </v-form>
        </v-form>
      </v-card-text>

      <v-card-actions>
        <DeleteButton @delete="onDelete" />
        <v-spacer />
        <v-btn @click="dialog = false">Cancel</v-btn>
        <v-btn color="primary" @click="onSubmit">Submit</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped>
.thread-note-textarea {
  flex: 1 1 auto;
}

.markdown-toolbar {
  margin-bottom: 8px;
}

.thread-note-textarea :deep(.v-field__input) {
  height: 100%;
}

.thread-note-textarea :deep(textarea) {
  height: 100%;
}
</style>
