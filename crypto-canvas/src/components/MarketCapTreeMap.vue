<template>
    <div>
      <h2>Average of Market Share (%) for Period</h2>
      <div id="market-cap-treemap"></div> <!-- Container for the D3.js treemap -->
    </div>
  </template>

<script>
import axios from 'axios'
import config from './config'
import * as d3 from 'd3'

export default {
  name: 'MarketCapTreeMap',
  data () {
    return {
      marketCapData: [],
      colorScale: d3.scaleOrdinal(d3.schemeSet2)
    }
  },
  props: {
    selectedTimeRange: String,
    selectedCoins: Array
  },
  mounted () {
    this.fetchMarketCapData(this.selectedTimeRange, this.selectedCoins)
  },
  watch: {
    selectedTimeRange () {
      this.fetchMarketCapData(this.selectedTimeRange, this.selectedCoins)
    },
    selectedCoins () {
      this.fetchMarketCapData(this.selectedTimeRange, this.selectedCoins)
    }
  },
  methods: {
    async fetchMarketCapData () {
      try {
        const response = await axios.get(`${config.backendApiUrl}/getMarketCapData`, {
          params: {
            timeRange: this.selectedTimeRange,
            coins: this.selectedCoins.join(',')
          }
        })
        this.marketCapData = response.data
        this.drawBarChart(this.selectedTimeRange, this.selectedCoins)
      } catch (error) {
        console.error('Error fetching market cap data:', error)
      }
    },
    drawBarChart () {
      const data = this.marketCapData.sort((a, b) => d3.descending(a.marketCap, b.marketCap))
      const container = d3.select('#market-cap-treemap')
      console.log('Drawing Bar Chart with Data:', data)

      // Define dimensions and margins
      const margin = { top: 5, right: 30, bottom: 30, left: 60 }
      const width = 700 - margin.left - margin.right
      const height = 280 - margin.top - margin.bottom
      container.select('svg').remove()

      // Create SVG container
      const svg = container
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`)

      // Create x and y scales
      const x = d3.scaleBand()
        .range([0, width])
        .domain(data.map(d => d.coin))
        .padding(0.1)

      const y = d3.scaleLinear()
        .range([height, 0])
        .domain([0, 1]) // Start domain at 1 to avoid log(0)

      // Draw bars
      svg.selectAll('.bar')
        .data(data)
        .enter().append('rect')
        .attr('class', 'bar')
        .attr('x', d => x(d.coin))
        .attr('width', x.bandwidth())
        .attr('y', d => y(d.avgMarketCap))
        .attr('height', d => height - y(d.avgMarketCap))
        .style('fill', d => this.colorScale(d.coin)) // Use the color scale here

      // Add the x Axis
      svg.append('g')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(x))

      // Add the y Axis
      svg.append('g')
        .call(d3.axisLeft(y))
    }
  }
}
</script>

  <style>
  /* Add styling for your treemap here */
  #market-cap-treemap svg {
    font-family: 'Arial', sans-serif;
  }
  </style>
