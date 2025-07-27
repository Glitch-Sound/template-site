<script setup lang="ts">
import { defineProps } from 'vue'

import { TypePost } from '@/types/User'

const props = defineProps<{
  post: TypePost
}>()
</script>

<template>
  <v-chip size="small" color="#dfaaaa" :value="TypePost.NONE" v-if="props.post == TypePost.NONE">
    ADMIN
  </v-chip>
  <v-chip size="small" color="#aaaadf" :value="TypePost.K" v-if="props.post == TypePost.K">
    K
  </v-chip>
  <v-chip size="small" color="#aaaadf" :value="TypePost.C" v-if="props.post == TypePost.C">
    C
  </v-chip>
  <v-chip size="small" color="#aaaadf" :value="TypePost.L" v-if="props.post == TypePost.L">
    L
  </v-chip>
  <v-chip size="small" color="#aaaadf" :value="TypePost.T" v-if="props.post == TypePost.T">
    T
  </v-chip>
  <v-chip size="small" color="#aaaadf" :value="TypePost.BP" v-if="props.post == TypePost.BP">
    BP
  </v-chip>
</template>

<style scoped></style>
