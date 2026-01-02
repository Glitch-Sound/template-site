<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { Doughnut } from 'vue-chartjs'
import type { ChartOptions, TooltipItem } from 'chart.js'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import { useSummaryStore } from '@/stores/SummaryStore'
import { useTargetStore } from '@/stores/TargetStore'

ChartJS.register(ArcElement, Tooltip, Legend)

const summaryStore = useSummaryStore()
const targetStore = useTargetStore()
const currentYear = new Date().getFullYear()

onMounted(async () => {
  await targetStore.fetchTargets()
  const year =
    targetStore.targets.find((target) => target.year === currentYear)?.year ?? currentYear
  await summaryStore.fetchSummariesCompany(year)
})

const palette = ['#2f6b7a', '#3a8f6b', '#7a6c2f', '#6b2f2f', '#4a4a4a', '#394b5a']

const companyTotals = computed(() => {
  const latestDate = summaryStore.summaries_company_year.reduce((acc, item) => {
    if (!acc) return item.date_snap
    return item.date_snap > acc ? item.date_snap : acc
  }, '')

  const map = new Map<number, { name: string; value: number }>()
  summaryStore.summaries_company_year.forEach((item) => {
    if (latestDate && item.date_snap !== latestDate) return
    const rid = item.company?.rid ?? item.rid
    const name = item.company?.name ?? 'Unknown'
    const existing = map.get(rid)
    if (existing) {
      existing.value += item.all_order
    } else {
      map.set(rid, { name, value: item.all_order })
    }
  })
  return Array.from(map.values())
})

const chartData = computed(() => ({
  labels: companyTotals.value.map((item) => item.name),
  datasets: [
    {
      data: companyTotals.value.map((item) => item.value),
      backgroundColor: companyTotals.value.map((_, index) => palette[index % palette.length]),
      borderColor: 'rgba(0, 0, 0, 0.7)',
      borderWidth: 2,
    },
  ],
}))

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
