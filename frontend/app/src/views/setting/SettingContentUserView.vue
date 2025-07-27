<script setup lang="ts">
import { onMounted, ref } from 'vue'

import type { User, UserCreate, UserUpdate } from '@/types/User'

import SettingEvent from '@/views/setting/SettingEvent'
import useUserStore from '@/stores/UserStore'
import UserPostLabel from '@/components/common/UserPostLabel.vue'
import UserContractLabel from '@/components/common/UserContractLabel.vue'
import UserPriceLavel from '@/components/common/UserPriceLabel.vue'
import CreateUserDialog from '@/components/dialog/CreateUserDialog.vue'
import UpdateUserDialog from '@/components/dialog/UpdateUserDialog.vue'

const headers = [
  { title: 'RID', width: '50px' },
  { title: 'ID', width: '50px' },
  { title: 'USER', width: '150px' },
  { title: 'NAME', width: '150px' },
  { title: 'COMPANY', width: '150px' },
  { title: 'POST', width: '30px' },
  { title: 'CONTRACT', width: '30px' },
  { title: 'PRICE', width: '100px' },
  { title: '', width: '140px' },
]

const store_user = useUserStore()

const dialog_user_create = ref()
const dialog_user_update = ref()

onMounted(() => {
  store_user.fetchUsers()
})

SettingEvent.on('openCreateUserDialog', () => {
  dialog_user_create.value?.open()
})

const openUpdateUserDialog = (data: User) => {
  dialog_user_update.value?.open(data)
}

const handleCreate = async (data: UserCreate) => {
  await store_user.createUser(data)
  dialog_user_create.value?.close()
}

const handleUpdate = async (data: UserUpdate) => {
  await store_user.updateUser(data)
  dialog_user_update.value?.close()
}

const handleDelete = async (data: UserUpdate) => {
  await store_user.deleteUser(data.rid)
  dialog_user_update.value?.close()
}
</script>

<template>
  <v-main>
    <v-sheet class="main">
      <v-data-table class="bg-black" :items="store_user.users" :headers="headers">
        <template v-slot:item="{ item }">
          <tr>
            <td>{{ item.rid }}</td>
            <td>{{ item.eid }}</td>
            <td>{{ item.username }}</td>
            <td>{{ item.name }}</td>
            <td>{{ item.company }}</td>
            <td><UserPostLabel :post="item.post" /></td>
            <td><UserContractLabel :contract="item.contract" /></td>
            <td><UserPriceLavel :price="item.price" /></td>
            <td>
              <v-btn
                size="small"
                prepend-icon="mdi-pencil"
                variant="outlined"
                @click="openUpdateUserDialog(item)"
              >
                UPDATE
              </v-btn>
            </td>
          </tr>
        </template>
      </v-data-table>
    </v-sheet>
  </v-main>

  <CreateUserDialog ref="dialog_user_create" @submit="handleCreate" />
  <UpdateUserDialog ref="dialog_user_update" @submit="handleUpdate" @delete="handleDelete" />
</template>

<style scoped>
@import '@/assets/main.css';
</style>
