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
  <v-main>
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
        <v-col cols="12" sm="6" md="3" class="card-col">
          <MainContentInformationView />
        </v-col>
        <v-col cols="12" sm="6" md="3" class="card-col mx-8">
          <MainContentNoticeView />
        </v-col>
        <v-col cols="12" sm="6" md="3" class="card-col">
          <MainContentWarningView />
        </v-col>
      </v-row>
      <v-row class="bottom-row" justify="center">
        <v-col cols="12" md="10" class="card-col">
          <MainContentNoteView />
        </v-col>
      </v-row>
    </v-container>
    <div v-else class="ghost-container">
      <v-icon icon="mdi-ghost" size="1100" class="icon" />
    </div>
  </v-main>
</template>

<style scoped>
@import '@/assets/main.css';

.cards-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 64px;
  position: relative;
}

.top-row,
.bottom-row {
  width: 100%;
}

.card-col {
  display: flex;
  justify-content: center;
}

.ghost-container {
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon {
  color: #3f3f3f;
  opacity: 0.4;
}
</style>
