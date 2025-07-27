<script setup lang="ts">
import { ref } from 'vue'

import type { Login } from '@/types/Auth'

import useAuthStore from '@/stores/AuthStore'
import UserIcon from '@/components/common/UserIcon.vue'
import LoginDialog from '@/components/dialog/LoginDialog.vue'

const store_auth = useAuthStore()

const dialog_login = ref()

const openLoginDialog = () => {
  dialog_login.value?.open()
}

const onSubmitLogin = async (data: Login) => {
  try {
    await store_auth.login(data)
    dialog_login.value?.close()
  } catch (error) {
    console.log(error)
  }
}
</script>

<template>
  <div v-if="!store_auth.isLogined()">
    <v-btn variant="text" @click="openLoginDialog">Login</v-btn>
  </div>
  <div v-else>
    <div class="align-center d-flex">
      <span class="mr-1">
        {{ store_auth.user_login?.name }}
      </span>

      <v-btn icon size="x-small" @click="openLoginDialog">
        <UserIcon :user="store_auth.user_login" :size="24" />
      </v-btn>
    </div>
  </div>

  <LoginDialog ref="dialog_login" @submit="onSubmitLogin" />
</template>

<style scoped></style>
