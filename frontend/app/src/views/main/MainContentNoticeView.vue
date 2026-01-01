<script setup lang="ts"></script>

<template>
  <v-card class="top-card main-card" elevation="2">
    <v-card-text class="main-content">
      <span class="main-status">Incomplete</span>
      <v-icon class="main-icon" size="82"> mdi-alert-outline </v-icon>
      <p class="main-text">
        xxx<br />
        xxx<br />
        xxx<br />
        xxx<br />
        xxx<br />
      </p>
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
</style>
