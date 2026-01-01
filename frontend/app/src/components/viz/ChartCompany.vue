<script setup lang="ts">
import { Doughnut } from 'vue-chartjs'
import type { ChartOptions, TooltipItem } from 'chart.js'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'

ChartJS.register(ArcElement, Tooltip, Legend)

const chartData = {
  labels: ['Alpha Inc.', 'Beacon Ltd.', 'Crest Co.', 'Dawn LLC', 'Echo PLC'],
  datasets: [
    {
      data: [3200000, 2400000, 1800000, 1200000, 900000],
      backgroundColor: ['#2f6b7a', '#3a8f6b', '#7a6c2f', '#6b2f2f', '#4a4a4a'],
      borderColor: 'rgba(0, 0, 0, 0.7)',
      borderWidth: 2,
    },
  ],
}

const currencyFormatter = new Intl.NumberFormat('ja-JP', {
  style: 'currency',
  currency: 'JPY',
  maximumFractionDigits: 0,
})

const chartOptions: ChartOptions<'doughnut'> = {
  responsive: true,
  maintainAspectRatio: false,
  cutout: '80%',
  layout: {
    padding: 0,
  },
  plugins: {
    legend: {
      position: 'right',
      labels: {
        color: '#d8d8d8',
        boxWidth: 20,
        boxHeight: 12,
        padding: 15,
      },
    },
    tooltip: {
      callbacks: {
        label: (context: TooltipItem<'doughnut'>) => {
          if (typeof context.raw !== 'number') return context.label ?? ''
          return `${context.label}: ${currencyFormatter.format(context.raw)}`
        },
      },
    },
  },
}
</script>

<template>
  <v-card class="company-card" rounded="xl" variant="tonal">
    <v-card-title class="text-h6 font-weight-medium">Company</v-card-title>

    <v-card-text class="pa-4">
      <div class="chart-wrap">
        <Doughnut :data="chartData" :options="chartOptions" />
      </div>
    </v-card-text>
  </v-card>
</template>

<style scoped>
@import '@/assets/main.css';

.company-card {
  background: rgba(4, 4, 4, 0.98);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.chart-wrap {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  height: 220px;
}
</style>
