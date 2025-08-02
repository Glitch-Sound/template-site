import { defineStore } from 'pinia'

import type { ProjectGroup, ProjectGroupCreate, ProjectGroupUpdate } from '@/types/ProjectGroup'

import service_project_group from '@/services/ProjectGroupService'

const useProjectGroupStore = defineStore('project_group', {
  state: () => ({
    project_groups: [] as Array<ProjectGroup>,
  }),
  actions: {
    async fetchProjectGroups() {
      this.project_groups = await service_project_group.fetchProjectGroups()
    },
    async createProjectGroup(user: ProjectGroupCreate): Promise<ProjectGroup> {
      const result = await service_project_group.createProjectGroup(user)
      await this.fetchProjectGroups()
      return result
    },
    async updateProjectGroup(user: ProjectGroupUpdate): Promise<ProjectGroup> {
      const result = await service_project_group.updateProjectGroup(user)
      await this.fetchProjectGroups()
      return result
    },
    async deleteProjectGroup(rid: number): Promise<void> {
      const result = await service_project_group.deleteProjectGroup(rid)
      await this.fetchProjectGroups()
      return result
    },
  },
})

export default useProjectGroupStore
