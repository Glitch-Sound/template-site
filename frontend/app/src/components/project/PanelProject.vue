<script setup lang="ts">
import { defineProps } from 'vue'

import type { Project } from '@/types/Project'
import RIDLabel from '@/components/common/RIDLabel.vue'
import RankLabelLarge from '@/components/common/RankLabelLarge.vue'
import ProjectDateLabel from '@/components/common/ProjectDateLabel.vue'
import AmountLabel from '@/components/common/AmountLabel.vue'
import UserLabel from '@/components/common/UserLabel.vue'
import NumberLabel from '@/components/common/NumberLabel.vue'
import KarteLabel from '@/components/common/KarteLabel.vue'

const props = defineProps<{
  project: Project
}>()
</script>

<template>
  <v-sheet class="mr-5">
    <v-row>
      <v-col cols="auto" class="d-flex align-center justify-center ml-5 mr-1 pa-1">
        <RankLabelLarge :rank="props.project.rank" />
      </v-col>
      <v-col>
        <v-card>
          <ProjectDateLabel
            :start="props.project.date_start"
            :delivery="props.project.date_delivery"
            :end="props.project.date_end"
          />
        </v-card>
        <v-card>
          <span class="text-subtitle-1 font-weight-bold">{{ props.project.name }}</span>
        </v-card>
      </v-col>
      <v-col cols="auto" class="mr-5">
        <AmountLabel :project="props.project" />
      </v-col>
      <v-col cols="auto" class="mr-5">
        <v-card>
          <NumberLabel :project="props.project" />
        </v-card>
        <v-card>
          <KarteLabel :project="props.project" />
        </v-card>
      </v-col>
      <v-col cols="auto" class="mr-2">
        <UserLabel class="mb-1" :user="props.project.user_pm" />
        <UserLabel :user="props.project.user_pl" />
      </v-col>
      <v-col cols="auto" class="d-flex align-center justify-center ga-5">
        <v-icon color="#c0c0c0">mdi-message-bulleted</v-icon>
        <v-icon color="#c0c0c0">mdi-pencil</v-icon>
      </v-col>
    </v-row>
  </v-sheet>
</template>

<style scoped>
@import '@/assets/main.css';
</style>
