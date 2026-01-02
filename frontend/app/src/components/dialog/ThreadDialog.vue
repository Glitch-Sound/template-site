<script setup lang="ts">
import { ref, computed } from 'vue'
import { storeToRefs } from 'pinia'

import { useDisplayDialog } from '@/components/dialog/BaseDialog'
import type { Project } from '@/types/Project'
import type { Thread, ThreadCreate, ThreadUpdate } from '@/types/Thread'
import { TypeThreadState } from '@/types/Thread'
import { useThreadStore } from '@/stores/ThreadStore'
import MarkedText from '@/components/common/MarkedText.vue'
import CreateThreadDialog from '@/components/dialog/CreateThreadDialog.vue'
import UpdateThreadDialog from '@/components/dialog/UpdateThreadDialog.vue'

const store_thread = useThreadStore()
const { fetchThreadsByRID, createThread, updateThread, deleteThread } = store_thread
const { threads, is_loading } = storeToRefs(store_thread)

const emit = defineEmits(['submit'])
const { dialog, onClose } = useDisplayDialog(emit)

const project = ref<Project | null>(null)
const title = computed(() => project.value?.name ?? '')
const dialog_thread_create = ref()
const dialog_thread_update = ref()

const indent_depth = (d: number) => `${Math.max(0, d) * 22}px`

defineExpose({
  async open(data: Project) {
    dialog.value = true
    project.value = data

    await fetchThreadsByRID(data.rid)
  },
  close() {
    dialog.value = false
    project.value = null
  },
})

const handleCreateThread = () => {
  dialog_thread_create.value?.open(project.value, null)
}

const handleCheckThread = async (data: Thread) => {
  if (!project.value) return

  if (data.state != TypeThreadState.COMPLETED) {
    await updateThread({
      rid: data.rid,
      rid_projects: project.value.rid,
      state: TypeThreadState.COMPLETED,
      note: data.note,
    })
  } else {
    await updateThread({
      rid: data.rid,
      rid_projects: project.value.rid,
      state: TypeThreadState.RUN,
      note: data.note,
    })
  }
}

const handleNoticeThread = async (data: Thread) => {
  if (!project.value) return

  if (data.state != TypeThreadState.IMPORTANT) {
    await updateThread({
      rid: data.rid,
      rid_projects: project.value.rid,
      state: TypeThreadState.IMPORTANT,
      note: data.note,
    })
  } else {
    await updateThread({
      rid: data.rid,
      rid_projects: project.value.rid,
      state: TypeThreadState.RUN,
      note: data.note,
    })
  }
}

const handleAddThread = (data: Thread) => {
  dialog_thread_create.value?.open(project.value, data.rid)
}

const handleEditThread = (data: Thread) => {
  if (!project.value) return
  dialog_thread_update.value?.open(data, project.value.rid)
}

async function handleCreate(data: ThreadCreate) {
  await createThread(data)
  dialog_thread_create.value?.close()
}

async function handleUpdate(data: ThreadUpdate) {
  await updateThread(data)
  dialog_thread_update.value?.close()
}

const handleDelete = async (data: ThreadUpdate) => {
  if (!project.value) return
  await deleteThread(project.value.rid, data.rid)
  dialog_thread_update.value?.close()
}
</script>

<template>
  <v-dialog v-model="dialog" max-width="1700px" min-height="1000px">
    <v-card class="d-flex flex-column" style="max-height: 80vh">
      <v-card-title>
        <span class="dialog-title">{{ title }}</span>

        <v-btn
          :icon="'mdi-plus-circle'"
          class="ml-3 mb-1"
          variant="text"
          color="#940000"
          size="small"
          @click="handleCreateThread"
        />
      </v-card-title>

      <v-card-text class="flex-grow-1 overflow-y-auto">
        <div v-if="!is_loading && (!threads || threads.length === 0)" class="text-medium-emphasis">
          No Thread.
        </div>

        <v-list v-else density="compact" class="py-0">
          <v-list-item v-for="t in threads" :key="t.rid" density="compact" class="py-0 my-0">
            <v-row class="ma-0 pa-0 no-gutter">
              <v-col class="pa-0">
                <div :style="{ paddingLeft: indent_depth(t.depth) }">
                  <template v-if="t.state == TypeThreadState.COMPLETED">
                    <MarkedText class="text-body-2 note-check" :src="t.note" />
                  </template>

                  <template v-else-if="t.state == TypeThreadState.IMPORTANT">
                    <MarkedText class="text-body-2 note-notice" :src="t.note" />
                  </template>

                  <template v-else>
                    <MarkedText class="text-body-2" :src="t.note" />
                  </template>
                </div>
              </v-col>

              <v-col cols="auto" class="pa-0 d-flex align-end">
                <span class="user text-no-wrap lh-1">
                  {{ t.created_at.replace('T', ' ').replace(/\.\d+Z?$/, '') }} - {{ t.user.name }}
                </span>
              </v-col>

              <v-col cols="auto" class="pa-0 d-flex align-end" style="gap: 0">
                <v-icon size="small" color="#c0c0c0" class="ml-5" @click="handleCheckThread(t)">
                  mdi-check
                </v-icon>

                <v-icon size="small" color="#c0c0c0" class="ml-3" @click="handleNoticeThread(t)">
                  mdi-exclamation
                </v-icon>

                <v-icon size="small" color="#c0c0c0" class="ml-3" @click="handleAddThread(t)">
                  mdi-plus
                </v-icon>

                <v-icon size="small" color="#c0c0c0" class="ml-3" @click="handleEditThread(t)">
                  mdi-pencil
                </v-icon>
              </v-col>
            </v-row>
          </v-list-item>
        </v-list>
      </v-card-text>

      <v-card-actions>
        <v-spacer />
        <v-btn color="primary" @click="onClose">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <CreateThreadDialog ref="dialog_thread_create" @submit="handleCreate" />
  <UpdateThreadDialog ref="dialog_thread_update" @submit="handleUpdate" @delete="handleDelete" />
</template>

<style scoped>
@import '@/assets/main.css';

.note-check {
  color: #6f6f6f;
}

.note-notice {
  color: #f5d90a;
}

.user {
  color: #9e9e9e;
  font-size: 13px;
}
</style>
