<!-- eslint-disable no-multiple-empty-lines -->
<template>
  <div id="heatmap"></div>
</template>

<script>
import * as d3 from 'd3'
import axios from 'axios'
import config from './config'

export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: 'Heatmap',
  mounted () {
    this.fetchCorrelationMatrix()
  },
  methods: {
    async fetchCorrelationMatrix () {
      try {
        const response = await axios.get(config.backendApiUrl.concat('/getCorrelationMatrix'))
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
        .attr('transform', `translate(${margin.left},${margin.top})`)

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
      const myColor = d3.scaleSequential()
        .interpolator(d3.interpolateInferno)
        .domain([0, 1])

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
        tooltip.style('opacity', 1)
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
