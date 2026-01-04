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
  <v-card class="top-card main-card status-amber" elevation="2">
    <v-card-text class="main-content">
      <span class="main-status">Incomplete</span>
      <v-icon class="main-icon" size="82"> mdi-alert-outline </v-icon>
      <div class="main-text">
        <div v-for="project in incompleteProjects" :key="project.rid" class="deadline-row">
          <span class="project-name">{{ project.name }}</span>
          <UserLabel :user="project.user_pl" class="user-label" />
        </div>
      </div>
    </v-card-text>
  </v-card>
</template>

<style scoped>
@import '@/views/main/main.css';
</style>
