<template>
    <BarChart :chart-data="chartData" :options="options" />
  </template>
  
  <script>
  import { defineComponent } from "vue";
  import { Chart, registerables } from "chart.js";
  import { BarChart } from "vue-chart-3";
  
  Chart.register(...registerables);
  
  export default defineComponent({
    components: { BarChart },
    props: {
      chartData: Object,
      options: Object,
    },
  });
  </script>