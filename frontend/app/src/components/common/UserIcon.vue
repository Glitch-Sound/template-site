<script setup lang="ts">
import Identicon from 'identicon.js'
import * as CryptoJS from 'crypto-js'

import { computed } from 'vue'

import type { User } from '@/types/User'

const props = defineProps<{
  user: User
  size: number
}>()

const hash_user = computed(() => {
  if (props.user.rid == null || props.user.username == null) {
    return ''
  }
  return CryptoJS.MD5(props.user.rid + props.user.username || '').toString()
})

const identicon_user = computed(() => {
  const options = {
    background: [255, 255, 255, 0] as [number, number, number, number],
    format: 'svg' as 'svg',
  }
  return 'data:image/svg+xml;base64,' + new Identicon(hash_user.value, options).toString()
})
</script>

<template>
  <img :src="identicon_user" :width="props.size" :height="props.size" />
</template>

<style scoped>
@import '@/assets/main.css';
</style>
