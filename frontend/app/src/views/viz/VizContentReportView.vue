<script setup lang="ts">
import { watch, computed } from 'vue'
import { storeToRefs } from 'pinia'

import { useProjectStore } from '@/stores/ProjectStore'
import { useThreadStore } from '@/stores/ThreadStore'
import { TypeThreadState } from '@/types/Thread'
import PanelProject from '@/components/project/PanelProject.vue'
import PanelProjectGroup from '@/components/project/PanelProjectGroup.vue'
import MarkedText from '@/components/common/MarkedText.vue'

const store_project = useProjectStore()
const { projects_report, report_user_rid, is_loading_projects_report } =
  storeToRefs(store_project)
const { fetchProjectsReport } = store_project

const store_thread = useThreadStore()
const { threads_report, is_loading_report } = storeToRefs(store_thread)
const { fetchThreadsByUser } = store_thread

const indent_depth = (d: number) => `${Math.max(0, d) * 22}px`

const threads_by_project = computed(
  () => new Map(threads_report.value.map((r) => [r.rid_projects, r.threads])),
)

watch(
  report_user_rid,
  async (rid) => {
    if (rid == null) return
    await Promise.all([fetchProjectsReport(rid), fetchThreadsByUser(rid)])
  },
  { immediate: true },
)
</script>

<template>
  <v-main>
    <v-sheet class="main">
      <v-overlay
        :model-value="is_loading_projects_report || is_loading_report"
        contained
        scrim="transparent"
        class="align-center justify-center"
      >
        <v-progress-circular indeterminate color="primary" />
      </v-overlay>

      <div v-if="report_user_rid == null" class="empty-message">PLを選択してください</div>
      <template v-else>
        <template v-for="(project_group, i) in projects_report" :key="project_group.rid">
          <PanelProjectGroup :project_group="project_group" :class="{ 'mt-10': 0 < i }" />
          <template v-for="(project, j) in project_group.projects" :key="project.rid">
            <div :class="{ 'project-spacing': 0 < j }">
              <PanelProject :project="project" />
              <v-list density="compact" class="py-0 thread-list">
                <v-list-item
                  v-for="t in threads_by_project.get(project.rid) ?? []"
                  :key="t.rid"
                  density="compact"
                  class="py-0 my-0"
                >
                  <v-row class="ma-0 pa-0 pb-5 no-gutter">
                    <v-col class="pa-0">
                      <div :style="{ paddingLeft: indent_depth(t.depth) }">
                        <template v-if="t.state == TypeThreadState.COMPLETED">
                          <MarkedText class="text-body-2 pr-6 note-check" :src="t.note" />
                        </template>

                        <template v-else-if="t.state == TypeThreadState.IMPORTANT">
                          <MarkedText class="text-body-2 pr-6 note-notice" :src="t.note" />
                        </template>

                        <template v-else>
                          <MarkedText class="text-body-2 pr-6" :src="t.note" />
                        </template>
                      </div>
                    </v-col>

                    <v-col cols="auto" class="pa-0 d-flex align-end">
                      <span class="user text-no-wrap lh-1">
                        {{ t.created_at.replace('T', ' ').replace(/\.\d+Z?$/, '') }} -
                        {{ t.user.name }}
                      </span>
                    </v-col>
                  </v-row>
                </v-list-item>
              </v-list>
              <div
                v-if="(threads_by_project.get(project.rid) ?? []).length === 0"
                class="text-medium-emphasis empty-thread thread-list"
              >
                No Thread.
              </div>
            </div>
          </template>
        </template>
      </template>
    </v-sheet>
  </v-main>
</template>

<style scoped>
.empty-message {
  color: #9f9f9f;
  font-size: 14px;
  letter-spacing: 0.2px;
  padding: 16px;
}

.thread-list {
  margin-left: 100px;
  padding-left: 10px;
  border-left: 1px solid #b8c9f2;
}

.project-spacing {
  margin-top: 50px;
}

.empty-thread {
  padding: 6px 16px 20px;
}

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
