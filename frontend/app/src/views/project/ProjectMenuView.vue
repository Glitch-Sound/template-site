<script setup lang="ts">
import { ref } from 'vue'

import type { TargetQuarter } from '@/types/Project'
import ProjectEvent from '@/views/project/ProjectEvent'
import QuarterFilter from '@/components/common/QuarterFilter.vue'
import UserFilter from '@/components/common/UserFilter.vue'

const filter_quarters = ref<TargetQuarter[]>([])
const filter_users_pm = ref<number[]>([])
const filter_users_pl = ref<number[]>([])
const filter_none_pre_approval = ref(false)
const filter_none_number_m = ref(false)
const filter_none_number_s = ref(false)
const filter_none_number_o = ref(false)

const handleAddProject = () => {
  ProjectEvent.emit('openCreateProjectDialog')
}

const handleFilter = () => {
  console.log(filter_quarters.value)
  console.log(filter_users_pm.value)
  console.log(filter_users_pl.value)
  console.log(filter_none_pre_approval.value)
  console.log(filter_none_number_m.value)
  console.log(filter_none_number_s.value)
  console.log(filter_none_number_o.value)
}
</script>

<template>
  <v-navigation-drawer class="no-border" color="background">
    <v-sheet class="navigation">
      <v-list-item class="mb-2">
        <v-btn
          width="250px"
          color="#940000"
          prepend-icon="mdi-plus-circle"
          @click="handleAddProject"
        >
          Project
        </v-btn>
      </v-list-item>

      <v-list-item>
        <QuarterFilter v-model="filter_quarters" />
      </v-list-item>

      <v-list-item>
        <UserFilter v-model="filter_users_pm" label="PM" />
      </v-list-item>

      <v-list-item>
        <UserFilter v-model="filter_users_pl" label="PL" />
      </v-list-item>

      <v-list-item>
        <v-checkbox v-model="filter_none_pre_approval" hide-details label="None Pre-Approval" />
        <v-checkbox v-model="filter_none_number_m" hide-details label="None Number M" />
        <v-checkbox v-model="filter_none_number_s" hide-details label="None Number S" />
        <v-checkbox v-model="filter_none_number_o" hide-details label="None Number Official" />
      </v-list-item>

      <v-list-item>
        <v-btn width="250px" color="#282B31" prepend-icon="mdi-tune-variant" @click="handleFilter">
          Filter
        </v-btn>
      </v-list-item>
    </v-sheet>
  </v-navigation-drawer>
</template>

<style scoped>
@import '@/assets/main.css';
</style>
