<template>
    <LineChart :chart-data="chartData" :options="options" />
  </template>
  
  <script>
  import { defineComponent } from "vue";
  import { Chart, registerables } from "chart.js";
  import { LineChart } from "vue-chart-3";
  
  Chart.register(...registerables);
  
  export default defineComponent({
    components: { LineChart },
    props: {
      chartData: Object,
      options: Object,
    },
  });
  </script>