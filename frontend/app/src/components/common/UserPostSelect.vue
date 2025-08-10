<script setup lang="ts">
import { ref } from 'vue'

import { TypePost } from '@/types/User'
import { type EmitType } from '@/components/common/events'
import UserPostLabel from '@/components/common/UserPostLabel.vue'

const props = defineProps<{
  modelValue?: number
}>()

const selected_post = ref(props.modelValue ?? TypeContract.K)

const emit = defineEmits<EmitType<'itemSelected', number>>()
const emitSelected = () => {
  emit('itemSelected', selected_post.value)
}
</script>

<template>
  <div class="d-flex justify-center">
    <v-chip-group v-model="selected_post" @update:modelValue="emitSelected">
      <UserPostLabel :post="TypePost.K" />
      <UserPostLabel :post="TypePost.C" />
      <UserPostLabel :post="TypePost.L" />
      <UserPostLabel :post="TypePost.T" />
      <UserPostLabel :post="TypePost.BP" />
    </v-chip-group>
  </div>
</template>

<style scoped>
@import '@/assets/main.css';

.v-chip-group {
  margin: 0 0 15px 0;
}
</style>
