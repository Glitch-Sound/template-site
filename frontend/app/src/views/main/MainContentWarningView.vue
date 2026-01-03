<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useSummaryStore } from '@/stores/SummaryStore'
import UserLabel from '@/components/common/UserLabel.vue'

const summaryStore = useSummaryStore()

onMounted(async () => {
  await summaryStore.fetchSummariesAlert()
})

const alertProjects = computed(() => summaryStore.summaries_alert.slice(0, 12))
</script>

<template>
  <v-card class="top-card main-card" elevation="2">
    <v-card-text class="main-content">
      <span class="main-status">Alert</span>
      <v-icon class="main-icon" size="82"> mdi-emoticon-devil-outline </v-icon>
      <div class="main-text">
        <div v-for="project in alertProjects" :key="project.rid" class="deadline-row">
          <span class="project-name">{{ project.name }}</span>
          <UserLabel :user="project.user_pl" class="user-label" />
        </div>
      </div>
    </v-card-text>
  </v-card>
</template>

<style scoped>
@import '@/assets/main.css';
@import '@/views/main/main.css';

.main-status {
  color: #c62828;
}

.main-icon {
  color: #c62828;
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

.user-label {
  min-width: 120px;
  text-align: left;
}
</style>
