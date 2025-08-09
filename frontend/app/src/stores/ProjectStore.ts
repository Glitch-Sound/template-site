import { ref, computed } from 'vue'
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

export const useProjectStore = defineStore('project', () => {
  // state.
  const project_groups = ref<ProjectGroup[]>([])
  const projects = ref<ProjectList[]>([])

  const is_loading_groups = ref(false)
  const is_loading_projects = ref(false)

  let inflight_groups: Promise<void> | null = null
  let inflight_projects: Promise<void> | null = null

  // getters.
  const by_rid_group = computed(() => new Map(project_groups.value.map((g) => [g.rid, g])))
  const by_rid_project = computed(() => new Map(projects.value.map((p) => [p.rid, p])))

  // helpers.
  function getGroupByRid(rid: number): ProjectGroup | undefined {
    return by_rid_group.value.get(rid)
  }
  function getProjectByRid(rid: number): ProjectList | undefined {
    return by_rid_project.value.get(rid)
  }

  function upsert_group(g: ProjectGroup) {
    const i = project_groups.value.findIndex((x) => x.rid === g.rid)
    if (i >= 0) project_groups.value[i] = g
    else project_groups.value.push(g)
  }

  // actions: groups.
  async function fetchProjectGroups(): Promise<void> {
    if (inflight_groups) return inflight_groups
    is_loading_groups.value = true
    inflight_groups = (async () => {
      try {
        project_groups.value = await service_project.fetchProjectGroups()
      } finally {
        is_loading_groups.value = false
        inflight_groups = null
      }
    })()
    return inflight_groups
  }

  async function createProjectGroup(payload: ProjectGroupCreate): Promise<ProjectGroup> {
    const created = await service_project.createProjectGroup(payload)
    upsert_group(created)
    return created
  }

  async function updateProjectGroup(payload: ProjectGroupUpdate): Promise<ProjectGroup> {
    const updated = await service_project.updateProjectGroup(payload)
    upsert_group(updated)
    return updated
  }

  async function deleteProjectGroup(rid: number): Promise<void> {
    await service_project.deleteProjectGroup(rid)
    const i = project_groups.value.findIndex((x) => x.rid === rid)
    if (0 <= i) project_groups.value.splice(i, 1)
  }

  // actions: projects.
  async function fetchProjects(): Promise<void> {
    if (inflight_projects) return inflight_projects
    is_loading_projects.value = true
    inflight_projects = (async () => {
      try {
        projects.value = await service_project.fetchProjects()
      } finally {
        is_loading_projects.value = false
        inflight_projects = null
      }
    })()
    return inflight_projects
  }

  async function createProject(payload: ProjectCreate): Promise<Project> {
    const created = await service_project.createProject(payload)
    await fetchProjects()
    return created
  }

  async function updateProject(payload: ProjectUpdate): Promise<Project> {
    const updated = await service_project.updateProject(payload)
    await fetchProjects()
    return updated
  }

  async function deleteProject(rid: number): Promise<void> {
    await service_project.deleteProject(rid)
    await fetchProjects()
  }

  //utils.
  function reset(): void {
    project_groups.value = []
    projects.value = []
  }

  return {
    // state
    project_groups,
    projects,
    is_loading_groups,
    is_loading_projects,

    // getters
    by_rid_group,
    by_rid_project,
    getGroupByRid,
    getProjectByRid,

    // actions
    fetchProjectGroups,
    createProjectGroup,
    updateProjectGroup,
    deleteProjectGroup,

    fetchProjects,
    createProject,
    updateProject,
    deleteProject,

    // utils
    reset,
  }
})
