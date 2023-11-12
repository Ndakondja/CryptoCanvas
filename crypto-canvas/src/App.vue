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

    <!-- App Bar (Title Bar) -->
    <v-app-bar app>
      <v-toolbar-title>Crypto Canvas Dashboard</v-toolbar-title>
    </v-app-bar>

    <!-- Main Content -->
    <v-main>
      <div v-if="currentTab === 'VolatilityComparison'">
        <CorrelationMatrix />
        <VolatilityComparison />
        <BitcoinHalving />
      </div>
      <div v-if="currentTab === 'MarketOverview'">
        <!-- Placeholder for Market Overview content -->
        <h2>Market Overview Content Goes Here</h2>
      </div>
    </v-main>
  </v-app>
</template>

<script>
import CorrelationMatrix from './components/CorrelationMatrix.vue'
import VolatilityComparison from './components/VolatilityComparison.vue'
import BitcoinHalving from './components/BitcoinHalving.vue'

export default {
  name: 'App',
  components: {
    CorrelationMatrix,
    VolatilityComparison,
    BitcoinHalving
  },
  data () {
    return {
      currentTab: 'VolatilityComparison'
    }
  }
}
</script>

<style>
/* Add any additional styles if necessary */
</style>
