<script setup lang="ts">
import { onMounted, ref } from 'vue'

import type { Company, CompanyCreate, CompanyUpdate } from '@/types/Company'

import SettingEvent from '@/views/setting/SettingEvent'
import useCompanyStore from '@/stores/CompanyStore'
import CreateCompanyDialog from '@/components/dialog/CreateCompanyDialog.vue'
import UpdateCompanyDialog from '@/components/dialog/UpdateCompanyDialog.vue'

const headers = [
  { title: 'RID', width: '50px' },
  { title: 'NAME', width: '150px' },
  { title: 'DETAIL', width: '500px' },
  { title: '', width: '140px' },
]

const store_company = useCompanyStore()

const dialog_company_create = ref()
const dialog_company_update = ref()

onMounted(() => {
  store_company.fetchCompanies()
})

SettingEvent.on('openCreateCompanyDialog', () => {
  dialog_company_create.value?.open()
})

const openUpdateCompanyDialog = (data: Company) => {
  dialog_company_update.value?.open(data)
}

const handleCreate = async (data: CompanyCreate) => {
  await store_company.createCompany(data)
  dialog_company_create.value?.close()
}

const handleUpdate = async (data: CompanyUpdate) => {
  await store_company.updateCompany(data)
  dialog_company_update.value?.close()
}

const handleDelete = async (data: CompanyUpdate) => {
  await store_company.deleteCompany(data.rid)
  dialog_company_update.value?.close()
}
</script>

<template>
  <v-main>
    <v-sheet class="main">
      <v-data-table class="bg-black" :items="store_company.companies" :headers="headers">
        <template v-slot:item="{ item }">
          <tr>
            <td>{{ item.rid }}</td>
            <td>{{ item.name }}</td>
            <td>{{ item.detrail }}</td>
            <td>
              <v-btn
                size="small"
                prepend-icon="mdi-pencil"
                variant="outlined"
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
