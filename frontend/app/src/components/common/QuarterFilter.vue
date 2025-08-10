<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useProjectStore } from '@/stores/ProjectStore'
import { type TargetQuarter, TypeQuarter } from '@/types/Project'

const props = defineProps<{
  modelValue?: TargetQuarter[] | null
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', v: TargetQuarter[]): void
  (e: 'itemSelected', v: TargetQuarter[]): void
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

interface Filter {
  label: string
  filter: TargetQuarter
}
const options = computed<Filter[]>(() =>
  project_targets.value
    .filter((fq) => fq.quarter !== TypeQuarter.NONE)
    .map((fq) => ({ label: `${fq.year} ${quarterLabel(fq.quarter)}`.trim(), filter: fq })),
)

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
const toOption = (fq: TargetQuarter): Filter | undefined =>
  options.value.find((o) => o.filter.year === fq.year && o.filter.quarter === fq.quarter)

const selected_option = ref<Filter[]>(
  (props.modelValue ?? []).map(toOption).filter((v): v is Filter => !!v),
)

watch(
  () => props.modelValue,
  (v) => {
    const next = (v ?? []).map(toOption).filter((x): x is Filter => !!x)
    if (!sameFilterArray(selected_option.value, next)) selected_option.value = next
  },
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
@import '@/assets/main.css';
</style>
