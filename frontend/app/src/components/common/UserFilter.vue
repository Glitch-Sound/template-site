<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { storeToRefs } from 'pinia'

import { useProjectStore } from '@/stores/ProjectStore'
import type { User } from '@/types/User'

const props = defineProps<{
  modelValue?: number[] | null
  label?: string
}>()

const emit = defineEmits<{
  'update:modelValue': [value: number[]]
  itemSelected: [users: User[]]
}>()

const projectStore = useProjectStore()
const { project_users } = storeToRefs(projectStore)

const selected_option = ref<number[]>(props.modelValue ?? [])

watch(
  () => props.modelValue,
  (v) => {
    selected_option.value = v ?? []
  },
)

watch(selected_option, (val) => {
  emit('update:modelValue', val)
  const selectedFilters = project_users.value.filter((user) => val.includes(user.rid))
  emit('itemSelected', selectedFilters)
})

const selectionText = computed(() => {
  const total = project_users.value.length
  const count = selected_option.value.length
  if (count === 0) return ''
  if (total > 0 && count === total) return 'ALL'
  if (count === 1) {
    const u = project_users.value.find((u) => u.rid === selected_option.value[0])
    return u?.name ?? '1件'
  }
  const firstUser = project_users.value.find((u) => u.rid === selected_option.value[0])
  return `${firstUser?.name ?? ''} + ${count - 1}`
})
</script>

<template>
  <v-select
    clearable
    multiple
    :items="project_users"
    v-model="selected_option"
    :label="props.label ?? 'User'"
    item-title="name"
    item-value="rid"
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
