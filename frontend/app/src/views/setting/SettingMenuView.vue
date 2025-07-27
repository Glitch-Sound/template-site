<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

import SettingEvent from '@/views/setting/SettingEvent'

const route = useRoute()

const is_enable_user = computed(() => route.path === '/setting/user')

const handleAddUser = () => {
  SettingEvent.emit('openCreateUserDialog')
}
</script>

<template>
  <v-navigation-drawer class="no-border" color="background">
    <v-sheet class="navigation">
      <v-list-item>
        <router-link to="/setting/main" class="link--normal" active-class="link--active">
          <v-icon icon="mdi-cog" />
          Main
        </router-link>
      </v-list-item>

      <v-list-item>
        <router-link to="/setting/user" class="link--normal" active-class="link--active">
          <v-icon icon="mdi-account" />
          User
        </router-link>

        <template #append>
          <v-btn
            icon="mdi-plus-circle"
            variant="plain"
            size="x-small"
            @click="handleAddUser"
            :disabled="!is_enable_user"
          />
        </template>
      </v-list-item>

      <v-list-item>
        <router-link to="/setting/project" class="link--normal" active-class="link--active">
          <v-icon icon="mdi-grain" />
          Project
        </router-link>
      </v-list-item>
    </v-sheet>
  </v-navigation-drawer>
</template>

<style scoped>
@import '@/assets/main.css';

.v-icon {
  margin: 0 15px 0 0;
}

.link--normal {
  color: #9f9f9f;
  text-decoration: none;
}

.link--active {
  color: #fcfcfc;
  text-decoration: none;
}
</style>
