<template>
  <div class="correlation-matrix" ref="correlationMatrix"></div>
</template>

<script>
import * as d3 from 'd3'

export default {
  name: 'CorrelationMatrix',
  mounted () {
    fetch('correlation_matrix.json')
      .then(response => response.json())
      .then(data => {
        this.createCorrelationMatrix(data)
      })
      .catch(error => console.error('Error fetching data:', error))
  },
  methods: {
    createCorrelationMatrix (data) {
      const margin = { top: 20, right: 20, bottom: 20, left: 20 }
      const width = 400 - margin.left - margin.right
      const height = 400 - margin.top - margin.bottom

      // Append SVG object to the DOM
      const svg = d3.select(this.$refs.correlationMatrix)
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left}, ${margin.top})`)

      // Create scales
      const x = d3.scaleBand()
        .range([0, width])
        .domain(Object.keys(data))
        .padding(0.05)

      svg.append('g')
        .attr('transform', `translate(0, ${height})`)
        .call(d3.axisBottom(x).tickSize(0))
        .select('.domain').remove()

      const y = d3.scaleBand()
        .range([height, 0])
        .domain(Object.keys(data))
        .padding(0.05)

      svg.append('g')
        .call(d3.axisLeft(y).tickSize(0))
        .select('.domain').remove()

      // Build color scale
      const myColor = d3.scaleSequential()
        .interpolator(d3.interpolateInferno)
        .domain([0, 1])

      // Create the squares
      svg.selectAll()
        .data(Object.entries(data).flatMap(([key, value]) => {
          return Object.keys(value).map(subKey => {
            return { group1: key, group2: subKey, value: value[subKey] }
          })
        }))
        .enter()
        .append('rect')
        .attr('x', d => x(d.group1))
        .attr('y', d => y(d.group2))
        .attr('width', x.bandwidth())
        .attr('height', y.bandwidth())
        .style('fill', d => myColor(d.value))
    }
  }
}
</script>

<style scoped>
.correlation-matrix {
  width: 100%;
  height: 400px;
}
</style>
