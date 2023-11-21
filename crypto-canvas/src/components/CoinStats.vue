<template>
    <div id="coin-stats">
      <h2>Quick Coin Stats</h2>
      <table>
        <thead>
          <tr>
            <th>Coin</th>
            <th>Average Price</th>
            <th>Standard Deviation</th>
            <th>Percentage Growth</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="coinStat in coinStats" :key="coinStat.coin">
            <td>{{ coinStat.coin }}</td>
            <td>{{ coinStat.average_price.toFixed(2) }}</td>
            <td>{{ coinStat.std_dev.toFixed(2) }}%</td>
            <td>{{ coinStat.percentage_growth.toFixed(2) }}%</td>
          </tr>
        </tbody>
      </table>
    </div>
</template>

<script>
import axios from 'axios'
import config from './config'

export default {
  name: 'CoinStats',
  props: {
    selectedTimeRange: String,
    selectedCoins: {
      type: Array
    }
  },
  mounted () {
    this.fetchCoinStats(this.selectedTimeRange, this.selectedCoins)
  },
  data () {
    return {
      coinStats: []
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
    async fetchCoinStats () {
      try {
        const response = await axios.get(`${config.backendApiUrl}/getCoinStats`, {
          params: {
            timeRange: this.selectedTimeRange,
            coins: this.selectedCoins.join(',')
          }
        })
        this.coinStats = response.data
      } catch (error) {
        console.error('Error fetching coin stats:', error)
      }
    }
  }
}
</script>

<style>

/* Add styling for your table here */
table {
  width: 100%;
  border-collapse: collapse;
  background-color: rgba(69, 31, 152, 0.241); /* Blue background color */
}

th, td {
  border: 2px solid rgba(45, 19, 101, 0.111); /* Darker gridlines */
  padding: 8px;
}

th {
  background-color: rgba(69, 31, 152, 0.185); /* Slightly darker blue for header */
}

/* Grid layout adjustments */
.main-content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr; /* Two equal columns */
  grid-template-rows: auto;
  gap: 16px; /* Adjust the gap as needed */
}

.main-content-grid > div {
  grid-column: 1 / -1; /* Make other content span full width */
}

.main-content-grid > div:nth-child(1) {
  display: flex;
  flex-direction: column;
}

.coin-stats {
  grid-column: 2; /* Place in the second column */
  max-width: 50%; /* Half the width of the column */
  align-self: start; /* Align to the top */
}

.statistics-container {
  display: flex;
  justify-content: space-between;
  /* Add more styles for positioning if necessary */
}

.coin-statistics {
  width: 48%; /* Adjust width as necessary */
  /* Adjust other styling as necessary */
}

.icon {
  padding-right: 8px; /* Adjust spacing as necessary */
}

</style>
