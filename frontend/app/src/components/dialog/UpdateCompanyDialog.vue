<script setup lang="ts">
import type { CompanyUpdate } from '@/types/Company'
import { useFormDialog } from '@/components/dialog/BaseDialog'

import DeleteButton from '@/components/common/DeleteButton.vue'

const emit = defineEmits(['submit', 'delete'])
const { dialog, valid, form_data, form_ref, rules, onSubmit, onDelete } =
  useFormDialog<CompanyUpdate>(emit)

defineExpose({
  open(data: CompanyUpdate) {
    dialog.value = true
    form_data.value = { ...data }
  },
  close() {
    dialog.value = false
  },
})
</script>

<template>
  <v-dialog v-model="dialog" max-width="600px">
    <v-card>
      <v-card-title>
        <span class="dialog-title">Update Company</span>
      </v-card-title>

      <v-card-text>
        <v-form ref="form_ref" v-model="valid" lazy-validation>
          <v-text-field
            v-model="form_data.name"
            :rules="[rules.required, rules.text]"
            label="Name"
          />

          <v-textarea v-model="form_data.detail" :rules="[]" label="Detail" />
        </v-form>
      </v-card-text>

      <v-card-actions>
        <DeleteButton @delete="onDelete" />
        <v-spacer />
        <v-btn @click="dialog = false">Cancel</v-btn>
        <v-btn color="primary" :disabled="!valid" @click="onSubmit">Submit</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped>
@import '@/assets/main.css';
</style>
