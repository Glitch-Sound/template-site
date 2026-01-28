<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { sankey, sankeyLinkHorizontal } from 'd3-sankey'
import { chartPalette } from '@/constants/chartPalette'
import { useSummaryStore } from '@/stores/SummaryStore'
import type { SankeySummary } from '@/types/Summary'

type NodeType = 'root' | 'company' | 'project-group' | 'pm' | 'project' | 'pl'

type LinkKind =
  | 'root-company'
  | 'company-project-group'
  | 'project-group-pm'
  | 'pm-project'
  | 'project-pl'

interface NodeDatum {
  id: string
  name: string
  type: NodeType
  rid?: number
  projectCount?: number
}

interface LinkDatum {
  id: string
  source: string
  target: string
  value: number
  kind: LinkKind
  meta: {
    companyName?: string
    projectGroupName?: string
    pmName?: string
    plName?: string
    projectName?: string
  }
}

interface NodeRender extends NodeDatum {
  x0: number
  x1: number
  y0: number
  y1: number
  value: number
  color: string
  labelLeft: string | null
  labelRight: string | null
  labelY: number
  labelLeftX: number
  labelRightX: number
  showLeft: boolean
  showRight: boolean
}

interface LinkRender extends LinkDatum {
  path: string
  width: number
  gradientId: string
  sourceNodeId: string
  targetNodeId: string
  sourceColor: string
  targetColor: string
  gradientX1: number
  gradientX2: number
}

const summaryStore = useSummaryStore()

const periodOptions = [
  { value: 'year', label: 'YEAR' },
  { value: 'h1', label: 'H1' },
  { value: 'h2', label: 'H2' },
  { value: 'q1', label: 'Q1' },
  { value: 'q2', label: 'Q2' },
  { value: 'q3', label: 'Q3' },
  { value: 'q4', label: 'Q4' },
] as const

const selectedPeriod = ref<string>('year')
const containerRef = ref<HTMLDivElement | null>(null)
const svgRef = ref<SVGSVGElement | null>(null)
const size = ref({ width: 0, height: 0 })
const layoutNodes = ref<NodeRender[]>([])
const layoutLinks = ref<LinkRender[]>([])
const selectedLinkId = ref<string | null>(null)
const selectedNodeId = ref<string | null>(null)
const highlightedNodes = ref<Set<string>>(new Set())
const highlightedLinks = ref<Set<string>>(new Set())
const tooltip = ref({ visible: false, x: 0, y: 0, text: '' })

const currencyFormatter = new Intl.NumberFormat('ja-JP', {
  style: 'currency',
  currency: 'JPY',
  maximumFractionDigits: 0,
})

const formatCurrency = (value: number) => currencyFormatter.format(value)

const periodLabel = (summary: SankeySummary | null, period: string) => {
  if (!summary) return ''
  const year = summary.year
  const suffix = period.toUpperCase()
  return period === 'year' ? `${year}` : `${year} ${suffix}`
}

const companyPalette = chartPalette.filter((color) => color.toLowerCase() !== '#ffffff')

const companyColor = (rid?: number) => {
  if (!rid || companyPalette.length === 0) return '#5c5c5c'
  return companyPalette[rid % companyPalette.length] ?? '#5c5c5c'
}

const personColor = (rid?: number) => {
  const safeRid = rid ?? 0
  const hue = (safeRid * 137) % 360
  return `hsl(${hue} 55% 46%)`
}

const nodeColor = (node: NodeDatum) => {
  switch (node.type) {
    case 'root':
      return '#5a5a5a'
    case 'company':
      return companyColor(node.rid)
    case 'project-group':
      return '#3c3c3c'
    case 'pm':
    case 'pl':
      return personColor(node.rid)
    case 'project':
      return '#4a4a4a'
    default:
      return '#5a5a5a'
  }
}

const labelConfig = (node: NodeDatum, percentLabel: string) => {
  switch (node.type) {
    case 'root':
      return { left: node.name, right: percentLabel }
    case 'company':
      return { left: node.name, right: percentLabel }
    case 'pm':
      return { left: percentLabel, right: node.name }
    case 'pl':
      return { left: percentLabel, right: node.name }
    default:
      return { left: null, right: null }
  }
}

const buildGraphData = (summary: SankeySummary, rootName: string) => {
  const nodes: NodeDatum[] = []
  const links: LinkDatum[] = []
  const nodeMap = new Map<string, NodeDatum>()

  const addNode = (node: NodeDatum) => {
    if (nodeMap.has(node.id)) return
    nodeMap.set(node.id, node)
    nodes.push(node)
  }

  addNode({
    id: 'root',
    name: rootName,
    type: 'root',
    projectCount: summary.project_groups.reduce((acc, group) => acc + group.project_count, 0),
  })

  const companyCounts = new Map<number, number>()
  summary.company_project_counts.forEach((item) => companyCounts.set(item.rid, item.project_count))

  const pmCounts = new Map<number, number>()
  summary.pm_project_counts.forEach((item) => pmCounts.set(item.rid, item.project_count))

  const plCounts = new Map<number, number>()
  summary.pl_project_counts.forEach((item) => plCounts.set(item.rid, item.project_count))

  summary.companies.forEach((company) => {
    addNode({
      id: `company-${company.rid}`,
      name: company.name,
      type: 'company',
      rid: company.rid,
      projectCount: companyCounts.get(company.rid) ?? 0,
    })

    links.push({
      id: `root-company-${company.rid}`,
      source: 'root',
      target: `company-${company.rid}`,
      value: company.amount,
      kind: 'root-company',
      meta: { companyName: company.name },
    })
  })

  summary.project_groups.forEach((group) => {
    addNode({
      id: `project-group-${group.rid}`,
      name: group.name,
      type: 'project-group',
      rid: group.rid,
      projectCount: group.project_count,
    })

    links.push({
      id: `company-project-group-${group.company_rid}-${group.rid}`,
      source: `company-${group.company_rid}`,
      target: `project-group-${group.rid}`,
      value: group.amount,
      kind: 'company-project-group',
      meta: { projectGroupName: group.name },
    })
  })

  summary.company_pm.forEach((item) => {
    addNode({
      id: `pm-${item.pm_rid}`,
      name: item.pm_name,
      type: 'pm',
      rid: item.pm_rid,
      projectCount: pmCounts.get(item.pm_rid) ?? 0,
    })

    links.push({
      id: `project-group-pm-${item.project_group_rid}-${item.pm_rid}`,
      source: `project-group-${item.project_group_rid}`,
      target: `pm-${item.pm_rid}`,
      value: item.amount,
      kind: 'project-group-pm',
      meta: { projectGroupName: item.project_group_name, pmName: item.pm_name },
    })
  })

  const projectLinks = new Map<string, LinkDatum>()

  summary.pm_pl.forEach((item) => {
    addNode({
      id: `project-${item.project_rid}`,
      name: item.project_name,
      type: 'project',
      rid: item.project_rid,
    })
    addNode({
      id: `pl-${item.pl_rid}`,
      name: item.pl_name,
      type: 'pl',
      rid: item.pl_rid,
      projectCount: plCounts.get(item.pl_rid) ?? 0,
    })

    const projectKey = `pm-project-${item.pm_rid}-${item.project_rid}`
    const existing = projectLinks.get(projectKey)
    if (existing) {
      existing.value += item.amount
    } else {
      projectLinks.set(projectKey, {
        id: projectKey,
        source: `pm-${item.pm_rid}`,
        target: `project-${item.project_rid}`,
        value: item.amount,
        kind: 'pm-project',
        meta: { projectName: item.project_name },
      })
    }

    links.push({
      id: `project-pl-${item.project_rid}-${item.pl_rid}`,
      source: `project-${item.project_rid}`,
      target: `pl-${item.pl_rid}`,
      value: item.amount,
      kind: 'project-pl',
      meta: { projectName: item.project_name, plName: item.pl_name },
    })
  })

  projectLinks.forEach((link) => links.push(link))

  return { nodes, links }
}

const resetSelection = () => {
  selectedLinkId.value = null
  selectedNodeId.value = null
  highlightedNodes.value = new Set()
  highlightedLinks.value = new Set()
}

const resetTooltip = () => {
  tooltip.value = { visible: false, x: 0, y: 0, text: '' }
}

const computeHighlights = (linkId: string) => {
  const selectedLink = layoutLinks.value.find((link) => link.id === linkId)
  if (!selectedLink) {
    resetSelection()
    return
  }

  const incoming = new Map<string, LinkRender[]>()
  const outgoing = new Map<string, LinkRender[]>()

  layoutLinks.value.forEach((link) => {
    const source = link.sourceNodeId
    const target = link.targetNodeId
    if (!outgoing.has(source)) outgoing.set(source, [])
    if (!incoming.has(target)) incoming.set(target, [])
    outgoing.get(source)?.push(link)
    incoming.get(target)?.push(link)
  })

  const nodes = new Set<string>()
  const links = new Set<string>()

  const walkUpstream = (nodeId: string) => {
    const incomingLinks = incoming.get(nodeId) ?? []
    incomingLinks.forEach((link) => {
      if (links.has(link.id)) return
      links.add(link.id)
      nodes.add(link.sourceNodeId)
      nodes.add(link.targetNodeId)
      walkUpstream(link.sourceNodeId)
    })
  }

  const walkDownstream = (nodeId: string) => {
    const outgoingLinks = outgoing.get(nodeId) ?? []
    outgoingLinks.forEach((link) => {
      if (links.has(link.id)) return
      links.add(link.id)
      nodes.add(link.sourceNodeId)
      nodes.add(link.targetNodeId)
      walkDownstream(link.targetNodeId)
    })
  }

  nodes.add(selectedLink.sourceNodeId)
  nodes.add(selectedLink.targetNodeId)
  links.add(selectedLink.id)
  walkUpstream(selectedLink.sourceNodeId)
  walkDownstream(selectedLink.targetNodeId)

  highlightedNodes.value = nodes
  highlightedLinks.value = links
}

const computeHighlightsFromNode = (nodeId: string) => {
  const incoming = new Map<string, LinkRender[]>()
  const outgoing = new Map<string, LinkRender[]>()

  layoutLinks.value.forEach((link) => {
    const source = link.sourceNodeId
    const target = link.targetNodeId
    if (!outgoing.has(source)) outgoing.set(source, [])
    if (!incoming.has(target)) incoming.set(target, [])
    outgoing.get(source)?.push(link)
    incoming.get(target)?.push(link)
  })

  const nodes = new Set<string>([nodeId])
  const links = new Set<string>()

  const walkUpstream = (currentId: string) => {
    const incomingLinks = incoming.get(currentId) ?? []
    incomingLinks.forEach((link) => {
      if (links.has(link.id)) return
      links.add(link.id)
      nodes.add(link.sourceNodeId)
      nodes.add(link.targetNodeId)
      walkUpstream(link.sourceNodeId)
    })
  }

  const walkDownstream = (currentId: string) => {
    const outgoingLinks = outgoing.get(currentId) ?? []
    outgoingLinks.forEach((link) => {
      if (links.has(link.id)) return
      links.add(link.id)
      nodes.add(link.sourceNodeId)
      nodes.add(link.targetNodeId)
      walkDownstream(link.targetNodeId)
    })
  }

  walkUpstream(nodeId)
  walkDownstream(nodeId)

  highlightedNodes.value = nodes
  highlightedLinks.value = links
}

const labelPadding = 140

const updateLayout = () => {
  const summary = summaryStore.summaries_sankey
  if (!summary || size.value.width === 0 || size.value.height === 0) {
    layoutNodes.value = []
    layoutLinks.value = []
    return
  }

  const rootName = periodLabel(summary, selectedPeriod.value)
  const { nodes, links } = buildGraphData(summary, rootName)

  if (nodes.length === 0 || links.length === 0) {
    layoutNodes.value = []
    layoutLinks.value = []
    return
  }

  const sankeyGen = sankey<NodeDatum, LinkDatum>()
    .nodeId((d) => d.id)
    .nodeWidth(16)
    .nodePadding(22)
    .extent([
      [labelPadding, 6],
      [Math.max(labelPadding + 40, size.value.width - labelPadding), size.value.height - 6],
    ])

  const graph = sankeyGen({
    nodes: nodes.map((node) => ({ ...node })),
    links: links.map((link) => ({ ...link })),
  })

  const linkPath = sankeyLinkHorizontal()
  const nodeColorMap = new Map<string, string>()

  const renderedNodes: NodeRender[] = graph.nodes.map((node) => {
    const color = nodeColor(node)
    nodeColorMap.set(node.id, color)

    const percent = summary.total_amount
      ? Math.min(100, (node.value / summary.total_amount) * 100)
      : 0
    const count = node.projectCount ?? 0
    const percentLabel = `${percent.toFixed(1)}% / ${count} PJ`
    const { left, right } = labelConfig(node, percentLabel)

    return {
      ...node,
      color,
      labelY: (node.y0 + node.y1) / 2,
      labelLeft: left,
      labelRight: right,
      labelLeftX: node.x0 - 10,
      labelRightX: node.x1 + 10,
      showLeft: left !== null,
      showRight: right !== null,
    }
  })

  const renderedLinks: LinkRender[] = graph.links.map((link, index) => {
    const source = link.source as NodeRender
    const target = link.target as NodeRender
    const sourceColor = nodeColorMap.get(source.id) ?? '#5a5a5a'
    const targetColor = nodeColorMap.get(target.id) ?? '#5a5a5a'

    return {
      ...link,
      path: linkPath(link) ?? '',
      width: link.width ?? 1,
      gradientId: `sankey-gradient-${index}`,
      sourceNodeId: source.id,
      targetNodeId: target.id,
      sourceColor,
      targetColor,
      gradientX1: source.x1,
      gradientX2: target.x0,
    }
  })

  layoutNodes.value = renderedNodes
  layoutLinks.value = renderedLinks

  if (selectedLinkId.value) {
    if (renderedLinks.some((link) => link.id === selectedLinkId.value)) {
      computeHighlights(selectedLinkId.value)
    } else {
      resetSelection()
    }
  }
}

const tooltipTextForLink = (link: LinkRender) => {
  switch (link.kind) {
    case 'root-company':
      return `${link.meta.companyName ?? ''}: ${formatCurrency(link.value)}`
    case 'company-project-group':
      return `${link.meta.projectGroupName ?? ''}: ${formatCurrency(link.value)}`
    case 'project-group-pm':
      return `${link.meta.projectGroupName ?? ''}: ${link.meta.pmName ?? ''}: ${formatCurrency(
        link.value,
      )}`
    case 'pm-project':
      return `${link.meta.projectName ?? ''}: ${formatCurrency(link.value)}`
    case 'project-pl':
      return `${link.meta.projectName ?? ''}: ${link.meta.plName ?? ''}: ${formatCurrency(
        link.value,
      )}`
    default:
      return formatCurrency(link.value)
  }
}

const updateTooltipPosition = (event: MouseEvent) => {
  if (!svgRef.value) return
  const rect = svgRef.value.getBoundingClientRect()
  tooltip.value = {
    ...tooltip.value,
    x: event.clientX - rect.left + 12,
    y: event.clientY - rect.top + 12,
  }
}

const handleLinkEnter = (link: LinkRender, event: MouseEvent) => {
  tooltip.value = { visible: true, x: 0, y: 0, text: tooltipTextForLink(link) }
  updateTooltipPosition(event)
}

const handleLinkMove = (event: MouseEvent) => {
  if (!tooltip.value.visible) return
  updateTooltipPosition(event)
}

const handleLinkLeave = () => {
  resetTooltip()
}

const toggleLinkSelection = (link: LinkRender) => {
  if (selectedLinkId.value === link.id) {
    resetSelection()
    return
  }
  selectedLinkId.value = link.id
  selectedNodeId.value = null
  computeHighlights(link.id)
}

const toggleNodeSelection = (node: NodeRender) => {
  if (selectedNodeId.value === node.id) {
    resetSelection()
    return
  }
  selectedNodeId.value = node.id
  selectedLinkId.value = null
  computeHighlightsFromNode(node.id)
}

const clearSelection = () => {
  resetSelection()
}

watch(
  selectedPeriod,
  async (nextPeriod) => {
    resetSelection()
    resetTooltip()
    await summaryStore.fetchSummariesSankey(nextPeriod)
    updateLayout()
  },
  { immediate: false },
)

watch(
  () => summaryStore.summaries_sankey,
  () => {
    updateLayout()
  },
)

let resizeObserver: ResizeObserver | null = null

onMounted(async () => {
  await summaryStore.fetchSummariesSankey(selectedPeriod.value)

  if (containerRef.value) {
    resizeObserver = new ResizeObserver((entries) => {
      const entry = entries[0]
      if (!entry) return
      const { width, height } = entry.contentRect
      size.value = { width, height }
      updateLayout()
    })
    resizeObserver.observe(containerRef.value)
  }
})

onBeforeUnmount(() => {
  if (resizeObserver && containerRef.value) {
    resizeObserver.unobserve(containerRef.value)
  }
})

const tooltipStyle = computed(() => ({
  left: `${tooltip.value.x}px`,
  top: `${tooltip.value.y}px`,
}))

const hasSelection = computed(() => selectedLinkId.value !== null || selectedNodeId.value !== null)

const isDimmedNode = (node: NodeRender) =>
  hasSelection.value && !highlightedNodes.value.has(node.id)

const isDimmedLink = (link: LinkRender) =>
  hasSelection.value && !highlightedLinks.value.has(link.id)
</script>

<template>
  <v-card class="viz-card result-card" color="#808080" rounded="xl" variant="tonal">
    <v-card-title class="text-subtitle-2 font-weight-medium viz-title">
      Results
      <v-btn-toggle v-model="selectedPeriod" mandatory density="compact" class="period-toggle">
        <v-btn v-for="option in periodOptions" :key="option.value" :value="option.value" size="small">
          {{ option.label }}
        </v-btn>
      </v-btn-toggle>
    </v-card-title>

    <v-card-text class="viz-card-text result-card__body">
      <div ref="containerRef" class="sankey-container" @click="clearSelection">
        <svg ref="svgRef" class="sankey-svg" :width="size.width" :height="size.height">
          <defs>
            <linearGradient
              v-for="link in layoutLinks"
              :key="link.gradientId"
              :id="link.gradientId"
              gradientUnits="userSpaceOnUse"
              :x1="link.gradientX1"
              :x2="link.gradientX2"
            >
              <stop offset="0%" :stop-color="link.sourceColor" stop-opacity="0.7" />
              <stop offset="100%" :stop-color="link.targetColor" stop-opacity="0.7" />
            </linearGradient>
          </defs>

          <g class="sankey-links">
            <path
              v-for="link in layoutLinks"
              :key="link.id"
              class="sankey-link"
              :class="{
                'sankey-link--dimmed': isDimmedLink(link),
                'sankey-link--active': selectedLinkId === link.id,
              }"
              :d="link.path"
              :stroke="`url(#${link.gradientId})`"
              :stroke-width="link.width"
              @mouseenter="(event) => handleLinkEnter(link, event)"
              @mousemove="handleLinkMove"
              @mouseleave="handleLinkLeave"
              @click.stop="toggleLinkSelection(link)"
            />
          </g>

          <g class="sankey-nodes">
            <rect
              v-for="node in layoutNodes"
              :key="node.id"
              class="sankey-node"
              :class="{ 'sankey-node--dimmed': isDimmedNode(node) }"
              :x="node.x0"
              :y="node.y0"
              :width="node.x1 - node.x0"
              :height="node.y1 - node.y0"
              :fill="node.color"
              @click.stop="toggleNodeSelection(node)"
            />

            <g v-for="node in layoutNodes" :key="`${node.id}-label`">
              <text
                v-if="node.showLeft"
                class="sankey-label"
                :class="{ 'sankey-label--dimmed': isDimmedNode(node) }"
                :x="node.labelLeftX"
                :y="node.labelY"
                text-anchor="end"
                dominant-baseline="middle"
              >
                {{ node.labelLeft }}
              </text>
              <text
                v-if="node.showRight"
                class="sankey-label sankey-label--right"
                :class="{ 'sankey-label--dimmed': isDimmedNode(node) }"
                :x="node.labelRightX"
                :y="node.labelY"
                text-anchor="start"
                dominant-baseline="middle"
              >
                {{ node.labelRight }}
              </text>
            </g>
          </g>
        </svg>

        <div v-show="tooltip.visible" class="sankey-tooltip" :style="tooltipStyle">
          {{ tooltip.text }}
        </div>
      </div>
    </v-card-text>
  </v-card>
</template>

<style scoped>
@import './viz.css';

.result-card {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.result-card__body {
  flex: 1;
  padding-top: 20px;
  padding-bottom: 20px;
}

.sankey-container {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 420px;
  cursor: default;
  overflow: visible;
}

.sankey-svg {
  width: 100%;
  height: 100%;
  display: block;
  overflow: visible;
}

.sankey-link {
  fill: none;
  stroke-linecap: butt;
  stroke-opacity: 0.5;
  transition: opacity 0.2s ease, stroke-opacity 0.2s ease;
}

.sankey-link--active {
  stroke-opacity: 0.85;
}

.sankey-link--dimmed {
  opacity: 0.15;
}

.sankey-node {
  rx: 3px;
  ry: 3px;
  transition: opacity 0.2s ease;
}

.sankey-node--dimmed {
  opacity: 0.2;
}

.sankey-label {
  fill: rgba(255, 255, 255, 0.9);
  font-size: 12px;
  letter-spacing: 0.2px;
}

.sankey-label--dimmed {
  opacity: 0.25;
}

.sankey-tooltip {
  position: absolute;
  background: rgba(15, 15, 15, 0.92);
  color: #ffffff;
  padding: 6px 10px;
  border-radius: 6px;
  font-size: 12px;
  pointer-events: none;
  white-space: nowrap;
  box-shadow: 0 6px 14px rgba(0, 0, 0, 0.3);
}

.period-toggle {
  background: rgba(255, 255, 255, 0.08);
}
</style>
