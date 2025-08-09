<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { storeToRefs } from 'pinia'

import type { ProjectGroup } from '@/types/Project'
import { useProjectStore } from '@/stores/ProjectStore'

const props = defineProps<{
  modelValue?: number | null
}>()

const emit = defineEmits<{
  'update:modelValue': [value: number | null]
  itemSelected: [projectGroup: ProjectGroup]
}>()

const store_project = useProjectStore()
const { project_groups, is_loading_groups } = storeToRefs(store_project)
const { fetchProjectGroups, getGroupByRid } = store_project

const selected_option = ref<number | null>(
  props.modelValue && props.modelValue !== 0 ? props.modelValue : null,
)

watch(
  () => props.modelValue,
  (v) => {
    selected_option.value = v ?? null
  },
)

watch(selected_option, (v) => {
  emit('update:modelValue', v ?? null)
  const item = v != null ? getGroupByRid(v) : undefined
  if (item) emit('itemSelected', item)
})

onMounted(async () => {
  try {
    await fetchProjectGroups()
  } catch (e) {
    console.error(e)
  }
})
</script>

<template>
  <v-select
    :items="project_groups"
    v-model="selected_option"
    label="Project Group"
    item-title="name"
    item-value="rid"
    :loading="is_loading_groups"
    :disabled="is_loading_groups"
    hide-details="auto"
  />
</template>

<style scoped></style>
