<template>
  <v-app>
    <!-- Navigation Drawer -->
    <v-navigation-drawer app class="custom-drawer">
      <v-list dense>
        <v-list-item link @click="currentTab = 'MarketOverview'" class="white--text">
          <v-list-item-icon>
            <v-icon>mdi-view-dashboard</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Market Overview</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item link @click="currentTab = 'VolatilityComparison'" class="white--text">
          <v-list-item-icon>
            <v-icon>mdi-chart-line</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Volatility Comparison</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar app>
      <img
        src="@/assets/crypto-canvas-high-resolution-logo-transparent.png"
        class="my-logo"
        alt="Logo"
        height="40"
      />
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
        style="max-width: 1000px;"
      ></v-select>
    </v-app-bar>

    <!-- Main Content -->
    <v-main>
      <div v-if="currentTab === 'MarketOverview'" class="market-overview-container">
        <div class="charts-container">
          <PriceChart :selectedTimeRange="selectedTimeRange" :selectedCoins="selectedCoins" />
         <MarketCapTreeMap :selectedTimeRange="selectedTimeRange" :selectedCoins="selectedCoins" />
        </div>
        <CoinStats :selectedTimeRange="selectedTimeRange" :selectedCoins="selectedCoins" class="coin-stats-container" />
      </div>
      <div v-if="currentTab === 'VolatilityComparison'">
          <correlation-matrix :selected-time-range="selectedTimeRange" :selected-coins="selectedCoins"></correlation-matrix>
          <VolatilityComparison />
          <BitcoinHalving />
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
import CoinStats from './components/CoinStats.vue' // Import the CoinStats component

export default {
  name: 'App',
  components: {
    CorrelationMatrix,
    VolatilityComparison,
    BitcoinHalving,
    PriceChart,
    MarketCapTreeMap,
    CoinStats

  },
  data () {
    return {
      currentTab: 'MarketOverview',
      selectedTimeRange: 'Last 6 Months',
      selectedCoins: ['Bitcoin', 'Ethereum', 'Dogecoin'],
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

<style scoped>
.v-app-bar {
  background: linear-gradient(90deg, rgba(39,37,89,1) 0%, rgba(69,31,152,1) 10%, rgba(0,212,255,1) 100%) !important;
}

.v-btn, .v-btn-text, .v-icon {
  color: #7d2ae8 !important; /* This sets the accent color for text and icons in the app bar */
}

.my-logo {
  margin-right: 10px;
  margin-left: 10px; /* Add some spacing between logo and title */
}

.custom-drawer {
  background-color: #272559; /* Background color for the drawer */
}

.custom-drawer .v-list-item {
  color: #7d2ae8; /* Accent color for list items */
}

.custom-drawer .v-list-item--active {
  background-color: rgba(125, 42, 232, 0.2); /* Lighter accent for active items */
}

.custom-drawer .v-icon {
  color: #7d2ae8;
}

.v-application .custom-drawer .v-list-item,
.v-application .custom-drawer .v-icon {
  color: white; /* Changed to white for better visibility */
}

/* Navigation Drawer active list item */
.v-application .custom-drawer .v-list-item.v-list-item--active {
  background-color: rgba(125, 42, 232, 0.2);
}

body, .v-application {
  background-color: #e6dcf8; /* Light purple color */
}
.market-overview-container {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.charts-container {
  flex-grow: 1; /* Allow the charts container to take up the available space */
}

/* Ensure that CoinStats takes only the necessary space */
.coin-stats-container {
  width: 50%; /* Or whatever width you prefer */
  margin-top: 0; /* Align to the top */
}

</style>
