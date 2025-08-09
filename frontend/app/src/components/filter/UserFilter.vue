<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { storeToRefs } from 'pinia'

import type { User } from '@/types/User'
import { useUserStore } from '@/stores/UserStore'

const props = defineProps<{
  modelValue?: number[] | null
  label?: string
}>()

const emit = defineEmits<{
  'update:modelValue': [value: number[]]
  itemSelected: [users: User[]]
}>()

const store_user = useUserStore()
const { users, is_loading } = storeToRefs(store_user)
const { fetchUsers } = store_user

const selected_option = ref<number[]>(props.modelValue ?? [])

onMounted(async () => {
  try {
    await fetchUsers()
  } catch (e) {
    console.error(e)
  }
})

watch(
  () => props.modelValue,
  (v) => {
    selected_option.value = v ?? []
  },
)

watch(selected_option, (val) => {
  emit('update:modelValue', val)
  const selectedFilters = users.value.filter((user) => val.includes(user.rid))
  emit('itemSelected', selectedFilters)
})
</script>

<template>
  <v-select
    clearable
    chips
    multiple
    :items="users"
    v-model="selected_option"
    :label="props.label ?? 'User'"
    item-title="name"
    item-value="rid"
    :loading="is_loading"
    :disabled="is_loading"
    hide-details="auto"
  />
</template>

<style scoped></style>
