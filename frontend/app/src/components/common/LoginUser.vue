<script setup lang="ts">
import { ref } from 'vue'
import { storeToRefs } from 'pinia'

import type { Login } from '@/types/Auth'
import { useAuthStore } from '@/stores/AuthStore'
import UserIcon from '@/components/common/UserIcon.vue'
import LoginDialog from '@/components/dialog/LoginDialog.vue'

const auth = useAuthStore()

const { user_logined, is_logined } = storeToRefs(auth)
const { login } = auth

const dialog_login = ref()

function openLoginDialog() {
  dialog_login.value?.open()
}

async function onSubmitLogin(data: Login) {
  try {
    await login(data)
    dialog_login.value?.close()
  } catch (error) {
    console.error(error)
  }
}
</script>

<template>
  <div v-if="!is_logined">
    <v-btn variant="text" @click="openLoginDialog">Login</v-btn>
  </div>
  <div v-else>
    <div class="align-center d-flex">
      <v-btn icon size="x-small" @click="openLoginDialog">
        <UserIcon :user="user_logined!" :size="24" />
      </v-btn>

      <span class="mx-2">
        {{ user_logined?.name }}
      </span>
    </div>
  </div>

  <LoginDialog ref="dialog_login" @submit="onSubmitLogin" />
</template>

<style scoped></style>
