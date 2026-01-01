<script setup lang="ts">
import ChartAmount from '@/components/viz/ChartAmount.vue'
import ChartQuarter from '@/components/viz/ChartQuarter.vue'
import ChartCompany from '@/components/viz/ChartCompany.vue'
import ChartProgress from '@/components/viz/ChartProgress.vue'
</script>

<template>
  <v-main>
    <v-sheet class="main">
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
@import '@/assets/main.css';

.charts-grid {
  display: grid;
  grid-template-columns: 3.2fr 4fr 2.8fr;
  gap: 24px;
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
  margin-top: 24px;
}
</style>
