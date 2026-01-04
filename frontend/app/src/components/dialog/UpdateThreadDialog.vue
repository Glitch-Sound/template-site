<script setup lang="ts">
import type { Thread } from '@/types/Thread'
import { type ThreadUpdate } from '@/types/Thread'
import { useFormDialog } from '@/components/dialog/BaseDialog'
import DeleteButton from '@/components/common/DeleteButton.vue'

const emit = defineEmits(['submit', 'delete'])
const { dialog, valid, form_data, form_ref, rules, onSubmit, onDelete } =
  useFormDialog<ThreadUpdate>(emit)

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
  <v-dialog v-model="dialog" max-width="1000px">
    <v-card>
      <v-card-title>
        <span class="dialog-title">Update Thread</span>
      </v-card-title>

      <v-card-text>
        <v-form ref="form_ref" v-model="valid" lazy-validation>
          <v-form ref="form_ref" v-model="valid" lazy-validation>
            <v-textarea v-model="form_data.note" :rules="[rules.text]" label="Note" />
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
</style>
