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
import { useChartFilterStore } from '@/stores/ChartFilterStore'
import { rankPalette } from '@/constants/chartPalette'
import { TypeRank } from '@/types/Project'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend)

const summaryStore = useSummaryStore()
const targetStore = useTargetStore()
const year = new Date().getFullYear()
const chartFilterStore = useChartFilterStore()

onMounted(async () => {
  await Promise.all([summaryStore.fetchSummariesAmount(year), targetStore.fetchTargets()])
})

const pad2 = (value: number) => String(value).padStart(2, '0')

const dateItems = computed(() => {
  const items: Array<{ label: string; month: number; index: number }> = []
  for (let month = 0; month < 12; month += 1) {
    const daysInMonth = new Date(year, month + 1, 0).getDate()
    for (let day = 1; day <= daysInMonth; day += 1) {
      const label = `${year}-${pad2(month + 1)}-${pad2(day)}`
      items.push({ label, month: month + 1, index: items.length })
    }
  }
  return items
})

const labels = computed(() => dateItems.value.map((item) => item.label))

const seriesFromQuarterValues = (quarters: number[]) =>
  dateItems.value.map((item) => {
    const quarterIndex = Math.floor((item.month - 1) / 3)
    return quarters[quarterIndex] ?? 0
  })

const toRgba = (hex: string, alpha: number) => {
  const normalized = hex.replace('#', '').trim()
  if (normalized.length !== 6) return `rgba(0, 0, 0, ${alpha})`
  const r = parseInt(normalized.slice(0, 2), 16)
  const g = parseInt(normalized.slice(2, 4), 16)
  const b = parseInt(normalized.slice(4, 6), 16)
  return `rgba(${r}, ${g}, ${b}, ${alpha})`
}

const rankSeries = [
  {
    rank: TypeRank.A,
    label: 'Rank A',
    color: rankPalette[TypeRank.A],
    fill: toRgba(rankPalette[TypeRank.A], 0.15),
  },
  {
    rank: TypeRank.B,
    label: 'Rank B',
    color: rankPalette[TypeRank.B],
    fill: toRgba(rankPalette[TypeRank.B], 0.15),
  },
  {
    rank: TypeRank.C,
    label: 'Rank C',
    color: rankPalette[TypeRank.C],
    fill: toRgba(rankPalette[TypeRank.C], 0.15),
  },
  {
    rank: TypeRank.D,
    label: 'Rank D',
    color: rankPalette[TypeRank.D],
    fill: toRgba(rankPalette[TypeRank.D], 0.15),
  },
  {
    rank: TypeRank.E,
    label: 'Rank E',
    color: rankPalette[TypeRank.E],
    fill: toRgba(rankPalette[TypeRank.E], 0.15),
  },
  {
    rank: TypeRank.X,
    label: 'Rank X',
    color: rankPalette[TypeRank.X],
    fill: toRgba(rankPalette[TypeRank.X], 0.15),
  },
]

const summariesByRank = computed(() => {
  const map = new Map<number, Map<string, number>>()
  summaryStore.summaries_amount_year.forEach((item) => {
    const rankMap = map.get(item.rank) ?? new Map<string, number>()
    const amount = chartFilterStore.amountMode === 'expected' ? item.all_expected : item.all_order
    rankMap.set(item.date_snap, amount)
    map.set(item.rank, rankMap)
  })
  return map
})

const seriesFromSnapshots = (rank: number) => {
  const rankMap = summariesByRank.value.get(rank)
  let lastValue = 0
  return dateItems.value.map((item) => {
    const value = rankMap?.get(item.label)
    if (typeof value === 'number') {
      lastValue = value
    }
    return lastValue
  })
}

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
  labels: labels.value,
  datasets: [
    ...rankSeries.map((series) => {
      return {
        label: series.label,
        data: seriesFromSnapshots(series.rank),
        borderColor: series.color,
        backgroundColor: series.fill,
        tension: 0.2,
        pointRadius: 0,
        fill: false,
        stepped: true,
      }
    }),
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
  animation: {
    duration: 1000,
    easing: 'easeOutQuart',
  },
  interaction: {
    mode: 'index',
    intersect: false,
  },
  plugins: {
    legend: {
      position: 'top',
      labels: {
        color: '#d8d8d8',
        font: {
          size: 11,
        },
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
        font: {
          size: 10,
        },
      },
      grid: {
        color: 'rgba(255, 255, 255, 0.06)',
      },
    },
    y: {
      ticks: {
        color: '#9c9c9c',
        font: {
          size: 10,
        },
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
    <v-card-title class="text-subtitle-2 font-weight-medium">
      Progress
      <v-btn-toggle v-model="chartFilterStore.amountMode" mandatory density="compact" class="ml-4">
        <v-btn value="order" size="small">ORDER</v-btn>
        <v-btn value="expected" size="small">EXPECTED</v-btn>
      </v-btn-toggle>
    </v-card-title>

    <v-card-text class="pa-4">
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
  height: clamp(260px, 60vh, 560px);
}
</style>
