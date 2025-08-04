<script setup lang="ts">
import { defineProps } from 'vue'

import { TypeRank } from '@/types/Project'

const props = defineProps<{
  rank: TypeRank
}>()
</script>

<template>
  <v-icon size="x-large" color="#2196f3" v-if="props.rank == TypeRank.A">mdi-alpha-a-box</v-icon>
  <v-icon size="x-large" color="#528edb" v-if="props.rank == TypeRank.B">mdi-alpha-b-box</v-icon>
  <v-icon size="x-large" color="#857fc3" v-if="props.rank == TypeRank.C">mdi-alpha-c-box</v-icon>
  <v-icon size="x-large" color="#b06fab" v-if="props.rank == TypeRank.D">mdi-alpha-d-box</v-icon>
  <v-icon size="x-large" color="#808080" v-if="props.rank == TypeRank.E">mdi-alpha-e-box</v-icon>
</template>

<style scoped></style>
