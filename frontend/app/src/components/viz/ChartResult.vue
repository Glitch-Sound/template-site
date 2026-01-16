<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { sankey as d3Sankey, sankeyJustify, sankeyLinkHorizontal } from 'd3-sankey'
import { chartPalette } from '@/constants/chartPalette'
import { useSummaryStore } from '@/stores/SummaryStore'

const summaryStore = useSummaryStore()
const primaryColor = ref('#2196f3')
const sankeySvg = ref<SVGSVGElement | null>(null)
const sankeyWrap = ref<HTMLElement | null>(null)
const wrapSize = ref({ width: 0, height: 0 })
const tooltip = ref({ visible: false, x: 0, y: 0, text: '' })
const selectedLink = ref<{
  key: string
  type:
    | 'root-company'
    | 'company-project-group'
    | 'project-group-pm'
    | 'pm-project'
    | 'project-pl'
  companyRid?: number
  projectGroupRid?: number
  pmRid?: number
  projectRid?: number
  plRid?: number
} | null>(null)
let resizeObserver: ResizeObserver | null = null

onMounted(async () => {
  await summaryStore.fetchSummariesSankey()
  const primary = getComputedStyle(document.documentElement)
    .getPropertyValue('--v-theme-primary')
    .trim()
  if (primary) {
    primaryColor.value = primary.includes(',') ? `rgb(${primary})` : primary
  }
})

const sankeySummary = computed(() => summaryStore.summaries_sankey)

const currencyFormatter = new Intl.NumberFormat('ja-JP', {
  style: 'currency',
  currency: 'JPY',
  maximumFractionDigits: 0,
})

const rootLabel = computed(() => {
  const year = sankeySummary.value?.year
  return year ? `Total ${year}` : 'Total'
})

const companyLabel = (name: string) => `${name}`
const projectLabel = (name: string) => `${name || 'Unknown'}`
const pmLabel = (name: string, rid: number) => `PM: ${name || 'Unknown'} (${rid || 0})`
const plLabel = (name: string, rid: number) => `PL: ${name || 'Unknown'} (${rid || 0})`

const colorForCompany = (rid: number) => {
  const index = Math.abs(rid) % chartPalette.length
  return chartPalette[index] ?? '#9c9c9c'
}

const colorForPerson = (rid: number) => {
  if (!rid) return '#7a7a7a'
  const hue = (Math.abs(rid) * 137.508) % 360
  return `hsl(${hue}, 55%, 55%)`
}

const metricsByNode = computed(() => {
  const summary = sankeySummary.value
  const empty = {
    totalAmount: 0,
    company: new Map<number, { amount: number; projectCount: number }>(),
    pm: new Map<number, { amount: number; projectCount: number }>(),
    pl: new Map<number, { amount: number; projectCount: number }>(),
  }
  if (!summary) return empty

  const company = new Map<number, { amount: number; projectCount: number }>()
  const pm = new Map<number, { amount: number; projectCount: number }>()
  const pl = new Map<number, { amount: number; projectCount: number }>()
  const companyCounts = new Map(
    summary.company_project_counts.map((row) => [row.rid, row.project_count]),
  )
  const pmCounts = new Map(summary.pm_project_counts.map((row) => [row.rid, row.project_count]))
  const plCounts = new Map(summary.pl_project_counts.map((row) => [row.rid, row.project_count]))

  summary.project_groups.forEach((projectGroup) => {
    if (!projectGroup.company_rid) return
    const entry = company.get(projectGroup.company_rid) ?? {
      amount: 0,
      projectCount: companyCounts.get(projectGroup.company_rid) ?? 0,
    }
    entry.amount += projectGroup.amount
    company.set(projectGroup.company_rid, entry)
  })

  summary.company_pm.forEach((item) => {
    if (!item.pm_rid) return
    const entry = pm.get(item.pm_rid) ?? {
      amount: 0,
      projectCount: pmCounts.get(item.pm_rid) ?? 0,
    }
    entry.amount += item.amount
    pm.set(item.pm_rid, entry)
  })

  summary.pm_pl.forEach((item) => {
    if (!item.pl_rid) return
    const entry = pl.get(item.pl_rid) ?? {
      amount: 0,
      projectCount: plCounts.get(item.pl_rid) ?? 0,
    }
    entry.amount += item.amount
    pl.set(item.pl_rid, entry)
  })

  return {
    totalAmount: summary.total_amount ?? 0,
    projectGroups: new Map(
      summary.project_groups.map((group) => [
        group.rid,
        { amount: group.amount, projectCount: group.project_count },
      ]),
    ),
    company,
    pm,
    pl,
  }
})

const sankeyIndex = computed(() => {
  const summary = sankeySummary.value
  if (!summary) return null

  const projectGroupById = new Map<number, { companyRid: number }>()
  const projectGroupsByCompany = new Map<number, Set<number>>()
  summary.project_groups.forEach((group) => {
    projectGroupById.set(group.rid, { companyRid: group.company_rid })
    const set = projectGroupsByCompany.get(group.company_rid) ?? new Set<number>()
    set.add(group.rid)
    projectGroupsByCompany.set(group.company_rid, set)
  })

  const projectGroupsByPm = new Map<number, Set<number>>()
  const pmsByProjectGroup = new Map<number, Set<number>>()
  summary.company_pm.forEach((item) => {
    const pmSet = projectGroupsByPm.get(item.pm_rid) ?? new Set<number>()
    pmSet.add(item.project_group_rid)
    projectGroupsByPm.set(item.pm_rid, pmSet)

    const groupSet = pmsByProjectGroup.get(item.project_group_rid) ?? new Set<number>()
    groupSet.add(item.pm_rid)
    pmsByProjectGroup.set(item.project_group_rid, groupSet)
  })

  const projectGroupByProject = new Map<number, number>()
  const projectsByProjectGroup = new Map<number, Set<number>>()
  const projectsByPm = new Map<number, Set<number>>()
  const projectsByPl = new Map<number, Set<number>>()
  const pmByProject = new Map<number, number>()
  const plByProject = new Map<number, number>()
  summary.pm_pl.forEach((item) => {
    projectGroupByProject.set(item.project_rid, item.project_group_rid)
    pmByProject.set(item.project_rid, item.pm_rid)
    plByProject.set(item.project_rid, item.pl_rid)

    const groupProjects = projectsByProjectGroup.get(item.project_group_rid) ?? new Set<number>()
    groupProjects.add(item.project_rid)
    projectsByProjectGroup.set(item.project_group_rid, groupProjects)

    const pmProjects = projectsByPm.get(item.pm_rid) ?? new Set<number>()
    pmProjects.add(item.project_rid)
    projectsByPm.set(item.pm_rid, pmProjects)

    const plProjects = projectsByPl.get(item.pl_rid) ?? new Set<number>()
    plProjects.add(item.project_rid)
    projectsByPl.set(item.pl_rid, plProjects)
  })

  return {
    projectGroupById,
    projectGroupsByCompany,
    projectGroupsByPm,
    pmsByProjectGroup,
    projectGroupByProject,
    projectsByProjectGroup,
    projectsByPm,
    projectsByPl,
    pmByProject,
    plByProject,
  }
})

const nodeRegistry = computed(() => {
  const summary = sankeySummary.value
  const nodes = new Map<string, { id: string; name: string; color: string; display: string }>()
  nodes.set('root', {
    id: 'root',
    name: rootLabel.value,
    display: rootLabel.value,
    color: primaryColor.value,
  })
  if (!summary) return nodes

  summary.companies.forEach((company) => {
    const id = `company:${company.rid}`
    nodes.set(id, {
      id,
      name: companyLabel(company.name),
      display: company.name,
      color: colorForCompany(company.rid),
    })
  })

  summary.project_groups.forEach((projectGroup) => {
    const id = `project-company:${projectGroup.rid}`
    nodes.set(id, {
      id,
      name: projectLabel(projectGroup.name),
      display: '',
      color: colorForCompany(projectGroup.company_rid),
    })
  })

  summary.company_pm.forEach((item) => {
    const id = `pm:${item.pm_rid}`
    if (nodes.has(id)) return
    nodes.set(id, {
      id,
      name: pmLabel(item.pm_name, item.pm_rid),
      display: `PM ${item.pm_name || 'Unknown'}`,
      color: colorForPerson(item.pm_rid),
    })
  })

  summary.pm_pl.forEach((item) => {
    const projectId = `project-pm:${item.project_rid}`
    if (!nodes.has(projectId)) {
      nodes.set(projectId, {
        id: projectId,
        name: projectLabel(item.project_name),
        display: '',
        color: colorForPerson(item.pm_rid),
      })
    }

    const id = `pl:${item.pl_rid}`
    if (nodes.has(id)) return
    nodes.set(id, {
      id,
      name: plLabel(item.pl_name, item.pl_rid),
      display: `PL ${item.pl_name || 'Unknown'}`,
      color: colorForPerson(item.pl_rid),
    })
  })

  return nodes
})

const sankeyLinks = computed(() => {
  const summary = sankeySummary.value
  if (!summary) return []

  const links: Array<{
    source: string
    target: string
    value: number
    projectName?: string
    projectRid?: number
    projectGroupRid?: number
  }> = []

  summary.companies.forEach((company) => {
    if (!company.amount) return
    links.push({
      source: 'root',
      target: `company:${company.rid}`,
      value: company.amount,
    })
  })

  summary.project_groups.forEach((projectGroup) => {
    if (!projectGroup.amount) return
    links.push({
      source: `company:${projectGroup.company_rid}`,
      target: `project-company:${projectGroup.rid}`,
      value: projectGroup.amount,
      projectName: projectGroup.name,
      projectRid: projectGroup.rid,
      projectGroupRid: projectGroup.rid,
    })
  })

  summary.company_pm.forEach((item) => {
    if (!item.amount) return
    links.push({
      source: `project-company:${item.project_group_rid}`,
      target: `pm:${item.pm_rid}`,
      value: item.amount,
      projectName: item.project_group_name,
      projectRid: item.project_group_rid,
      projectGroupRid: item.project_group_rid,
    })
  })

  summary.pm_pl.forEach((item) => {
    if (!item.amount) return
    links.push({
      source: `pm:${item.pm_rid}`,
      target: `project-pm:${item.project_rid}`,
      value: item.amount,
      projectName: item.project_name,
      projectRid: item.project_rid,
      projectGroupRid: item.project_group_rid,
    })
    links.push({
      source: `project-pm:${item.project_rid}`,
      target: `pl:${item.pl_rid}`,
      value: item.amount,
      projectName: item.project_name,
      projectRid: item.project_rid,
      projectGroupRid: item.project_group_rid,
    })
  })

  return links
})

const renderSankey = () => {
  const svg = sankeySvg.value
  const size = wrapSize.value
  const nodesMap = nodeRegistry.value
  if (!svg || !size.width || !size.height || !nodesMap.size) return

  while (svg.firstChild) {
    svg.removeChild(svg.firstChild)
  }

  const ns = 'http://www.w3.org/2000/svg'
  const width = size.width
  const height = size.height
  svg.setAttribute('width', `${width}`)
  svg.setAttribute('height', `${height}`)

  const nodes = Array.from(nodesMap.values()).map((node) => ({
    id: node.id,
    name: node.name,
    display: node.display,
    color: node.color,
  }))

  const links = sankeyLinks.value.map((link) => ({
    source: link.source,
    target: link.target,
    value: link.value,
    projectName: link.projectName,
    projectRid: link.projectRid,
    projectGroupRid: link.projectGroupRid,
  }))

  if (!links.length) return

  const paddingLeft = 80
  const paddingRight = 80
  const paddingTop = 20
  const paddingBottom = 36
  const layout = d3Sankey()
    .nodeId((d: { id: string }) => d.id)
    .nodeWidth(18)
    .nodePadding(18)
    .nodeAlign(sankeyJustify)
    .extent([
      [paddingLeft, paddingTop],
      [width - paddingRight, height - paddingBottom],
    ])

  const graph = layout({
    nodes: nodes.map((node) => ({ ...node })),
    links: links.map((link) => ({ ...link })),
  })

  const linkGroup = document.createElementNS(ns, 'g')
  const nodeGroup = document.createElementNS(ns, 'g')
  svg.appendChild(linkGroup)
  svg.appendChild(nodeGroup)

  const linkPath = sankeyLinkHorizontal()
  const centerX = width / 2
  const leftEdge = paddingLeft + (width - paddingLeft - paddingRight) * 0.35
  const rightEdge = paddingLeft + (width - paddingLeft - paddingRight) * 0.65
  const shiftByType = [
    { prefix: 'company:', shift: 8 },
    { prefix: 'project-company:', shift: -6 },
    { prefix: 'pm:', shift: -10 },
    { prefix: 'project-pm:', shift: -12 },
    { prefix: 'pl:', shift: -10 },
  ]

  graph.nodes.forEach((node: any) => {
    const nodeId = String(node.id ?? '')
    const match = shiftByType.find((entry) => nodeId.startsWith(entry.prefix))
    if (!match) return
    node.x0 += match.shift
    node.x1 += match.shift
  })

  const index = sankeyIndex.value
  const selection = selectedLink.value
  const parseRid = (id: string) => Number(id.split(':')[1] ?? 0)
  const addAll = (target: Set<number>, source?: Set<number>) => {
    if (!source) return
    source.forEach((value) => target.add(value))
  }
  const collectCompaniesFromGroups = (groupIds: Set<number>) => {
    const companies = new Set<number>()
    if (!index) return companies
    groupIds.forEach((groupId) => {
      const companyRid = index.projectGroupById.get(groupId)?.companyRid
      if (companyRid) companies.add(companyRid)
    })
    return companies
  }
  const collectGroupsFromProjects = (projectIds: Set<number>) => {
    const groups = new Set<number>()
    if (!index) return groups
    projectIds.forEach((projectId) => {
      const groupId = index.projectGroupByProject.get(projectId)
      if (groupId) groups.add(groupId)
    })
    return groups
  }
  const collectPmsFromProjects = (projectIds: Set<number>) => {
    const pms = new Set<number>()
    if (!index) return pms
    projectIds.forEach((projectId) => {
      const pmRid = index.pmByProject.get(projectId)
      if (pmRid) pms.add(pmRid)
    })
    return pms
  }
  const collectPlsFromProjects = (projectIds: Set<number>) => {
    const pls = new Set<number>()
    if (!index) return pls
    projectIds.forEach((projectId) => {
      const plRid = index.plByProject.get(projectId)
      if (plRid) pls.add(plRid)
    })
    return pls
  }

  let selectionSets:
    | {
        companyRids?: Set<number>
        projectGroupRids?: Set<number>
        pmRids?: Set<number>
        projectRids?: Set<number>
        plRids?: Set<number>
      }
    | null = null

  if (selection && index) {
    if (selection.type === 'root-company' && selection.companyRid) {
      const companyRids = new Set([selection.companyRid])
      const projectGroupRids = index.projectGroupsByCompany.get(selection.companyRid) ?? new Set()
      const projectRids = new Set<number>()
      projectGroupRids.forEach((groupId) => {
        addAll(projectRids, index.projectsByProjectGroup.get(groupId))
      })
      selectionSets = {
        companyRids,
        projectGroupRids,
        projectRids,
      }
    } else if (selection.type === 'company-project-group' && selection.projectGroupRid) {
      const projectGroupRids = new Set([selection.projectGroupRid])
      const companyRids = collectCompaniesFromGroups(projectGroupRids)
      const projectRids = new Set<number>()
      projectGroupRids.forEach((groupId) => {
        addAll(projectRids, index.projectsByProjectGroup.get(groupId))
      })
      selectionSets = {
        companyRids,
        projectGroupRids,
        projectRids,
      }
    } else if (selection.type === 'project-group-pm' && selection.pmRid) {
      const pmRids = new Set([selection.pmRid])
      const projectGroupRids = index.projectGroupsByPm.get(selection.pmRid) ?? new Set()
      const projectRids = index.projectsByPm.get(selection.pmRid) ?? new Set()
      const companyRids = collectCompaniesFromGroups(projectGroupRids)
      selectionSets = {
        companyRids,
        projectGroupRids,
        pmRids,
        projectRids,
      }
    } else if (selection.type === 'pm-project' && selection.projectRid) {
      const projectRids = new Set([selection.projectRid])
      const projectGroupRids = collectGroupsFromProjects(projectRids)
      const companyRids = collectCompaniesFromGroups(projectGroupRids)
      const pmRids = selection.pmRid ? new Set([selection.pmRid]) : collectPmsFromProjects(projectRids)
      const plRids = collectPlsFromProjects(projectRids)
      selectionSets = {
        companyRids,
        projectGroupRids,
        pmRids,
        projectRids,
        plRids,
      }
    } else if (selection.type === 'project-pl' && selection.plRid) {
      const plRids = new Set([selection.plRid])
      const projectRids = index.projectsByPl.get(selection.plRid) ?? new Set()
      const projectGroupRids = collectGroupsFromProjects(projectRids)
      const companyRids = collectCompaniesFromGroups(projectGroupRids)
      const pmRids = collectPmsFromProjects(projectRids)
      selectionSets = {
        companyRids,
        projectGroupRids,
        pmRids,
        projectRids,
        plRids,
      }
    }
  }

  const linkKeyMap = new Map<any, string>()
  graph.links.forEach((link: any) => {
    const sourceId = String(link.source?.id ?? '')
    const targetId = String(link.target?.id ?? '')
    const linkKey = `${sourceId}|${targetId}|${link.projectRid ?? ''}|${link.value ?? ''}`
    linkKeyMap.set(link, linkKey)
  })

  const activeLinkKeys = new Set<string>()
  const activeNodeIds = new Set<string>()

  graph.links.forEach((link: any) => {
    const sourceId = String(link.source?.id ?? '')
    const targetId = String(link.target?.id ?? '')
    const sourceRid = parseRid(sourceId)
    const targetRid = parseRid(targetId)
    const linkKey = linkKeyMap.get(link) ?? ''
    const projectGroupRid = link.projectGroupRid ?? 0
    const projectRid = link.projectRid ?? 0
    let linkType: 'root-company' | 'company-project-group' | 'project-group-pm' | 'pm-project' | 'project-pl' =
      'root-company'
    let pmRid = 0
    let plRid = 0
    let companyRid = 0
    if (sourceId === 'root' && targetId.startsWith('company:')) {
      linkType = 'root-company'
      companyRid = targetRid
    } else if (sourceId.startsWith('company:') && targetId.startsWith('project-company:')) {
      linkType = 'company-project-group'
      companyRid = sourceRid
    } else if (sourceId.startsWith('project-company:') && targetId.startsWith('pm:')) {
      linkType = 'project-group-pm'
      pmRid = targetRid
    } else if (sourceId.startsWith('pm:') && targetId.startsWith('project-pm:')) {
      linkType = 'pm-project'
      pmRid = sourceRid
    } else if (sourceId.startsWith('project-pm:') && targetId.startsWith('pl:')) {
      linkType = 'project-pl'
      plRid = targetRid
    }

    const inSet = (set: Set<number> | undefined, value: number) => !set || set.has(value)
    const isActive = (() => {
      if (!selectionSets) return true
      if (linkType === 'root-company') {
        return inSet(selectionSets.companyRids, companyRid)
      }
      if (linkType === 'company-project-group') {
        return inSet(selectionSets.projectGroupRids, projectGroupRid)
      }
      if (linkType === 'project-group-pm') {
        return (
          inSet(selectionSets.projectGroupRids, projectGroupRid) &&
          inSet(selectionSets.pmRids, pmRid)
        )
      }
      if (linkType === 'pm-project') {
        return (
          inSet(selectionSets.projectRids, projectRid) && inSet(selectionSets.pmRids, pmRid)
        )
      }
      return (
        inSet(selectionSets.projectRids, projectRid) && inSet(selectionSets.plRids, plRid)
      )
    })()

    if (isActive) {
      activeLinkKeys.add(linkKey)
      activeNodeIds.add(sourceId)
      activeNodeIds.add(targetId)
    }

    const path = document.createElementNS(ns, 'path')
    const d = linkPath(link)
    if (!d) return
    path.setAttribute('d', d)
    path.setAttribute('fill', 'none')
    const color = link.source?.color ?? '#888888'
    path.setAttribute('stroke', color)
    if (selectionSets) {
      path.style.strokeOpacity = '0.3'
      path.dataset.fadeToStroke = isActive ? '0.3' : '0.03'
    } else {
      path.style.strokeOpacity = '0.3'
      delete path.dataset.fadeToStroke
    }
    path.setAttribute('stroke-width', `${Math.max(1, link.width ?? 1)}`)
    path.setAttribute('stroke-linecap', 'butt')
    path.style.transition = 'stroke-opacity 10ms ease'

    const targetName = (link.target?.display ?? link.target?.name ?? '').trim()
    const projectName = (link.projectName ?? '').trim()
    const tooltipLabel = (() => {
      if (sourceId === 'root' && targetId.startsWith('company:')) return targetName
      if (sourceId.startsWith('company:') && targetId.startsWith('project-company:'))
        return projectName || targetName
      if (sourceId.startsWith('project-company:') && targetId.startsWith('pm:'))
        return targetName.replace(/^PM\\s*/, '')
      if (sourceId.startsWith('pm:') && targetId.startsWith('project-pm:'))
        return projectName || targetName
      if (sourceId.startsWith('project-pm:') && targetId.startsWith('pl:')) {
        const plName = targetName.replace(/^PL\\s*/, '')
        return projectName ? `${projectName}: ${plName}` : plName
      }
      return targetName
    })()
    const tooltipText = `${tooltipLabel}: ${currencyFormatter.format(link.value ?? 0)}`

    path.addEventListener('mouseenter', (event) => {
      const wrap = sankeyWrap.value
      if (!wrap) return
      const rect = wrap.getBoundingClientRect()
      tooltip.value = {
        visible: true,
        x: event.clientX - rect.left + 12,
        y: event.clientY - rect.top + 12,
        text: tooltipText,
      }
    })
    path.addEventListener('mousemove', (event) => {
      const wrap = sankeyWrap.value
      if (!wrap) return
      const rect = wrap.getBoundingClientRect()
      tooltip.value = {
        ...tooltip.value,
        x: event.clientX - rect.left + 12,
        y: event.clientY - rect.top + 12,
      }
    })
    path.addEventListener('mouseleave', () => {
      tooltip.value = { ...tooltip.value, visible: false }
    })
    path.addEventListener('click', () => {
      let selectionInfo: typeof selectedLink.value = null
      if (linkType === 'root-company') {
        selectionInfo = { key: linkKey, type: linkType, companyRid }
      } else if (linkType === 'company-project-group') {
        selectionInfo = { key: linkKey, type: linkType, projectGroupRid }
      } else if (linkType === 'project-group-pm') {
        selectionInfo = { key: linkKey, type: linkType, pmRid }
      } else if (linkType === 'pm-project') {
        selectionInfo = { key: linkKey, type: linkType, pmRid, projectRid }
      } else if (linkType === 'project-pl') {
        selectionInfo = { key: linkKey, type: linkType, plRid }
      }
      selectedLink.value =
        selectedLink.value && selectedLink.value.key === linkKey ? null : selectionInfo
      renderSankey()
    })

    linkGroup.appendChild(path)
  })

  graph.nodes.forEach((node: any) => {
    const nodeId = String(node.id ?? '')
    const isProjectNode = nodeId.startsWith('project-company:') || nodeId.startsWith('project-pm:')
    const fullWidth = node.x1 - node.x0
    const targetWidth = isProjectNode ? 8 : fullWidth
    const widthDiff = Math.max(0, fullWidth - targetWidth)
    const x0 = node.x0 + widthDiff / 2
    const x1 = node.x1 - widthDiff / 2
    const rect = document.createElementNS(ns, 'rect')
    rect.setAttribute('x', `${x0}`)
    rect.setAttribute('y', `${node.y0}`)
    rect.setAttribute('width', `${Math.max(2, x1 - x0)}`)
    rect.setAttribute('height', `${Math.max(2, node.y1 - node.y0)}`)
    rect.setAttribute('fill', node.color ?? '#888888')
    rect.setAttribute('rx', '2')
    if (selectionSets) {
      rect.style.opacity = activeNodeIds.has(nodeId) ? '1' : '0.6'
      rect.dataset.fadeTo = activeNodeIds.has(nodeId) ? '1' : '0.12'
    } else {
      rect.style.opacity = '1'
      delete rect.dataset.fadeTo
    }
    rect.style.transition = 'opacity 10ms ease'
    nodeGroup.appendChild(rect)

    const label = document.createElementNS(ns, 'text')
    const xMid = (node.x0 + node.x1) / 2
    const yMid = node.y0 + (node.y1 - node.y0) / 2
    label.setAttribute('y', `${yMid}`)
    label.setAttribute('fill', '#efefef')
    label.setAttribute('font-size', '12')
    label.setAttribute('dominant-baseline', 'middle')

    if (nodeId.startsWith('pm:')) {
      label.setAttribute('x', `${node.x1 + 12}`)
      label.setAttribute('text-anchor', 'start')
    } else if (node.x0 < leftEdge) {
      label.setAttribute('x', `${node.x0 - 12}`)
      label.setAttribute('text-anchor', 'end')
    } else if (node.x0 > rightEdge) {
      label.setAttribute('x', `${node.x1 + 12}`)
      label.setAttribute('text-anchor', 'start')
    } else {
      label.setAttribute('x', `${centerX}`)
      label.setAttribute('text-anchor', 'middle')
    }
    const text = (node.display ?? node.name ?? '').trim()
    if (text) {
      label.textContent = text
      if (selectionSets) {
        label.style.opacity = activeNodeIds.has(nodeId) ? '1' : '0.6'
        label.dataset.fadeTo = activeNodeIds.has(nodeId) ? '1' : '0.12'
      } else {
        label.style.opacity = '1'
        delete label.dataset.fadeTo
      }
      label.style.transition = 'opacity 10ms ease'
      nodeGroup.appendChild(label)
    }

    const metrics = metricsByNode.value
    const ridPart = Number(nodeId.split(':')[1] ?? 0)
    let metricSource: { amount: number; projectCount: number } | undefined
    let metricAnchor: { x: number; align: 'start' | 'end' } | null = null
    if (nodeId.startsWith('company:')) {
      metricSource = metrics.company.get(ridPart)
      metricAnchor = { x: node.x1 + 12, align: 'start' }
    } else if (nodeId.startsWith('pm:')) {
      metricSource = metrics.pm.get(ridPart)
      metricAnchor = { x: node.x0 - 12, align: 'end' }
    } else if (nodeId.startsWith('pl:')) {
      metricSource = metrics.pl.get(ridPart)
      metricAnchor = { x: node.x0 - 12, align: 'end' }
    }

    if (metricSource && metricAnchor) {
      const percent = metrics.totalAmount ? (metricSource.amount / metrics.totalAmount) * 100 : 0
      const projectCount = metricSource.projectCount
      const metricText = `${percent.toFixed(1)}% (${projectCount}PJ)`
      const metricLabel = document.createElementNS(ns, 'text')
      metricLabel.setAttribute('x', `${metricAnchor.x}`)
      metricLabel.setAttribute('y', `${yMid}`)
      metricLabel.setAttribute('fill', '#efefef')
      metricLabel.setAttribute('font-size', '11')
      metricLabel.setAttribute('dominant-baseline', 'middle')
      metricLabel.setAttribute('text-anchor', metricAnchor.align)
      metricLabel.textContent = metricText
      if (selectionSets) {
        metricLabel.style.opacity = activeNodeIds.has(nodeId) ? '1' : '0.6'
        metricLabel.dataset.fadeTo = activeNodeIds.has(nodeId) ? '1' : '0.12'
      } else {
        metricLabel.style.opacity = '1'
        delete metricLabel.dataset.fadeTo
      }
      metricLabel.style.transition = 'opacity 10ms ease'
      nodeGroup.appendChild(metricLabel)
    }

  })

  if (selectionSets) {
    requestAnimationFrame(() => {
      const svgEl = sankeySvg.value
      if (!svgEl) return
      svgEl.querySelectorAll<SVGElement>('[data-fade-to]').forEach((element) => {
        const target = element.dataset.fadeTo
        if (target) {
          element.style.opacity = target
        }
      })
      svgEl.querySelectorAll<SVGElement>('[data-fade-to-stroke]').forEach((element) => {
        const target = element.dataset.fadeToStroke
        if (target) {
          element.style.strokeOpacity = target
        }
      })
    })
  }
}

const updateSize = () => {
  if (!sankeyWrap.value) return
  wrapSize.value = {
    width: Math.max(0, sankeyWrap.value.clientWidth),
    height: Math.max(0, sankeyWrap.value.clientHeight),
  }
}

watch([sankeySummary, wrapSize], () => {
  renderSankey()
})

onMounted(() => {
  updateSize()
  if (sankeyWrap.value) {
    resizeObserver = new ResizeObserver(() => {
      updateSize()
    })
    resizeObserver.observe(sankeyWrap.value)
  }
})

onBeforeUnmount(() => {
  resizeObserver?.disconnect()
  resizeObserver = null
})
</script>

<template>
  <v-card class="viz-card viz-card--tall company-card sankey-card" rounded="xl" variant="tonal">
    <v-card-title class="text-subtitle-2 font-weight-medium"> Results </v-card-title>

    <v-card-text class="pa-3 viz-card-text sankey-body">
      <div ref="sankeyWrap" class="sankey-wrap">
        <svg ref="sankeySvg" class="sankey-svg" role="img" aria-label="Sankey diagram" />
        <div
          v-if="tooltip.visible"
          class="sankey-tooltip"
          :style="{ left: `${tooltip.x}px`, top: `${tooltip.y}px` }"
        >
          {{ tooltip.text }}
        </div>
      </div>
    </v-card-text>
  </v-card>
</template>

<style scoped>
@import './viz.css';

.sankey-card {
  height: 100%;
}

.sankey-body {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.sankey-header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 12px;
}

.sankey-total {
  font-size: 18px;
  font-weight: 600;
}

.sankey-wrap {
  position: relative;
  width: 100%;
  flex: 1;
  min-height: 0;
}

.sankey-svg {
  width: 100%;
  height: 100%;
}

.sankey-tooltip {
  position: absolute;
  z-index: 2;
  padding: 6px 8px;
  border-radius: 6px;
  background: rgba(6, 6, 6, 0.95);
  color: #efefef;
  font-size: 12px;
  pointer-events: none;
  white-space: nowrap;
}

.sankey-empty {
  position: absolute;
  inset: 0;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
