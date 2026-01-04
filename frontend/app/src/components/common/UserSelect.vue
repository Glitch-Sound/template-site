<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'
import { storeToRefs } from 'pinia'

import type { User } from '@/types/User'
import { TypePost } from '@/types/User'
import { useUserStore } from '@/stores/UserStore'

const props = defineProps<{
  modelValue: number | null
  label?: string
}>()

const emit = defineEmits<{
  'update:modelValue': [value: number | null]
  itemSelected: [user: User | null]
}>()

const store_user = useUserStore()
const { users, is_loading } = storeToRefs(store_user)
const { fetchUsers, getByRid } = store_user

const selected_option = ref<number | null>(
  props.modelValue && props.modelValue !== 0 ? props.modelValue : null,
)

const filtered_users = computed(() =>
  users.value.filter((user) => user.post !== TypePost.NONE && user.post !== TypePost.GUEST),
)

onMounted(async () => {
  await fetchUsers()
})

watch(
  () => props.modelValue,
  (v) => {
    selected_option.value = v && v !== 0 ? v : null
  },
)

watch(selected_option, (v) => {
  emit('update:modelValue', v)
  const item = v != null ? (getByRid(v) ?? null) : null
  emit('itemSelected', item)
})
</script>

<template>
  <v-select
    v-model="selected_option"
    :items="filtered_users"
    :label="props.label ?? 'User'"
    item-title="name"
    item-value="rid"
    :loading="is_loading"
    :disabled="is_loading"
    clearable
    hide-details="auto"
  />
</template>

<style scoped>
</style>
