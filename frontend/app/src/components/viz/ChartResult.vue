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

const companyLabel = (name: string, rid: number) => `Company: ${name} (${rid || 0})`
const projectLabel = (name: string, rid: number) => `Project: ${name || 'Unknown'} (${rid || 0})`
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
      name: companyLabel(company.name, company.rid),
      display: company.name,
      color: colorForCompany(company.rid),
    })
  })

  summary.projects.forEach((project) => {
    const id = `project-company:${project.rid}`
    nodes.set(id, {
      id,
      name: projectLabel(project.name, project.rid),
      display: '',
      color: colorForCompany(project.company_rid),
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
        name: projectLabel(item.project_name, item.project_rid),
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
  }> = []

  summary.companies.forEach((company) => {
    if (!company.amount) return
    links.push({
      source: 'root',
      target: `company:${company.rid}`,
      value: company.amount,
    })
  })

  summary.projects.forEach((project) => {
    if (!project.amount) return
    links.push({
      source: `company:${project.company_rid}`,
      target: `project-company:${project.rid}`,
      value: project.amount,
      projectName: project.name,
      projectRid: project.rid,
    })
  })

  summary.company_pm.forEach((item) => {
    if (!item.amount) return
    links.push({
      source: `project-company:${item.project_rid}`,
      target: `pm:${item.pm_rid}`,
      value: item.amount,
      projectName: item.project_name,
      projectRid: item.project_rid,
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
    })
    links.push({
      source: `project-pm:${item.project_rid}`,
      target: `pl:${item.pl_rid}`,
      value: item.amount,
      projectName: item.project_name,
      projectRid: item.project_rid,
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
  }))

  if (!links.length) return

  const paddingLeft = 160
  const paddingRight = 160
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

  graph.links.forEach((link: any) => {
    const path = document.createElementNS(ns, 'path')
    const d = linkPath(link)
    if (!d) return
    path.setAttribute('d', d)
    path.setAttribute('fill', 'none')
    const color = link.source?.color ?? '#888888'
    path.setAttribute('stroke', color)
    path.setAttribute('stroke-opacity', '0.22')
    path.setAttribute('stroke-width', `${Math.max(1, link.width ?? 1)}`)
    path.setAttribute('stroke-linecap', 'butt')

    const title = document.createElementNS(ns, 'title')
    const projectLabel = link.projectName
      ? ` (${link.projectName}${link.projectRid ? `#${link.projectRid}` : ''})`
      : ''
    title.textContent = `${link.source?.display ?? ''} → ${link.target?.display ?? ''}${projectLabel}: ${currencyFormatter.format(link.value ?? 0)}`
    path.appendChild(title)
    linkGroup.appendChild(path)
  })

  graph.nodes.forEach((node: any) => {
    const nodeId = String(node.id ?? '')
    const isProjectNode =
      nodeId.startsWith('project-company:') || nodeId.startsWith('project-pm:')
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
    nodeGroup.appendChild(rect)

    const label = document.createElementNS(ns, 'text')
    const xMid = (node.x0 + node.x1) / 2
    const yMid = node.y0 + (node.y1 - node.y0) / 2
    label.setAttribute('y', `${yMid}`)
    label.setAttribute('fill', '#d8d8d8')
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
      nodeGroup.appendChild(label)
    }
  })
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

.sankey-empty {
  position: absolute;
  inset: 0;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
