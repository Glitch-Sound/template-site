<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { storeToRefs } from 'pinia'

import type { Company } from '@/types/Company'
import { useCompanyStore } from '@/stores/CompanyStore'

const props = defineProps<{
  modelValue?: number | null
}>()

const emit = defineEmits<{
  'update:modelValue': [value: number | null]
  itemSelected: [company: Company]
}>()

const store_company = useCompanyStore()
const { companies, is_loading } = storeToRefs(store_company)
const { fetchCompanies, getByRid } = store_company

const selected_option = ref<number | null>(
  props.modelValue && props.modelValue !== 0 ? props.modelValue : null,
)

onMounted(() => {
  fetchCompanies()
})

watch(
  () => props.modelValue,
  (v) => {
    selected_option.value = v ?? null
  },
)

watch(selected_option, (v) => {
  emit('update:modelValue', v ?? null)
  const item = v != null ? getByRid(v) : undefined
  if (item) emit('itemSelected', item)
})
</script>

<template>
  <v-select
    :items="companies"
    v-model="selected_option"
    label="Company"
    item-title="name"
    item-value="rid"
    :loading="is_loading"
    :disabled="is_loading"
    hide-details="auto"
  />
</template>

<style scoped>
</style>
