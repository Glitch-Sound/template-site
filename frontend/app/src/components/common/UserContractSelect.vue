<script setup lang="ts">
import { ref } from 'vue'

import { TypeContract } from '@/types/User'
import { type EmitType } from '@/components/common/events'

import UserContractLabel from '@/components/common/UserContractLabel.vue'

const selected_contract = ref(0)

const emit = defineEmits<EmitType<'itemSelected', number>>()
const emitSelected = () => {
  emit('itemSelected', selected_contract.value)
}
</script>

<template>
  <div class="d-flex justify-center">
    <v-chip-group v-model="selected_contract" @update:modelValue="emitSelected">
      <UserContractLabel :contract="TypeContract.PROPER" />
      <UserContractLabel :contract="TypeContract.TEMP" />
      <UserContractLabel :contract="TypeContract.CONSIGN_C" />
      <UserContractLabel :contract="TypeContract.CONSIGN_M" />
    </v-chip-group>
  </div>
</template>

<style scoped>
.v-chip-group {
  margin: 0 0 15px 0;
}
</style>
