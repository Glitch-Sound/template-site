<script setup lang="ts">
import type { Login } from '@/types/Auth'
import { useFormDialog } from '@/components/dialog/BaseDialog'

const emit = defineEmits(['submit'])
const { dialog, valid, form_data, form_ref, rules, onSubmit } = useFormDialog<Login>(emit)

defineExpose({
  open() {
    dialog.value = true
    form_data.value = {
      username: '',
      password: '',
    }
  },
  close() {
    dialog.value = false
  },
})
</script>

<template>
  <v-dialog v-model="dialog" max-width="600px">
    <v-card>
      <v-card-title>
        <span class="dialog-title">Login</span>
      </v-card-title>

      <v-card-text>
        <v-form ref="form_ref" v-model="valid" lazy-validation>
          <v-text-field
            v-model="form_data.username"
            :rules="[rules.required, rules.alphanumeric]"
            label="Username"
            autocomplete="current-user"
          />

          <v-text-field
            v-model="form_data.password"
            :rules="[rules.required, rules.password]"
            label="Password"
            type="password"
            autocomplete="current-password"
          />
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
