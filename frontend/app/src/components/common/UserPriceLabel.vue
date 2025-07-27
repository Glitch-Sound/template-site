<script setup lang="ts">
import { defineProps } from 'vue'

const props = defineProps<{
  price: number
}>()
</script>

<template>
  <div style="width: 90px; text-align: right">{{ props.price.toLocaleString() }}</div>
</template>

<style scoped></style>
