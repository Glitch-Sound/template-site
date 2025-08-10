<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { storeToRefs } from 'pinia'

import type { Company, CompanyCreate, CompanyUpdate } from '@/types/Company'
import { useCompanyStore } from '@/stores/CompanyStore'
import SettingEvent from '@/views/setting/SettingEvent'
import CreateCompanyDialog from '@/components/dialog/CreateCompanyDialog.vue'
import UpdateCompanyDialog from '@/components/dialog/UpdateCompanyDialog.vue'

const headers = [
  { title: 'RID', width: '50px' },
  { title: 'NAME', width: '150px' },
  { title: 'DETAIL', width: '500px' },
  { title: '', width: '140px' },
]

const store_company = useCompanyStore()
const { companies, is_loading } = storeToRefs(store_company)
const { fetchCompanies, createCompany, updateCompany, deleteCompany } = store_company

const dialog_company_create = ref()
const dialog_company_update = ref()

onMounted(async () => {
  try {
    await fetchCompanies()
  } catch (e) {
    console.error(e)
  }
})

SettingEvent.on('openCreateCompanyDialog', () => {
  dialog_company_create.value?.open()
})

const openUpdateCompanyDialog = (data: Company) => {
  dialog_company_update.value?.open(data)
}

const handleCreate = async (data: CompanyCreate) => {
  try {
    await createCompany(data)
    dialog_company_create.value?.close()
  } catch (e) {
    console.error(e)
  }
}

const handleUpdate = async (data: CompanyUpdate) => {
  try {
    await updateCompany(data)
    dialog_company_update.value?.close()
  } catch (e) {
    console.error(e)
  }
}

const handleDelete = async (data: CompanyUpdate) => {
  try {
    await deleteCompany(data.rid)
    dialog_company_update.value?.close()
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
        :items="companies"
        :headers="headers"
        :loading="is_loading"
        loading-text="Loading companies..."
      >
        <template #item="{ item }">
          <tr>
            <td>{{ item.rid }}</td>
            <td>{{ item.name }}</td>
            <td>{{ item.detail }}</td>
            <td>
              <v-btn
                size="small"
                prepend-icon="mdi-pencil"
                variant="outlined"
                :disabled="is_loading"
                @click="openUpdateCompanyDialog(item)"
              >
                UPDATE
              </v-btn>
            </td>
          </tr>
        </template>
      </v-data-table>
    </v-sheet>
  </v-main>

  <CreateCompanyDialog ref="dialog_company_create" @submit="handleCreate" />
  <UpdateCompanyDialog ref="dialog_company_update" @submit="handleUpdate" @delete="handleDelete" />
</template>

<style scoped>
@import '@/assets/main.css';
</style>
