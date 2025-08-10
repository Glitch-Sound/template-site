<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { type TargetQuarter, TypeQuarter } from '@/types/Project'

const props = defineProps<{
  modelValue?: TargetQuarter[] | null
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', v: TargetQuarter[]): void
  (e: 'itemSelected', v: TargetQuarter[]): void
}>()

interface Filter {
  label: string
  filter: TargetQuarter
}

const quarterOptions: Filter[] = [
  { label: '2025 3Q', filter: { year: 2025, quarter: TypeQuarter.Q3 } },
  { label: '2025 4Q', filter: { year: 2025, quarter: TypeQuarter.Q4 } },
  { label: '2026 1Q', filter: { year: 2026, quarter: TypeQuarter.Q1 } },
  { label: '2026 2Q', filter: { year: 2026, quarter: TypeQuarter.Q2 } },
  { label: '2026 3Q', filter: { year: 2026, quarter: TypeQuarter.Q3 } },
  { label: '2026 4Q', filter: { year: 2026, quarter: TypeQuarter.Q4 } },
]

const toOption = (fq: TargetQuarter): Filter | undefined =>
  quarterOptions.find((o) => o.filter.year === fq.year && o.filter.quarter === fq.quarter)

const sameFQArray = (a: TargetQuarter[], b: TargetQuarter[]) => {
  if (a.length !== b.length) return false
  const key = (x: TargetQuarter) => `${x.year}-${x.quarter}`
  const A = new Set(a.map(key))
  for (const s of b.map(key)) if (!A.has(s)) return false
  return true
}

const sameFilterArray = (a: Filter[], b: Filter[]) =>
  sameFQArray(
    a.map((x) => x.filter),
    b.map((x) => x.filter),
  )

const selected_option = ref<Filter[]>(
  (props.modelValue ?? []).map(toOption).filter((v): v is Filter => !!v),
)

watch(
  () => props.modelValue,
  (v) => {
    const next = (v ?? []).map(toOption).filter((x): x is Filter => !!x)
    if (!sameFilterArray(selected_option.value, next)) {
      selected_option.value = next
    }
  },
  { deep: false },
)

watch(
  () => selected_option.value.map((x) => `${x.filter.year}-${x.filter.quarter}`),
  () => {
    const nextFQ = selected_option.value.map((v) => v.filter)
    const current = props.modelValue ?? []
    if (!sameFQArray(current, nextFQ)) {
      emit('update:modelValue', nextFQ)
      emit('itemSelected', nextFQ)
    }
  },
)

const selectionText = computed(() => {
  const total = quarterOptions.length
  const count = selected_option.value.length
  if (count === 0) return ''
  if (total > 0 && count === total) return 'ALL'
  if (count === 1) return selected_option.value[0].label
  return `${selected_option.value[0].label} + ${count - 1}`
})
</script>

<template>
  <v-select
    clearable
    multiple
    :items="quarterOptions"
    v-model="selected_option"
    label="Quarter"
    item-title="label"
    :return-object="true"
    hide-details="auto"
  >
    <template #selection="{ index }">
      <span v-if="index === 0">{{ selectionText }}</span>
    </template>
  </v-select>
</template>

<style scoped>
@import '@/assets/main.css';
</style>
