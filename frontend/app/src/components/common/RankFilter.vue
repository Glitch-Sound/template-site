<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { TypeRank } from '@/types/Project'

const props = defineProps<{
  modelValue?: number[] | null
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', v: number[]): void
  (e: 'itemSelected', v: number[]): void
}>()

interface Filter {
  label: string
  value: TypeRank
}

const options: Filter[] = [
  { label: 'A', value: TypeRank.A },
  { label: 'B', value: TypeRank.B },
  { label: 'C', value: TypeRank.C },
  { label: 'D', value: TypeRank.D },
  { label: 'E', value: TypeRank.E },
  { label: 'X', value: TypeRank.X },
]

const toOptionByValue = (value: number): Filter | undefined =>
  options.find((o) => o.value === value)

const sameFilterArray = (a: Filter[], b: Filter[]) => {
  if (a.length !== b.length) return false
  const A = new Set(a.map((x) => x.value))
  for (const s of b.map((x) => x.value)) if (!A.has(s)) return false
  return true
}
const sameNumberArray = (a: number[], b: number[]) => {
  if (a.length !== b.length) return false
  const A = new Set(a)
  for (const x of b) if (!A.has(x)) return false
  return true
}

const selected_option = ref<Filter[]>(
  (props.modelValue ?? []).map(toOptionByValue).filter((v): v is Filter => !!v),
)

watch(
  () => props.modelValue,
  (v) => {
    const next = (v ?? []).map(toOptionByValue).filter((x): x is Filter => !!x)
    if (!sameFilterArray(selected_option.value, next)) selected_option.value = next
  },
)

watch(
  () => selected_option.value.map((x) => x.value),
  () => {
    const nextNums = selected_option.value.map((v) => v.value)
    const current = props.modelValue ?? []
    if (!sameNumberArray(current, nextNums)) {
      emit('update:modelValue', nextNums)
      emit('itemSelected', nextNums)
    }
  },
)

const selectionText = computed(() => {
  const total = options.length
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
    :items="options"
    v-model="selected_option"
    label="Rank"
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
</style>
