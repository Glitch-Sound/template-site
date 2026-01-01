<script setup lang="ts"></script>

<template>
  <v-card class="bottom-card" elevation="3" prepend-icon="mdi-apps">
    <template v-slot:title>
      <span class="font-weight-black">Rule</span>
    </template>

    <v-card-text class="note pa-4 pl-6">
      xxx<br />
      xxx<br />
      xxx<br />
      xxx<br />
    </v-card-text>
  </v-card>
</template>

<style scoped>
@import '@/assets/main.css';

.bottom-card {
  width: min(1750px, 100%);
  height: 650px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  text-align: left;
}

.note {
  background-color: #0c0c0c;
  text-align: left;
  width: 100%;
}
</style>
