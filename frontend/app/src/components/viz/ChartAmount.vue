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
]

onMounted(async () => {
  await Promise.all([summaryStore.fetchSummariesAmountLatest(), targetStore.fetchTargets()])
})

const currentTarget = computed(
  () => targetStore.targets.find((target) => target.year === currentYear) ?? null,
)

const targetTotals = computed(() => {
  if (!currentTarget.value) return { total: 0, firstHalf: 0, secondHalf: 0 }
  const { quarter1, quarter2, quarter3, quarter4 } = currentTarget.value
  return {
    total: quarter1 + quarter2 + quarter3 + quarter4,
    firstHalf: quarter1 + quarter2,
    secondHalf: quarter3 + quarter4,
  }
})

const achievedTotals = computed(() => {
  const base = { total: 0, firstHalf: 0, secondHalf: 0 }
  return summaryStore.summaries_amount_latest
    .filter((item) => chartFilterStore.selectedRanks.includes(item.rank))
    .reduce((acc, item) => {
      if (chartFilterStore.amountMode === 'expected') {
        acc.total += item.all_expected
        acc.firstHalf += item.half_first_expected
        acc.secondHalf += item.half_second_expected
      } else {
        acc.total += item.all_order
        acc.firstHalf += item.half_first_order
        acc.secondHalf += item.half_second_order
      }
      return acc
    }, base)
})

const amount = computed(() => ({
  total: {
    achieved: achievedTotals.value.total,
    target: targetTotals.value.total,
  },
  halves: [
    {
      title: 'First half',
      achieved: achievedTotals.value.firstHalf,
      target: targetTotals.value.firstHalf,
    },
    {
      title: 'Second half',
      achieved: achievedTotals.value.secondHalf,
      target: targetTotals.value.secondHalf,
    },
  ],
}))

const totalProgress = computed(() => {
  if (!amount.value.total.target) return 0
  return Math.min(100, Math.round((amount.value.total.achieved / amount.value.total.target) * 100))
})

const currencyFormatter = new Intl.NumberFormat('ja-JP', {
  style: 'currency',
  currency: 'JPY',
  maximumFractionDigits: 0,
})

const formatCurrency = (value: number) => currencyFormatter.format(value)

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
  <v-card class="amount-card" rounded="xl" variant="tonal">
    <v-card-title class="text-h6 font-weight-medium">
      Amount
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
            <v-btn size="small" color="primary" variant="flat" @click="applyRanks">
              Apply
            </v-btn>
          </div>
        </v-list-item>
        </v-list>
      </v-menu>
      <v-btn-toggle v-model="chartFilterStore.amountMode" mandatory density="compact" class="ml-4">
        <v-btn value="order">ORDER</v-btn>
        <v-btn value="expected">EXPECTED</v-btn>
      </v-btn-toggle>
    </v-card-title>

    <v-card-text class="pa-6">
      <div class="top-row">
        <div class="total-block">
          <div class="total-label text-caption text-medium-emphasis">Total</div>
          <v-progress-circular
            :model-value="totalProgress"
            size="100"
            width="3"
            color="primary"
            bg-color="grey-darken-4"
            class="progress"
          >
            <span class="progress-label">{{ totalProgress }}%</span>
          </v-progress-circular>
        </div>

        <div class="total-amount">
          <div class="amount-stack">
            <div class="amount-display">
              <div class="amount-achieved">
                {{ formatCurrency(amount.total.achieved) }}
              </div>
              <div class="amount-divider">/</div>
              <div class="amount-target">
                {{ formatCurrency(amount.total.target) }}
              </div>
            </div>
            <div :class="diffClass(diffValue(amount.total.achieved, amount.total.target))">
              {{ formatCurrency(diffValue(amount.total.achieved, amount.total.target)) }}
            </div>
          </div>
        </div>
      </div>

      <v-divider class="my-6" />

      <div class="half-row">
        <div v-for="half in amount.halves" :key="half.title" class="half-card">
          <div class="half-title text-caption text-medium-emphasis">
            {{ half.title }}
          </div>
          <div class="amount-stack">
            <div class="amount-display">
              <div class="amount-achieved">
                {{ formatCurrency(half.achieved) }}
              </div>
              <div class="amount-divider">/</div>
              <div class="amount-target">
                {{ formatCurrency(half.target) }}
              </div>
            </div>
            <div :class="diffClass(diffValue(half.achieved, half.target))">
              {{ formatCurrency(diffValue(half.achieved, half.target)) }}
            </div>
          </div>
        </div>
      </div>
    </v-card-text>
  </v-card>
</template>

<style scoped>
@import '@/assets/main.css';

.amount-card {
  background: rgba(4, 4, 4, 0.98);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.top-row {
  display: flex;
  gap: 32px;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  margin-top: 12px;
}

.total-block {
  position: relative;
  width: 100px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.progress {
  font-weight: 600;
}

.progress :deep(.v-progress-circular__overlay) {
  transition: stroke-dashoffset 0.6s ease;
}

.progress-label {
  font-size: 1.25rem;
}

.total-label {
  position: absolute;
  top: -28px;
  left: 50%;
  transform: translateX(-50%);
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.total-amount {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 8px;
  min-width: 200px;
  align-self: center;
}

.amount-display {
  display: flex;
  align-items: baseline;
  gap: 12px;
}

.amount-stack {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.amount-achieved {
  font-size: clamp(1.5rem, 2.5vw, 2rem);
  font-weight: 700;
}

.amount-divider {
  font-size: 1.5rem;
  color: rgba(255, 255, 255, 0.5);
}

.amount-target {
  font-size: 1.1rem;
  opacity: 0.8;
}

.amount-diff {
  font-size: 0.95rem;
  margin-top: 4px;
  align-self: flex-start;
}

.amount-diff--positive {
  color: #3a8f6b;
}

.amount-diff--negative {
  color: #b24b4b;
}

.half-row {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 24px;
}

.half-card {
  padding: 4px 0;
}

.half-card .amount-achieved {
  font-size: clamp(1.05rem, 1.8vw, 1.4rem);
}

.half-card .amount-divider {
  font-size: 1.05rem;
}

.half-card .amount-target {
  font-size: 0.9rem;
}

.half-card .amount-diff {
  font-size: 0.85rem;
}

.half-title {
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-bottom: 8px;
}

@media (max-width: 600px) {
  .half-row {
    grid-template-columns: 1fr;
  }

  .top-row {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
