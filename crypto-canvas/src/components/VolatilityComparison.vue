<template>
  <div>
    <select v-model="selectedTimeFrame" @change="filterData">
      <option value="1m">1 Month</option>
      <option value="1y">1 Year</option>
      <option value="5y">5 Years</option>
    </select>
    <div class="volatility-comparison" ref="volatilityChart"></div>
  </div>
</template>

<script>
import * as d3 from 'd3'

export default {
  name: 'VolatilityComparison',
  data () {
    return {
      selectedTimeFrame: '1m',
      originalData: []
    }
  },
  mounted () {
    this.fetchAndProcessData()
  },
  methods: {
    fetchAndProcessData () {
      fetch('volatility_comparison.json')
        .then(response => response.json())
        .then(rawData => {
          console.log('Fetched data:', rawData)
          if (rawData && rawData.length) {
            this.originalData = rawData
            this.filterData()
          } else {
            console.error('Data is empty or not in expected format')
          }
        })
        .catch(error => console.error('Error fetching data:', error))
    },
    filterData () {
      const filteredData = this.filterByTimeFrame(this.originalData, this.selectedTimeFrame)
      const transformedData = this.transformData(filteredData)
      this.createVolatilityComparison(transformedData)
    },
    filterByTimeFrame (data, timeFrame) {
      const endDate = new Date()
      const startDate = new Date()
      switch (timeFrame) {
        case '1m':
          startDate.setMonth(endDate.getMonth() - 1)
          break
        case '1y':
          startDate.setFullYear(endDate.getFullYear() - 1)
          break
        case '5y':
          startDate.setFullYear(endDate.getFullYear() - 5)
          break
      }
      return data.filter(d => new Date(d.date) >= startDate && new Date(d.date) <= endDate)
    },
    transformData (rawData) {
      const groupedData = d3.groups(rawData, d => d.name)
        .map(([name, values]) => ({ name, values }))
      return groupedData
    },
    createVolatilityComparison (data) {
      d3.select(this.$refs.volatilityChart).selectAll('*').remove()

      const margin = { top: 10, right: 30, bottom: 30, left: 50 }
      const width = 460 - margin.left - margin.right
      const height = 400 - margin.top - margin.bottom

      const svg = d3.select(this.$refs.volatilityChart)
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left}, ${margin.top})`)

      // Add X axis --> it is a date format
      const x = d3.scaleTime()
        .domain(d3.extent(this.originalData, d => new Date(d.date)))
        .range([0, width])
      svg.append('g')
        .attr('transform', `translate(0, ${height})`)
        .call(d3.axisBottom(x))

      // Add Y axis
      const y = d3.scaleLinear()
        .domain([0, d3.max(this.originalData, d => +d.value)])
        .range([height, 0])
      svg.append('g')
        .call(d3.axisLeft(y))

      // Color scale
      const color = d3.scaleOrdinal(d3.schemeCategory10)

      // Draw the line for each group
      data.forEach((crypto) => {
        const line = d3.line()
          .x(d => x(new Date(d.date)))
          .y(d => y(+d.value))

        svg.append('path')
          .datum(crypto.values)
          .attr('fill', 'none')
          .attr('stroke', color(crypto.name))
          .attr('stroke-width', 1.5)
          .attr('d', line)
      })
    }
  }
}
</script>

<style scoped>
.volatility-comparison {
  width: 100%;
  height: 400px;
}
</style>
