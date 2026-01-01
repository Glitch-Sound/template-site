<script setup lang="ts">
import MainContentInformationView from '@/views/main/MainContentInformationView.vue'
import MainContentNoticeView from '@/views/main/MainContentNoticeView.vue'
import MainContentWarningView from '@/views/main/MainContentWarningView.vue'
import MainContentNoteView from '@/views/main/MainContentNoteView.vue'
</script>

<template>
  <v-main>
    <v-container class="cards-container" fluid>
      <v-row class="top-row" justify="center" align="stretch">
        <v-col cols="12" sm="6" md="3" class="card-col">
          <MainContentInformationView />
        </v-col>
        <v-col cols="12" sm="6" md="3" class="card-col">
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
  </v-main>
</template>

<style scoped>
@import '@/assets/main.css';

.cards-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 48px;
}

.top-row,
.bottom-row {
  width: 100%;
}

.card-col {
  display: flex;
  justify-content: center;
}
</style>
