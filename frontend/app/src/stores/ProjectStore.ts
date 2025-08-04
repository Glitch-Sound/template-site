import { defineStore } from 'pinia'

import type {
  ProjectGroup,
  ProjectGroupCreate,
  ProjectGroupUpdate,
  Project,
  ProjectCreate,
  ProjectUpdate,
  ProjectList,
} from '@/types/Project'

import service_project from '@/services/ProjectService'

const useProjectStore = defineStore('project', {
  state: () => ({
    project_groups: [] as Array<ProjectGroup>,
    projects: [] as Array<ProjectList>,
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
    async fetchProjects() {
      this.projects = await service_project.fetchProjects()
    },
    async createProject(project: ProjectCreate): Promise<Project> {
      const result = await service_project.createProject(project)
      await this.fetchProjects()
      return result
    },
    async updateProject(project: ProjectUpdate): Promise<Project> {
      const result = await service_project.updateProject(project)
      await this.fetchProjects()
      return result
    },
    async deleteProject(rid: number): Promise<void> {
      const result = await service_project.deleteProject(rid)
      await this.fetchProjects()
      return result
    },
  },
})

export default useProjectStore
