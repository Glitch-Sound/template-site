import apiClient from '@/services/ApiClient'
import type { ProjectGroup, ProjectGroupCreate, ProjectGroupUpdate } from '@/types/Project'

class ProjectService {
  public async fetchProjectGroups(): Promise<ProjectGroup[]> {
    try {
      const response = await apiClient.get<ProjectGroup[]>('/project_group')
      return response.data
    } catch (error: any) {
      console.error(error)
      throw new Error(`fetchProjectGroups: ${error?.message || error}`)
    }
  }

  public async createProjectGroup(project_group: ProjectGroupCreate): Promise<ProjectGroup> {
    try {
      const response = await apiClient.post<ProjectGroup>('/project_group', project_group)
      return response.data
    } catch (error: any) {
      console.error(error)
      throw new Error(`createProjectGroup: ${error?.message || error}`)
    }
  }

  public async updateProjectGroup(project_group: ProjectGroupUpdate): Promise<ProjectGroup> {
    try {
      const response = await apiClient.put<ProjectGroup>('/project_group', project_group)
      return response.data
    } catch (error: any) {
      console.error(error)
      throw new Error(`updateProjectGroup: ${error?.message || error}`)
    }
  }

  public async deleteProjectGroup(rid: number): Promise<void> {
    try {
      await apiClient.delete(`/project_group/${rid}`)
    } catch (error: any) {
      console.error(error)
      throw new Error(`deleteProjectGroup: ${error?.message || error}`)
    }
  }
}

const service_project = new ProjectService()
export default service_project
