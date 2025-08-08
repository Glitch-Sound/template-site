<script setup lang="ts">
import { computed } from 'vue'

import { TypeRank } from '@/types/Project'
import type { User } from '@/types/User'
import type { ProjectCreate, ProjectGroup } from '@/types/Project'
import { useFormDialog } from '@/components/dialog/BaseDialog'
import ProjectGroupSelect from '@/components/common/ProjectGroupSelect.vue'
import UserSelect from '@/components/common/UserSelect.vue'
import RankSelect from '@/components/common/RankSelect.vue'

const emit = defineEmits(['submit'])
const { dialog, valid, form_data, form_ref, rules, onSubmit } = useFormDialog<ProjectCreate>(emit)

defineExpose({
  open() {
    dialog.value = true
    form_data.value = {
      rid_project_groups: 0,
      rid_users_pm: 0,
      rid_users_pl: 0,
      rank: TypeRank.NONE,
      pre_approval: '',
      name: '',
      number_parent: '',
      amount_expected: 0,
      amount_order: 0,
      date_start: '',
      date_delivery: '',
      date_end: '',
    }
  },
  close() {
    dialog.value = false
  },
})

const canSubmit = computed(
  () =>
    form_data.value.rid_project_groups !== 0 &&
    form_data.value.rid_users_pm !== 0 &&
    form_data.value.rid_users_pl !== 0 &&
    form_data.value.rank !== TypeRank.NONE &&
    form_data.value.name !== '',
)

const handleProjectGroupSelected = (project_group: ProjectGroup) => {
  form_data.value.rid_project_groups = project_group.rid
}

const handleUserPMSelected = (user: User) => {
  form_data.value.rid_users_pm = user.rid
}

const handleUserPLSelected = (user: User) => {
  form_data.value.rid_users_pl = user.rid
}

const handleRankSelected = (rank: number) => {
  form_data.value.rank = rank
}
</script>

<template>
  <v-dialog v-model="dialog" max-width="600px">
    <v-card>
      <v-card-title>
        <span class="dialog-title">Add Project</span>
      </v-card-title>

      <v-card-text>
        <v-form ref="form_ref" v-model="valid" lazy-validation>
          <ProjectGroupSelect
            v-model="form_data.rid_project_groups"
            @itemSelected="handleProjectGroupSelected"
          />

          <UserSelect
            v-model="form_data.rid_users_pm"
            label="PM"
            @itemSelected="handleUserPMSelected"
          />

          <UserSelect
            v-model="form_data.rid_users_pl"
            label="PL"
            @itemSelected="handleUserPLSelected"
          />

          <RankSelect v-model="form_data.rank" @itemSelected="handleRankSelected" />

          <v-text-field v-model="form_data.pre_approval" label="Pre-Approval" type="date" />

          <v-text-field v-model="form_data.name" :rules="[rules.text]" label="Name" />

          <v-text-field
            v-model="form_data.number_parent"
            :rules="[rules.text]"
            label="Number Parent"
          />

          <v-text-field
            v-model="form_data.amount_expected"
            :rules="[rules.numeric]"
            label="Amount Expected"
          />

          <v-text-field
            v-model="form_data.amount_order"
            :rules="[rules.numeric]"
            label="Amount Order"
          />

          <v-text-field v-model="form_data.date_start" label="Date Start" type="date" />
          <v-text-field v-model="form_data.date_delivery" label="Date Delivery" type="date" />
          <v-text-field v-model="form_data.date_end" label="Date End" type="date" />
        </v-form>
      </v-card-text>

      <v-card-actions>
        <v-spacer />
        <v-btn @click="dialog = false">Cancel</v-btn>
        <v-btn color="primary" :disabled="!canSubmit" @click="onSubmit">Submit</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped>
@import '@/assets/main.css';
</style>
