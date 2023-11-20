<template>
    <div>
        <h2>Cryptocurrency Price over Period</h2>
        <div id="price-chart"></div> <!-- Container for the D3.js chart -->
    </div>
</template>

<script>
import * as d3 from 'd3'
import axios from 'axios'
import config from './config'

export default {
  name: 'PriceChart',
  props: {
    selectedTimeRange: String,
    selectedCoins: {
      type: Array
    }
  },
  mounted () {
    this.fetchAllCoinData(this.selectedTimeRange, this.selectedCoins)
  },
  data () {
    return {
      pricesData: {},
      colorScale: d3.scaleOrdinal(d3.schemeSet2)
    }
  },
  watch: {
    selectedTimeRange () {
      this.fetchAllCoinData(this.selectedTimeRange, this.selectedCoins)
    },
    selectedCoins () {
      this.fetchAllCoinData(this.selectedTimeRange, this.selectedCoins)
    }
  },
  methods: {
    async fetchAllCoinData (timeRange, coins) {
      try {
        const coinQueryParam = coins.join(',')
        const response = await axios.get(`${config.backendApiUrl}/getAllCoinData`, {
          params: { timeRange, coins: coinQueryParam }
        })
        this.pricesData = this.processData(response.data.data)
        this.drawPriceChart()
      } catch (error) {
        console.error('Error fetching all coin data:', error)
      }
    },
    processData (data) {
      const processedData = {}
      data.forEach(d => {
        const coin = d.Coin
        const date = new Date(d.Date)
        const price = +d.Close

        if (!processedData[coin]) {
          processedData[coin] = []
        }
        processedData[coin].push({ date, price })
      })
      return processedData
    },
    drawPriceChart () {
      const margin = { top: 5, right: 30, bottom: 30, left: 60 }
      const width = 700 - margin.left - margin.right
      const height = 280 - margin.top - margin.bottom
      d3.select('#price-chart').select('svg').remove()

      const svg = d3.select('#price-chart')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`)

      const x = d3.scaleTime()
        .domain(d3.extent(Object.values(this.pricesData).flat(), d => d.date))
        .range([0, width])
      svg.append('g')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(x))

      const y = d3.scaleLinear()
        .domain([0, d3.max(Object.values(this.pricesData).flat(), d => d.price)])
        .range([height, 0])
      svg.append('g')
        .call(d3.axisLeft(y))

      const color = d3.scaleOrdinal()
        .domain(Object.keys(this.pricesData))
        .range(d3.schemeSet2)

      Object.keys(this.pricesData).forEach(coin => {
        svg.append('path')
          .datum(this.pricesData[coin])
          .attr('fill', 'none')
          .attr('stroke', color(coin))
          .attr('stroke-width', 1.5)
          .attr('d', d3.line()
            .x(d => x(d.date))
            .y(d => y(d.price))

          )
      })
      // Legend code
      const legendYPosition = height + margin.bottom + margin.top - 10
      const legendSpace = width / Object.keys(this.pricesData).length // Spacing for legend items

      Object.keys(this.pricesData).forEach((coin, index) => {
        svg.append('text')
          .attr('x', (legendSpace / 2) + index * legendSpace) // Spacing of legend items
          .attr('y', legendYPosition + 5)
          .attr('class', 'legend') // Style the legend
          .style('fill', this.colorScale(coin)) // Use the same color scale
          .text(coin)

        // Optional: Add colored rectangles next to text if needed
        svg.append('rect')
          .attr('x', (legendSpace / 2) - 10 + index * legendSpace)
          .attr('y', legendYPosition - 5)
          .attr('width', 10)
          .attr('height', 10)
          .style('fill', this.colorScale(coin)) // Use the same color scale
      })

      // Tooltip for line hover
      const tooltip = d3.select('#price-chart').append('div')
        .attr('class', 'tooltip')
        .style('opacity', 0)

      Object.keys(this.pricesData).forEach(coin => {
        const line = svg.append('path')
          .datum(this.pricesData[coin])
          .attr('fill', 'none')
          .attr('stroke', color(coin))
          .attr('stroke-width', 1.5)
          .attr('d', d3.line()
            .x(d => x(d.date))
            .y(d => y(d.price))
          )

        // Event listeners for tooltip
        line.on('mouseover', () => tooltip.style('opacity', 1))
          .on('mousemove', function (event, d) {
            const [xPosition, yPosition] = d3.pointer(event, this)
            tooltip.html(`Price: ${y.invert(yPosition).toFixed(2)}`)
              .style('left', (xPosition + 190) + 'px')
              .style('top', (yPosition + 50) + 'px')
          })
          .on('mouseleave', () => tooltip.style('opacity', 0))
      })
    }
  }
}
</script>

<style>
h2 {
  text-align: left;
  margin-bottom: 10px; /* Reduced bottom margin */
  margin-top: 20px; /* Add top margin if needed */
  margin-left: 60px;
}

#price-chart {
  padding-top: 20px; /* Add padding to the top of the chart container */
}

.tooltip {
  position: absolute;
  text-align: center;
  transition: opacity 0.3s;
}

.legend {
  font-size: 12px;
}
</style>
