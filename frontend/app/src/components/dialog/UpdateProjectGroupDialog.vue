<script setup lang="ts">
import type { CompanyUpdate } from '@/types/Company'
import { useFormDialog } from '@/components/dialog/BaseDialog'

import DeleteButton from '@/components/common/DeleteButton.vue'
import CompanySelect from '@/components/common/CompanySelect.vue'

const emit = defineEmits(['submit', 'delete'])
const { dialog, valid, form_data, form_ref, rules, submitData, deleteData } =
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

const handleCompanySelected = (company: Company) => {
  form_data.value.rid_companies = company.rid
}
</script>

<template>
  <v-dialog v-model="dialog" max-width="600px">
    <v-card>
      <v-card-title>
        <span class="dialog-title">Update Project Group</span>
      </v-card-title>

      <v-card-text>
        <v-form ref="form_ref" v-model="valid" lazy-validation>
          <CompanySelect v-model="form_data.rid_companies" @itemSelected="handleCompanySelected" />

          <v-text-field
            v-model="form_data.name"
            :rules="[rules.required, rules.text]"
            label="Name"
          />

          <v-textarea v-model="form_data.detail" :rules="[rules.text]" label="Detail" />
        </v-form>
      </v-card-text>

      <v-card-actions>
        <DeleteButton @delete="deleteData" />
        <v-spacer />
        <v-btn @click="dialog = false">Cancel</v-btn>
        <v-btn color="primary" :disabled="!valid" @click="submitData">Submit</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped>
@import '@/assets/main.css';
</style>
