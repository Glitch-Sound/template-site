<script setup lang="ts">
import { onMounted, ref, watch, computed } from 'vue'
import { storeToRefs } from 'pinia'

import type { Company } from '@/types/Company'
import { useCompanyStore } from '@/stores/CompanyStore'

const props = defineProps<{
  modelValue?: number[] | null
}>()

const emit = defineEmits<{
  'update:modelValue': [value: number[]]
  itemSelected: [companies: Company[]]
}>()

const store_company = useCompanyStore()
const { companies, is_loading } = storeToRefs(store_company)
const { fetchCompanies } = store_company

const selected_option = ref<number[]>(props.modelValue ?? [])
const is_initialized = ref(false)

onMounted(() => {
  fetchCompanies()
})

watch(
  () => props.modelValue,
  (v) => {
    selected_option.value = v ?? []
  },
)

watch(companies, (list) => {
  if (is_initialized.value) return
  if (!list.length) return
  if (selected_option.value.length === 0) {
    selected_option.value = list.map((company) => company.rid)
  }
  is_initialized.value = true
})

watch(selected_option, (val) => {
  emit('update:modelValue', val)
  const selectedFilters = companies.value.filter((company) => val.includes(company.rid))
  emit('itemSelected', selectedFilters)
})

const selectionText = computed(() => {
  const total = companies.value.length
  const count = selected_option.value.length
  if (count === 0) return ''
  if (total > 0 && count === total) return 'ALL'
  if (count === 1) {
    const c = companies.value.find((c) => c.rid === selected_option.value[0])
    return c?.name ?? '1件'
  }
  const firstCompany = companies.value.find((c) => c.rid === selected_option.value[0])
  return `${firstCompany?.name ?? ''} + ${count - 1}`
})
</script>

<template>
  <v-select
    clearable
    multiple
    :items="companies"
    v-model="selected_option"
    label="Company"
    item-title="name"
    item-value="rid"
    :loading="is_loading"
    :disabled="is_loading"
    hide-details="auto"
  >
    <template #selection="{ index }">
      <span v-if="index === 0">{{ selectionText }}</span>
    </template>
  </v-select>
</template>

<style scoped>
</style>
