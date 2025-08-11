<script setup lang="ts">
import { computed } from 'vue'

import type { Company } from '@/types/Company'
import type { ProjectGroupCreate } from '@/types/Project'
import { useFormDialog } from '@/components/dialog/BaseDialog'
import CompanySelect from '@/components/common/CompanySelect.vue'

const emit = defineEmits(['submit'])
const { dialog, valid, form_data, form_ref, rules, onSubmit } =
  useFormDialog<ProjectGroupCreate>(emit)

defineExpose({
  open() {
    dialog.value = true
    form_data.value = {
      rid_companies: 0,
      name: '',
      detail: '',
    }
  },
  close() {
    dialog.value = false
  },
})

const canSubmit = computed(() => form_data.value.rid_companies !== null)

const handleCompanySelected = (company: Company) => {
  form_data.value.rid_companies = company.rid
}
</script>

<template>
  <v-dialog v-model="dialog" max-width="600px">
    <v-card>
      <v-card-title>
        <span class="dialog-title">Add Project Group</span>
      </v-card-title>

      <v-card-text>
        <v-form ref="form_ref" v-model="valid" lazy-validation>
          <CompanySelect
            v-model="form_data.rid_companies"
            @itemSelected="handleCompanySelected"
            required
          />

          <v-text-field
            v-model="form_data.name"
            :rules="[rules.required, rules.text]"
            label="Name"
          />

          <v-textarea v-model="form_data.detail" :rules="[rules.text]" label="Detail" />
        </v-form>
      </v-card-text>

      <v-card-actions>
        <v-spacer />
        <v-btn @click="dialog = false">Cancel</v-btn>
        <v-btn color="primary" :disabled="!valid || !canSubmit" @click="onSubmit">Submit</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped>
@import '@/assets/main.css';
</style>
