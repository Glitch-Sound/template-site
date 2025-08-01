import { defineStore } from 'pinia'

import type { ProjectGroup, ProjectGroupCreate, ProjectGroupUpdate } from '@/types/ProjectGroup'

import service_company from '@/services/ProjectGroupService'

const useProjectGroupStore = defineStore('company', {
  state: () => ({
    project_groups: [] as Array<ProjectGroup>,
  }),
  actions: {
    async fetchProjectGroups() {
      this.project_groups = await service_company.fetchProjectGroups()
    },
    async createProjectGroup(user: ProjectGroupCreate): Promise<ProjectGroup> {
      const result = await service_company.createProjectGroup(user)
      await this.fetchProjectGroups()
      return result
    },
    async updateProjectGroup(user: ProjectGroupUpdate): Promise<ProjectGroup> {
      const result = await service_company.updateProjectGroup(user)
      await this.fetchProjectGroups()
      return result
    },
    async deleteProjectGroup(rid: number): Promise<void> {
      const result = await service_company.deleteProjectGroup(rid)
      await this.fetchProjectGroups()
      return result
    },
  },
})

export default useProjectGroupStore
