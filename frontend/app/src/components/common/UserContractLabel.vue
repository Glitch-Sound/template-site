<script setup lang="ts">
import { defineProps } from 'vue'

import { TypeContract } from '@/types/User'

const props = defineProps<{
  contract: TypeContract
}>()
</script>

<template>
  <v-chip
    size="small"
    :value="TypeContract.PROPER"
    color="#b0e0e6"
    v-if="props.contract == TypeContract.PROPER"
  >
    PROPER
  </v-chip>

  <v-chip
    size="small"
    :value="TypeContract.TEMP"
    color="#84c69b"
    v-if="props.contract == TypeContract.TEMP"
  >
    TEMPORARY
  </v-chip>

  <v-chip
    size="small"
    :value="TypeContract.CONSIGN_C"
    color="#e94560"
    v-if="props.contract == TypeContract.CONSIGN_C"
  >
    C CHIEF
  </v-chip>

  <v-chip
    size="small"
    :value="TypeContract.CONSIGN_M"
    color="#f4a261"
    v-if="props.contract == TypeContract.CONSIGN_M"
  >
    C MEMBER
  </v-chip>
</template>

<style scoped></style>
