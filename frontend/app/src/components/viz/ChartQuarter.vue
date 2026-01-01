<script setup lang="ts">
const quarters = [
  { title: '1Q', achieved: 2150000, target: 3000000 },
  { title: '2Q', achieved: 2550000, target: 3000000 },
  { title: '3Q', achieved: 1900000, target: 3000000 },
  { title: '4Q', achieved: 2150000, target: 3000000 },
]

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
</script>

<template>
  <v-card class="quarter-card" rounded="xl" variant="tonal">
    <v-card-title class="text-h6 font-weight-medium">Quarter</v-card-title>

    <v-card-text class="pa-6">
      <div class="quarter-row">
        <div v-for="quarter in quarters" :key="quarter.title" class="quarter-item">
          <div class="quarter-title text-caption text-medium-emphasis">
            {{ quarter.title }}
          </div>

          <div class="quarter-body">
            <v-progress-circular
              :model-value="progressFor(quarter.achieved, quarter.target)"
              size="80"
              width="3"
              color="primary"
              bg-color="grey-darken-4"
              class="progress"
            >
              <span class="progress-label">
                {{ progressFor(quarter.achieved, quarter.target) }}%
              </span>
            </v-progress-circular>

            <div class="amount-stack">
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
  gap: 24px;
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
  font-size: 1rem;
  width: 80px;
  text-align: center;
}

.quarter-body {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 16px;
}

.progress {
  font-weight: 600;
}

.progress-label {
  font-size: 1rem;
}

.amount-display {
  display: flex;
  align-items: baseline;
  gap: 8px;
}

.amount-stack {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  text-align: left;
  justify-content: center;
  min-height: 80px;
}

.amount-achieved {
  font-size: 1.25rem;
  font-weight: 700;
}

.amount-divider {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.5);
}

.amount-target {
  font-size: 0.9rem;
  opacity: 0.8;
}

.amount-diff {
  font-size: 0.85rem;
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
