<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { storeToRefs } from 'pinia'

import type { User } from '@/types/User'
import { useUserStore } from '@/stores/UserStore'

const props = defineProps<{
  modelValue?: number | null
  label?: string
}>()

const emit = defineEmits<{
  'update:modelValue': [value: number | null]
  itemSelected: [user: User]
}>()

const store_user = useUserStore()
const { users, is_loading } = storeToRefs(store_user)
const { fetchUsers, getByRid } = store_user

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
  const item = v != null ? getByRid(v) : undefined
  if (item) emit('itemSelected', item)
})

onMounted(async () => {
  try {
    await fetchUsers()
  } catch (e) {
    console.error(e)
  }
})
</script>

<template>
  <v-select
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
