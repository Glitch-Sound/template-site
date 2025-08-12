<script setup lang="ts">
import { useRoute } from 'vue-router'

import LoginUser from '@/components/common/LoginUser.vue'

const route = useRoute()
</script>

<template>
  <v-app-bar>
    <template #image>
      <v-img gradient="to top, rgba(0, 0, 0, 0), rgba(29, 35, 46, 0.4), rgba(106, 113, 124, 0.7)" />
    </template>

    <v-app-bar-title style="cursor: pointer">
      <div class="d-flex align-center">
        <v-icon color="primary">mdi-grain</v-icon>
        <span class="ml-2"> muu </span>
      </div>
    </v-app-bar-title>

    <v-btn icon to="/" :color="route.path === '/' ? 'primary' : 'icon'">
      <v-icon>mdi-home</v-icon>
    </v-btn>

    <v-btn icon to="/project" :color="route.path === '/project' ? 'primary' : 'icon'">
      <v-icon>mdi-view-list</v-icon>
    </v-btn>

    <v-btn icon variant="text" to="/viz" :color="route.path === '/viz' ? 'primary' : 'icon'">
      <v-icon>mdi-chart-scatter-plot-hexbin</v-icon>
    </v-btn>

    <v-spacer />

    <div class="mr-2">
      <LoginUser />
    </div>

    <v-btn icon to="/setting/main" :color="route.path.startsWith('/setting') ? 'primary' : 'icon'">
      <v-icon>mdi-cog</v-icon>
    </v-btn>
  </v-app-bar>
</template>

<style scoped>
@import '@/assets/main.css';
</style>
