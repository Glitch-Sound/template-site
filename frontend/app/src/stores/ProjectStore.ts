import { defineStore } from 'pinia'

import type { ProjectGroup, ProjectGroupCreate, ProjectGroupUpdate } from '@/types/Project'

import service_project from '@/services/ProjectService'

const useProjectStore = defineStore('project', {
  state: () => ({
    project_groups: [] as Array<ProjectGroup>,
  }),
  actions: {
    async fetchProjectGroups() {
      this.project_groups = await service_project.fetchProjectGroups()
    },
    async createProjectGroup(user: ProjectGroupCreate): Promise<ProjectGroup> {
      const result = await service_project.createProjectGroup(user)
      await this.fetchProjectGroups()
      return result
    },
    async updateProjectGroup(user: ProjectGroupUpdate): Promise<ProjectGroup> {
      const result = await service_project.updateProjectGroup(user)
      await this.fetchProjectGroups()
      return result
    },
    async deleteProjectGroup(rid: number): Promise<void> {
      const result = await service_project.deleteProjectGroup(rid)
      await this.fetchProjectGroups()
      return result
    },
  },
})

export default useProjectStore
