<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useProjectStore } from '@/stores/ProjectStore'
import { type TargetQuarter, TypeQuarter } from '@/types/Project'

const props = defineProps<{
  modelValue?: number[] | null
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', v: number[]): void
  (e: 'itemSelected', v: number[]): void
}>()

const projectStore = useProjectStore()
const { project_targets } = storeToRefs(projectStore)

const Q_LABEL: Record<Exclude<TypeQuarter, TypeQuarter.NONE>, string> = {
  [TypeQuarter.Q1]: '1Q',
  [TypeQuarter.Q2]: '2Q',
  [TypeQuarter.Q3]: '3Q',
  [TypeQuarter.Q4]: '4Q',
} as const
const quarterLabel = (q: TypeQuarter) => (q === TypeQuarter.NONE ? '' : Q_LABEL[q])

const fqToNumber = (fq: TargetQuarter) => fq.year * 10 + fq.quarter
const numberToFQ = (n: number): TargetQuarter | undefined => {
  const year = Math.trunc(n / 10)
  const qNum = n % 10
  if (
    qNum === TypeQuarter.Q1 ||
    qNum === TypeQuarter.Q2 ||
    qNum === TypeQuarter.Q3 ||
    qNum === TypeQuarter.Q4
  ) {
    return { year, quarter: qNum }
  }
  return undefined
}

interface Filter {
  label: string
  filter: TargetQuarter
}
const options = computed<Filter[]>(() =>
  project_targets.value
    .filter((fq) => fq.quarter !== TypeQuarter.NONE)
    .map((fq) => ({ label: `${fq.year} ${quarterLabel(fq.quarter)}`.trim(), filter: fq })),
)

const toOptionByNumber = (n: number): Filter | undefined => {
  const fq = numberToFQ(n)
  if (!fq) return undefined
  return options.value.find((o) => o.filter.year === fq.year && o.filter.quarter === fq.quarter)
}

const sameFilterArray = (a: Filter[], b: Filter[]) => {
  const key = (x: Filter) => `${x.filter.year}-${x.filter.quarter}`
  if (a.length !== b.length) return false
  const A = new Set(a.map(key))
  for (const s of b.map(key)) if (!A.has(s)) return false
  return true
}
const sameNumberArray = (a: number[], b: number[]) => {
  if (a.length !== b.length) return false
  const A = new Set(a)
  for (const x of b) if (!A.has(x)) return false
  return true
}

const selected_option = ref<Filter[]>(
  (props.modelValue ?? []).map(toOptionByNumber).filter((v): v is Filter => !!v),
)

watch(
  () => props.modelValue,
  (v) => {
    const next = (v ?? []).map(toOptionByNumber).filter((x): x is Filter => !!x)
    if (!sameFilterArray(selected_option.value, next)) selected_option.value = next
  },
)

watch(
  () => selected_option.value.map((x) => fqToNumber(x.filter)),
  () => {
    const nextNums = selected_option.value.map((v) => fqToNumber(v.filter))
    const current = props.modelValue ?? []
    if (!sameNumberArray(current, nextNums)) {
      emit('update:modelValue', nextNums)
      emit('itemSelected', nextNums)
    }
  },
)

const selectionText = computed(() => {
  const total = options.value.length
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
</style>
