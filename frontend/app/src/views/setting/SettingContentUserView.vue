<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { storeToRefs } from 'pinia'

import type { User, UserCreate, UserUpdate } from '@/types/User'
import { useUserStore } from '@/stores/UserStore'
import SettingEvent from '@/views/setting/SettingEvent'
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
const { users, is_loading } = storeToRefs(store_user)
const { fetchUsers, createUser, updateUser, deleteUser } = store_user

const dialog_user_create = ref()
const dialog_user_update = ref()

onMounted(async () => {
  try {
    await fetchUsers()
  } catch (e) {
    console.error(e)
  }
})

SettingEvent.on('openCreateUserDialog', () => {
  dialog_user_create.value?.open()
})

const openUpdateUserDialog = (data: User) => {
  dialog_user_update.value?.open(data)
}

const handleCreate = async (data: UserCreate) => {
  try {
    await createUser(data)
    dialog_user_create.value?.close()
  } catch (e) {
    console.error(e)
  }
}

const handleUpdate = async (data: UserUpdate) => {
  try {
    await updateUser(data)
    dialog_user_update.value?.close()
  } catch (e) {
    console.error(e)
  }
}

const handleDelete = async (data: UserUpdate) => {
  try {
    await deleteUser(data.rid)
    dialog_user_update.value?.close()
  } catch (e) {
    console.error(e)
  }
}
</script>

<template>
  <v-main>
    <v-sheet class="main">
      <v-data-table
        class="bg-black"
        :items="users"
        :headers="headers"
        :loading="is_loading"
        loading-text="Loading users..."
      >
        <template #item="{ item }">
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
                :disabled="is_loading"
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

<style scoped></style>
