<script setup lang="ts">
import { computed } from 'vue'
import { type Project } from '@/types/Project'

const props = defineProps<{
  project: Project
}>()

const isPreApprovalCurrentOrFuture = computed(() => {
  const value = props.project.pre_approval
  if (!value) return false

  const preApprovalDate = new Date(value)
  if (Number.isNaN(preApprovalDate.getTime())) return false

  const today = new Date()
  today.setHours(0, 0, 0, 0)
  preApprovalDate.setHours(0, 0, 0, 0)

  return preApprovalDate.getTime() <= today.getTime()
})
</script>

<template>
  <v-row>
    <v-col cols="auto">
      <span class="text-body-2 gray-light"> Number : </span>

      <template v-if="props.project.number_parent !== ''">
        <span class="text-body-2 primary-light"> {{ props.project.number_parent }} </span>
      </template>
      <template v-else>
        <span class="text-body-2 red-light"> XXXXXX </span>
      </template>
    </v-col>

    <v-col cols="auto">
      <template v-if="props.project.pre_approval !== ''">
        <span
          class="text-caption"
          :class="isPreApprovalCurrentOrFuture ? 'pre-approval-warning' : 'gray-dark'"
        >
          {{ props.project.pre_approval }}
        </span>
      </template>
      <template v-else>
        <span class="text-caption black"> 0000-00-00 </span>
      </template>
    </v-col>

    <v-col cols="auto">
      <template v-if="props.project.number_m">
        <v-chip size="small" color="#198b48" class="font-weight-bold"> M </v-chip>
      </template>
      <template v-else>
        <v-chip size="small" disabled> M </v-chip>
      </template>
    </v-col>
    <v-col cols="auto">
      <template v-if="props.project.number_s">
        <v-chip size="small" color="#198b48" class="font-weight-bold"> S </v-chip>
      </template>
      <template v-else>
        <v-chip size="small" disabled> S </v-chip>
      </template>
    </v-col>
    <v-col cols="auto">
      <template v-if="props.project.number_o">
        <v-chip size="small" color="#198b48" class="font-weight-bold"> 0 </v-chip>
      </template>
      <template v-else>
        <v-chip size="small" disabled> 0 </v-chip>
      </template>
    </v-col>
  </v-row>
</template>

<style scoped>
.pre-approval-warning {
  color: #c49116 !important;
}

.primary-light {
  color: #2196f3 !important;
}

.red-light {
  color: #940000 !important;
}

.black {
  color: #000000 !important;
}
</style>
