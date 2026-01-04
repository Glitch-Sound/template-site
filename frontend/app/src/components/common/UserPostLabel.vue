<script setup lang="ts">
import { TypePost } from '@/types/User'

const props = defineProps<{
  post: TypePost
}>()
</script>

<template>
  <v-chip size="small" color="#dfaaaa" :value="TypePost.NONE" v-if="props.post == TypePost.NONE">
    ADMIN
  </v-chip>
  <v-chip size="small" color="#b0e0e6" :value="TypePost.MNG" v-if="props.post == TypePost.MNG">
    MNG
  </v-chip>
  <v-chip size="small" color="#b0e0e6" :value="TypePost.AM" v-if="props.post == TypePost.AM">
    AM
  </v-chip>
  <v-chip size="small" color="#b0e0e6" :value="TypePost.L" v-if="props.post == TypePost.L">
    L
  </v-chip>
  <v-chip size="small" color="#b0e0e6" :value="TypePost.T" v-if="props.post == TypePost.T">
    T
  </v-chip>
  <v-chip size="small" color="#f4a261" :value="TypePost.BP" v-if="props.post == TypePost.BP">
    BP
  </v-chip>
  <v-chip size="small" color="#6f6f6f" :value="TypePost.GUEST" v-if="props.post == TypePost.GUEST">
    GUEST
  </v-chip>
</template>

<style scoped>
</style>
