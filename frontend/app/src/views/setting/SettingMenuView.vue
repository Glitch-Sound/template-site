<script setup lang="ts"></script>

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
