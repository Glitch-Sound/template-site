import apiClient from '@/services/ApiClient'
import type { User } from '@/types/User'
import type {
  ProjectGroup,
  ProjectGroupCreate,
  ProjectGroupUpdate,
  ProjectNumber,
  ProjectNumberCreate,
  ProjectNumberUpdate,
  SearchCondition,
  TargetQuarter,
  Project,
  ProjectCreate,
  ProjectUpdate,
  ProjectList,
} from '@/types/Project'

class ProjectService {
  public async fetchProjectGroups(): Promise<ProjectGroup[]> {
    try {
      const response = await apiClient.get<ProjectGroup[]>('/project_groups')
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(
        `fetchProjectGroups: ${error instanceof Error ? error.message : String(error)}`,
      )
    }
  }

  public async createProjectGroup(project_group: ProjectGroupCreate): Promise<ProjectGroup> {
    try {
      const response = await apiClient.post<ProjectGroup>('/project_groups', project_group)
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(
        `createProjectGroup: ${error instanceof Error ? error.message : String(error)}`,
      )
    }
  }

  public async updateProjectGroup(project_group: ProjectGroupUpdate): Promise<ProjectGroup> {
    try {
      const response = await apiClient.put<ProjectGroup>('/project_groups', project_group)
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(
        `updateProjectGroup: ${error instanceof Error ? error.message : String(error)}`,
      )
    }
  }

  public async deleteProjectGroup(rid: number): Promise<void> {
    try {
      await apiClient.delete(`/project_groups/${rid}`)
    } catch (error: unknown) {
      console.error(error)
      throw new Error(
        `deleteProjectGroup: ${error instanceof Error ? error.message : String(error)}`,
      )
    }
  }

  public async fetchProjectNumbers(rid: number): Promise<ProjectNumber[]> {
    try {
      const response = await apiClient.get<ProjectNumber[]>(`/project_numbers/${rid}`)
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(
        `fetchProjectNumbers: ${error instanceof Error ? error.message : String(error)}`,
      )
    }
  }

  public async createProjectNumber(project_number: ProjectNumberCreate): Promise<ProjectNumber> {
    try {
      const response = await apiClient.post<ProjectNumber>('/project_numbers', project_number)
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(
        `createProjectNumber: ${error instanceof Error ? error.message : String(error)}`,
      )
    }
  }

  public async updateProjectNumber(project_number: ProjectNumberUpdate): Promise<ProjectNumber> {
    try {
      const response = await apiClient.put<ProjectNumber>('/project_numbers', project_number)
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(
        `updateProjectNumber: ${error instanceof Error ? error.message : String(error)}`,
      )
    }
  }

  public async deleteProjectNumber(rid: number): Promise<void> {
    try {
      await apiClient.delete(`/project_numbers/${rid}`)
    } catch (error: unknown) {
      console.error(error)
      throw new Error(
        `deleteProjectNumber: ${error instanceof Error ? error.message : String(error)}`,
      )
    }
  }

  public async fetchProjectCondition(): Promise<SearchCondition> {
    try {
      const response = await apiClient.get<SearchCondition>('/projects/condition')
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(
        `fetchProjectCondition: ${error instanceof Error ? error.message : String(error)}`,
      )
    }
  }

  public async fetchProjectTargets(): Promise<TargetQuarter[]> {
    try {
      const response = await apiClient.get<TargetQuarter[]>('/projects/targets')
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(
        `fetchProjectTargets: ${error instanceof Error ? error.message : String(error)}`,
      )
    }
  }

  public async fetchProjectUsers(): Promise<User[]> {
    try {
      const response = await apiClient.get<User[]>('/projects/users')
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(
        `fetchProjectUsers: ${error instanceof Error ? error.message : String(error)}`,
      )
    }
  }

  public async fetchProjects(condition: SearchCondition): Promise<ProjectList[]> {
    try {
      const response = await apiClient.post<ProjectList[]>('/projects/search', condition)
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(`fetchProjects: ${error instanceof Error ? error.message : String(error)}`)
    }
  }

  public async createProject(project: ProjectCreate): Promise<Project> {
    try {
      const response = await apiClient.post<Project>('/projects', project)
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(`createProject: ${error instanceof Error ? error.message : String(error)}`)
    }
  }

  public async updateProject(project: ProjectUpdate): Promise<Project> {
    try {
      const response = await apiClient.put<Project>('/projects', project)
      return response.data
    } catch (error: unknown) {
      console.error(error)
      throw new Error(`updateProject: ${error instanceof Error ? error.message : String(error)}`)
    }
  }

  public async deleteProject(rid: number): Promise<void> {
    try {
      await apiClient.delete(`/projects/${rid}`)
    } catch (error: unknown) {
      console.error(error)
      throw new Error(`deleteProject: ${error instanceof Error ? error.message : String(error)}`)
    }
  }
}

const service_project = new ProjectService()
export default service_project
