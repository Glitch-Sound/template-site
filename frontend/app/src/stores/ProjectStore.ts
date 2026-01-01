import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

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
import service_project from '@/services/ProjectService'

export const useProjectStore = defineStore('project', () => {
  // state.
  const project_groups = ref<ProjectGroup[]>([])
  const project_numbers = ref<ProjectNumber[]>([])
  const projects = ref<ProjectList[]>([])
  const condition = ref<SearchCondition>(defaultCondition())
  const project_targets = ref<TargetQuarter[]>([])
  const project_users = ref<User[]>([])

  const is_loading_groups = ref(false)
  const is_loading_numbers = ref(false)
  const is_loading_projects = ref(false)

  let inflight_groups: Promise<void> | null = null
  let inflight_numbers: Promise<void> | null = null
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

  // function upsertGroup(g: ProjectGroup) {
  //   const i = project_groups.value.findIndex((x) => x.rid === g.rid)
  //   if (i >= 0) project_groups.value[i] = g
  //   else project_groups.value.push(g)
  // }

  function setCondition(cond: SearchCondition) {
    condition.value = cond
  }

  function patchCondition(patch: Partial<SearchCondition>) {
    condition.value = { ...(condition.value ?? defaultCondition()), ...patch }
  }

  function clearCondition() {
    condition.value = defaultCondition()
  }

  function defaultCondition(): SearchCondition {
    return {
      target: [],
      rid_users_pm: [],
      rid_users_pl: [],
      is_none_pre_approval: false,
      is_none_number_m: false,
      is_none_number_s: false,
      is_none_number_o: false,
    }
  }

  async function fetchProjectTargets(): Promise<void> {
    project_targets.value = await service_project.fetchProjectTargets()
  }

  async function fetchProjectUsers(): Promise<void> {
    project_users.value = await service_project.fetchProjectUsers()
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
    // upsertGroup(created)
    fetchProjectGroups()
    return created
  }

  async function updateProjectGroup(payload: ProjectGroupUpdate): Promise<ProjectGroup> {
    const updated = await service_project.updateProjectGroup(payload)
    // upsertGroup(updated)
    fetchProjectGroups()
    return updated
  }

  async function deleteProjectGroup(rid: number): Promise<void> {
    await service_project.deleteProjectGroup(rid)
    const i = project_groups.value.findIndex((x) => x.rid === rid)
    if (0 <= i) project_groups.value.splice(i, 1)
  }

  // actions: numbers.
  async function fetchProjectNumbers(rid: number): Promise<void> {
    if (inflight_numbers) return inflight_numbers
    is_loading_numbers.value = true
    inflight_numbers = (async () => {
      try {
        project_numbers.value = await service_project.fetchProjectNumbers(rid)
      } finally {
        is_loading_numbers.value = false
        inflight_numbers = null
      }
    })()
    return inflight_numbers
  }

  async function createProjectNumber(payload: ProjectNumberCreate): Promise<ProjectNumber> {
    // for batch.
    return await service_project.createProjectNumber(payload)
  }

  async function updateProjectNumber(payload: ProjectNumberUpdate): Promise<ProjectNumber> {
    // for batch.
    return await service_project.updateProjectNumber(payload)
  }

  async function deleteProjectNumber(rid: number): Promise<void> {
    // for batch.
    await service_project.deleteProjectNumber(rid)
  }

  // actions: projects.
  async function fetchProjects(): Promise<void> {
    if (inflight_projects) return inflight_projects

    is_loading_projects.value = true
    inflight_projects = (async () => {
      try {
        projects.value = await service_project.fetchProjects(condition.value)
        await fetchProjectTargets()
        await fetchProjectUsers()
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
  async function initSearchCondition(): Promise<void> {
    await fetchProjectTargets()
    await fetchProjectUsers()
    const condition = await service_project.fetchProjectCondition()
    patchCondition(condition)
  }

  function reset(): void {
    project_groups.value = []
    projects.value = []
    condition.value = defaultCondition()
  }

  return {
    // state
    project_groups,
    project_numbers,
    projects,
    condition,
    project_targets,
    project_users,
    is_loading_groups,
    is_loading_numbers,
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
    fetchProjectNumbers,
    createProjectNumber,
    updateProjectNumber,
    deleteProjectNumber,
    setCondition,
    patchCondition,
    clearCondition,
    defaultCondition,
    fetchProjects,
    createProject,
    updateProject,
    deleteProject,

    // utils
    initSearchCondition,
    reset,
  }
})
