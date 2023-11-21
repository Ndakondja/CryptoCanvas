<template>
  <div id="volatility-chart"></div>
</template>

<script>
import * as d3 from 'd3'
import axios from 'axios'
import config from './config'

export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: 'Volatility',
  mounted () {
    this.fetchVolatilityData(this.selectedTimeRange, this.selectedCoins)
  },
  data () {
    return {
      selected_coins: [], // Default selected coins
      volatilityData: null
    }
  },
  watch: {
    selectedTimeRange () {
      this.fetchCoinStats(this.selectedTimeRange, this.selectedCoins)
    },
    selectedCoins () {
      this.fetchCoinStats(this.selectedTimeRange, this.selectedCoins)
    }
  },
  methods: {
    async fetchVolatilityData() {
      try {
        const response = await axios.get(config.backendApiUrl.concat('/getCoinVolatilityComparisons',{
          params: {
            timeRange: this.selectedTimeRange,
            coins: this.selectedCoins.join(',')
          }
        }))
        this.drawVolatilityChart(response.data)
      } catch (error) {
        console.error('Error fetching volatility data:', error)
      }
    },
    drawVolatilityChart (rawData) {
      // Parse data and group by coin
      const parseTime = d3.timeParse('%a, %d %b %Y %H:%M:%S GMT')
      const data = rawData.map(d => ({
        coin: d.Coin,
        date: parseTime(d.Date),
        value: +d.Volatility
      }))

      // Define dimensions and margins
      const margin = { top: 10, right: 80, bottom: 30, left: 50 }
      const width = 960 - margin.left - margin.right
      const height = 500 - margin.top - margin.bottom

      // Remove any existing SVG to avoid overlapping charts
      d3.select('#volatility-chart').select('svg').remove()

      // Append the svg object
      const svg = d3.select('#volatility-chart')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`)

      // Add X & Y scales and axes
      const x = d3.scaleTime().range([0, width])
      const y = d3.scaleLinear().range([height, 0])
      x.domain(d3.extent(data, d => d.date))
      y.domain([0, d3.max(data, d => d.value)])

      // Define the line generator
      const valueline = d3.line()
        .x(d => x(d.date))
        .y(d => y(d.value))

      // Create a color scale
      const color = d3.scaleOrdinal(d3.schemeCategory10)

      // Add the valueline path for each coin
      this.selected_coins.forEach(coin => {
        svg.append('path')
          .datum(data.filter(d => d.coin === coin))
          .attr('class', 'line')
          .attr('d', valueline)
          .style('stroke', color(coin))
          .style('fill', 'none')
      })

      // Add the X Axis
      svg.append('g')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(x))

      // Add the Y Axis
      svg.append('g')
        .call(d3.axisLeft(y))
        // ...after your axes have been appended to the SVG

      // Add X axis label:
      svg.append('text')
        .attr('text-anchor', 'end')
        .attr('x', width / 2 + margin.left)
        .attr('y', height + margin.top + 20)
        .text('Months')

      // Add Y axis label:
      svg.append('text')
        .attr('text-anchor', 'end')
        .attr('transform', 'rotate(-90)')
        .attr('y', -margin.left + 20)
        .attr('x', -margin.top - height / 2 + 20)
        .text('Volatility')

      // Tooltip logic (assuming you have CSS styles defined for .tooltip)
      const tooltip = d3.select('#volatility-chart').append('div')
        .attr('class', 'tooltip')
        .style('opacity', 0)

      const mouseover = function (event, d) {
        tooltip.transition()
          .duration(200) // Time in milliseconds for the tooltip to become fully opaque
          .style('opacity', 0.9) // Fully opaque
      }

      const mousemove = function (event, d) {
        tooltip.html('Volatility: ' + d.value + '<br/>Date: ' + d3.timeFormat('%B %d, %Y')(d.date))
          .style('left', (event.pageX + 10) + 'px') // 10px to the right of the cursor
          .style('top', (event.pageY - 10) + 'px') // 10px above the cursor
      }

      const mouseleave = function (event, d) {
        tooltip.transition()
          .duration(500) // Time in milliseconds for the tooltip to become fully transparent
          .style('opacity', 0) // Fully transparent
      }
      const legend = svg.append('g')
        .attr('font-family', 'sans-serif')
        .attr('font-size', 10)
        .attr('text-anchor', 'end')
        .selectAll('g')
        .data(this.selected_coins.slice().reverse()) // Assuming this.selected_coins contains the list of coins
        .enter().append('g')
        .attr('transform', function (d, i) { return 'translate(0,' + i * 20 + ')' })

      // Add rectangles to the legend group
      legend.append('rect')
        .attr('x', width - 19)
        .attr('width', 19)
        .attr('height', 19)
        .attr('fill', color) // Assuming color is your d3.scaleOrdinal() for colors

      // Add text labels to the legend group
      legend.append('text')
        .attr('x', width - 24)
        .attr('y', 9.5)
        .attr('dy', '0.32em')
        .text(function (d) { return d })

      // Add the scatterplot points
      svg.selectAll('dot')
        .data(data)
        .enter().append('circle')
        .attr('r', 2)
        .attr('cx', function (d) { return x(d.date) })
        .attr('cy', function (d) { return y(d.value) })
        .attr('fill', function (d) { return color(d.coin) })
        .on('mouseover', mouseover)
        .on('mouseout', mouseleave)
        .on('mousemove', mousemove)
    }

  }
}
</script>

<style>
.tooltip {
  position: absolute;
  text-align: center;
  padding: 8px;
  font: 12px sans-serif;
  background: rgba(255, 255, 255, 0.8); /* Semi-transparent white background */
  border: 1px solid #333; /* Solid border for contrast */
  border-radius: 5px;
  pointer-events: none; /* Prevents the tooltip from capturing mouse events */
  z-index: 10; /* Ensures the tooltip is above other elements */
}

</style>
