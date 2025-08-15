<script setup lang="ts">
import type { ProjectGroup, Project, ProjectUpdate } from '@/types/Project'
import type { User } from '@/types/User'
import { useFormDialog } from '@/components/dialog/BaseDialog'
import DeleteButton from '@/components/common/DeleteButton.vue'
import ProjectGroupSelect from '@/components/common/ProjectGroupSelect.vue'
import UserSelect from '@/components/common/UserSelect.vue'
import RankSelect from '@/components/common/RankSelect.vue'

const emit = defineEmits(['submit', 'delete'])
const { dialog, valid, form_data, form_ref, rules, onSubmit, onDelete } =
  useFormDialog<ProjectUpdate>(emit)

defineExpose({
  open(data: Project) {
    dialog.value = true
    form_data.value = {
      rid: data.rid,
      rid_project_groups: data.project_group.rid,
      rid_users_pm: data.user_pm.rid,
      rid_users_pl: data.user_pl.rid,
      rank: data.rank,
      pre_approval: data.pre_approval,
      name: data.name,
      number_parent: data.number_parent,
      amount_expected: data.amount_expected,
      amount_order: data.amount_order,
      date_start: data.date_start,
      date_delivery: data.date_delivery,
      date_end: data.date_end,
    }
  },
  close() {
    dialog.value = false
  },
})

const handleProjectGroupSelected = (project_group: ProjectGroup) => {
  form_data.value.rid_project_groups = project_group.rid
}

const handleUserPMSelected = (user: User | null) => {
  if (!user) return
  form_data.value.rid_users_pm = user.rid
}

const handleUserPLSelected = (user: User | null) => {
  if (!user) return
  form_data.value.rid_users_pl = user.rid
}

const handleRankSelected = (rank: number) => {
  form_data.value.rank = rank
}
</script>

<template>
  <v-dialog v-model="dialog" max-width="1000px">
    <v-card>
      <v-card-title>
        <span class="dialog-title">Update Project</span>
      </v-card-title>

      <v-card-text>
        <v-form ref="form_ref" v-model="valid" lazy-validation>
          <ProjectGroupSelect
            v-model="form_data.rid_project_groups"
            @itemSelected="handleProjectGroupSelected"
          />

          <v-row dense class="my-4">
            <v-col cols="6">
              <UserSelect
                v-model="form_data.rid_users_pm"
                label="PM"
                @itemSelected="handleUserPMSelected"
              />
            </v-col>

            <v-col cols="6">
              <UserSelect
                v-model="form_data.rid_users_pl"
                label="PL"
                @itemSelected="handleUserPLSelected"
              />
            </v-col>
          </v-row>

          <RankSelect v-model="form_data.rank" @itemSelected="handleRankSelected" />

          <v-text-field v-model="form_data.pre_approval" label="Pre-Approval" type="date" />

          <v-text-field v-model="form_data.name" :rules="[]" label="Name" />

          <v-text-field
            v-model="form_data.number_parent"
            :rules="[rules.text]"
            label="Number Parent"
          />

          <v-row dense class="mb-4">
            <v-col cols="6">
              <v-text-field
                v-model="form_data.amount_expected"
                :rules="[rules.numeric]"
                label="Amount Expected"
              />
            </v-col>

            <v-col cols="6">
              <v-text-field
                v-model="form_data.amount_order"
                :rules="[rules.numeric]"
                label="Amount Order"
              />
            </v-col>
          </v-row>

          <v-row dense class="mb-4">
            <v-col cols="4">
              <v-text-field v-model="form_data.date_start" label="Date Start" type="date" />
            </v-col>

            <v-col cols="4">
              <v-text-field v-model="form_data.date_delivery" label="Date Delivery" type="date" />
            </v-col>

            <v-col cols="4">
              <v-text-field v-model="form_data.date_end" label="Date End" type="date" />
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>

      <v-card-actions>
        <DeleteButton @delete="onDelete" />
        <v-spacer />
        <v-btn @click="dialog = false">Cancel</v-btn>
        <v-btn color="primary" :disabled="!valid" @click="onSubmit">Submit</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped>
@import '@/assets/main.css';
</style>
