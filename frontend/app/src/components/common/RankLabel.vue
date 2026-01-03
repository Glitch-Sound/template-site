<script setup lang="ts">
import { TypeRank } from '@/types/Project'
import { rankPalette } from '@/constants/chartPalette'

const props = defineProps<{
  rank: TypeRank
}>()
</script>

<template>
  <v-chip
    size="small"
    :value="TypeRank.A"
    :color="rankPalette[TypeRank.A]"
    v-if="props.rank == TypeRank.A"
  >
    A
  </v-chip>

  <v-chip
    size="small"
    :value="TypeRank.B"
    :color="rankPalette[TypeRank.B]"
    v-if="props.rank == TypeRank.B"
  >
    B
  </v-chip>

  <v-chip
    size="small"
    :value="TypeRank.C"
    :color="rankPalette[TypeRank.C]"
    v-if="props.rank == TypeRank.C"
  >
    C
  </v-chip>

  <v-chip
    size="small"
    :value="TypeRank.D"
    :color="rankPalette[TypeRank.D]"
    v-if="props.rank == TypeRank.D"
  >
    D
  </v-chip>

  <v-chip
    size="small"
    :value="TypeRank.E"
    :color="rankPalette[TypeRank.E]"
    v-if="props.rank == TypeRank.E"
  >
    E
  </v-chip>

  <v-chip
    size="small"
    :value="TypeRank.X"
    :color="rankPalette[TypeRank.X]"
    v-if="props.rank == TypeRank.X"
  >
    X
  </v-chip>
</template>

<style scoped>
@import '@/assets/main.css';
</style>
