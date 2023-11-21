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
  data () {
    return {
      selected_coins: ['Cardano', 'XRP', 'Litecoin', 'Ethereum', 'Bitcoin'], // Default selected coins
      volatilityData: null
    }
  },
  mounted () {
    this.fetchVolatilityData()
  },
  methods: {
    async fetchVolatilityData () {
      try {
        const response = await axios.get(config.backendApiUrl.concat('/getCoinVolatilityComparisons'))
        this.drawVolatilityChart(response.data)
      } catch (error) {
        console.error('Error fetching volatility data:', error)
      }
    },
    drawVolatilityChart (data) {
      // Parse data
      const parseTime = d3.timeParse('%Y-%m-%dT%H:%M:%S.%LZ') // Modify this to match your date format

      data.forEach(d => {
        d.date = parseTime(d.Date) // Parse the date
        console.log(d.date) // Log to see if the date is parsed correctly
        d.value = +d.Volatility
      })

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

      // Scale the range of the data
      x.domain(d3.extent(data, d => d.date))
      y.domain([0, d3.max(data, d => d.value)])

      // Define the line
      const valueline = d3.line()
        .x(d => x(d.date))
        .y(d => y(d.value))

      // Add the valueline path for each coin
      // eslint-disable-next-line camelcase, no-undef
      this.selected_coins.forEach(coin => {
        svg.append('path')
          .data([data.filter(d => d.coin === coin)])
          .attr('class', 'line')
          .attr('d', valueline)
          .style('stroke' /* assign color based on coin */)
      })

      // Add the X Axis
      svg.append('g')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(x))

      // Add the Y Axis
      svg.append('g')
        .call(d3.axisLeft(y))

      // Add tooltip
      const tooltip = d3.select('#volatility-chart')
        .append('div')
        .style('opacity', 0)
        .attr('class', 'tooltip')
        .style('background-color', 'white')
        .style('border', 'solid')
        .style('border-width', '2px')
        .style('border-radius', '5px')
        .style('padding', '5px')
        .style('position', 'absolute')

      // Tooltip event handlers
      const mouseover = function (event, d) {
        tooltip.style('opacity', 1)
        d3.select(this).style('stroke', 'black')
      }

      const mousemove = function (event, d) {
        if (d.date) {
          tooltip.html('Date: ' + d.date.toISOString().substring(0, 10) + '<br>Volatility: ' + d.value.toFixed(2))
            .style('left', (event.x / 2) + 'px')
            .style('top', (event.y / 2 - 30) + 'px')
        }
      }

      const mouseleave = function (event, d) {
        tooltip.style('opacity', 0)
        d3.select(this).style('stroke', 'none')
      }

      // Add the points with tooltips
      svg.selectAll('dot')
        .data(data)
        .enter().append('circle')
        .attr('r', 5)
        .attr('cx', d => x(d.date))
        .attr('cy', d => y(d.value))
        .on('mouseover', mouseover)
        .on('mousemove', mousemove)
        .on('mouseleave', mouseleave)
    }
  }
}
</script>

<style>
/* Add styles for your chart and tooltip */
.tooltip {
  position: absolute;
  text-align: center;
  transition: opacity 0.3s;
}
</style>
