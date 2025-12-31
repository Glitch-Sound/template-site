<script setup lang="ts">
import type { TargetUpdate } from '@/types/Target'
import { useFormDialog } from '@/components/dialog/BaseDialog'

import DeleteButton from '@/components/common/DeleteButton.vue'

const emit = defineEmits(['submit', 'delete'])
const { dialog, valid, form_data, form_ref, rules, onSubmit, onDelete } =
  useFormDialog<TargetUpdate>(emit)

type QuarterField = 'quarter1' | 'quarter2' | 'quarter3' | 'quarter4'

const formatCurrency = (value: number) => {
  if (value === null || value === undefined) return ''
  return value.toLocaleString()
}

const handleQuarterInput = (field: QuarterField, rawValue: string | number) => {
  if (typeof rawValue === 'number') {
    form_data.value[field] = rawValue
    return
  }

  const sanitized = rawValue.replace(/,/g, '')
  const parsed = Number(sanitized)
  form_data.value[field] = Number.isNaN(parsed) ? 0 : parsed
}

const numericWithCommaRule = (value: string | number) => {
  if (value === undefined || value === null) return 'Please use numbers only'
  const normalized = typeof value === 'number' ? String(value) : value.replace(/,/g, '')
  return /^[0-9]+$/.test(normalized) || 'Please use numbers only'
}

defineExpose({
  open(data: TargetUpdate) {
    dialog.value = true
    form_data.value = { ...data }
  },
  close() {
    dialog.value = false
  },
})
</script>

<template>
  <v-dialog v-model="dialog" max-width="400px">
    <v-card>
      <v-card-title>
        <span class="dialog-title">Update Target</span>
      </v-card-title>

      <v-card-text>
        <v-form ref="form_ref" v-model="valid" lazy-validation>
          <v-text-field
            v-model="form_data.year"
            :rules="[rules.required, rules.numeric]"
            label="Year"
            class="text-right-field"
          />

          <v-text-field
            :model-value="formatCurrency(form_data.quarter1)"
            class="text-right-field"
            :rules="[rules.required, numericWithCommaRule]"
            label="Quarter 1"
            @update:model-value="(value) => handleQuarterInput('quarter1', value)"
          />

          <v-text-field
            :model-value="formatCurrency(form_data.quarter2)"
            class="text-right-field"
            :rules="[rules.required, numericWithCommaRule]"
            label="Quarter 2"
            @update:model-value="(value) => handleQuarterInput('quarter2', value)"
          />

          <v-text-field
            :model-value="formatCurrency(form_data.quarter3)"
            class="text-right-field"
            :rules="[rules.required, numericWithCommaRule]"
            label="Quarter 3"
            @update:model-value="(value) => handleQuarterInput('quarter3', value)"
          />

          <v-text-field
            :model-value="formatCurrency(form_data.quarter4)"
            class="text-right-field"
            :rules="[rules.required, numericWithCommaRule]"
            label="Quarter 4"
            @update:model-value="(value) => handleQuarterInput('quarter4', value)"
          />
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

.text-right-field :deep(.v-field__input) {
  text-align: right;
}
</style>
