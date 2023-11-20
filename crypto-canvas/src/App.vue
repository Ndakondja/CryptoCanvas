<template>
  <v-app>
    <!-- Navigation Drawer -->
    <v-navigation-drawer app>
      <v-list dense>
        <v-list-item link @click="currentTab = 'VolatilityComparison'">
          <v-list-item-icon>
            <v-icon>mdi-chart-line</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Volatility Comparison</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item link @click="currentTab = 'MarketOverview'">
          <v-list-item-icon>
            <v-icon>mdi-view-dashboard</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Market Overview</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar app>
      <v-toolbar-title>Crypto Canvas Dashboard</v-toolbar-title>
      <v-select
        v-model="selectedTimeRange"
        :items="['Last 6 Months', 'Last 12 Months', 'Last 24 Months', 'Last 48 Months', 'BTC Halving 2016-07-09', 'BTC Halving 2020-05-11', ]"
        label="Select Time Range"
        style="max-width: 180px;"
      ></v-select>
      <v-select
        v-model="selectedCoins"
        :items="availableCoins"
        label="Select Coins"
        multiple
        dense
        style="max-width: 500px;"
      ></v-select>
    </v-app-bar>

    <!-- Main Content -->
    <v-main>
      <div v-if="currentTab === 'VolatilityComparison'">
      <correlation-matrix
        :selected-time-range="selectedTimeRange"
        :selected-coins="selectedCoins">
      </correlation-matrix>
        <VolatilityComparison />
        <BitcoinHalving />
      </div>
      <div v-if="currentTab === 'MarketOverview'">
        <PriceChart :selectedTimeRange="selectedTimeRange" :selectedCoins="selectedCoins" />
        <MarketCapTreeMap :selectedTimeRange="selectedTimeRange" :selectedCoins="selectedCoins" />
      </div>
    </v-main>
  </v-app>
</template>

<script>
import Axios from 'axios'
import CorrelationMatrix from './components/CorrelationMatrix.vue'
import VolatilityComparison from './components/VolatilityComparison.vue'
import BitcoinHalving from './components/BitcoinHalving.vue'
import PriceChart from './components/PriceOverTime.vue'
import MarketCapTreeMap from './components/MarketCapTreeMap.vue'

export default {
  name: 'App',
  components: {
    CorrelationMatrix,
    VolatilityComparison,
    BitcoinHalving,
    PriceChart,
    MarketCapTreeMap
  },
  data () {
    return {
      currentTab: 'VolatilityComparison',
      selectedTimeRange: 'Last 6 Months',
      selectedCoins: ['Bitcoin', 'Ethereum', 'Dogecoin', 'Litecoin'],
      availableCoins: []
    }
  },
  created () {
    this.fetchAvailableCoins()
  },
  methods: {
    fetchAvailableCoins () {
      Axios.get('http://127.0.0.1:5000/available-coins') // Update with your API URL if different
        .then(response => {
          this.availableCoins = response.data.coins
        })
        .catch(error => {
          console.error('Error fetching available coins:', error)
        })
    }
  },
  watch: {
    selectedTimeRange (newVal) {
      console.log('Selected Time Range:', newVal)
      // Additional logic to handle the change in time range
    },
    selectedCoins (newVal) {
      console.log('Selected Coins:', newVal)
      // Additional logic to handle the change in time range
    }
  }
}
</script>

<style>
/* Add any additional styles if necessary */
</style>
