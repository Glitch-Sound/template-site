<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  rid: number
}>()

const rid = computed(() => String(props.rid).padStart(4, '0'))
</script>

<template>
  <span class="mx-3"> #{{ rid }} </span>
</template>

<style scoped>
@import '@/assets/main.css';
</style>
