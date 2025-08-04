<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'

import { type EmitType } from '@/components/common/events'
import useUserStore from '@/stores/UserStore'

const props = defineProps<{
  modelValue?: number[] | null
  label?: string
}>()

const store_user = useUserStore()

const selected_option = ref<number[]>(props.modelValue ?? [])

onMounted(() => {
  store_user.fetchUsers()
})

const emit = defineEmits<EmitType>()
const itemSelected = (val: number[]) => {
  const selectedFilters = store_user.users.filter((user) => val.includes(user.rid))
  emit('itemSelected', selectedFilters)
  emit('update:modelValue', val)
}
</script>

<template>
  <v-select
    clearable
    chips
    multiple
    :items="store_user.users"
    v-model="selected_option"
    :label="props.label ?? 'User'"
    item-title="name"
    item-value="rid"
    @update:modelValue="itemSelected"
  />
</template>

<style scoped></style>
