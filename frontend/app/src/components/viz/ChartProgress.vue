<script setup lang="ts">
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

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend)

const year = new Date().getFullYear()

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

const seriesFromFormula = (base: number, slope: number, amplitude: number, phase = 0) =>
  dateItems.map((item) =>
    Math.round(base + slope * item.index + amplitude * Math.sin((item.index + phase) / 18)),
  )

const quarterTargets = [2500000, 3000000, 2800000, 3200000]
const quarterTargetSeries = dateItems.map((item) => {
  const quarterIndex = Math.floor((item.month - 1) / 3)
  return quarterTargets[quarterIndex]
})

const chartData = {
  labels,
  datasets: [
    {
      label: 'Rank A',
      data: seriesFromFormula(900000, 480, 80000, 0),
      borderColor: '#5fa7c8',
      backgroundColor: 'rgba(95, 167, 200, 0.15)',
      tension: 0.3,
      pointRadius: 0,
      fill: false,
    },
    {
      label: 'Rank B',
      data: seriesFromFormula(760000, 430, 72000, 6),
      borderColor: '#6bb48e',
      backgroundColor: 'rgba(107, 180, 142, 0.15)',
      tension: 0.3,
      pointRadius: 0,
      fill: false,
    },
    {
      label: 'Rank C',
      data: seriesFromFormula(620000, 380, 65000, 12),
      borderColor: '#b3a45a',
      backgroundColor: 'rgba(179, 164, 90, 0.15)',
      tension: 0.3,
      pointRadius: 0,
      fill: false,
    },
    {
      label: 'Rank D',
      data: seriesFromFormula(480000, 320, 54000, 18),
      borderColor: '#a06b6b',
      backgroundColor: 'rgba(160, 107, 107, 0.15)',
      tension: 0.3,
      pointRadius: 0,
      fill: false,
    },
    {
      label: 'Rank E',
      data: seriesFromFormula(360000, 260, 42000, 24),
      borderColor: '#8a8a8a',
      backgroundColor: 'rgba(138, 138, 138, 0.15)',
      tension: 0.3,
      pointRadius: 0,
      fill: false,
    },
    {
      label: 'Quarter Target',
      data: quarterTargetSeries,
      borderColor: 'rgba(255, 255, 255, 0.45)',
      borderDash: [6, 6],
      borderWidth: 2,
      pointRadius: 0,
      stepped: true,
    },
  ],
}

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
