<!-- eslint-disable no-multiple-empty-lines -->
<template>
  <div>
      <h2>Bitcoin Correlation Heatmap</h2>
      <div id="heatmap"></div> <!-- Container for the D3.js treemap -->
    </div>
</template>

<script>
import * as d3 from 'd3'
import axios from 'axios'
import config from './config'

export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: 'Heatmap',
  props: {
    selectedTimeRange: {
      type: String,
      default: ''
    },
    selectedCoins: {
      type: Array,
      default: () => []
    }
  },
  mounted () {
    this.fetchCorrelationMatrix()
  },
  // CorrelationMatrix.vue
  watch: {
    selectedTimeRange () {
      this.fetchCorrelationMatrix()
    },
    selectedCoins () {
      this.fetchCorrelationMatrix()
    }
  },
  methods: {
    async fetchCorrelationMatrix () {
      try {
        const coinQueryParam = this.selectedCoins.join(',')
        const response = await axios.get(`${config.backendApiUrl}/getCorrelationMatrix`, {
          params: {
            timeRange: this.selectedTimeRange,
            coins: coinQueryParam
          }
        })
        this.drawHeatmap(response.data.matrix, response.data.labels)
      } catch (error) {
        console.error('Error fetching correlation matrix:', error)
      }
    },
    drawHeatmap (matrix, labels) {
      // Define the dimensions and margins for the heatmap
      const margin = { top: 80, right: 80, bottom: 80, left: 80 }
      const width = 1000 - margin.left - margin.right
      const height = 400 - margin.top - margin.bottom

      // Remove any existing SVG to avoid overlapping heatmaps
      d3.select('#heatmap').select('svg').remove()

      // Append the svg object to the body of the page
      const svg = d3.select('#heatmap')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top - 80})`)

      // Build X scales and axis
      const x = d3.scaleBand()
        .range([0, width])
        .domain(labels)
        .padding(0.05)
      svg.append('g')
        .style('font-size', 15)
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(x).tickSize(0))
        .select('.domain').remove()

      // Build Y scales and axis
      const y = d3.scaleBand()
        .range([height, 0])
        .domain(labels)
        .padding(0.05)
      svg.append('g')
        .style('font-size', 15)
        .call(d3.axisLeft(y).tickSize(0))
        .select('.domain').remove()

      // Build color scale
      // eslint-disable-next-line indent
    // Create a diverging color scale
      const myColor = d3.scaleDiverging()
        .interpolator(d3.interpolateRdYlBu) // This is a common diverging color interpolator
        .domain([-1, 0, 1])

      // After your heatmap squares have been added:
      // Assume myColor is your color scale

      // Define the legend
      const legendWidth = 300
      const legendHeight = 20
      const legendMargin = { top: 10, right: 60, bottom: 10, left: 60 }

      // Append a defs (for definition) element to your SVG
      const defs = svg.append('defs')

      // Append a linearGradient element to the defs and give it a unique id
      const linearGradient = defs.append('linearGradient')
        .attr('id', 'linear-gradient')

      // Horizontal gradient
      linearGradient
        .attr('x1', '0%')
        .attr('y1', '0%')
        .attr('x2', '100%')
        .attr('y2', '0%')

      // Set the color for the start (0%)
      linearGradient.append('stop')
        .attr('offset', '0%')
        .attr('stop-color', myColor(0)) // light color

      // Set the color for the end (100%)
      linearGradient.append('stop')
        .attr('offset', '100%')
        .attr('stop-color', myColor(1)) // dark color

      // Draw the rectangle and fill with gradient
      svg.append('rect')
        .attr('width', legendWidth)
        .attr('height', legendHeight)
        .style('fill', 'url(#linear-gradient)')
        .attr('transform', `translate(${margin.left}, ${height + margin.top + legendMargin.top})`)

      // Append title
      svg.append('text')
        .attr('class', 'legend-title')
        .attr('x', margin.left)
        .attr('y', height + margin.top)
        .style('text-anchor', 'left')
        .text('Correlation Scale')

      // Create a scale and axis for the legend
      const legendScale = d3.scaleLinear()
        .domain([-1, 1])
        .range([0, legendWidth])

      const legendAxis = d3.axisBottom(legendScale)
        .ticks(5)
        .tickFormat(d3.format('.1f'))

      svg.append('g')
        .attr('class', 'legend-axis')
        .attr('transform', `translate(${margin.left}, ${height + margin.top + legendHeight + legendMargin.top})`)
        .call(legendAxis)
      svg.selectAll()
        .data(matrix.flatMap((row, i) => row.map((value, j) => ({ row: labels[i], column: labels[j], value }))))
        .enter()
        .append('text')
        .text(d => d.value.toFixed(2))
        .attr('x', d => x(d.column) + x.bandwidth() / 2)
        .attr('y', d => y(d.row) + y.bandwidth() / 2)
        .style('text-anchor', 'middle')
        .style('alignment-baseline', 'central')
        .style('fill', d => myColor(d.value))

      // create a tooltip
      const tooltip = d3.select('#heatmap')
        .append('div')
        .style('opacity', 0)
        .attr('class', 'tooltip')
        .style('background-color', 'white')
        .style('border', 'solid')
        .style('border-width', '2px')
        .style('border-radius', '5px')
        .style('padding', '5px')
        .style('position', 'absolute')

      // Three functions that change the tooltip when user hovers, moves, or leaves a cell
      const mouseover = function (event, d) {
        tooltip
          .html(`The correlation between ${d.row} and ${d.column} is ${d.value.toFixed(2)}.<br/>
           A value close to 1 indicates a strong positive relationship, while a value close to -1 indicates a strong negative relationship.`)
          .style('opacity', 1)
        d3.select(this)
          .style('stroke', 'black')
          .style('opacity', 1)
      }
      const mousemove = function (event, d) {
        tooltip.html('Correlation: ' + d.value.toFixed(2))
          .style('left', (event.x) + 'px')
          .style('top', (event.y) + 'px')
      }
      const mouseleave = function (event, d) {
        tooltip.style('opacity', 0)
        d3.select(this)
          .style('stroke', 'none')
          .style('opacity', 0.8)
      }

      // Add the squares
      svg.selectAll()
        .data(matrix.flatMap((row, i) => row.map((value, j) => ({ row: labels[i], column: labels[j], value }))))
        .enter()
        .append('rect')
        .attr('x', d => x(d.column))
        .attr('y', d => y(d.row))
        .attr('rx', 4)
        .attr('ry', 4)
        .attr('width', x.bandwidth())
        .attr('height', y.bandwidth())
        .style('fill', d => myColor(d.value))
        .style('stroke-width', 4)
        .style('stroke', 'none')
        .style('opacity', 0.8)
        .on('mouseover', mouseover)
        .on('mousemove', mousemove)
        .on('mouseleave', mouseleave)
    }
  }
}

</script>

<style>
.tooltip {
  position: absolute;
  text-align: center;
  transition: opacity 0.3s;
}
</style>
