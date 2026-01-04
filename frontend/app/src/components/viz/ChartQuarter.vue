<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useSummaryStore } from '@/stores/SummaryStore'
import { useTargetStore } from '@/stores/TargetStore'
import { useChartFilterStore } from '@/stores/ChartFilterStore'
import { TypeRank } from '@/types/Project'

const summaryStore = useSummaryStore()
const targetStore = useTargetStore()
const currentYear = new Date().getFullYear()
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
  await Promise.all([summaryStore.fetchSummariesAmountLatest(), targetStore.fetchTargets()])
})

const currentTarget = computed(
  () => targetStore.targets.find((target) => target.year === currentYear) ?? null,
)

const targetByQuarter = computed(() => ({
  q1: currentTarget.value?.quarter1 ?? 0,
  q2: currentTarget.value?.quarter2 ?? 0,
  q3: currentTarget.value?.quarter3 ?? 0,
  q4: currentTarget.value?.quarter4 ?? 0,
}))

const achievedByQuarter = computed(() => {
  const base = { q1: 0, q2: 0, q3: 0, q4: 0 }
  return summaryStore.summaries_amount_latest
    .filter((item) => chartFilterStore.selectedRanks.includes(item.rank))
    .reduce((acc, item) => {
      if (chartFilterStore.amountMode === 'expected') {
        acc.q1 += item.quarter1_expected
        acc.q2 += item.quarter2_expected
        acc.q3 += item.quarter3_expected
        acc.q4 += item.quarter4_expected
      } else {
        acc.q1 += item.quarter1_order
        acc.q2 += item.quarter2_order
        acc.q3 += item.quarter3_order
        acc.q4 += item.quarter4_order
      }
      return acc
    }, base)
})

const quarters = computed(() => [
  { title: '1Q', achieved: achievedByQuarter.value.q1, target: targetByQuarter.value.q1 },
  { title: '2Q', achieved: achievedByQuarter.value.q2, target: targetByQuarter.value.q2 },
  { title: '3Q', achieved: achievedByQuarter.value.q3, target: targetByQuarter.value.q3 },
  { title: '4Q', achieved: achievedByQuarter.value.q4, target: targetByQuarter.value.q4 },
])

const currencyFormatter = new Intl.NumberFormat('ja-JP', {
  style: 'currency',
  currency: 'JPY',
  maximumFractionDigits: 0,
})

const formatCurrency = (value: number) => currencyFormatter.format(value)

const progressFor = (achieved: number, target: number) => {
  if (!target) return 0
  return Math.min(100, Math.round((achieved / target) * 100))
}

const diffValue = (achieved: number, target: number) => achieved - target

const diffClass = (diff: number) =>
  diff >= 0 ? 'amount-diff amount-diff--positive' : 'amount-diff amount-diff--negative'

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
  <v-card class="quarter-card" rounded="xl" variant="tonal">
    <v-card-title class="text-subtitle-2 font-weight-medium">
      Quarter
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

    <v-card-text class="pa-4">
      <div class="quarter-row">
        <div v-for="quarter in quarters" :key="quarter.title" class="quarter-item">
          <div class="quarter-title text-caption text-medium-emphasis">
            {{ quarter.title }}
          </div>

          <div class="quarter-body">
            <v-progress-circular
              :model-value="progressFor(quarter.achieved, quarter.target)"
              size="64"
              width="3"
              color="primary"
              bg-color="grey-darken-4"
              class="progress"
            >
              <span class="progress-label">
                {{ progressFor(quarter.achieved, quarter.target) }}%
              </span>
            </v-progress-circular>

            <div class="amount-stack ml-3">
              <div class="amount-display">
                <div class="amount-achieved">
                  {{ formatCurrency(quarter.achieved) }}
                </div>
                <div class="amount-divider">/</div>
                <div class="amount-target">
                  {{ formatCurrency(quarter.target) }}
                </div>
              </div>
              <div :class="diffClass(diffValue(quarter.achieved, quarter.target))">
                {{ formatCurrency(diffValue(quarter.achieved, quarter.target)) }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </v-card-text>
  </v-card>
</template>

<style scoped>
@import '@/assets/main.css';

.quarter-card {
  background: rgba(4, 4, 4, 0.98);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.quarter-row {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.quarter-item {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
}

.quarter-title {
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-size: 0.85rem;
  width: 72px;
  text-align: center;
}

.quarter-body {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 12px;
}

.progress {
  font-weight: 600;
}

.progress :deep(.v-progress-circular__overlay) {
  transition: stroke-dashoffset 0.6s ease;
}

.progress-label {
  font-size: 0.85rem;
}

.amount-display {
  display: flex;
  align-items: baseline;
  gap: 6px;
}

.amount-stack {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  text-align: left;
  justify-content: center;
  min-height: 64px;
}

.amount-achieved {
  font-size: 1.05rem;
  font-weight: 700;
}

.amount-divider {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.5);
}

.amount-target {
  font-size: 0.8rem;
  opacity: 0.8;
}

.amount-diff {
  font-size: 0.75rem;
  margin-top: 4px;
}

.amount-diff--positive {
  color: #3a8f6b;
}

.amount-diff--negative {
  color: #b24b4b;
}

@media (max-width: 600px) {
  .quarter-row {
    grid-template-columns: 1fr;
  }

  .quarter-body {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
