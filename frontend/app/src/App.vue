<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { RouterView } from 'vue-router'

import type { UserCreate } from '@/types/User'

import useAuthStore from '@/stores/AuthStore'
import HeaderView from '@/views/header/HeaderView.vue'
import CreateAdministratorDialog from '@/components/dialog/CreateAdministratorDialog.vue'

const store_auth = useAuthStore()

const dialog_create_admin = ref()

onMounted(async () => {
  const staus = await store_auth.fetchStatus()
  if (!staus.is_setup) {
    dialog_create_admin.value?.open()
  }
})

const onSubmitCreateAdmin = async (data: UserCreate) => {
  await store_auth.createAdmin(data)
  await store_auth.login({
    username: data.username,
    password: data.password,
  })
  dialog_create_admin.value?.close()
}
</script>

<template>
  <v-app>
    <HeaderView />
    <RouterView />

    <CreateAdministratorDialog ref="dialog_create_admin" @submit="onSubmitCreateAdmin" />
  </v-app>
</template>

<style scoped></style>
