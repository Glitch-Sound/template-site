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
      <v-tooltip location="top" text="A ： 作業確定 + 正式番号発行">
        <template #activator="{ props }">
          <span v-bind="props">
            <RankLabel :rank="TypeRank.A" />
          </span>
        </template>
      </v-tooltip>
      <v-tooltip location="top" text="B ： 作業確定 + 正式番号未発行">
        <template #activator="{ props }">
          <span v-bind="props">
            <RankLabel :rank="TypeRank.B" />
          </span>
        </template>
      </v-tooltip>
      <v-tooltip location="top" text="C ： 作業内容調整中">
        <template #activator="{ props }">
          <span v-bind="props">
            <RankLabel :rank="TypeRank.C" />
          </span>
        </template>
      </v-tooltip>
      <v-tooltip location="top" text="D ： 継続予定">
        <template #activator="{ props }">
          <span v-bind="props">
            <RankLabel :rank="TypeRank.D" />
          </span>
        </template>
      </v-tooltip>
      <v-tooltip location="top" text="E ： 新規予定">
        <template #activator="{ props }">
          <span v-bind="props">
            <RankLabel :rank="TypeRank.E" />
          </span>
        </template>
      </v-tooltip>
      <v-tooltip location="top" text="X ： ドロップ">
        <template #activator="{ props }">
          <span v-bind="props">
            <RankLabel :rank="TypeRank.X" />
          </span>
        </template>
      </v-tooltip>
    </v-chip-group>
  </div>
</template>

<style scoped>

.v-chip-group {
  margin: 0 0 15px 0;
}
</style>
