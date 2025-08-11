<script setup lang="ts">
import type { ProjectGroup, ProjectGroupUpdate } from '@/types/Project'
import type { Company } from '@/types/Company'
import { useFormDialog } from '@/components/dialog/BaseDialog'

import DeleteButton from '@/components/common/DeleteButton.vue'
import CompanySelect from '@/components/common/CompanySelect.vue'

const emit = defineEmits(['submit', 'delete'])
const { dialog, valid, form_data, form_ref, rules, onSubmit, onDelete } =
  useFormDialog<ProjectGroupUpdate>(emit)

defineExpose({
  open(data: ProjectGroup) {
    dialog.value = true
    form_data.value = {
      rid: data.rid,
      rid_companies: data.company.rid,
      name: data.name,
      detail: data.detail,
    }
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
            class="mt-5"
            :rules="[rules.required, rules.text]"
            label="Name"
          />

          <v-textarea v-model="form_data.detail" :rules="[rules.text]" label="Detail" />
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
