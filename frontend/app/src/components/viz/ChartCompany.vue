<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { Doughnut } from 'vue-chartjs'
import type { ChartOptions, TooltipItem } from 'chart.js'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import { useSummaryStore } from '@/stores/SummaryStore'
import { useTargetStore } from '@/stores/TargetStore'
import { useChartFilterStore } from '@/stores/ChartFilterStore'
import { chartPalette } from '@/constants/chartPalette'
import { TypeRank } from '@/types/Project'

ChartJS.register(ArcElement, Tooltip, Legend)

const summaryStore = useSummaryStore()
const targetStore = useTargetStore()
const chartFilterStore = useChartFilterStore()
const draftRanks = ref<TypeRank[]>([...chartFilterStore.selectedRanks])
const isRankMenuOpen = ref(false)

const rankOptions = [
  { value: TypeRank.A, label: 'Rank A' },
  { value: TypeRank.B, label: 'Rank B' },
  { value: TypeRank.C, label: 'Rank C' },
  { value: TypeRank.D, label: 'Rank D' },
  { value: TypeRank.E, label: 'Rank E' },
  { value: TypeRank.X, label: 'Rank X' },
]

onMounted(async () => {
  await targetStore.fetchTargets()
  await summaryStore.fetchSummariesCompanyLatest()
})

const companyTotals = computed(() => {
  const map = new Map<number, { rid: number; name: string; value: number }>()
  summaryStore.summaries_company_latest
    .filter((item) => chartFilterStore.selectedRanks.includes(item.rank))
    .forEach((item) => {
      const rid = item.company?.rid ?? item.rid
      const name = item.company?.name ?? 'Unknown'
      const existing = map.get(rid)
      const amount = chartFilterStore.amountMode === 'expected' ? item.all_expected : item.all_order
      if (existing) {
        existing.value += amount
      } else {
        map.set(rid, { rid, name, value: amount })
      }
    })
  return Array.from(map.values())
})

const chartData = computed(() => ({
  labels: companyTotals.value.map((item) => item.name),
  datasets: [
    {
      data: companyTotals.value.map((item) => item.value),
      backgroundColor: companyTotals.value.map((item) => {
        const rid = item.rid ?? 0
        const index = Math.abs(rid) % chartPalette.length
        return chartPalette[index]
      }),
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
  cutout: '90%',
  animation: {
    duration: 900,
    easing: 'easeOutQuart',
  },
  layout: {
    padding: 0,
  },
  plugins: {
    legend: {
      position: 'right',
      labels: {
        color: '#d8d8d8',
        boxWidth: 16,
        boxHeight: 10,
        padding: 15,
        font: {
          size: 11,
        },
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

const applyRanks = () => {
  chartFilterStore.selectedRanks = [...draftRanks.value]
  isRankMenuOpen.value = false
}

watch(isRankMenuOpen, (isOpen) => {
  if (isOpen) {
    draftRanks.value = [...chartFilterStore.selectedRanks]
  }
})
</script>

<template>
  <v-card class="company-card" rounded="xl" variant="tonal">
    <v-card-title class="text-subtitle-2 font-weight-medium">
      Company
      <v-menu v-model="isRankMenuOpen" location="bottom end" :close-on-content-click="false">
        <template #activator="{ props }">
          <v-btn
            v-bind="props"
            icon="mdi-filter-variant"
            variant="text"
            density="comfortable"
            class="ml-2"
            aria-label="Rank filter"
          />
        </template>
        <v-list min-width="220">
          <v-list-item v-for="rank in rankOptions" :key="rank.value">
            <v-checkbox
              v-model="draftRanks"
              :value="rank.value"
              :label="rank.label"
              density="compact"
              hide-details
            />
          </v-list-item>
          <v-list-item>
            <div class="d-flex justify-end w-100">
              <v-btn size="small" color="primary" variant="flat" @click="applyRanks"> Apply </v-btn>
            </div>
          </v-list-item>
        </v-list>
      </v-menu>
      <v-btn-toggle v-model="chartFilterStore.amountMode" mandatory density="compact" class="ml-4">
        <v-btn value="order" size="small">ORDER</v-btn>
        <v-btn value="expected" size="small">EXPECTED</v-btn>
      </v-btn-toggle>
    </v-card-title>

    <v-card-text class="pa-3">
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
  height: 180px;
}
</style>
