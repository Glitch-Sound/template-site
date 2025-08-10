<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'

import { type EmitType } from '@/components/common/events'

import { type FilterQuarter, TypeQuarter } from '@/types/Project'

const props = defineProps<{
  modelValue?: FilterQuarter[]
}>()

interface Filter {
  label: string
  filter: FilterQuarter
}

const quarterOptions: FilterQuarter[] = [
  { label: '2025 1Q', filter: { year: 2025, quarter: TypeQuarter.Q1 } },
  { label: '2025 2Q', filter: { year: 2025, quarter: TypeQuarter.Q2 } },
  { label: '2025 3Q', filter: { year: 2025, quarter: TypeQuarter.Q3 } },
  { label: '2025 4Q', filter: { year: 2025, quarter: TypeQuarter.Q4 } },
  { label: '2026 1Q', filter: { year: 2026, quarter: TypeQuarter.Q1 } },
  { label: '2026 2Q', filter: { year: 2026, quarter: TypeQuarter.Q2 } },
  { label: '2026 3Q', filter: { year: 2026, quarter: TypeQuarter.Q3 } },
  { label: '2026 4Q', filter: { year: 2026, quarter: TypeQuarter.Q4 } },
]

const selected_option = ref(props.modelValue || null)

const emit = defineEmits<EmitType>()
const itemSelected = (val: FilterQuarter[]) => {
  const selectedFilters = quarterOptions
    .filter((opt) => val.some((v) => v.label === opt.label))
    .map((opt) => opt.filter)
  emit('update:modelValue', selectedFilters)
  emit('itemSelected', val)
}
</script>

<template>
  <v-select
    clearable
    chips
    multiple
    :items="quarterOptions"
    v-model="selected_option"
    label="Quarter"
    item-title="label"
    item-value="label"
    :return-object="true"
    @update:modelValue="itemSelected"
  />
</template>

<style scoped></style>
