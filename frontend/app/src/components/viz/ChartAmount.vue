<script setup lang="ts">
import { computed } from 'vue'

const amount = {
  total: {
    achieved: 8750000,
    target: 12000000,
  },
  halves: [
    { title: 'First half', achieved: 4700000, target: 6000000 },
    { title: 'Second half', achieved: 4050000, target: 6000000 },
  ],
}

const totalProgress = computed(() => {
  if (!amount.total.target) return 0
  return Math.min(
    100,
    Math.round((amount.total.achieved / amount.total.target) * 100),
  )
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
</script>

<template>
  <v-card class="amount-card" rounded="xl" variant="tonal">
    <v-card-title class="text-h6 font-weight-medium">Amount</v-card-title>

    <v-card-text class="pa-6">
      <div class="top-row">
        <div class="progress-wrapper">
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
          <div class="total-label text-caption text-medium-emphasis">Total</div>
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
}

.progress-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
}

.progress {
  font-weight: 600;
}

.progress-label {
  font-size: 1.25rem;
}

.total-amount {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-width: 200px;
}

.total-label {
  letter-spacing: 0.08em;
  text-transform: uppercase;
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
