<script setup lang="ts">
import type { UserCreate } from '@/types/User'
import { useFormDialog } from '@/components/dialog/BaseDialog'

import { TypePost, TypeContract } from '@/types/User'
import UserPostSelect from '@/components/common/UserPostSelect.vue'
import UserContractSelect from '@/components/common/UserContractSelect.vue'

const emit = defineEmits(['submit'])
const { dialog, valid, form_data, form_ref, rules, onSubmit } = useFormDialog<UserCreate>(emit)

defineExpose({
  open() {
    dialog.value = true
    form_data.value = {
      eid: '',
      username: '',
      password: '',
      name: '',
      company: '',
      post: TypePost.NONE,
      contract: TypeContract.NONE,
      is_admin: false,
    }
  },
  close() {
    dialog.value = false
  },
})

const handlePostSelected = (post: number) => {
  form_data.value.post = post
}

const handleContractSelected = (contract: number) => {
  form_data.value.contract = contract
}
</script>

<template>
  <v-dialog v-model="dialog" max-width="600px">
    <v-card>
      <v-card-title>
        <span class="dialog-title">Add User</span>
      </v-card-title>

      <v-card-text>
        <v-form ref="form_ref" v-model="valid" lazy-validation>
          <v-text-field
            v-model="form_data.eid"
            :rules="[rules.required, rules.alphanumeric]"
            label="ID"
          />

          <v-text-field
            v-model="form_data.username"
            :rules="[rules.required, rules.alphanumeric]"
            label="User"
            autocomplete="current-user"
          />

          <v-text-field
            v-model="form_data.password"
            :rules="[rules.required, rules.password]"
            label="Password"
            type="password"
            autocomplete="current-password"
          />

          <v-text-field
            v-model="form_data.name"
            :rules="[rules.required, rules.text]"
            label="Name"
          />

          <v-text-field v-model="form_data.company" :rules="[rules.required]" label="Company" />

          <UserPostSelect v-model="form_data.post" @itemSelected="handlePostSelected" />
          <UserContractSelect v-model="form_data.contract" @itemSelected="handleContractSelected" />
        </v-form>
      </v-card-text>

      <v-card-actions>
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
