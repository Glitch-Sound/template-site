<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'

import { type EmitType } from '@/components/common/events'
import useProjectStore from '@/stores/ProjectStore'

const props = defineProps<{
  modelValue?: number | null
}>()

const store_project = useProjectStore()

const selected_option = ref(props.modelValue || null)

onMounted(() => {
  store_project.fetchProjectGroups()
})

const emit = defineEmits<EmitType>()
const itemSelected = () => {
  const selectedItem = store_project.project_groups.find(
    (item) => item.rid === selected_option.value,
  )
  if (selectedItem) {
    emit('itemSelected', selectedItem)
  }
}
</script>

<template>
  <v-select
    :items="store_project.project_groups"
    v-model="selected_option"
    label="Project Group"
    item-title="name"
    item-value="rid"
    @update:modelValue="itemSelected"
  />
</template>

<style scoped></style>
