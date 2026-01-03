<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/stores/AuthStore'
import { useSummaryStore } from '@/stores/SummaryStore'
import MainContentInformationView from '@/views/main/MainContentInformationView.vue'
import MainContentNoticeView from '@/views/main/MainContentNoticeView.vue'
import MainContentWarningView from '@/views/main/MainContentWarningView.vue'
import MainContentNoteView from '@/views/main/MainContentNoteView.vue'

const authStore = useAuthStore()
const { user_initial } = storeToRefs(authStore)
const summaryStore = useSummaryStore()
const { is_loading_deadline, is_loading_incomplete, is_loading_alert } = storeToRefs(summaryStore)
</script>

<template>
  <v-main class="main-root">
    <v-container v-if="user_initial" class="cards-container" fluid>
      <v-overlay
        :model-value="is_loading_deadline || is_loading_incomplete || is_loading_alert"
        contained
        scrim="transparent"
        class="align-center justify-center"
      >
        <v-progress-circular indeterminate color="primary" />
      </v-overlay>

      <v-row class="top-row" justify="center" align="stretch">
        <v-col cols="12" sm="6" md="4" class="card-col">
          <MainContentInformationView class="card-item" />
        </v-col>
        <v-col cols="12" sm="6" md="4" class="card-col">
          <MainContentNoticeView class="card-item" />
        </v-col>
        <v-col cols="12" sm="6" md="4" class="card-col">
          <MainContentWarningView class="card-item" />
        </v-col>
      </v-row>

      <v-divider class="main-divider" />

      <v-row class="bottom-row" justify="center">
        <v-col class="card-col">
          <MainContentNoteView />
        </v-col>
      </v-row>
    </v-container>
    <div v-else class="ghost-container">
      <v-icon icon="mdi-ghost" size="900" class="ghost-icon" />
    </div>
  </v-main>
</template>

<style scoped>
@import '@/assets/main.css';
@import '@/views/main/main.css';
</style>
