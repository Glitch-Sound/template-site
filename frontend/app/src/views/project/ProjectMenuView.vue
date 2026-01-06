<script setup lang="ts">
import { computed } from 'vue'
import { storeToRefs } from 'pinia'

import ProjectEvent from '@/views/project/ProjectEvent'
import QuarterFilter from '@/components/common/QuarterFilter.vue'
import UserFilter from '@/components/common/UserFilter.vue'
import { useProjectStore } from '@/stores/ProjectStore'

const store = useProjectStore()
const { condition } = storeToRefs(store)

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
  await store.fetchProjects()
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
    </v-sheet>
  </v-navigation-drawer>
</template>

<style scoped></style>
