<script setup lang="ts">
import { ref } from 'vue'

import { type EmitType } from '@/components/common/events'

const is_enable = ref(false)

const emit = defineEmits<EmitType>()
const emitSelected = () => {
  emit('delete')
}
</script>

<template>
  <v-row class="ma-1">
    <v-col cols="auto">
      <v-switch :hide-details="true" base-color="#3e3e3e" color="#930000" v-model="is_enable" />
    </v-col>

    <v-col cols="auto">
      <v-btn :disabled="!is_enable" @click="emitSelected">DELETE</v-btn>
    </v-col>
  </v-row>
</template>

<style scoped>
.v-row {
  align-items: center;
}
</style>
