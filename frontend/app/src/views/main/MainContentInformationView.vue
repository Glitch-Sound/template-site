<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useSummaryStore } from '@/stores/SummaryStore'
import UserLabel from '@/components/common/UserLabel.vue'

const summaryStore = useSummaryStore()

onMounted(async () => {
  await summaryStore.fetchSummariesDeadline()
})

const deadlineProjects = computed(() => summaryStore.summaries_deadline.slice(0, 6))
</script>

<template>
  <v-card class="top-card main-card" elevation="2">
    <v-card-text class="main-content">
      <span class="main-status">Deadline</span>
      <v-icon class="main-icon" size="82"> mdi-information-outline </v-icon>
      <div class="main-text">
        <div v-for="project in deadlineProjects" :key="project.rid" class="deadline-row">
          <span class="project-name">{{ project.name }}</span>
          <UserLabel :user="project.user_pl" />
        </div>
      </div>
    </v-card-text>
  </v-card>
</template>

<style scoped>
@import '@/assets/main.css';
@import '@/views/main/main.css';

.main-status {
  color: #2e7d32;
}

.main-icon {
  color: #2e7d32;
}

.main-text {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.deadline-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.project-name {
  flex: 1;
  min-width: 0;
}
</style>
