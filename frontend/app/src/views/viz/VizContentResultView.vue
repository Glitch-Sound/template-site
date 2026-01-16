<script setup lang="ts">
import { storeToRefs } from 'pinia'
import ChartResult from '@/components/viz/ChartResult.vue'
import { useSummaryStore } from '@/stores/SummaryStore'
import { useTargetStore } from '@/stores/TargetStore'

const summaryStore = useSummaryStore()
const targetStore = useTargetStore()
const {
  is_loading_amount_latest,
  is_loading_amount_year,
  is_loading_company_latest,
  is_loading_company_year,
  is_loading_sankey,
} = storeToRefs(summaryStore)
const { is_loading: is_loading_targets } = storeToRefs(targetStore)
</script>

<template>
  <v-main>
    <v-sheet class="main">
      <v-overlay
        :model-value="
          is_loading_amount_latest ||
          is_loading_amount_year ||
          is_loading_company_latest ||
          is_loading_company_year ||
          is_loading_sankey ||
          is_loading_targets
        "
        contained
        scrim="transparent"
        class="align-center justify-center"
      >
        <v-progress-circular indeterminate color="primary" />
      </v-overlay>

      <ChartResult />
    </v-sheet>
  </v-main>
</template>

<style scoped>
.main {
  height: calc(100vh - var(--v-layout-top) - 70px);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
</style>
