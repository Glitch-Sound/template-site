<script setup lang="ts">
import { computed } from 'vue'

import type { Project } from '@/types/Project'
import { TypeThreadState, type ThreadCreate } from '@/types/Thread'
import { useFormDialog } from '@/components/dialog/BaseDialog'

const emit = defineEmits(['submit'])
const { dialog, valid, form_data, form_ref, rules, onSubmit } = useFormDialog<ThreadCreate>(emit)

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
  <v-dialog v-model="dialog" max-width="600px">
    <v-card>
      <v-card-title>
        <span class="dialog-title">Add Thread</span>
      </v-card-title>

      <v-card-text>
        <v-form ref="form_ref" v-model="valid" lazy-validation>
          <v-textarea v-model="form_data.note" :rules="[rules.required]" label="Note" />
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
@import '@/assets/main.css';
</style>
