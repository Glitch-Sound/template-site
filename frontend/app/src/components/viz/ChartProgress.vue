<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { Line } from 'vue-chartjs'
import type { ChartOptions, TooltipItem } from 'chart.js'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from 'chart.js'
import { useSummaryStore } from '@/stores/SummaryStore'
import { useTargetStore } from '@/stores/TargetStore'
import { TypeRank } from '@/types/Project'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend)

const summaryStore = useSummaryStore()
const targetStore = useTargetStore()
const year = new Date().getFullYear()

onMounted(async () => {
  await Promise.all([
    summaryStore.fetchSummariesAmountLatest(),
    targetStore.fetchTargets(),
  ])
})

const pad2 = (value: number) => String(value).padStart(2, '0')

const dateItems = (() => {
  const items: Array<{ label: string; month: number; index: number }> = []
  for (let month = 0; month < 12; month += 1) {
    const daysInMonth = new Date(year, month + 1, 0).getDate()
    for (let day = 1; day <= daysInMonth; day += 1) {
      const label = `${year}-${pad2(month + 1)}-${pad2(day)}`
      items.push({ label, month: month + 1, index: items.length })
    }
  }
  return items
})()

const labels = dateItems.map((item) => item.label)

const seriesFromQuarterValues = (quarters: number[]) =>
  dateItems.map((item) => {
    const quarterIndex = Math.floor((item.month - 1) / 3)
    return quarters[quarterIndex] ?? 0
  })

const summariesByRank = computed(() => {
  const map = new Map<number, { q1: number; q2: number; q3: number; q4: number }>()
  summaryStore.summaries_amount_latest.forEach((item) => {
    map.set(item.rank, {
      q1: item.quarter1_order,
      q2: item.quarter2_order,
      q3: item.quarter3_order,
      q4: item.quarter4_order,
    })
  })
  return map
})

const currentTarget = computed(
  () => targetStore.targets.find((target) => target.year === year) ?? null,
)

const quarterTargets = computed(() => {
  const q1 = currentTarget.value?.quarter1 ?? 0
  const q2 = currentTarget.value?.quarter2 ?? 0
  const q3 = currentTarget.value?.quarter3 ?? 0
  const q4 = currentTarget.value?.quarter4 ?? 0
  return [q1, q1 + q2, q1 + q2 + q3, q1 + q2 + q3 + q4]
})

const chartData = computed(() => ({
  labels,
  datasets: [
    {
      label: 'Rank A',
      data: seriesFromQuarterValues([
        summariesByRank.value.get(TypeRank.A)?.q1 ?? 0,
        summariesByRank.value.get(TypeRank.A)?.q2 ?? 0,
        summariesByRank.value.get(TypeRank.A)?.q3 ?? 0,
        summariesByRank.value.get(TypeRank.A)?.q4 ?? 0,
      ]),
      borderColor: '#5fa7c8',
      backgroundColor: 'rgba(95, 167, 200, 0.15)',
      tension: 0.2,
      pointRadius: 0,
      fill: false,
      stepped: true,
    },
    {
      label: 'Rank B',
      data: seriesFromQuarterValues([
        summariesByRank.value.get(TypeRank.B)?.q1 ?? 0,
        summariesByRank.value.get(TypeRank.B)?.q2 ?? 0,
        summariesByRank.value.get(TypeRank.B)?.q3 ?? 0,
        summariesByRank.value.get(TypeRank.B)?.q4 ?? 0,
      ]),
      borderColor: '#6bb48e',
      backgroundColor: 'rgba(107, 180, 142, 0.15)',
      tension: 0.2,
      pointRadius: 0,
      fill: false,
      stepped: true,
    },
    {
      label: 'Rank C',
      data: seriesFromQuarterValues([
        summariesByRank.value.get(TypeRank.C)?.q1 ?? 0,
        summariesByRank.value.get(TypeRank.C)?.q2 ?? 0,
        summariesByRank.value.get(TypeRank.C)?.q3 ?? 0,
        summariesByRank.value.get(TypeRank.C)?.q4 ?? 0,
      ]),
      borderColor: '#b3a45a',
      backgroundColor: 'rgba(179, 164, 90, 0.15)',
      tension: 0.2,
      pointRadius: 0,
      fill: false,
      stepped: true,
    },
    {
      label: 'Rank D',
      data: seriesFromQuarterValues([
        summariesByRank.value.get(TypeRank.D)?.q1 ?? 0,
        summariesByRank.value.get(TypeRank.D)?.q2 ?? 0,
        summariesByRank.value.get(TypeRank.D)?.q3 ?? 0,
        summariesByRank.value.get(TypeRank.D)?.q4 ?? 0,
      ]),
      borderColor: '#a06b6b',
      backgroundColor: 'rgba(160, 107, 107, 0.15)',
      tension: 0.2,
      pointRadius: 0,
      fill: false,
      stepped: true,
    },
    {
      label: 'Rank E',
      data: seriesFromQuarterValues([
        summariesByRank.value.get(TypeRank.E)?.q1 ?? 0,
        summariesByRank.value.get(TypeRank.E)?.q2 ?? 0,
        summariesByRank.value.get(TypeRank.E)?.q3 ?? 0,
        summariesByRank.value.get(TypeRank.E)?.q4 ?? 0,
      ]),
      borderColor: '#8a8a8a',
      backgroundColor: 'rgba(138, 138, 138, 0.15)',
      tension: 0.2,
      pointRadius: 0,
      fill: false,
      stepped: true,
    },
    {
      label: 'Quarter Target',
      data: seriesFromQuarterValues(quarterTargets.value),
      borderColor: 'rgba(255, 255, 255, 0.45)',
      borderDash: [6, 6],
      borderWidth: 2,
      pointRadius: 0,
      stepped: true,
    },
  ],
}))

const currencyFormatter = new Intl.NumberFormat('ja-JP', {
  style: 'currency',
  currency: 'JPY',
  maximumFractionDigits: 0,
})

const chartOptions: ChartOptions<'line'> = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    mode: 'index',
    intersect: false,
  },
  plugins: {
    legend: {
      position: 'top',
      labels: {
        color: '#d8d8d8',
      },
    },
    tooltip: {
      callbacks: {
        label: (context: TooltipItem<'line'>) => {
          if (typeof context.raw !== 'number') return context.dataset.label ?? ''
          return `${context.dataset.label}: ${currencyFormatter.format(context.raw)}`
        },
      },
    },
  },
  scales: {
    x: {
      ticks: {
        color: '#9c9c9c',
        maxTicksLimit: 12,
      },
      grid: {
        color: 'rgba(255, 255, 255, 0.06)',
      },
    },
    y: {
      ticks: {
        color: '#9c9c9c',
        callback: (value) => {
          if (typeof value !== 'number') return `${value}`
          const thousands = Math.round(value / 1000)
          return `¥${thousands.toLocaleString('ja-JP')}k`
        },
      },
      grid: {
        color: 'rgba(255, 255, 255, 0.08)',
      },
    },
  },
}
</script>

<template>
  <v-card class="progress-card" rounded="xl" variant="tonal">
    <v-card-title class="text-h6 font-weight-medium">Progress</v-card-title>

    <v-card-text class="pa-6">
      <div class="chart-wrap">
        <Line :data="chartData" :options="chartOptions" />
      </div>
    </v-card-text>
  </v-card>
</template>

<style scoped>
@import '@/assets/main.css';

.progress-card {
  background: rgba(4, 4, 4, 0.98);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.chart-wrap {
  height: 680px;
}
</style>
