<script setup lang="ts">
import { computed, nextTick } from 'vue'
import { storeToRefs } from 'pinia'

import ProjectEvent from '@/views/project/ProjectEvent'
import QuarterFilter from '@/components/common/QuarterFilter.vue'
import UserFilter from '@/components/common/UserFilter.vue'
import RankFilter from '@/components/common/RankFilter.vue'
import CompanyFilter from '@/components/common/CompanyFilter.vue'
import { useProjectStore } from '@/stores/ProjectStore'
import { useCompanyStore } from '@/stores/CompanyStore'
import { TypePost } from '@/types/User'
import { TypeQuarter } from '@/types/Project'

const store = useProjectStore()
const store_company = useCompanyStore()
const { condition, project_targets, project_users } = storeToRefs(store)
const { companies } = storeToRefs(store_company)
const { fetchProjectTargets, fetchProjectUsers, fetchProjects } = store
const { fetchCompanies } = store_company

const selectable_quarters = computed(() =>
  project_targets.value
    .filter((fq) => fq.quarter !== TypeQuarter.NONE)
    .map((fq) => fq.year * 10 + fq.quarter),
)

const selectable_users = computed(() =>
  project_users.value
    .filter((user) => user.post !== TypePost.NONE && user.post !== TypePost.GUEST)
    .map((user) => user.rid),
)

const model_quarters = computed<number[]>({
  get: () => condition.value.target ?? [],
  set: (v) => store.patchCondition({ target: v ?? [] }),
})

const model_users_pm = computed<number[]>({
  get: () => condition.value.rid_users_pm ?? [],
  set: (v) => store.patchCondition({ rid_users_pm: v ?? [] }),
})

const model_users_pl = computed<number[]>({
  get: () => condition.value.rid_users_pl ?? [],
  set: (v) => store.patchCondition({ rid_users_pl: v ?? [] }),
})

const model_companies = computed<number[]>({
  get: () => condition.value.rid_companies ?? [],
  set: (v) => store.patchCondition({ rid_companies: v ?? [] }),
})

const model_ranks = computed<number[]>({
  get: () => condition.value.ranks ?? [],
  set: (v) => store.patchCondition({ ranks: v ?? [] }),
})

const model_none_pre_approval = computed<boolean>({
  get: () => condition.value.is_none_pre_approval ?? false,
  set: (v) => store.patchCondition({ is_none_pre_approval: !!v }),
})

const model_none_number_m = computed<boolean>({
  get: () => condition.value.is_none_number_m ?? false,
  set: (v) => store.patchCondition({ is_none_number_m: !!v }),
})

const model_none_number_s = computed<boolean>({
  get: () => condition.value.is_none_number_s ?? false,
  set: (v) => store.patchCondition({ is_none_number_s: !!v }),
})

const model_none_number_o = computed<boolean>({
  get: () => condition.value.is_none_number_o ?? false,
  set: (v) => store.patchCondition({ is_none_number_o: !!v }),
})

const handleAddProject = () => {
  ProjectEvent.emit('openCreateProjectDialog')
}

const handleFilter = async () => {
  await fetchProjects()
}

const handleClear = async () => {
  await Promise.all([fetchProjectTargets(), fetchProjectUsers(), fetchCompanies()])
  await nextTick()
  model_quarters.value = selectable_quarters.value
  model_companies.value = companies.value.map((company) => company.rid)
  model_users_pm.value = selectable_users.value
  model_users_pl.value = selectable_users.value
  model_ranks.value = store.defaultCondition().ranks ?? []
  model_none_pre_approval.value = false
  model_none_number_m.value = false
  model_none_number_s.value = false
  model_none_number_o.value = false
  await fetchProjects()
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
        <QuarterFilter v-model="model_quarters" />
      </v-list-item>

      <v-list-item>
        <CompanyFilter v-model="model_companies" />
      </v-list-item>

      <v-list-item>
        <RankFilter v-model="model_ranks" />
      </v-list-item>

      <v-list-item>
        <UserFilter v-model="model_users_pm" label="PM" />
      </v-list-item>

      <v-list-item>
        <UserFilter v-model="model_users_pl" label="PL" />
      </v-list-item>

      <v-list-item>
        <v-checkbox v-model="model_none_pre_approval" hide-details label="未設定：承認予定日" />
        <v-checkbox v-model="model_none_number_m" hide-details label="未登録：M番" />
        <v-checkbox v-model="model_none_number_s" hide-details label="未登録：S番" />
        <v-checkbox v-model="model_none_number_o" hide-details label="未登録：正式番号" />
      </v-list-item>

      <v-list-item>
        <v-btn width="250px" color="#282B31" prepend-icon="mdi-tune-variant" @click="handleFilter">
          Filter
        </v-btn>
      </v-list-item>

      <v-list-item>
        <v-btn width="250px" color="#0b0c0e" prepend-icon="mdi-close" @click="handleClear">
          CLEAR
        </v-btn>
      </v-list-item>
    </v-sheet>
  </v-navigation-drawer>
</template>

<style scoped></style>
