<script setup lang="ts">
import { ref } from 'vue'

import { type EmitType } from '@/components/common/events'
import { TypeRank } from '@/types/Project'
import RankLabel from '@/components/common/RankLabel.vue'

const props = defineProps<{
  modelValue?: number
}>()

const selected_rank = ref(props.modelValue ?? TypeRank.E)

const emit = defineEmits<EmitType<'itemSelected', number>>()
const emitSelected = () => {
  emit('itemSelected', selected_rank.value)
}
</script>

<template>
  <div class="d-flex justify-center">
    <v-chip-group v-model="selected_rank" @update:modelValue="emitSelected">
      <RankLabel :rank="TypeRank.A" />
      <RankLabel :rank="TypeRank.B" />
      <RankLabel :rank="TypeRank.C" />
      <RankLabel :rank="TypeRank.D" />
      <RankLabel :rank="TypeRank.E" />
      <RankLabel :rank="TypeRank.X" />
    </v-chip-group>
  </div>
</template>

<style scoped>

.v-chip-group {
  margin: 0 0 15px 0;
}
</style>
