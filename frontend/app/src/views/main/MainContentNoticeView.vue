<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useSummaryStore } from '@/stores/SummaryStore'
import UserLabel from '@/components/common/UserLabel.vue'

const summaryStore = useSummaryStore()

onMounted(async () => {
  await summaryStore.fetchSummariesIncomplete()
})

const incompleteProjects = computed(() => summaryStore.summaries_incomplete.slice(0, 12))
</script>

<template>
  <v-card class="top-card main-card" elevation="2">
    <v-card-text class="main-content">
      <span class="main-status">Incomplete</span>
      <v-icon class="main-icon" size="82"> mdi-alert-outline </v-icon>
      <div class="main-text">
        <div v-for="project in incompleteProjects" :key="project.rid" class="deadline-row">
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
  color: #f9a825;
}

.main-icon {
  color: #f9a825;
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
