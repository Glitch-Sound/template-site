<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { useRoute } from 'vue-router'
import { storeToRefs } from 'pinia'

import { useUserStore } from '@/stores/UserStore'
import { useProjectStore } from '@/stores/ProjectStore'
import { TypePost } from '@/types/User'

const route = useRoute()

const draft_user = ref<number | null>(null)
const is_filter_open = ref(false)

const is_report_view = computed(() => route.path === '/viz/report')

const store_user = useUserStore()
const store_project = useProjectStore()
const { users, is_loading } = storeToRefs(store_user)
const { report_user_rid } = storeToRefs(store_project)
const { fetchUsers } = store_user
const { setReportUser } = store_project

const filtered_users = computed(() => users.value.filter((user) => user.post !== TypePost.NONE))

watch(is_filter_open, async (is_open) => {
  if (is_open) {
    draft_user.value = report_user_rid.value
    await fetchUsers()
  }
})

const handleApplyFilter = () => {
  setReportUser(draft_user.value ?? null)
  is_filter_open.value = false
}
</script>

<template>
  <v-navigation-drawer class="no-border" color="background">
    <v-sheet class="navigation">
      <v-list-item>
        <router-link to="/viz/main" class="link--normal" active-class="link--active">
          <v-icon icon="mdi-chart-scatter-plot-hexbin" />
          Main
        </router-link>
      </v-list-item>

      <v-list-item>
        <div class="menu-row">
          <router-link to="/viz/report" class="link--normal" active-class="link--active">
            <v-icon icon="mdi-file-document-outline" />
            Report
          </router-link>
          <v-menu
            v-model="is_filter_open"
            location="end"
            :close-on-content-click="false"
            :disabled="!is_report_view"
          >
            <template #activator="{ props }">
              <v-btn
                icon="mdi-filter-variant"
                variant="text"
                size="small"
                class="filter-button"
                :disabled="!is_report_view"
                v-bind="props"
              />
            </template>
            <v-card class="filter-card">
              <v-card-title class="filter-title">Filter</v-card-title>
              <v-card-text>
                <v-radio-group v-model="draft_user" :disabled="is_loading">
                  <v-radio
                    v-for="user in filtered_users"
                    :key="user.rid"
                    :label="user.name"
                    :value="user.rid"
                    color="primary"
                  />
                </v-radio-group>
              </v-card-text>
              <v-card-actions class="filter-actions">
                <v-btn color="primary" variant="flat" @click="handleApplyFilter">Apply</v-btn>
              </v-card-actions>
            </v-card>
          </v-menu>
        </div>
      </v-list-item>
    </v-sheet>
  </v-navigation-drawer>
</template>

<style scoped>

.v-icon {
  margin: 0 15px 0 0;
}

.menu-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.filter-button {
  color: #9f9f9f;
}

.filter-card {
  min-width: 260px;
  padding: 6px 8px 10px;
}

.filter-title {
  font-size: 14px;
  letter-spacing: 0.5px;
}

.filter-actions {
  justify-content: flex-end;
  padding: 0 12px 10px;
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
