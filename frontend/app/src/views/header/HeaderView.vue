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

    <v-app-bar-title>
      <router-link to="/" class="title-link">
        <div class="d-flex align-center">
          <v-icon color="primary">mdi-horse-variant</v-icon>
          <span class="ml-2"> muu </span>
        </div>
      </router-link>
    </v-app-bar-title>

    <v-btn
      icon
      to="/"
      :color="route.path === '/' ? 'primary' : 'icon'"
      class="nav-btn nav-home-btn"
    >
      <div class="nav-btn-inner">
        <v-icon>mdi-home</v-icon>
      </div>
    </v-btn>

    <v-btn
      icon
      to="/project"
      :color="route.path === '/project' ? 'primary' : 'icon'"
      class="nav-btn"
    >
      <div class="nav-btn-inner">
        <v-icon>mdi-view-list</v-icon>
      </div>
    </v-btn>

    <v-btn
      icon
      to="/viz/main"
      :color="route.path.startsWith('/viz') ? 'primary' : 'icon'"
      class="nav-btn"
    >
      <div class="nav-btn-inner">
        <v-icon>mdi-chart-scatter-plot-hexbin</v-icon>
      </div>
    </v-btn>

    <v-spacer />

    <div class="mr-2 login-user-wrapper">
      <LoginUser />
    </div>

    <v-btn icon to="/setting/main" :color="route.path.startsWith('/setting') ? 'primary' : 'icon'">
      <v-icon>mdi-cog</v-icon>
    </v-btn>
  </v-app-bar>
</template>

<style scoped>
.nav-btn {
  height: auto;
}

.nav-btn-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.nav-home-btn {
  margin-left: 240px;
}

.login-user-wrapper {
  width: 200px;
  display: flex;
  justify-content: flex-end;
}

.title-link {
  display: inline-flex;
  align-items: center;
  text-decoration: none;
  color: inherit;
  cursor: pointer;
}
</style>
