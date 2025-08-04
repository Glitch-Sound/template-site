<script setup lang="ts">
import { defineProps } from 'vue'

import { TypeRank } from '@/types/Project'

const props = defineProps<{
  rank: TypeRank
}>()
</script>

<template>
  <v-chip size="small" :value="TypeRank.A" color="#2196f3" v-if="props.rank == TypeRank.A">
    A
  </v-chip>

  <v-chip size="small" :value="TypeRank.B" color="#528edb" v-if="props.rank == TypeRank.B">
    B
  </v-chip>

  <v-chip size="small" :value="TypeRank.C" color="#857fc3" v-if="props.rank == TypeRank.C">
    C
  </v-chip>

  <v-chip size="small" :value="TypeRank.D" color="#b06fab" v-if="props.rank == TypeRank.D">
    D
  </v-chip>

  <v-chip size="small" :value="TypeRank.E" color="#808080" v-if="props.rank == TypeRank.E">
    E
  </v-chip>
</template>

<style scoped></style>
