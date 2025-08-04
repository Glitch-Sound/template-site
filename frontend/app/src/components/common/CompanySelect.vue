<script setup lang="ts">
import { onMounted, ref } from 'vue'

import { type EmitType } from '@/components/common/events'
import useCompanyStore from '@/stores/CompanyStore'

const props = defineProps<{
  modelValue?: number | null
}>()

const store_company = useCompanyStore()

const selected_option = ref(props.modelValue || null)

onMounted(() => {
  store_company.fetchCompanies()
})

const emit = defineEmits<EmitType>()
const itemSelected = () => {
  const selectedItem = store_company.companies.find((item) => item.rid === selected_option.value)
  if (selectedItem) {
    emit('itemSelected', selectedItem)
  }
}
</script>

<template>
  <v-select
    :items="store_company.companies"
    v-model="selected_option"
    label="Company"
    item-title="name"
    item-value="rid"
    @update:modelValue="itemSelected"
  />
</template>

<style scoped></style>
