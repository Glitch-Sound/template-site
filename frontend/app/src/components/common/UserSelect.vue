<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'

import { type EmitType } from '@/components/common/events'
import useUserStore from '@/stores/UserStore'

const props = defineProps<{
  modelValue?: number | null
  label?: string
}>()

const store_user = useUserStore()

const selected_option = ref(props.modelValue || null)

onMounted(() => {
  store_user.fetchUsers()
})

const emit = defineEmits<EmitType>()
const itemSelected = () => {
  const selectedItem = store_user.users.find((item) => item.rid === selected_option.value)
  if (selectedItem) {
    emit('itemSelected', selectedItem)
  }
}
</script>

<template>
  <v-select
    :items="store_user.users"
    v-model="selected_option"
    :label="props.label ?? 'User'"
    item-title="name"
    item-value="rid"
    @update:modelValue="itemSelected"
  />
</template>

<style scoped></style>
