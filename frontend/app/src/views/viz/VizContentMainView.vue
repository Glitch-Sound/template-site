<script setup lang="ts">
import { storeToRefs } from 'pinia'
import ChartAmount from '@/components/viz/ChartAmount.vue'
import ChartQuarter from '@/components/viz/ChartQuarter.vue'
import ChartCompany from '@/components/viz/ChartCompany.vue'
import ChartProgress from '@/components/viz/ChartProgress.vue'
import { useSummaryStore } from '@/stores/SummaryStore'
import { useTargetStore } from '@/stores/TargetStore'

const summaryStore = useSummaryStore()
const targetStore = useTargetStore()
const {
  is_loading_amount_latest,
  is_loading_amount_year,
  is_loading_company_latest,
  is_loading_company_year,
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
          is_loading_targets
        "
        contained
        scrim="transparent"
        class="align-center justify-center"
      >
        <v-progress-circular indeterminate color="primary" />
      </v-overlay>

      <div class="charts-grid">
        <ChartAmount />
        <ChartQuarter />
        <ChartCompany />
      </div>
      <div class="charts-row">
        <ChartProgress />
      </div>
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

.charts-grid {
  display: grid;
  grid-template-columns: 3.2fr 4.3fr 2.5fr;
  gap: 8px;
  align-items: stretch;
}

@media (max-width: 1200px) {
  .charts-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 800px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
}

.charts-row {
  margin-top: 8px;
  flex: 1;
  min-height: 0;
}
</style>
