<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { Chart } from 'vue-chartjs'
import { Chart as ChartJS, Tooltip, Legend } from 'chart.js'
import { SankeyController, Flow } from 'chartjs-chart-sankey'
import { chartPalette } from '@/constants/chartPalette'
import { useSummaryStore } from '@/stores/SummaryStore'

ChartJS.register(SankeyController, Flow, Tooltip, Legend)

const summaryStore = useSummaryStore()
const primaryColor = ref('#2196f3')

onMounted(async () => {
  await summaryStore.fetchSummariesSankey()
  const primary = getComputedStyle(document.documentElement)
    .getPropertyValue('--v-theme-primary')
    .trim()
  if (primary) {
    primaryColor.value = primary.includes(',') ? `rgb(${primary})` : primary
  }
})

const sankeySummary = computed(() => summaryStore.summaries_sankey)

const currencyFormatter = new Intl.NumberFormat('ja-JP', {
  style: 'currency',
  currency: 'JPY',
  maximumFractionDigits: 0,
})

const rootLabel = computed(() => {
  const year = sankeySummary.value?.year
  return year ? `Total ${year}` : 'Total'
})

const companyLabel = (name: string, rid: number) => `Company: ${name} (${rid || 0})`
const pmLabel = (name: string, rid: number) => `PM: ${name || 'Unknown'} (${rid || 0})`
const plLabel = (name: string, rid: number) => `PL: ${name || 'Unknown'} (${rid || 0})`

const colorForCompany = (rid: number) => {
  const index = Math.abs(rid) % chartPalette.length
  return chartPalette[index] ?? '#9c9c9c'
}

const colorForPerson = (rid: number) => {
  if (!rid) return '#7a7a7a'
  const hue = (Math.abs(rid) * 137.508) % 360
  return `hsl(${hue}, 55%, 55%)`
}

const nodeColors = computed(() => {
  const map = new Map<string, string>()
  const summary = sankeySummary.value
  map.set(rootLabel.value, primaryColor.value)
  if (!summary) return map

  summary.companies.forEach((company) => {
    map.set(companyLabel(company.name, company.rid), colorForCompany(company.rid))
  })

  summary.company_pm.forEach((item) => {
    map.set(pmLabel(item.pm_name, item.pm_rid), colorForPerson(item.pm_rid))
  })

  summary.pm_pl.forEach((item) => {
    map.set(plLabel(item.pl_name, item.pl_rid), colorForPerson(item.pl_rid))
  })

  return map
})

const chartLinks = computed(() => {
  const summary = sankeySummary.value
  if (!summary) return []

  const links: Array<{ from: string; to: string; flow: number }> = []
  const root = rootLabel.value

  summary.companies.forEach((company) => {
    if (!company.amount) return
    links.push({
      from: root,
      to: companyLabel(company.name, company.rid),
      flow: company.amount,
    })
  })

  summary.company_pm.forEach((item) => {
    if (!item.amount) return
    links.push({
      from: companyLabel(item.company_name, item.company_rid),
      to: pmLabel(item.pm_name, item.pm_rid),
      flow: item.amount,
    })
  })

  summary.pm_pl.forEach((item) => {
    if (!item.amount) return
    links.push({
      from: pmLabel(item.pm_name, item.pm_rid),
      to: plLabel(item.pl_name, item.pl_rid),
      flow: item.amount,
    })
  })

  return links
})

const chartData = computed(() => ({
  datasets: [
    {
      label: 'Sankey',
      data: chartLinks.value,
      colorFrom: (context: { raw?: { from?: string } }) =>
        (context.raw?.from ? nodeColors.value.get(context.raw.from) : null) ?? '#888888',
      colorTo: (context: { raw?: { to?: string } }) =>
        (context.raw?.to ? nodeColors.value.get(context.raw.to) : null) ?? '#888888',
      colorMode: 'gradient',
      borderWidth: 0,
    },
  ],
}))

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  animation: {
    duration: 900,
    easing: 'easeOutQuart',
  },
  plugins: {
    legend: {
      display: false,
    },
    tooltip: {
      callbacks: {
        label: (context: { raw?: { from?: string; to?: string; flow?: number } }) => {
          const raw = context.raw
          if (!raw || typeof raw.flow !== 'number') return ''
          return `${raw.from ?? ''} → ${raw.to ?? ''}: ${currencyFormatter.format(raw.flow)}`
        },
      },
    },
  },
}))

const totalAmountText = computed(() => {
  const total = sankeySummary.value?.total_amount ?? 0
  return currencyFormatter.format(total)
})
</script>

<template>
  <v-card class="viz-card viz-card--tall company-card sankey-card" rounded="xl" variant="tonal">
    <v-card-title class="text-subtitle-2 font-weight-medium"> Results </v-card-title>

    <v-card-text class="pa-3 viz-card-text sankey-body">
      <div class="sankey-header">
        <div class="text-caption text-medium-emphasis">Sales Total</div>
        <div class="sankey-total">{{ totalAmountText }}</div>
      </div>
      <div class="sankey-wrap">
        <Chart v-if="chartLinks.length" type="sankey" :data="chartData" :options="chartOptions" />
        <div v-else class="sankey-empty text-caption text-medium-emphasis">No data</div>
      </div>
    </v-card-text>
  </v-card>
</template>

<style scoped>
@import './viz.css';

.sankey-card {
  height: 100%;
}

.sankey-body {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.sankey-header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 12px;
}

.sankey-total {
  font-size: 18px;
  font-weight: 600;
}

.sankey-wrap {
  position: relative;
  width: 100%;
  flex: 1;
  min-height: 0;
}

.sankey-empty {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
