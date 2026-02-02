<script setup lang="ts">
import { computed, watch } from 'vue'
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

const numberFormatter = new Intl.NumberFormat('ja-JP')

const formatNumber = (value: number) => numberFormatter.format(value)

const parseNumber = (value: string) => {
  const sanitized = value.replace(/,/g, '').trim()
  if (sanitized === '') return 0
  const numberValue = Number(sanitized)
  return Number.isNaN(numberValue) ? 0 : numberValue
}

const numericWithComma = (value: string) => rules.numeric(value.replace(/,/g, ''))
const numberParentRules = [
  (value: string) => /^[a-zA-Z0-9]{6}$/.test(value) || '6-digit alphanumeric required',
]

const formattedAmountExpected = computed(() => formatNumber(form_data.value.amount_expected))
const formattedAmountOrder = computed(() => formatNumber(form_data.value.amount_order))

const updateAmountExpected = (value: string) => {
  form_data.value.amount_expected = parseNumber(value)
}

const updateAmountOrder = (value: string) => {
  form_data.value.amount_order = parseNumber(value)
}

watch(
  () => form_data.value.amount_order,
  (value) => {
    const numberValue = Number(value)
    if (!Number.isNaN(numberValue) && numberValue !== 0) {
      form_data.value.amount_expected = value
    }
  },
)

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

          <v-text-field v-model="form_data.pre_approval" label="承認予定" type="date" />

          <v-text-field v-model="form_data.name" :rules="[]" label="プロジェクト名" />

          <v-text-field
            v-model="form_data.number_parent"
            :rules="numberParentRules"
            label="親番"
          />

          <v-row dense class="mb-4">
            <v-col cols="6">
              <v-text-field
                :model-value="formattedAmountExpected"
                :rules="[numericWithComma]"
                label="見込金額"
                inputmode="numeric"
                @update:model-value="updateAmountExpected"
              />
            </v-col>

            <v-col cols="6">
              <v-text-field
                :model-value="formattedAmountOrder"
                :rules="[numericWithComma]"
                label="受注金額"
                inputmode="numeric"
                @update:model-value="updateAmountOrder"
              />
            </v-col>
          </v-row>

          <v-row dense class="mb-4">
            <v-col cols="4">
              <v-text-field v-model="form_data.date_start" label="開始日" type="date" />
            </v-col>

            <v-col cols="4">
              <v-text-field v-model="form_data.date_delivery" label="納品日" type="date" />
            </v-col>

            <v-col cols="4">
              <v-text-field v-model="form_data.date_end" label="検収日" type="date" />
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

<style scoped></style>
