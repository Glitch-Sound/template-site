<script setup lang="ts">
import { defineProps } from 'vue'

import { type User } from '@/types/User'
import UserIcon from '@/components/common/UserIcon.vue'

const props = defineProps<{
  user: User
}>()
</script>

<template>
  <span style="display: flex; align-items: center">
    <UserIcon class="mr-2" :user="props.user" :size="20" />
    <span style="color: #c0c0c0">
      {{ props.user.name }}
    </span>
  </span>
</template>

<style scoped></style>
